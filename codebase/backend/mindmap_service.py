"""
Service xử lý trích xuất Slide và gọi Gemini API thật
Dành cho: VLearn Mindmap Prototype - Hackathon Batch 04 (Team BungChay)
"""

import os
import sys
import json
import time
import re
from pathlib import Path
from typing import Dict, Any, Optional, List
import pypdf
import dotenv

try:
    import json_repair
    HAS_JSON_REPAIR = True
except ImportError:
    HAS_JSON_REPAIR = False

# Set UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Load .env
dotenv.load_dotenv(override=True)

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
DATA_DIR = BASE_DIR.parent / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

# Auto-initialize storage if empty or on fresh git clone
try:
    from backend.seed_data import init_default_storage
    init_default_storage()
except Exception as _e:
    pass

from backend.prompts import build_upload_slide_prompt

# Rate limiting tracker: min 4.2s for 15 RPM free tier
_LAST_API_CALL = 0.0
MIN_CALL_INTERVAL = 4.2


def throttle_api():
    global _LAST_API_CALL
    elapsed = time.time() - _LAST_API_CALL
    if elapsed < MIN_CALL_INTERVAL:
        time.sleep(MIN_CALL_INTERVAL - elapsed)
    _LAST_API_CALL = time.time()


def get_api_config() -> Dict[str, Any]:
    """Đọc cấu hình API từ file .env mới nhất."""
    dotenv.load_dotenv(override=True)
    key = os.getenv("GEMINI_API_KEY", "").strip()
    model = os.getenv("LLM_MODEL", "gemini-2.5-flash").strip()
    if not model:
        model = "gemini-2.5-flash"
    return {
        "api_key": key,
        "has_key": bool(key),
        "model": model
    }


def extract_text_from_pdf(file_path: Path, max_pages: int = 100) -> List[Dict[str, Any]]:
    """Trích xuất text từng trang slide bằng pypdf."""
    reader = pypdf.PdfReader(str(file_path))
    pages_data = []
    total = len(reader.pages)
    limit = min(total, max_pages)

    for i in range(limit):
        page = reader.pages[i]
        text = page.extract_text() or ""
        clean_text = re.sub(r'\s+', ' ', text).strip()
        pages_data.append({
            "page_num": i + 1,
            "text": clean_text
        })
    return pages_data


def get_existing_knowledge_context() -> str:
    """Tạo tóm tắt ngắn gọn của các ngày học hiện có để AI tạo liên kết chéo (cross-link)."""
    meta_path = STORAGE_DIR / "metadata.json"
    if not meta_path.exists():
        return ""
    
    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        
        summary_lines = []
        for d in meta.get("days", []):
            topics = ", ".join(d.get("core_topics", [])[:4])
            summary_lines.append(f"- Day {d['day']} ({d['title']}): {topics}")
        return "\n".join(summary_lines)
    except Exception:
        return ""


def call_gemini_api(prompt: str, api_key: str, requested_model: str) -> str:
    """
    Gọi Gemini API qua google-genai hoặc google-generativeai.
    Hỗ trợ fallback sang model phổ biến nếu requested_model bị 404.
    """
    throttle_api()
    candidate_models = [requested_model, "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    # Loại bỏ trùng lặp giữ nguyên thứ tự
    seen = set()
    models_to_try = [m for m in candidate_models if not (m in seen or seen.add(m))]

    last_error = None

    # Cách 1: Thử với google-genai SDK mới
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        for model_name in models_to_try:
            try:
                print(f"[API CALL] Đang gửi yêu cầu đến Gemini model: {model_name}...")
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.2,
                    )
                )
                if response.text:
                    print(f"[API SUCCESS] Nhận phản hồi thành công từ model: {model_name}")
                    return response.text
            except Exception as e:
                print(f"[API WARNING] Thử model {model_name} thất bại: {e}. Thử model kế tiếp...")
                last_error = e
                continue
    except ImportError:
        pass

    # Cách 2: Thử với google-generativeai SDK truyền thống
    try:
        import google.generativeai as legacy_genai
        legacy_genai.configure(api_key=api_key)

        for model_name in models_to_try:
            # Format model name cho legacy nếu cần
            clean_name = model_name if model_name.startswith("models/") else f"models/{model_name}"
            try:
                print(f"[API CALL - LEGACY] Đang thử model: {clean_name}...")
                model = legacy_genai.GenerativeModel(
                    clean_name,
                    generation_config={"response_mime_type": "application/json", "temperature": 0.2}
                )
                res = model.generate_content(prompt)
                if res.text:
                    print(f"[API SUCCESS] Thành công với model: {clean_name}")
                    return res.text
            except Exception as e:
                print(f"[API WARNING] Thử {clean_name} thất bại: {e}")
                last_error = e
                continue
    except ImportError:
        pass

    raise RuntimeError(f"Không thể kết nối Gemini API với bất kỳ model nào. Chi tiết lỗi: {last_error}")


