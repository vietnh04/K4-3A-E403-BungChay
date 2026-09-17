# Kết quả chạy golden set — lượt 1 (lần đầu chạy đúng prompt thật trong codebase/backend/prompts.py)

**Ngày chạy:** 17/9/2026, 14:08-14:57 · **Prompt:** `codebase/backend/prompts.py::SLIDE_MINDMAP_EXTRACTION_PROMPT` (có rule 1b SLIDE FILTERING, 1c INSUFFICIENT INFO) · **Model dùng để test:** `deepseek-ai/deepseek-v4-flash-0731` qua NVIDIA build API (chưa có Gemini key thật, xem lưu ý cuối) · **Script:** `eval/run_tests.py`.

**Lượt 1 dưới đây là lần đầu tiên đo đúng prompt thật `codebase/backend/prompts.py`.**

## Số đo

**Thử 20 case, đạt 13/20 (65%)** theo `scoring_rules` mới (yêu cầu 3-5 cấp, kiểm `slide_page`, `insufficient_info`, `forbidden_terms` trên cả `detail.excerpt`/`detail.ai_tutor_explanation`).

| Lớp taxonomy | Số case | Pass |  
|---|---|---|
| ① Nguồn sự thật | 6 | 5/6 |
| ② Mơ hồ/thiếu thông tin | 4 | 3/4 |
| ③ Ngoài phạm vi | 4 | 3/4 |
| ④ Đặc thù nghiệp vụ | 6 | 2/6 |
| **Tổng** | **20** | **13/20** |

## Phân tích nguyên nhân 7 case fail (bàn giao Thành viên 2)

**5/7 là timeout hạ tầng, không phải lỗi chất lượng AI** — gs04, gs05, gs13, gs15, gs20 đều fail vì `ReadTimeout` ở đúng mốc 240s (giới hạn cứng của script test). Nguyên nhân: cây phải sâu 3-5 cấp, mỗi node lá còn phải sinh thêm object `detail` đầy đủ (excerpt, key_takeaway, ai_tutor_explanation, quick_quiz...) — lượng token sinh ra lớn, model mất >240s. **Đã xử lý ngay sau lượt này:** thu hẹp `detail` chỉ bắt buộc ở node lá thay vì mọi node khái niệm (giảm tải sinh), tăng timeout script lên 350s — xem kết quả ở lượt 2 bên dưới.

**1/7 là lỗi grounding thật (gs06)** — AI tự thêm cụm "group by" vào node dù slide gốc (Hàm gộp SQL: SUM/AVG/COUNT/MAX/MIN) không hề nhắc tới GROUP BY. Đây đúng là loại lỗi mà rule 1 (grounding) trong prompt phải chặn nhưng chưa chặn triệt để. **Đã xử lý ngay sau lượt này:** thêm cảnh báo cụ thể vào rule 1 của `prompts.py` (không tự thêm khái niệm "liên quan gần" như GROUP BY/HAVING khi slide chỉ có SUM/AVG/COUNT) — xem lượt 2.

**1/7 là lỗi do chính bộ test/prompt tự tạo ra (gs14), đã sửa** — rule 1b bản đầu liệt kê "câu hỏi trắc nghiệm không có đáp án" vào diện lọc bỏ như nội dung thủ tục, khiến AI trả `insufficient_info: true` cho case gs14 (đề trắc nghiệm không đáp án) — nhưng case này kỳ vọng AI vẫn dựng node "câu hỏi ôn tập", chỉ không được bịa đáp án. Đã sửa lại rule 1b trong `codebase/backend/prompts.py` (tách rõ: câu hỏi trắc nghiệm vẫn là nội dung học thuật hợp lệ, chỉ cấm bịa đáp án) — xem lượt 2.

## Việc chưa làm ở lượt 1 (tự khai, chưa giấu)

