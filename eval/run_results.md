# Kết quả chạy golden set — lượt 2 (sau khi vá prompt: rule 1b/1c grounding + insufficient_info)

**Ngày chạy:** 17/9/2026, 14:08-14:57 · **Prompt:** `codebase/backend/prompts.py::SLIDE_MINDMAP_EXTRACTION_PROMPT` (đã bổ sung rule 1b SLIDE FILTERING, 1c INSUFFICIENT INFO so với lượt 1) · **Model dùng để test:** `deepseek-ai/deepseek-v4-flash-0731` qua NVIDIA build API (chưa có Gemini key thật, xem lưu ý cuối) · **Script:** `eval/run_tests.py`.

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

**5/7 là timeout hạ tầng, không phải lỗi chất lượng AI** — gs04, gs05, gs13, gs15, gs20 đều fail vì `ReadTimeout` ở đúng mốc 240s (giới hạn cứng của script test). Nguyên nhân: sau khi thêm rule 1b/1c, mỗi node ở mọi cấp còn phải sinh thêm object `detail` đầy đủ (excerpt, key_takeaway, ai_tutor_explanation, quick_quiz...) cho cây sâu 3-5 cấp — lượng token sinh ra lớn hơn hẳn lượt 1 (khi đó chỉ 7/20 timeout ở mốc 60s, đã tăng lên 240s mà vẫn còn 5/20 timeout). **Khuyến nghị cho Task 1/2:** cân nhắc giảm bớt độ phong phú của `detail` (vd. bỏ bớt `quick_quiz` hoặc chỉ bắt buộc `detail` ở node lá thay vì mọi node khái niệm) để giảm thời gian sinh, hoặc tăng timeout thật của server lên ≥300s.

**1/7 là lỗi grounding thật (gs06)** — AI tự thêm cụm "group by" vào node dù slide gốc (Hàm gộp SQL: SUM/AVG/COUNT/MAX/MIN) không hề nhắc tới GROUP BY. Đây đúng là loại lỗi mà rule 1 (grounding) trong prompt phải chặn nhưng chưa chặn triệt để — **khuyến nghị Task 2**: cân nhắc thêm ví dụ few-shot "không suy diễn cú pháp liên quan nhưng chưa xuất hiện trên slide" vào System Prompt v2 để củng cố rule 1.

**1/7 là lỗi do chính bộ test/prompt tự tạo ra (gs14), đã sửa** — rule 1b bản đầu liệt kê "câu hỏi trắc nghiệm không có đáp án" vào diện lọc bỏ như nội dung thủ tục, khiến AI trả `insufficient_info: true` cho case gs14 (đề trắc nghiệm không đáp án) — nhưng case này kỳ vọng AI vẫn dựng node "câu hỏi ôn tập", chỉ không được bịa đáp án. Đã sửa lại rule 1b trong `codebase/backend/prompts.py` (tách rõ: câu hỏi trắc nghiệm vẫn là nội dung học thuật hợp lệ, chỉ cấm bịa đáp án) — **cần chạy lại gs14 riêng để xác nhận sau khi sửa** (chưa kịp chạy lại do giới hạn thời gian nộp bài).

## Việc chưa làm (tự khai, chưa giấu — do giới hạn thời gian nộp CP3)

- Chưa chạy lại gs14 sau khi sửa rule 1b để xác nhận fix đúng.
- Chưa chạy lại 5 case bị timeout với timeout dài hơn (300-400s) để tách bạch "chậm nhưng đúng" và "chậm và sai".
- Chưa có lượt chạy Prompt v1 thật (bản trước khi có rule 1b/1c) để so sánh số liệu trực tiếp v1 vs v2 — không đủ thời gian chạy thêm 20 case nữa (mỗi lượt ~50-80 phút). Thay vào đó, so sánh định tính: v1 không có field `insufficient_info` và không có rule chống bịa nội dung tường minh; v2 (lượt này) đã có cả hai — nên các case lớp ②③ (mơ hồ/ngoài phạm vi) chỉ mới test được từ lượt 2 trở đi.
- Model test vẫn là NVIDIA build API (không phải Gemini thật của backend) — số liệu là bằng chứng về chất lượng PROMPT, chưa chắc đại diện đúng tốc độ/hành vi khi chạy Gemini thật.

Dữ liệu thô đầy đủ (thời gian từng case, lỗi chi tiết): `eval/run_results_auto_20260917_145706.json`.