def clean_and_parse_mindmap_json(raw_json_str: str) -> Dict[str, Any]:
    """
    Phân tích chuỗi JSON trả về từ Gemini một cách siêu bền bỉ (resilient):
    1. Bóc tách markdown codeblock ```json ... ```
    2. Trích xuất đúng phân đoạn { ... } ngoài cùng
    3. Xóa trailing commas (dấu phẩy thừa trước } hoặc ])
    4. Thử json.loads tiêu chuẩn với strict=False
    5. Nếu lỗi cú pháp, dùng json_repair tự động sửa chữa
    6. Tự động đóng ngoặc nếu chuỗi bị cắt cụt do chạm token limit
    """
    text = (raw_json_str or "").strip()

    # 1. Bóc markdown block
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    # 2. Tìm phân đoạn JSON ngoài cùng từ dấu { đầu tiên đến dấu } cuối cùng
    start_idx = text.find('{')
    if start_idx != -1:
        end_idx = text.rfind('}')
        if end_idx != -1 and end_idx > start_idx:
            text = text[start_idx:end_idx + 1]
        else:
            text = text[start_idx:]

    # 3. Làm sạch trailing commas phổ biến trước } và ]
    cleaned = re.sub(r',\s*([\}\]])', r'\1', text)

    # 4. Thử parse tiêu chuẩn với strict=False
    last_err = None
    try:
        parsed = json.loads(cleaned, strict=False)
        if isinstance(parsed, dict):
            return parsed
    except Exception as e1:
        last_err = e1
        print(f"[JSON SANITIZER] json.loads trực tiếp gặp lỗi ({e1}), đang kích hoạt bộ phục hồi...")

    # 5. Dùng thư viện json_repair nếu có
    if HAS_JSON_REPAIR:
        try:
            repaired = json_repair.repair_json(text, return_objects=True)
            if isinstance(repaired, dict):
                print("[JSON SANITIZER] Phục hồi JSON thành công bằng json_repair!")
                return repaired
        except Exception as e2:
            print(f"[JSON SANITIZER] json_repair thất bại: {e2}")

    # 6. Tự động cân bằng ngoặc đóng nếu JSON bị cắt cụt do token limit
    try:
        open_braces = text.count('{') - text.count('}')
        open_brackets = text.count('[') - text.count(']')
        patch = text.rstrip(' ,\n\r\t')
        patch += (']' * max(0, open_brackets)) + ('}' * max(0, open_braces))
        patch = re.sub(r',\s*([\}\]])', r'\1', patch)
        parsed = json.loads(patch, strict=False)
        if isinstance(parsed, dict):
            print("[JSON SANITIZER] Phục hồi JSON thành công bằng auto-closing brackets!")
            return parsed
    except Exception as e3:
        pass

    raise ValueError(f"Không thể giải mã cấu trúc JSON từ AI (Lỗi gốc: {last_err}). Vui lòng thử tải lại slide.")


