"""
Runner script cho eval/golden_set.json.
Chay tung case qua dung prompt that (backend.prompts.build_upload_slide_prompt)
va goi Gemini API that (backend.mindmap_service.call_gemini_api), roi tu cham
Pass/Fail theo scoring_rules trong golden_set.json.

Cach dung:
    python eval/run_tests.py                # chay het 20 case
    python eval/run_tests.py gs01 gs05       # chi chay 2 case chi dinh (test nhanh)

Yeu cau: da dien GEMINI_API_KEY trong file .env o thu muc goc du an.
"""
import os
import sys
import json
import re
import time
from pathlib import Path
from datetime import datetime

import dotenv
import requests

ROOT_DIR = Path(__file__).resolve().parent.parent
CODEBASE_DIR = ROOT_DIR / "codebase"
sys.path.insert(0, str(CODEBASE_DIR))

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

dotenv.load_dotenv(ROOT_DIR / ".env", override=True)

from backend.prompts import build_upload_slide_prompt  # noqa: E402
from backend.mindmap_service import call_gemini_api, get_api_config  # noqa: E402

NVIDIA_ENDPOINT = "https://integrate.api.nvidia.com/v1/chat/completions"


def call_nvidia_api(prompt: str, api_key: str, model: str) -> str:
    """Goi model qua NVIDIA build API (tuong thich OpenAI chat completions).
    Chi dung cho muc dich test golden set khi chua co Gemini key that -
    khong dung trong san pham thuc te (san pham that chi goi Gemini qua call_gemini_api)."""
    resp = requests.post(
        NVIDIA_ENDPOINT,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        },
        timeout=350,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]


PLACEHOLDER_KEYS = {"your_gemini_api_key_here", "your_openai_api_key_here", "your_anthropic_api_key_here"}


def resolve_provider():
    """Uu tien Gemini (dung backend that) neu co key that; khong thi fallback NVIDIA (chi de test)."""
    gemini_config = get_api_config()
    if gemini_config["has_key"] and gemini_config["api_key"] not in PLACEHOLDER_KEYS:
        return "gemini", gemini_config["api_key"], gemini_config["model"]

    nvidia_key = os.getenv("NVIDIA_API_KEY", "").strip()
    nvidia_model = os.getenv("NVIDIA_MODEL", "deepseek-ai/deepseek-v4-flash-0731").strip()
    if nvidia_key:
        return "nvidia", nvidia_key, nvidia_model

    return None, None, None


def convert_input_to_slide_corpus(raw_input: str) -> str:
    """Chuyen '[Trang N] noi dung' (format trong golden_set.json) sang
    dung format '--- Slide N ---\\nnoi dung' ma mindmap_service.py dung that
    khi trich xuat PDF, de test dung nguyen prompt/pipeline that."""
    blocks = re.split(r"\[Trang (\d+)\]", raw_input)
    # blocks[0] la phan truoc marker dau tien (thuong rong), sau do xen ke (so_trang, noi_dung)
    parts = []
    for i in range(1, len(blocks), 2):
        page_num = blocks[i].strip()
        content = blocks[i + 1].strip() if i + 1 < len(blocks) else ""
        parts.append(f"--- Slide {page_num} ---\n{content}")
    return "\n\n".join(parts)


def clean_json_response(raw: str) -> str:
    clean = raw.strip()
    if clean.startswith("```json"):
        clean = clean[7:]
    if clean.startswith("```"):
        clean = clean[3:]
    if clean.endswith("```"):
        clean = clean[:-3]
    return clean.strip()


def parse_slide_pages(slide_page_str) -> set:
    """Tach 'Slide 4', 'Slide 9-11', 'Slide 1, 3' ... thanh set so trang {4} / {9,10,11} / {1,3}."""
    if not slide_page_str or not isinstance(slide_page_str, str):
        return set()
    pages = set()
    for a, b in re.findall(r"(\d+)\s*-\s*(\d+)", slide_page_str):
        pages.update(range(int(a), int(b) + 1))
    remaining = re.sub(r"\d+\s*-\s*\d+", "", slide_page_str)
    for n in re.findall(r"\d+", remaining):
        pages.add(int(n))
    return pages


def walk_nodes(node, depth=1):
    """Sinh ra (node, depth) cho toan bo cay, depth=1 la root."""
    if not isinstance(node, dict):
        return
    yield node, depth
    for child in node.get("children") or []:
        yield from walk_nodes(child, depth + 1)


