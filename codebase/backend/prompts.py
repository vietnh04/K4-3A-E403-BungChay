"""
VLearn System Prompts & Prompt Templates
Dự án: Mini Hackathon AI - Batch 04 · Track A (VLearn Tutor / ConceptMap)
Nhóm: BungChay · Phòng: E403 · Lớp: 3A

Tách biệt hoàn toàn System Prompts khỏi Code Logic (FastAPI / D3 Canvas / Pipeline).
Giúp Prompt Engineer dễ dàng tinh chỉnh (tune), kiểm thử (test), và maintain mà không làm ảnh hưởng đến mã nguồn backend.
"""

# ==============================================================================
# 1. SYSTEM PROMPT: TRÍCH XUẤT MINDMAP KHI UPLOAD SLIDE MỚI (LIVE WEBSERVER)
# ==============================================================================
SLIDE_MINDMAP_EXTRACTION_PROMPT = """[ROLE]: Chuyên gia Sư phạm & Kỹ sư Trực quan hoá Kiến thức VLearn AI.
[TASK]: Phân tích nội dung slide bài giảng sau đây và trích xuất thành Cây Sơ Đồ Tư Duy (Mindmap Tree) tương tác định dạng JSON.

[BỐI CẢNH CÁC NGÀY HỌC TRƯỚC ĐÓ (để tạo liên kết chéo nếu có liên quan)]:
{knowledge_context}

[QUY TẮC BẮT BUỘC VỀ NỘI DUNG (THEO ĐẶC TẢ VLEARN)]:
1. Cấu trúc cây 3 cấp:
   - Cấp 0 (Root): Tên bài giảng tổng quát.
   - Cấp 1 (Chương/Phần): 2 đến 4 chương chính của bài giảng.
   - Cấp 2 (Khái niệm cụ thể): 2 đến 4 khái niệm cốt lõi của mỗi chương.
2. Tiêu đề node (title): RẤT NGẮN GỌN (từ 2 đến 4 từ tiếng Việt, ví dụ: 'Cơ Chế Attention', 'Vòng Lặp ReAct', 'Local Checklist').
3. Tóm tắt node (summary): KHÔNG ĐƯỢC QUÁ 40 TỪ. Nêu rõ khái quát cốt lõi, súc tích, giải thích được ý niệm chính mà KHÔNG chép nguyên văn cả đoạn slide dài.
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
  "summary": "Tóm tắt cốt lõi dưới 40 từ.",
  "slide_page": "Slide 1",
  "type": "root",
  "children": [
    {{
      "id": "node_sec1",
      "title": "Tên Chương (2-4 từ)",
      "summary": "Tóm tắt chương dưới 40 từ.",
      "slide_page": "Slide 2",
      "type": "branch",
      "children": [
        {{
          "id": "node_c1",
          "title": "Tên Khái Niệm (2-4 từ)",
          "summary": "Tóm tắt khái niệm dưới 40 từ.",
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

# ==============================================================================
# 2. SYSTEM PROMPT: BATCH PIPELINE TRÍCH XUẤT CHO TỪNG BÀI GIẢNG (STRUCTURED OUTPUT)
# ==============================================================================
PIPELINE_MINDMAP_EXTRACTION_PROMPT = """[ROLE]: Chuyên gia Sư phạm & Kỹ sư AI VLearn.
[TASK]: Trích xuất cây sơ đồ tư duy (Concept Mindmap) cho Day {day}.
[QUY TẮC BẮT BUỘC]:
1. Cây có 3 cấp: Root (Ngày học) -> Branches (Chương/Phần) -> Leaf (Khái niệm cụ thể).
2. Title: Ngắn gọn từ 2 đến 4 từ (Ví dụ: 'Local Checklist', 'ReAct Pattern').
3. Summary: Khái quát cốt lõi KHÔNG QUÁ 40 TỪ. Nêu rõ ý chính, súc tích, không sao chép nguyên văn cả trang slide.
4. Ghi rõ số trang slide trích dẫn ('Slide X').
5. Chi tiết (detail): Có trích đoạn gốc, takeaway, giải thích của AI Tutor và câu hỏi trắc nghiệm nhanh.

NỘI DUNG SLIDE TỔNG HỢP:
{concise_content}
"""


def build_upload_slide_prompt(knowledge_context: str, slide_corpus: str) -> str:
    """
    Tạo prompt hoàn chỉnh để trích xuất slide PDF tải lên từ giao diện web.
    
    Args:
        knowledge_context: Danh mục kiến thức các ngày trước để tìm liên kết chéo.
        slide_corpus: Nội dung text trích xuất từ các trang slide PDF.
    
    Returns:
        Chuỗi prompt RTCF hoàn chỉnh sẵn sàng gửi cho Gemini API.
    """
    return SLIDE_MINDMAP_EXTRACTION_PROMPT.format(
        knowledge_context=knowledge_context,
        slide_corpus=slide_corpus
    )


def build_pipeline_mindmap_prompt(day: int, concise_content: str) -> str:
    """
    Tạo prompt cho batch pipeline xử lý bài giảng theo ngày.
    
    Args:
        day: Số thứ tự ngày học (1-5).
        concise_content: Nội dung các trang slide đã gom nhóm.
        
    Returns:
        Chuỗi prompt hoàn chỉnh cho Gemini Structured Output.
    """
    return PIPELINE_MINDMAP_EXTRACTION_PROMPT.format(
        day=day,
        concise_content=concise_content
    )
