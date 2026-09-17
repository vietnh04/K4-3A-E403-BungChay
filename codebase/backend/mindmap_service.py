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


def extract_text_from_pdf(file_path: Path, max_pages: int = 40) -> List[Dict[str, Any]]:
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
    print(f"[EXTRACT] Đang trích xuất văn bản từ: {pdf_path.name}")
    pages = extract_text_from_pdf(pdf_path, max_pages=35)
    total_pages = len(pages)
    if total_pages == 0:
        raise ValueError("File PDF không có trang nào hoặc không thể đọc được nội dung văn bản.")

    # Lấy tiêu đề từ trang đầu nếu không nhập
    doc_title = custom_title or f"Bài Giảng: {pdf_path.stem}"
    
    # Chuẩn bị nội dung rút gọn các trang để gửi trong 1 request duy nhất (tiết kiệm token)
    content_snippets = []
    for p in pages:
        txt = p["text"][:400]
        if txt:
            content_snippets.append(f"--- Slide {p['page_num']} ---\n{txt}")
    
    slide_corpus = "\n\n".join(content_snippets[:20])  # Giới hạn 20 slides quan trọng đầu tiên

    # 2. Lấy bối cảnh các ngày trước để tìm liên kết chéo
    knowledge_context = get_existing_knowledge_context()

    # 3. Tạo prompt RTCF
    prompt = f"""
[ROLE]: Chuyên gia Sư phạm & Kỹ sư Trực quan hoá Kiến thức VLearn AI.
[TASK]: Phân tích nội dung slide bài giảng sau đây và trích xuất thành Cây Sơ Đồ Tư Duy (Mindmap Tree) tương tác định dạng JSON.

[BỐI CẢNH CÁC NGÀY HỌC TRƯỚC ĐÓ (để tạo liên kết chéo nếu có liên quan)]:
{knowledge_context}

[QUY TẮC BẮT BUỘC VỀ NỘI DUNG (THEO ĐẶC TẢ VLEARN)]:
1. Cấu trúc cây 3 cấp:
   - Cấp 0 (Root): Tên bài giảng tổng quát.
   - Cấp 1 (Chương/Phần): 2 đến 4 chương chính của bài giảng.
   - Cấp 2 (Khái niệm cụ thể): 2 đến 4 khái niệm cốt lõi của mỗi chương.
2. Tiêu đề node (title): RẤT NGẮN GỌN (từ 2 đến 4 từ tiếng Việt, ví dụ: 'Cơ Chế Attention', 'Vòng Lặp ReAct', 'Local Checklist').
3. Tóm tắt node (summary): KHÔNG ĐƯỢC QUÁ 15 TỪ. Chỉ nêu khái quát cốt lõi nhất, KHÔNG chép cả đoạn văn dài.
4. Trích dẫn số trang (slide_page): Bắt buộc ghi rõ trang slide gốc (ví dụ 'Slide 4', 'Slide 9').
5. Liên kết chéo (cross_link): Nếu một khái niệm kế thừa hoặc liên quan đến kiến thức của Day 1-5, hãy thêm:
   "cross_link": {{
       "target_day": 1..5,
       "target_node_id": "id_ngay_truoc",
       "label": "🔗 Kế thừa từ Day X [Slide Y]"
   }}
   Nếu không liên quan thì để null.
6. Chi tiết mở rộng (detail):
   - "title": Tiêu đề chi tiết
   - "slide_page": Số trang trích dẫn
   - "excerpt": Trích đoạn văn bản thực tế từ slide
   - "key_takeaway": Điểm mấu chốt học viên cần nhớ
   - "ai_tutor_explanation": Lời giảng giải sư phạm thực chiến từ AI Tutor
   - "code_snippet": Lệnh terminal hoặc code mẫu (nếu bài học có code, nếu không thì null)
   - "quick_quiz": Một câu hỏi trắc nghiệm nhanh kiểm tra độ hiểu bài kèm đáp án.

[SCHEMA JSON TRẢ VỀ]:
{{
  "id": "node_root",
  "title": "Tên Ngắn Gọn (2-4 từ)",
  "summary": "Tóm tắt cốt lõi dưới 15 từ.",
  "slide_page": "Slide 1",
  "type": "root",
  "children": [
    {{
      "id": "node_sec1",
      "title": "Tên Chương (2-4 từ)",
      "summary": "Tóm tắt chương dưới 15 từ.",
      "slide_page": "Slide 2",
      "type": "branch",
      "children": [
        {{
          "id": "node_c1",
          "title": "Tên Khái Niệm (2-4 từ)",
          "summary": "Tóm tắt khái niệm dưới 15 từ.",
          "slide_page": "Slide 5",
          "cross_link": null,
          "detail": {{
            "title": "Tiêu đề đầy đủ",
            "slide_page": "Slide 5",
            "excerpt": "Trích đoạn gốc...",
            "key_takeaway": "Khái quát cốt lõi...",
            "ai_tutor_explanation": "Giải thích sư phạm...",
            "code_snippet": null,
            "quick_quiz": "Câu hỏi? A/B/C. Đáp án: A"
          }}
        }}
      ]
    }}
  ]
}}

[DỮ LIỆU SLIDE CẦN XỬ LÝ]:
{slide_corpus}
"""

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

    parsed_tree = json.loads(clean_str)

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
