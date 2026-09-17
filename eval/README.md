# eval/ — Golden set & kết quả kiểm thử

## File

- `golden_set.json` — 20 case kiểm thử cho prompt trích xuất cấu trúc thật đang chạy trong backend (`codebase/backend/prompts.py::SLIDE_MINDMAP_EXTRACTION_PROMPT`, gọi qua `build_upload_slide_prompt` trong `mindmap_service.py`).
- `run_results.md` — bảng kết quả chạy thật (số đo cho CP3: thử bao nhiêu, đúng bao nhiêu).
- `run_tests.py` — script chạy tự động 20 case qua backend thật (Gemini API) và tự chấm Pass/Fail.

## Cập nhật quan trọng (2026-09-17): đồng bộ với schema thật của prompt

Bản trước của file này giả định prompt thật chỉ có 1 lời gọi AI, cấu trúc tối đa 2 cấp, field `source_pages`, và **không có** cơ chế báo thiếu thông tin — nên phải "diễn giải lại" lớp ②③ để test được. Sau khi rà lại `codebase/backend/prompts.py`, phát hiện prompt thật thực ra bắt buộc **3-5 cấp sâu** (`id/title/summary/slide_page/type/detail/children`), không phải 2 cấp, và **thiếu hẳn** rule chống bịa nội dung (grounding) + rule báo thiếu thông tin.

Đã xử lý bằng cách bổ sung trực tiếp vào `codebase/backend/prompts.py` (mục 1b SLIDE FILTERING, 1c INSUFFICIENT INFO ở `SLIDE_MINDMAP_EXTRACTION_PROMPT`; mục 7-8 ở `PIPELINE_MINDMAP_EXTRACTION_PROMPT`) thêm field `insufficient_info` ở cấp root. Bộ 20 case dưới đây giờ test đúng theo schema thật, không còn phải "diễn giải lại":

| Lớp | Ý nghĩa gốc | Test theo prompt thật (đã vá) |
|---|---|---|
| ① Nguồn sự thật | AI bịa thông tin không có căn cứ | Kiểm tra `title`/`summary`/`detail.excerpt`/`detail.ai_tutor_explanation` của MỌI node không chứa `forbidden_terms` — tức không thêm khái niệm ngoài slide gốc |
| ② Mơ hồ/thiếu thông tin | Input không đủ rõ để trả lời chắc chắn | Kiểm tra `insufficient_info` đúng theo kỳ vọng (rule 1c); nếu `true` thì `children` phải rỗng, không ép bịa cho đủ 3-5 cấp |
| ③ Ngoài phạm vi/thẩm quyền | Yêu cầu vượt phạm vi hệ thống được giao | Nội dung **không phải bài giảng thật** (trang bìa, đề thi, thông báo hành chính, ảnh không chữ) — AI phải lọc bỏ theo rule 1b, trả `insufficient_info: true` |
| ④ Đặc thù nghiệp vụ | Case đặc thù miền chuyên môn | Slide có định dạng đặc thù (code, SQL, cấu trúc dữ liệu) — kiểm tra trích xuất đúng kỹ thuật, đủ 3-5 cấp, không làm hỏng thuật ngữ |

**Rủi ro còn lại (chưa đo được bằng golden set này):** chất lượng thật của việc AI tự quyết định "đủ căn cứ hay không" chỉ được xác nhận khi chạy qua API thật (xem `run_tests.py` + `run_results.md`) — 2 rule mới (1b/1c) là suy luận ngôn ngữ tự nhiên, không có validation cứng ở code, nên vẫn có khả năng model không tuân thủ 100%. Đây chính là lý do golden set + runner script tồn tại: để đo tỷ lệ tuân thủ thật, không phải chỉ tin vào prompt viết đúng ý.

## Về tỷ lệ common/edge

Ảnh phân công ghi "8-10 case phổ biến" và "2-4 case hiếm gặp". Bộ này có **16 common / 4 edge** (đúng trần edge=4) — common vượt 10 vì đa số slide bài giảng thật đều thuộc dạng "phổ biến hàng ngày" (bài học bình thường), số 8-10 được hiểu là **số sàn tối thiểu** chứ không phải giới hạn trên, nếu không sẽ phải cố nhét thêm case giả tạo cho đủ tỷ lệ.

## Cách chấm Pass/Fail

Không so khớp chữ tuyệt đối (AI diễn đạt khác nhau mỗi lần chạy). Một case **Pass** khi thoả cả 5 điều kiện trong `scoring_rules` của `golden_set.json`:
1. Response là JSON hợp lệ, parse trực tiếp được.
2. `insufficient_info` đúng như kỳ vọng — nếu `true` thì `children` phải rỗng.
3. Nếu `insufficient_info` kỳ vọng là `false`: mọi số trang trong `must_cover_pages` phải xuất hiện trong field `slide_page` của ít nhất 1 node ở bất kỳ cấp nào, VÀ cây phải sâu tối thiểu 3 cấp (đúng RULE 2 của prompt thật).
4. Không chứa từ khoá trong `forbidden_terms` ở `title`/`summary`/`detail.excerpt`/`detail.ai_tutor_explanation` của bất kỳ node nào (dấu hiệu bịa nội dung ngoài nguồn).
5. Cấu trúc không vượt quá 5 cấp.

Chạy `python eval/run_tests.py` để tự động chấm 20 case qua backend thật — xem hướng dẫn cụ thể ở cuối file này hoặc hỏi lại trong chat. Case nào fail điều kiện nào, script sẽ in rõ lý do và ghi vào `run_results.md` để dùng làm bằng chứng "vì sao sai" (ăn điểm hơn nói suông theo README chấm điểm khoá).
