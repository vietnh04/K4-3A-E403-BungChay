# Kết quả chạy golden set — lượt 1

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
