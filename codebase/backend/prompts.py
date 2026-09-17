"""
VLearn System Prompts & Prompt Templates
Dự án: Mini Hackathon AI - Batch 04 · Track A (VLearn Tutor / ConceptMap)
Nhóm: BungChay · Phòng: E403 · Lớp: 3A

Tách biệt hoàn toàn System Prompts khỏi Code Logic (FastAPI / D3 Canvas / Pipeline).
Tối ưu hóa: Phân rã cấu trúc đa cấp sâu (Multi-level Deep Mindmap), bao quát toàn bộ nội dung slide
không bị nông, không bỏ sót kiến thức, vừa có cái nhìn tổng quan vừa xem được chi tiết từng phần.
"""

# ==============================================================================
# 1. SYSTEM PROMPT: TRÍCH XUẤT MINDMAP KHI UPLOAD SLIDE MỚI (LIVE WEBSERVER)
# ==============================================================================
SLIDE_MINDMAP_EXTRACTION_PROMPT = """[ROLE]: Chuyên gia Sư phạm Cấp cao & Kỹ sư Kiến trúc Tri thức VLearn AI.
[TASK]: Phân tích toàn diện nội dung toàn bộ các trang slide bài giảng sau đây và trích xuất thành Cây Sơ Đồ Tư Duy Đa Tầng Chi Tiết (Deep Hierarchical Mindmap) định dạng JSON.

[BỐI CẢNH CÁC BÀI HỌC TRƯỚC ĐÓ (để tạo liên kết chéo nếu có liên quan)]:
{knowledge_context}

[QUY TẮC BẮT BUỘC VỀ PHÂN RÃ CẤU TRÚC VÀ ĐỘ BAO PHỦ KIẾN THỨC]:
1. NGUYÊN TẮC KHÔNG BỎ SÓT KIẾN THỨC (ZERO KNOWLEDGE LOSS):
   - Phân tích cẩn thận và bao quát TOÀN BỘ các trang slide được cung cấp trong [DỮ LIỆU SLIDE CẦN XỬ LÝ].
   - Không được bỏ sót các ý chính, định nghĩa, bước thực thi, công thức, cú pháp lệnh hay lưu ý kỹ thuật.
   - Phân bổ đều khắp các slide từ đầu đến cuối bài giảng, không chỉ tập trung ở một vài slide đầu.

2. CẤU TRÚC PHÂN CẤP ĐA TẦNG SÂU (MULTI-LEVEL DEEP HIERARCHY):
   - Sơ đồ PHẢI phân rã từ 3 đến 5 cấp nhánh chi tiết (thay vì nông hay bằng phẳng) để vừa có cái nhìn khái quát, vừa xem được chi tiết sâu từng slide:
     * Cấp 0 (Root): Tên tổng thể bài giảng (1 node duy nhất).
     * Cấp 1 (Chương / Module chính): Các phần lớn / chương mục của buổi học.
     * Cấp 2 (Tiểu mục / Chủ đề con): Các chủ đề hoặc quy trình cụ thể trong từng chương.
     * Cấp 3 (Khái niệm cốt lõi / Kỹ thuật / Công cụ): Định nghĩa, cơ chế hoạt động, thuật toán, mô hình.
     * Cấp 4+ (Chi tiết sâu / Bước thực hiện / Tham số / Ví dụ / Cú pháp code / Lưu ý thực chiến): Tiếp tục phân nhánh sâu nếu khái niệm đó có nhiều bước, nhiều thành phần con hoặc các trường hợp đặc biệt trên slide.

3. TIÊU ĐỀ NODE (title):
   - RẤT NGẮN GỌN (từ 2 đến 5 từ tiếng Việt, ví dụ: 'Cơ Chế Attention', 'Vòng Lặp ReAct', 'Ma Trận Tác Động', 'Local Checklist').
   - Đi thẳng vào trọng tâm khái niệm, giúp người học đọc lướt sơ đồ là nắm được cấu trúc.

4. TÓM TẮT CỐT LÕI (summary):
   - KHÔNG ĐƯỢC QUÁ 40 TỪ. Súc tích, nêu bật bản chất, vai trò hoặc ý niệm quan trọng nhất, không sao chép nguyên văn cả đoạn văn bản dài từ slide.

5. TRÍCH DẪN SỐ TRANG (slide_page):
   - Bắt buộc ghi rõ trang slide gốc (ví dụ: 'Slide 4', 'Slide 9-11'). Mọi node đều phải có nguồn gốc slide minh chứng.

6. LIÊN KẾT CHÉO (cross_link):
   - Nếu một khái niệm kế thừa, bổ trợ hoặc liên quan mật thiết đến kiến thức của Day 1-5, hãy thêm:
     "cross_link": {{
         "target_day": 1..5,
         "target_node_id": "id_ngay_truoc",
         "label": "🔗 Kế thừa từ Day X [Slide Y]"
     }}
     Nếu không có liên kết chéo thì đặt null.

7. CHI TIẾT MỞ RỘNG (detail):
   - Ở các node lá (leaf nodes) hoặc các node khái niệm/kỹ thuật quan trọng, bắt buộc cung cấp object "detail" phong phú:
     * "title": Tiêu đề đầy đủ của khái niệm/bước kỹ thuật
     * "slide_page": Trang slide trích dẫn
     * "excerpt": Đoạn trích dẫn nguyên văn ngắn gọn từ slide
     * "key_takeaway": Điểm mấu chốt học viên bắt buộc phải nhớ
     * "ai_tutor_explanation": Lời giảng giải sư phạm thực chiến, dễ hiểu từ góc nhìn chuyên gia AI Tutor
     * "code_snippet": Cú pháp lệnh terminal, code mẫu, hoặc tham số cấu hình (nếu có trên slide, nếu không thì null)
     * "quick_quiz": Một câu hỏi trắc nghiệm nhanh kiểm tra độ hiểu bài kèm đáp án rõ ràng.

[SCHEMA JSON TRẢ VỀ (MINH HOẠ CẤU TRÚC ĐA CẤP SÂU)]:
{{
  "id": "node_root",
  "title": "Tên Bài Giảng (2-5 từ)",
  "summary": "Khái quát toàn bộ buổi học dưới 40 từ.",
  "slide_page": "Slide 1-3",
  "type": "root",
  "children": [
    {{
      "id": "node_sec1",
      "title": "Tên Chương Lớn (2-5 từ)",
      "summary": "Tóm tắt chương dưới 40 từ.",
      "slide_page": "Slide 4-10",
      "type": "branch",
      "children": [
        {{
          "id": "node_sec1_sub1",
          "title": "Tên Chủ Đề Con (2-5 từ)",
          "summary": "Tóm tắt chủ đề con dưới 40 từ.",
          "slide_page": "Slide 4-6",
          "type": "branch",
          "children": [
            {{
              "id": "node_sec1_sub1_c1",
              "title": "Khái Niệm Cốt Lõi (2-5 từ)",
              "summary": "Giải thích khái niệm cốt lõi dưới 40 từ.",
              "slide_page": "Slide 5",
              "type": "concept",
              "cross_link": null,
              "detail": {{
                "title": "Tiêu đề đầy đủ của khái niệm",
                "slide_page": "Slide 5",
                "excerpt": "Trích đoạn thực tế từ slide...",
                "key_takeaway": "Điểm mấu chốt cần nhớ...",
                "ai_tutor_explanation": "Lời giải thích sư phạm từ AI Tutor...",
                "code_snippet": null,
                "quick_quiz": "Câu hỏi kiểm tra nhanh? A. Lựa chọn 1 | B. Lựa chọn 2. Đáp án: A"
              }},
              "children": [
                {{
                  "id": "node_sec1_sub1_c1_d1",
                  "title": "Chi Tiết / Thực Thi (2-5 từ)",
                  "summary": "Mô tả bước thực hiện hoặc tham số kỹ thuật dưới 40 từ.",
                  "slide_page": "Slide 6",
                  "type": "detail",
                  "cross_link": null,
                  "detail": {{
                    "title": "Chi tiết bước thực thi và lưu ý kỹ thuật",
                    "slide_page": "Slide 6",
                    "excerpt": "Cú pháp hoặc quy tắc cụ thể từ slide...",
                    "key_takeaway": "Lưu ý quan trọng khi triển khai...",
                    "ai_tutor_explanation": "Hướng dẫn thực chiến...",
                    "code_snippet": "python -m command --param value",
                    "quick_quiz": "Câu hỏi nhanh về thông số? Đáp án: ..."
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
5. SLIDE_PAGE: Ghi rõ số trang slide trích dẫn ('Slide X' hoặc 'Slide X-Y').
6. DETAIL: Bắt buộc cung cấp detail đầy đủ (excerpt, key_takeaway, ai_tutor_explanation, code_snippet nếu có, quick_quiz) cho các node khái niệm và node chi tiết.

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