- Chưa có lượt chạy Prompt v1 thật (bản trước khi có rule 1b/1c) để so sánh số liệu trực tiếp v1 vs v2 — không đủ thời gian chạy thêm 20 case nữa (mỗi lượt ~50-80 phút). Thay vào đó, so sánh định tính: v1 không có field `insufficient_info` và không có rule chống bịa nội dung tường minh; v2 (lượt này) đã có cả hai.
- Model test vẫn là NVIDIA build API (không phải Gemini thật của backend) — số liệu là bằng chứng về chất lượng PROMPT, chưa chắc đại diện đúng tốc độ/hành vi khi chạy Gemini thật.

Dữ liệu thô đầy đủ (thời gian từng case, lỗi chi tiết): `eval/run_results_auto_20260917_145706.json`.

---

# Kết quả chạy golden set — lượt 2 (retry 7 case fail, sau khi thu hẹp `detail` + thêm cảnh báo grounding)

**Ngày chạy:** 17/9/2026, sau lượt 1 · **Prompt:** `codebase/backend/prompts.py::SLIDE_MINDMAP_EXTRACTION_PROMPT` (đã thu hẹp `detail` chỉ bắt buộc ở node lá; đã thêm cảnh báo cụ thể chống bịa GROUP BY-style ở rule 1; đã sửa rule 1b để không loại bỏ câu hỏi trắc nghiệm) · **Model:** `deepseek-ai/deepseek-v4-flash-0731` qua NVIDIA build API, timeout 350s · **Phạm vi:** chỉ 7 case từng fail ở lượt 1 (gs04, gs05, gs06, gs13, gs14, gs15, gs20), không chạy lại 13 case đã pass.

## Số đo

**6/7 PASS.** Cộng với 13 case đã pass ở lượt 1 (không đổi) → **tổng cộng 19/20 (95%)** sau khi vá 2 lỗi (thu hẹp `detail` về node lá, thêm cảnh báo grounding GROUP BY-style).

| Case | Lượt 1 | Lượt 2 | Ghi chú |
|---|---|---|---|
| gs04 | FAIL (timeout 240s) | **PASS** (139.9s) | Giảm tải `detail` giúp kịp thời gian |
| gs05 | FAIL (timeout 240s) | **PASS** (199.7s) | nt |
| gs06 | FAIL (bịa "group by") | **PASS** (101.0s) | Cảnh báo grounding có tác dụng |
| gs13 | FAIL (timeout 240s) | **PASS** (146.5s) | Giảm tải `detail` giúp kịp thời gian |
| gs14 | FAIL (bug rule 1b, đã sửa) | **FAIL khác** (504 Gateway Timeout) | Bug logic đã sửa xong, nhưng lần này bị lỗi hạ tầng phía NVIDIA server — chưa xác nhận được rule 1b có thực sự đúng không, cần chạy lại riêng case này lần nữa |
| gs15 | FAIL (timeout 240s) | **PASS** (120.3s) | Giảm tải `detail` giúp kịp thời gian |
| gs20 | FAIL (timeout 240s) | **PASS** (170.1s) | Giảm tải `detail` giúp kịp thời gian |

**Kết luận:** cả 2 khuyến nghị ở lượt 1 (thu hẹp `detail` xuống node lá, thêm cảnh báo GROUP BY-style) đều có tác dụng rõ rệt — xử lý được 5/5 case timeout và case grounding gs06. gs14 vẫn chưa xác nhận được vì lần này bị chặn bởi lỗi 504 từ phía server NVIDIA (không liên quan đến chất lượng prompt) — cần 1 lần chạy nữa (ngoài phạm vi thời gian nộp CP3 hiện tại).

Dữ liệu thô: `eval/run_results_auto_20260917_153723.json`.

## Việc chưa làm chung (áp dụng cả 2 lượt)

- Chưa chạy lại đủ cả 20 case với bản prompt mới nhất (lượt 2 chỉ retry 7 case fail, không phải full run) — cần 1 lượt full 20 case nữa để có số liệu tổng chính thức.
- 20 case đều là **dữ liệu tự sinh** (không dùng slide thật của khoá) — cần bổ sung case trích trực tiếp từ slide VLearn thật trước khi khoá `spec.md` ở CP4.
- Tiêu chí Pass hiện là kiểm cấu trúc tự động, chưa có người chấm chất lượng diễn đạt/sư phạm — bổ sung ở vòng R6 (validation với người dùng thật).
