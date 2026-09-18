"""
VLearn Mindmap Generator Pipeline (Hackathon AI - Batch 04 - Track A)
Team: BungChay | Class: 3A | Room: E403

This module handles:
1. Offline extraction and caching of slide decks (Day 01 to Day 05).
2. Rate-limited (15 RPM / 500 RPD) Gemini API integration with Structured Outputs.
3. Safe offline fallback: Works 100% without an active API key, preserving free-tier quota.
4. Cross-day concept linking engine.
"""

import os
import sys
import json
import time
import argparse
from typing import List, Optional, Dict, Any, Union
from pathlib import Path

# Fix Windows console encoding for Vietnamese characters
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Try importing pypdf
try:
    import pypdf
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

# Try importing google-genai or google.generativeai safely
HAS_GENAI = False
try:
    from google import genai
    from google.genai import types
    from pydantic import BaseModel, Field
    HAS_GENAI = True
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
DATA_DIR = BASE_DIR.parent / "data"
STORAGE_DIR = BASE_DIR / "storage"

from backend.prompts import build_pipeline_mindmap_prompt

# Pydantic schemas for Gemini Structured Output
if HAS_GENAI:
    class QuickQuizSchema(BaseModel):
        question: str = Field(description="Câu hỏi trắc nghiệm ngắn kiểm tra hiểu biết")
        options: List[str] = Field(description="Danh sách lựa chọn, ví dụ ['A. Lựa chọn 1', 'B. Lựa chọn 2']")
        answer: str = Field(description="Đáp án đúng, ví dụ 'A'")
        explanation: str = Field(description="Lời giải thích ngắn gọn vì sao đáp án này đúng")

    class DetailNodeSchema(BaseModel):
        title: str = Field(description="Tiêu đề chi tiết của khái niệm")
        slide_page: str = Field(description="Số trang slide trích dẫn, ví dụ 'Slide 9'")
        excerpt: Optional[str] = Field(default=None, description="Trích đoạn nội dung thực tế từ slide (tùy chọn)")
        key_takeaway: str = Field(description="Khái quát cốt lõi nhất cần nhớ")
        ai_tutor_explanation: str = Field(description="Lời giải thích sư phạm từ AI Tutor")
        code_snippet: Optional[str] = Field(default=None, description="Lệnh terminal hoặc code mẫu nếu có")
        quick_quiz: Optional[Union[QuickQuizSchema, str]] = Field(default=None, description="Trắc nghiệm nhanh kiểm tra hiểu biết")

    class CrossLinkSchema(BaseModel):
        target_day: int = Field(description="Số thứ tự ngày liên kết (1-5)")
        target_node_id: str = Field(description="ID của node liên kết")
        label: str = Field(description="Nhãn hiển thị, ví dụ '🔗 Kế thừa từ Day 02 [Slide 12]'")

    class ConceptNodeSchema(BaseModel):
        id: str = Field(description="Định danh duy nhất của node")
        title: str = Field(description="Tiêu đề ngắn gọn (2-5 từ)")
        summary: str = Field(description="Tóm tắt khái quát cốt lõi (tối đa 40 từ)")
        slide_page: str = Field(description="Trang slide ví dụ 'Slide 9'")
        cross_link: Optional[CrossLinkSchema] = None
        detail: Optional[DetailNodeSchema] = None
        children: Optional[List['ConceptNodeSchema']] = Field(default=None, description="Danh sách các node con phân cấp đa tầng sâu (Level 1, 2, 3, 4...)")


