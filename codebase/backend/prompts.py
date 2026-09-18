"""
VLearn System Prompts & Prompt Templates
Dự án: Mini Hackathon AI - Batch 04 · Track A (VLearn Tutor / ConceptMap)
Nhóm: BungChay · Phòng: E403 · Lớp: 3A

Tách biệt hoàn toàn System Prompts khỏi Code Logic (FastAPI / D3 Canvas / Pipeline).
Tối ưu hóa: Phân rã cấu trúc đa cấp sâu (Multi-level Deep Mindmap), bao quát toàn bộ nội dung slide
không bị nông, không bỏ sót kiến thức, vừa có cái nhìn tổng quan vừa xem được chi tiết từng phần.
"""

# ==============================================================================
# SYSTEM PROMPT: TRÍCH XUẤT MINDMAP (TỐI ĐA 40 TỪ CHO MỖI SUMMARY - PRODUCTION)
# ==============================================================================
SLIDE_MINDMAP_EXTRACTION_PROMPT = """[ROLE]: Chuyên gia Sư phạm Cấp cao & Kỹ sư Kiến trúc Tri thức VLearn AI.
[TASK]: Phân tích toàn diện nội dung toàn bộ các trang slide bài giảng được cung cấp và trích xuất thành Cây Sơ Đồ Tư Duy Đa Tầng Chi Tiết (Deep Hierarchical Mindmap) chuẩn JSON.

[BỐI CẢNH CÁC BÀI HỌC TRƯỚC (để tạo liên kết chéo)]:
{knowledge_context}

[NGUYÊN TẮC BẮT BUỘC VỀ PHÂN RÃ CẤU TRÚC VÀ ĐỘ DÀI TÓM TẮT]:
1. NGUYÊN TẮC BÁM NGUỒN & ĐỘ BAO PHỦ (GROUNDING & COVERAGE):
   - Chỉ sử dụng dữ liệu xuất hiện trong [DỮ LIỆU SLIDE CẦN XỬ LÝ]. Tuyệt đối không tự suy diễn hoặc bịa thông tin ngoài bài giảng.
   - Bao quát toàn bộ tiến trình slide từ trang đầu đến trang cuối, không bỏ sót các định nghĩa, công thức, mã lệnh hay lưu ý kỹ thuật then chốt.

2. CẤU TRÚC PHÂN CẤP ĐA TẦNG (3 - 5 CẤP):
   - Phân rã theo hình cây có chiều sâu logic:
     * Cấp 0 (Root): Tên tổng thể bài giảng (1 node duy nhất).
     * Cấp 1 (Chương / Module chính): Các phần lớn / chương mục của buổi học.
     * Cấp 2 (Chủ đề con / Quy trình): Các chủ đề hoặc quy trình cụ thể trong từng chương.
     * Cấp 3 (Khái niệm cốt lõi / Kỹ thuật / Công cụ): Định nghĩa, cơ chế hoạt động, thuật toán, mô hình.
     * Cấp 4+ (Chi tiết sâu / Bước thực thi / Tham số / Cú pháp code / Lưu ý): Nhánh chi tiết bước thực hiện hoặc tham số kỹ thuật.

3. RÀNG BUỘC ĐỘ DÀI & ĐỊNH DẠNG NODE (QUAN TRỌNG):
   - "title": RẤT NGẮN GỌN (từ 2 đến 5 từ tiếng Việt, ví dụ: 'Cơ Chế Attention', 'Vòng Lặp ReAct', 'Tối Ưu Cache').
   - "summary": BẮT BUỘC TỐI ĐA 40 TỪ. Trình bày súc tích, đi thẳng vào bản chất khái niệm hoặc vai trò kỹ thuật, không sao chép nguyên văn cả đoạn văn dài.
   - "slide_page": Bắt buộc ghi rõ số trang slide gốc (ví dụ: 'Slide 4', 'Slide 12-14').

4. CHI TIẾT MỞ RỘNG (detail) TẠI NODE LÁ VÀ KHÁI NIỆM QUAN TRỌNG:
   - Tại các node khái niệm (concept) hoặc chi tiết thực thi (detail) quan trọng, cung cấp object "detail" tinh gọn:
     * "key_takeaway": Điểm cốt lõi học viên bắt buộc phải nhớ (1 câu, dưới 30 từ).
     * "ai_tutor_explanation": Lời giảng giải ngắn gọn, dễ hiểu từ AI Tutor (1-2 câu).
     * "code_snippet": Lệnh terminal, cú pháp code, hoặc cấu hình tham số (nếu có trên slide, không có thì null).
     * "quick_quiz": Câu hỏi trắc nghiệm nhanh kiểm tra hiểu biết (CHỈ TẠO Ở CÁC NODE KHÁI NIỆM CỐT LÕI CẤP 2-3, các node khác để null để tiết kiệm token). Cấu trúc object:
       {{
         "question": "Câu hỏi ngắn kiểm tra bản chất khái niệm?",
         "options": ["A. Lựa chọn 1", "B. Lựa chọn 2"],
         "answer": "A",
         "explanation": "Giải thích ngắn gọn 1 câu vì sao đáp án A đúng."
       }}

5. LIÊN KẾT CHÉO (cross_link):
   - Nếu có liên quan mật thiết với Day 1-5, thêm "cross_link": {{"target_day": 1..5, "target_node_id": "id_ngay_truoc", "label": "🔗 Kế thừa từ Day X [Slide Y]"}}, nếu không thì null.

[SCHEMA JSON BẮT BUỘC]:
Chỉ trả về 1 block JSON duy nhất, không kèm markdown hay lời dẫn:
{{
  "id": "node_root",
  "title": "Tên Bài Học (2-5 từ)",
  "summary": "Tóm tắt tổng quan bài học (tối đa 40 từ)",
  "slide_page": "Slide 1-3",
  "type": "root",
  "children": [
    {{
      "id": "node_c1_1",
      "title": "Tên Chương Lớn (2-5 từ)",
      "summary": "Tóm tắt chương mục (tối đa 40 từ)",
      "slide_page": "Slide 4-15",
      "type": "branch",
      "children": [
        {{
          "id": "node_c2_1",
          "title": "Chủ Đề Con (2-5 từ)",
          "summary": "Tóm tắt chủ đề (tối đa 40 từ)",
          "slide_page": "Slide 4-8",
          "type": "branch",
          "children": [
            {{
              "id": "node_c3_1",
              "title": "Khái Niệm Cốt Lõi (2-5 từ)",
              "summary": "Giải thích khái niệm (tối đa 40 từ)",
              "slide_page": "Slide 5",
              "type": "concept",
              "cross_link": null,
              "children": [
                {{
                  "id": "node_c4_1",
                  "title": "Chi Tiết Thực Thi (2-5 từ)",
                  "summary": "Mô tả bước thực hiện hoặc tham số (tối đa 40 từ)",
                  "slide_page": "Slide 6",
                  "type": "detail",
                  "cross_link": null,
                  "detail": {{
                    "key_takeaway": "Điểm then chốt cần ghi nhớ...",
                    "ai_tutor_explanation": "Giải thích chi tiết từ góc nhìn thực hành...",
                    "code_snippet": "python -m venv .venv",
                    "quick_quiz": {{
                      "question": "Lệnh trên dùng để làm gì?",
                      "options": ["A. Tạo môi trường ảo venv", "B. Cài thư viện pip"],
                      "answer": "A",
                      "explanation": "Lệnh 'python -m venv .venv' tạo một môi trường Python ảo biệt lập cho dự án."
                    }}
                  }}
                }}
              ]
            }}
          ]
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
PIPELINE_MINDMAP_EXTRACTION_PROMPT = """[ROLE]: Chuyên gia Sư phạm Cấp cao & Kỹ sư Kiến trúc Tri thức VLearn AI.
[TASK]: Trích xuất cây sơ đồ tư duy đa tầng chi tiết (Deep Hierarchical Concept Mindmap) cho Day {day}.