def process_uploaded_slide(
    pdf_path: Path,
    custom_title: Optional[str] = None
) -> Dict[str, Any]:
    """
    Toàn bộ luồng xử lý thực tế:
    1. Trích xuất text từ slide PDF bằng pypdf
    2. Đọc API config từ .env
    3. Tạo prompt RTCF tối ưu token
    4. Gọi Gemini API thật
    5. Lưu kết quả vào storage và trả về dữ liệu Mindmap cho frontend
    """
    config = get_api_config()
    if not config["has_key"]:
        raise ValueError(
            "CHƯA CÓ GEMINI_API_KEY TRONG FILE .env!\n"
            "Vui lòng mở file .env tại thư mục gốc dự án và điền: GEMINI_API_KEY=your_key_here\n"
            "Sau khi điền key, hãy bấm thử lại để gọi API thật."
        )

    # 1. Trích xuất text
    print(f"[EXTRACT] Đang trích xuất toàn bộ văn bản từ: {pdf_path.name}")
    pages = extract_text_from_pdf(pdf_path, max_pages=80)
    total_pages = len(pages)
    if total_pages == 0:
        raise ValueError("File PDF không có trang nào hoặc không thể đọc được nội dung văn bản.")

    # Lấy tiêu đề từ trang đầu nếu không nhập
    doc_title = custom_title or f"Bài Giảng: {pdf_path.stem}"
    
    # Chuẩn bị toàn bộ nội dung các trang slide để gửi cho AI (đảm bảo không bị bỏ sót kiến thức)
    content_snippets = []
    for p in pages:
        txt = p["text"][:1500].strip()
        if txt:
            content_snippets.append(f"--- Slide {p['page_num']} ---\n{txt}")
    
    slide_corpus = "\n\n".join(content_snippets)

    # 2. Lấy bối cảnh các ngày trước để tìm liên kết chéo
    knowledge_context = get_existing_knowledge_context()

    # 3. Tạo prompt RTCF (tách từ backend.prompts)
    prompt = build_upload_slide_prompt(
        knowledge_context=knowledge_context,
        slide_corpus=slide_corpus
    )

    # 4. Gọi Gemini API thật
    raw_json_str = call_gemini_api(prompt, config["api_key"], config["model"])

    # Làm sạch markdown nếu có
    clean_str = raw_json_str.strip()
    if clean_str.startswith("```json"):
        clean_str = clean_str[7:]
    if clean_str.startswith("```"):
        clean_str = clean_str[3:]
    if clean_str.endswith("```"):
        clean_str = clean_str[:-3]
    clean_str = clean_str.strip()
    # Làm sạch và parse JSON siêu bền bỉ (chống trailing commas, unescaped quotes, cắt cụt)
    parsed_tree = clean_and_parse_mindmap_json(raw_json_str)

    parsed_tree = json.loads(clean_str)
    # Kiểm tra nếu AI báo lỗi ngoại vi / out_of_scope
    if parsed_tree.get("status") == "error":
        msg = parsed_tree.get("message", "Tài liệu tải lên không phải bài giảng học tập hợp lệ.")
        raise ValueError(f"AI từ chối phân tích: {msg}")

    # Mở lớp vỏ envelope nếu AI bọc trong {'tree': ...} hoặc {'data': ...}
    if "tree" in parsed_tree and isinstance(parsed_tree["tree"], dict):
        parsed_tree = parsed_tree["tree"]
    elif "data" in parsed_tree and isinstance(parsed_tree["data"], dict):
        parsed_tree = parsed_tree["data"]

    # 5. Xác định số thứ tự ngày mới
    meta_path = STORAGE_DIR / "metadata.json"
    meta = {"days": []}
    if meta_path.exists():
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
        except Exception:
            pass

    next_day_num = len(meta.get("days", [])) + 1
    day_code = f"DAY_{next_day_num:02d}"

    result_day = {
        "day": next_day_num,
        "code": day_code,
        "title": doc_title,
        "subtitle": f"Tự động trích xuất từ {pdf_path.name}",
        "pdf_file": pdf_path.name,
        "total_slides": total_pages,
        "tree": parsed_tree
    }

    # Lưu file day_X.json
    storage_file_name = f"day_{next_day_num}.json"
    with open(STORAGE_DIR / storage_file_name, "w", encoding="utf-8") as f:
        json.dump(result_day, f, ensure_ascii=False, indent=2)

    # Cập nhật metadata.json
    core_topics = [c.get("title", "") for c in parsed_tree.get("children", [])]
    meta.setdefault("days", []).append({
        "day": next_day_num,
        "code": day_code,
        "title": doc_title,
        "subtitle": f"Trích xuất từ {pdf_path.name}",
        "pdf_file": pdf_path.name,
        "total_slides": total_pages,
        "core_topics": core_topics,
        "storage_file": storage_file_name
    })

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"[SUCCESS] Đã tạo thành công Day {next_day_num} từ slide thực tế!")
    return result_day