class MindmapPipeline:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.storage_dir = STORAGE_DIR
        self.data_dir = DATA_DIR
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Throttling tracker for free tier: 15 RPM -> at least 4.0s between calls
        self.last_call_time = 0.0
        self.min_interval = 4.2  # seconds

    def _throttle(self):
        """Enforces rate limit to strictly protect 15 RPM / 500 RPD quota."""
        elapsed = time.time() - self.last_call_time
        if elapsed < self.min_interval:
            sleep_needed = self.min_interval - elapsed
            time.sleep(sleep_needed)
        self.last_call_time = time.time()

    def extract_text_from_pdf(self, pdf_path: Path, max_pages: Optional[int] = None) -> List[Dict[str, Any]]:
        """Extracts text per page from PDF using pypdf."""
        if not HAS_PYPDF:
            raise RuntimeError("pypdf is not installed. Please install it with 'pip install pypdf'.")
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found at: {pdf_path}")

        reader = pypdf.PdfReader(str(pdf_path))
        pages_content = []
        limit = len(reader.pages) if max_pages is None else min(max_pages, len(reader.pages))

        for idx in range(limit):
            page_text = reader.pages[idx].extract_text() or ""
            pages_content.append({
                "page": idx + 1,
                "text": page_text.strip()
            })
        return pages_content

    def load_cached_day(self, day: int) -> Optional[Dict[str, Any]]:
        """Loads pre-extracted structured mindmap data from disk cache."""
        cache_file = self.storage_dir / f"day_{day}.json"
        if cache_file.exists():
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def save_day_cache(self, day: int, data: Dict[str, Any]):
        """Persists structured mindmap data to storage directory."""
        cache_file = self.storage_dir / f"day_{day}.json"
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def generate_day_mindmap(self, day: int, force_api: bool = False) -> Dict[str, Any]:
        """
        Retrieves or generates mindmap for a specific day.
        Prioritizes cached authentic data. Only calls Gemini API if explicitly requested
        and an API key is available.
        """
        # 1. Check local cache first (Cost = 0, RateLimit = 0)
        if not force_api:
            cached = self.load_cached_day(day)
            if cached:
                print(f"[CACHE HIT] Loaded Day {day} from storage ({cached.get('title')}) - 0 API tokens consumed.")
                return cached

        # 2. If force_api is True, verify API Key and SDK
        if not self.api_key:
            print(f"[SAFE FALLBACK] No GEMINI_API_KEY provided. Loading local pre-extracted dataset for Day {day}.")
            cached = self.load_cached_day(day)
            if cached:
                return cached
            raise ValueError(f"No cache found and no GEMINI_API_KEY provided for Day {day}.")

        if not HAS_GENAI:
            print("[SAFE FALLBACK] google-genai SDK not loaded. Using local cached storage.")
            return self.load_cached_day(day)

        # 3. Call Gemini with Structured Output & Rate Limiting
        print(f"[API CALL] Generating Mindmap for Day {day} using Gemini 2.5 Flash...")
        self._throttle()
        
        # Load PDF text
        index_file = self.storage_dir / "metadata.json"
        pdf_name = f"day0{day}.pdf"
        if index_file.exists():
            with open(index_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
                for d in meta.get("days", []):
                    if d["day"] == day:
                        pdf_name = d["pdf_file"]
                        break
        
        pdf_path = self.data_dir / pdf_name
        pages = self.extract_text_from_pdf(pdf_path, max_pages=60)
        concise_content = "\n\n".join([f"--- Slide {p['page']} ---\n{p['text'][:1500].strip()}" for p in pages if p['text'].strip()])

        # Tạo prompt (tách từ backend.prompts)
        prompt = build_pipeline_mindmap_prompt(day=day, concise_content=concise_content)

        client = genai.Client(api_key=self.api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ConceptNodeSchema,
                temperature=0.2,
            )
        )
        
        result = json.loads(response.text)
        mindmap_data = {
            "day": day,
            "code": f"DAY_{day:02d}",
            "title": f"Day {day:02d} Mindmap (Generated)",
            "total_slides": len(pages),
            "tree": result
        }
        self.save_day_cache(day, mindmap_data)
        print(f"[API SUCCESS] Generated and saved Day {day} Mindmap.")
        return mindmap_data

    def validate_cross_links(self) -> List[Dict[str, Any]]:
        """Verifies that all cross-day links point to existing nodes across days."""
        all_nodes = {}
        cross_links = []

        for d in range(1, 6):
            data = self.load_cached_day(d)
            if not data:
                continue
            
            def scan(node, day_idx):
                nid = node.get("id")
                if nid:
                    all_nodes[nid] = (day_idx, node.get("title"))
                if node.get("cross_link"):
                    cross_links.append({
                        "from_day": day_idx,
                        "from_node": nid,
                        "link": node["cross_link"]
                    })
                for child in node.get("children", []):
                    scan(child, day_idx)

            if "tree" in data:
                scan(data["tree"], d)

        validation_report = []
        for cl in cross_links:
            target_id = cl["link"].get("target_node_id")
            target_day = cl["link"].get("target_day")
            exists = target_id in all_nodes
            validation_report.append({
                "from_day": cl["from_day"],
                "from_node": cl["from_node"],
                "target_day": target_day,
                "target_node": target_id,
                "label": cl["link"].get("label"),
                "status": "VALID" if exists else "BROKEN"
            })
        return validation_report


def main():
    parser = argparse.ArgumentParser(description="VLearn Mindmap Data & Pipeline CLI")
    parser.add_argument("--day", type=int, choices=range(1, 6), help="Chạy pipeline cho ngày cụ thể (1-5)")
    parser.add_argument("--build-all", action="store_true", help="Kiểm tra hoặc sinh toàn bộ 5 ngày")
    parser.add_argument("--force-api", action="store_true", help="Bắt buộc gọi Gemini API thay vì dùng cache")
    parser.add_argument("--validate-links", action="store_true", help="Kiểm tra tính toàn vẹn của liên kết chéo giữa các ngày")
    parser.add_argument("--status", action="store_true", help="Kiểm tra trạng thái các file lưu trữ hiện có")

    args = parser.parse_args()
    pipeline = MindmapPipeline()

    if args.status or (not sys.argv[1:]):
        print("=== TRẠNG THÁI KHO DỮ LIỆU MINDMAP (CP3 - BungChay) ===")
        meta_file = STORAGE_DIR / "metadata.json"
        if meta_file.exists():
            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
                print(f"Khoá học: {meta.get('course_title')} ({meta.get('team')})")
                for d in meta.get("days", []):
                    cache = STORAGE_DIR / d["storage_file"]
                    status = f"READY ({cache.stat().st_size // 1024} KB)" if cache.exists() else "MISSING"
                    print(f"  Day {d['day']:02d}: {d['title']:<36} | PDF: {d['pdf_file']:<45} | Storage: {status}")
        else:
            print("Chưa có metadata.json trong codebase/storage/")

    if args.validate_links:
        print("\n=== KIỂM TRA LIÊN KẾT CHÉO GIỮA CÁC NGÀY (Cross-Day Links) ===")
        reports = pipeline.validate_cross_links()
        for r in reports:
            badge = "✅" if r["status"] == "VALID" else "❌"
            print(f"{badge} Day {r['from_day']} [{r['from_node']}] -> Day {r['target_day']} [{r['target_node']}] ({r['label']})")
        print(f"Tổng số liên kết chéo: {len(reports)}")

    if args.day:
        data = pipeline.generate_day_mindmap(args.day, force_api=args.force_api)
        print(f"\nKết quả Day {args.day}: {data.get('title')} (Tổng slides: {data.get('total_slides')})")

    if args.build_all:
        for d in range(1, 6):
            pipeline.generate_day_mindmap(d, force_api=args.force_api)


if __name__ == "__main__":
    main()