def check_case(case: dict, parsed: dict) -> list:
    """Tra ve list loi (rong = pass)."""
    errors = []
    expected = case["expected"]

    all_nodes = list(walk_nodes(parsed))
    max_depth = max((d for _, d in all_nodes), default=0)

    actual_insufficient = bool(parsed.get("insufficient_info", False))
    expected_insufficient = bool(expected["insufficient_info"])

    if actual_insufficient != expected_insufficient:
        errors.append(
            f"insufficient_info sai: ky vong {expected_insufficient}, thuc te {actual_insufficient}"
        )

    if expected_insufficient:
        children = parsed.get("children") or []
        if children:
            errors.append(f"insufficient_info=true nhung children khong rong ({len(children)} node) - co dau hieu bia cay gia")
    else:
        if max_depth < 3:
            errors.append(f"cau truc chi sau {max_depth} cap, yeu cau toi thieu 3 cap (RULE 2 cua prompt that)")

        covered_pages = set()
        for node, _ in all_nodes:
            covered_pages |= parse_slide_pages(node.get("slide_page"))
        missing_pages = set(expected["must_cover_pages"]) - covered_pages
        if missing_pages:
            errors.append(f"thieu trich dan trang: {sorted(missing_pages)} khong xuat hien trong slide_page cua node nao")

    if max_depth > 5:
        errors.append(f"cau truc vuot qua 5 cap (thuc te {max_depth} cap)")

    forbidden = [t.lower() for t in expected.get("forbidden_terms", [])]
    if forbidden:
        haystacks = []
        for node, _ in all_nodes:
            haystacks.append(str(node.get("title", "")))
            haystacks.append(str(node.get("summary", "")))
            detail = node.get("detail") or {}
            haystacks.append(str(detail.get("excerpt", "")))
            haystacks.append(str(detail.get("ai_tutor_explanation", "")))
        full_text = " \n ".join(haystacks).lower()
        hit_terms = [t for t in forbidden if t in full_text]
        if hit_terms:
            errors.append(f"chua tu khoa cam (nghi ngo bia noi dung): {hit_terms}")

    return errors


def main():
    target_ids = set(sys.argv[1:]) or None

    golden_path = ROOT_DIR / "eval" / "golden_set.json"
    with open(golden_path, encoding="utf-8") as f:
        golden = json.load(f)

    provider, api_key, model = resolve_provider()
    if provider is None:
        print("LOI: chua co GEMINI_API_KEY hoac NVIDIA_API_KEY trong file .env o thu muc goc du an.")
        print("Mo file .env, dien 1 trong 2 key roi chay lai.")
        sys.exit(1)

    cases = golden["cases"]
    if target_ids:
        cases = [c for c in cases if c["id"] in target_ids]
        if not cases:
            print(f"Khong tim thay case nao khop id: {sorted(target_ids)}")
            sys.exit(1)

    results = []
    print(f"Chay {len(cases)} case qua provider={provider}, model={model}...")
    if provider == "nvidia":
        print("(Dang dung NVIDIA build API de test golden set vi chua co Gemini key that - "
              "san pham thuc te van chi goi Gemini qua mindmap_service.call_gemini_api, "
              "khong bi anh huong boi lua chon nay)")
    print()

    for case in cases:
        cid = case["id"]
        print(f"[{cid}] dang goi API...", end=" ", flush=True)
        slide_corpus = convert_input_to_slide_corpus(case["input"])
        prompt = build_upload_slide_prompt(knowledge_context="", slide_corpus=slide_corpus)

        t0 = time.time()
        try:
            if provider == "gemini":
                raw = call_gemini_api(prompt, api_key, model)
            else:
                raw = call_nvidia_api(prompt, api_key, model)
            parsed = json.loads(clean_json_response(raw))
            errors = check_case(case, parsed)
        except Exception as e:
            errors = [f"LOI KY THUAT: {type(e).__name__}: {e}"]
            parsed = None
        elapsed = time.time() - t0

        status = "PASS" if not errors else "FAIL"
        print(f"{status} ({elapsed:.1f}s)")
        for err in errors:
            print(f"    - {err}")

        results.append({
            "id": cid,
            "taxonomy": case["taxonomy"],
            "status": status,
            "errors": errors,
            "elapsed_sec": round(elapsed, 1),
        })

    passed = sum(1 for r in results if r["status"] == "PASS")
    print(f"\n=== TONG KET: {passed}/{len(results)} PASS ===")

    by_tax = {}
    for r in results:
        for t in r["taxonomy"]:
            by_tax.setdefault(t, [0, 0])
            by_tax[t][1] += 1
            if r["status"] == "PASS":
                by_tax[t][0] += 1
    for t, (p, n) in sorted(by_tax.items()):
        print(f"  {t}: {p}/{n}")

    out_path = ROOT_DIR / "eval" / f"run_results_auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "run_at": datetime.now().isoformat(),
            "provider": provider,
            "model": model,
            "passed": passed,
            "total": len(results),
            "results": results,
        }, f, ensure_ascii=False, indent=2)
    print(f"\nDa ghi ket qua chi tiet vao: {out_path}")
    print("Ban tu doi chieu va cap nhat vao eval/run_results.md (giu lai phan phan tich da viet tay).")


if __name__ == "__main__":
    main()