def delete_day_data(day_num: int) -> Dict[str, Any]:
    """
    Xoá một bài học bao gồm:
    1. File slide PDF trong data/uploads/ (nếu có)
    2. File cấu trúc Mindmap day_{day_num}.json
    3. Cập nhật và đánh chỉ mục lại các ngày còn lại trong metadata.json
    """
    meta_path = STORAGE_DIR / "metadata.json"
    if not meta_path.exists():
        raise FileNotFoundError("Không tìm thấy metadata.json")

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    days_list = meta.get("days", [])
    if len(days_list) <= 1:
        raise ValueError("Không thể xoá bài học duy nhất còn lại trong hệ thống.")

    target_idx = -1
    for idx, d in enumerate(days_list):
        if d.get("day") == day_num:
            target_idx = idx
            break

    if target_idx == -1:
        raise FileNotFoundError(f"Không tìm thấy bài học Day {day_num} để xoá.")

    target_day = days_list[target_idx]

    # 1. Xoá file PDF nếu nằm trong thư mục uploads
    pdf_name = target_day.get("pdf_file", "")
    if pdf_name:
        upload_pdf = UPLOAD_DIR / pdf_name
        if upload_pdf.exists():
            try:
                upload_pdf.unlink()
                print(f"[DELETE] Đã xoá file PDF upload: {pdf_name}")
            except Exception as e:
                print(f"[WARN] Không thể xoá file PDF: {e}")

    # 2. Xoá file day_{day_num}.json
    target_storage_file = STORAGE_DIR / f"day_{day_num}.json"
    if target_storage_file.exists():
        target_storage_file.unlink()
        print(f"[DELETE] Đã xoá storage file: {target_storage_file.name}")

    # 3. Loại bỏ khỏi danh sách
    days_list.pop(target_idx)

    # 4. Đánh chỉ mục lại (Re-index) các ngày còn lại từ 1 đến N
    temp_records = []
    for new_num, d in enumerate(days_list, start=1):
        old_day_num = d["day"]
        old_file = STORAGE_DIR / f"day_{old_day_num}.json"
        temp_file = STORAGE_DIR / f"_temp_swap_{old_day_num}.json"
        if old_file.exists():
            old_file.rename(temp_file)
            temp_records.append((temp_file, new_num, d))

    new_days_list = []
    for temp_file, new_num, d in temp_records:
        with open(temp_file, "r", encoding="utf-8") as f:
            day_data = json.load(f)

        day_data["day"] = new_num
        day_data["code"] = f"DAY_{new_num:02d}"
        if "tree" in day_data:
            day_data["tree"]["id"] = f"d{new_num}_root"

        d["day"] = new_num
        d["code"] = f"DAY_{new_num:02d}"
        d["storage_file"] = f"day_{new_num}.json"

        final_file = STORAGE_DIR / f"day_{new_num}.json"
        with open(final_file, "w", encoding="utf-8") as f:
            json.dump(day_data, f, ensure_ascii=False, indent=2)

        temp_file.unlink()
        new_days_list.append(d)

    meta["days"] = new_days_list
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"[DELETE SUCCESS] Đã xoá Day {day_num} và tái lập chỉ mục {len(new_days_list)} bài học thành công!")
    return {
        "deleted_day": day_num,
        "total_remaining": len(new_days_list),
        "days": new_days_list
    }


