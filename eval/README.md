# eval/ — Golden set & kết quả kiểm thử

## File

- `golden_set.json` — 20 case kiểm thử cho prompt trích xuất cấu trúc (`codebase/prompts/system_prompt_v2.md`).
- `run_results.md` — bảng kết quả chạy thật (số đo cho CP3: thử bao nhiêu, đúng bao nhiêu).

## Quy ước taxonomy 4 lớp chỗ khó

Sản phẩm hiện chỉ có **1 lời gọi AI** (đọc slide → dựng cây), chưa có lời gọi AI thứ hai cho tính năng "click node để giải thích thêm" (canvas §7). Vì vậy 2 lớp ③④ trong taxonomy được diễn giải lại để test được trong phạm vi lời gọi AI đang có, thay vì bỏ trống:

| Lớp | Ý nghĩa gốc (theo bảng phân công) | Diễn giải áp dụng cho lời gọi trích xuất cấu trúc |
|---|---|---|
| ① Nguồn sự thật | AI bịa thông tin không có căn cứ | Slide có nội dung rõ ràng — kiểm tra AI không thêm khái niệm/thuật ngữ ngoài văn bản gốc (xem `forbidden_terms` mỗi case) |
| ② Mơ hồ/thiếu thông tin | Input không đủ rõ để trả lời chắc chắn | Slide quá ngắn/thiếu chi tiết — kiểm tra AI báo `insufficient_info` đúng, không ép bịa cho đủ |
| ③ Ngoài phạm vi/thẩm quyền | Yêu cầu vượt phạm vi hệ thống được giao | Nội dung đưa vào **không phải bài giảng thật** (trang bìa, đề thi trắc nghiệm, thông báo hành chính, hình không có chữ) — kiểm tra AI không cố dựng cây giả cho nội dung không phải kiến thức |
| ④ Đặc thù nghiệp vụ | Case đặc thù miền chuyên môn | Slide có định dạng đặc thù (code, công thức SQL, cây cấu trúc dữ liệu) — kiểm tra AI trích xuất đúng, không làm hỏng thuật ngữ kỹ thuật |

**Khi nào cần đổi lại quy ước này:** nếu sau này team build thêm lời gọi AI thứ hai (giải thích node), nên viết bộ case ③④ riêng đúng nghĩa gốc (câu hỏi ngoài phạm vi tài liệu / câu hỏi đặc thù nghiệp vụ do học viên tự gõ) cho lời gọi đó, giữ nguyên bộ 20 case này cho lời gọi trích xuất.

## Về tỷ lệ common/edge

Ảnh phân công ghi "8-10 case phổ biến" và "2-4 case hiếm gặp". Bộ này có **16 common / 4 edge** (đúng trần edge=4) — common vượt 10 vì đa số slide bài giảng thật đều thuộc dạng "phổ biến hàng ngày" (bài học bình thường), số 8-10 được hiểu là **số sàn tối thiểu** chứ không phải giới hạn trên, nếu không sẽ phải cố nhét thêm case giả tạo cho đủ tỷ lệ.

## Cách chấm Pass/Fail

Không so khớp chữ tuyệt đối (AI diễn đạt khác nhau mỗi lần chạy). Một case **Pass** khi thoả cả 4 điều kiện trong `scoring_rules` của `golden_set.json`:
1. Response là JSON hợp lệ, parse trực tiếp được (không bọc markdown).
2. `insufficient_info` đúng như kỳ vọng.
3. Nếu không phải insufficient_info: mọi số trang trong `must_cover_pages` phải xuất hiện trong `source_pages` của ít nhất 1 node.
4. Không chứa từ khoá trong `forbidden_terms` (dấu hiệu bịa nội dung ngoài nguồn).
5. Cấu trúc tối đa 2 cấp.

Case nào fail điều kiện nào, ghi rõ trong `run_results.md` để dùng làm bằng chứng "vì sao sai" (ăn điểm hơn nói suông theo README chấm điểm khoá).