[QUY TẮC BẮT BUỘC]:
1. KHÔNG BỎ SÓT KIẾN THỨC: Phân tích kỹ toàn bộ nội dung các trang slide được cung cấp. Tuyệt đối không lược bỏ các phần kiến thức cốt lõi, công cụ, công thức hay bước thực hành.
2. PHÂN RÃ ĐA CẤP SÂU (3-5 CẤP): Tạo cấu trúc cây có chiều sâu:
   Root (Bài học) -> Cấp 1 (Chương lớn) -> Cấp 2 (Chủ đề con / Quy trình) -> Cấp 3 (Khái niệm / Kỹ thuật) -> Cấp 4+ (Chi tiết / Bước thực hiện / Thông số / Code mẫu).
   Giúp người học vừa nắm được bức tranh tổng quan vừa tra cứu được tường tận từng chi tiết.
3. TITLE: Cực kỳ ngắn gọn (từ 2 đến 5 từ tiếng Việt), nêu đúng tên chủ đề hoặc khái niệm kỹ thuật.
4. SUMMARY: Khái quát cốt lõi KHÔNG QUÁ 40 TỪ. Nêu rõ ý chính, súc tích, không sao chép nguyên văn cả trang slide.
6. DETAIL: Bắt buộc cung cấp detail đầy đủ (key_takeaway: câu đúc kết cốt lõi; ai_tutor_explanation; code_snippet nếu có).
   - "quick_quiz": Trắc nghiệm tương tác compact tại các node khái niệm chính dạng {"question": "...", "options": ["A. ...", "B. ..."], "answer": "A", "explanation": "..."}. Node khác để null.

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