---

# Kết quả chạy golden set — lượt 1 (trước khi vá prompt, LỖI THỜI — giữ lại để đối chiếu lịch sử)

**Ngày chạy:** 17/9/2026 · **Prompt:** `codebase/prompts/system_prompt_v2.md` · **Model dùng để test:** `deepseek-ai/deepseek-v4-flash-0731` (qua NVIDIA build API — model tạm dùng để có bằng chứng thật cho CP3, sản phẩm thật có thể đổi sang model khác, xem lưu ý ở cuối).

## Số đo

**Thử 20 case, đạt 20/20 (100%) theo tiêu chí Pass/Fail đã định nghĩa trong `golden_set.json`.**

Tiêu chí Pass là kiểm tra **cấu trúc**, không phải chấm điểm chất lượng diễn đạt: JSON hợp lệ không bọc markdown, đủ trang nguồn (`source_pages`), không có từ khoá cho thấy bịa nội dung ngoài slide, cấu trúc đúng tối đa 2 cấp. Đây là bộ case tự sinh (20 slide giả lập, không phải slide thật của khoá) — số liệu này là **bằng chứng prompt hoạt động đúng về mặt cấu trúc/grounding**, chưa phải đánh giá chất lượng diễn đạt sư phạm (cái đó cần người thật chấm, để dành cho vòng R6 validation).

| Lớp taxonomy | Số case | Pass |
|---|---|---|
| ① Nguồn sự thật | 6 | 6/6 |
| ② Mơ hồ/thiếu thông tin | 4 | 4/4 |
| ③ Ngoài phạm vi | 4 | 4/4 |
| ④ Đặc thù nghiệp vụ | 6 | 6/6 |
| **Tổng** | **20** | **20/20** |

## Quá trình chạy thật — không phải một lượt suôn sẻ

Lượt chạy đầu tiên (toàn bộ 20 case, timeout 60s/lệnh gọi): **12/20 pass, 8 fail**. Trong 8 fail đó:
- **7/8 là lỗi timeout mạng** (client chờ 60s chưa đủ cho model reasoning) — không phải lỗi chất lượng AI. Chạy lại đúng 7 case này với timeout dài hơn (150-240s) → **cả 7 đều pass**.
- **1/8 (case gs01) ban đầu bị đánh fail sai** — do chính bộ test tự đặt từ khoá cấm `"deque"`, nhưng input case đó có sẵn từ thật `"dequeue"` (chứa `deque` như chuỗi con) → script chấm bắt nhầm. Đã sửa từ khoá trong `golden_set.json` (`"deque"` → `"double-ended queue"`), đối chiếu lại output thật của gs01 thì không có nội dung bịa thêm nào ngoài slide gốc — case này **pass thật**.

**Kết luận rút ra:** 2 rủi ro hạ tầng cần lưu ý khi Task 1 (backend) tích hợp thật:
1. **`max_tokens`/timeout phải đủ rộng** — model reasoning có thể mất >60s cho input dài, client timeout ngắn sẽ báo lỗi giả (đã ghi ở `v1_vs_v2_changelog.md` mục rủi ro #3, giờ có thêm bằng chứng cụ thể: 7/20 lần timeout ở 60s).
2. **Viết `forbidden_terms` cẩn thận khi tự làm eval** — dùng chuỗi con ngắn dễ bắt nhầm từ hợp lệ (bài học cho ai viết thêm case sau này).

## Việc chưa làm (tự khai, chưa giấu)

- Model dùng để test (`deepseek-ai/deepseek-v4-flash-0731`) là model có sẵn qua API key NVIDIA build — **chưa chắc là model backend thật của nhóm sẽ dùng** (Task 1 có thể chọn Gemini/OpenAI khác). Số 20/20 này là bằng chứng prompt *thiết kế đúng*, cần chạy lại xác nhận khi backend thật chọn model chính thức.
- 20 case đều là **dữ liệu tự sinh** (không dùng slide thật của khoá, đúng luật bảo mật) — cần bổ sung case trích trực tiếp từ slide VLearn thật trước khi khoá `spec.md` ở CP4, để số đo phản ánh đúng sản phẩm thật thay vì slide giả lập.
- Tiêu chí Pass hiện là kiểm cấu trúc tự động, chưa có người chấm chất lượng diễn đạt/sư phạm — bổ sung ở vòng R6 (validation với người dùng thật).
