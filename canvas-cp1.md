# Canvas CP1 — Nhóm BungChay (K4-3A-E403-BungChay)

> Nội dung này để copy trực tiếp vào form nộp CP1. Theo khung "7 dòng" ở `02-guide.md` §1.5: hướng · job executor · pain một câu · bằng chứng đầu tiên · lát cắt MỘT CÂU · automation dự kiến · willing users dự kiến · phân công có tên.

## 1. Hướng
Track A — VLearn Tutor · **A2 (Tính năng AI mới trên VLearn, cho học viên)**

## 2. Job executor + quy trình hiện tại
Học viên đang ôn tập/tổng hợp kiến thức từ slide bài giảng dài (PDF/PowerPoint nhiều trang) trên VLearn. Hiện tại: đọc lướt từng slide và tự ghi chép gạch đầu dòng, hoặc tự tay vẽ sơ đồ tư duy ra giấy/phần mềm (XMind, Canva...), hoặc dùng AI tóm tắt thành văn bản — nhưng vẫn phải tự ngồi vẽ lại mối liên hệ giữa các phần.

## 3. Nỗi đau cốt lõi (1 câu, không chữ AI)
Người học bị quá tải khi phải đọc lượng slide bài giảng dài và nhiều chữ, dẫn đến việc khó nhìn ra bức tranh tổng thể và mạch logic giữa các bài học. Việc tự tay tóm tắt hoặc vẽ sơ đồ tư duy tiêu tốn quá nhiều thời gian học tập; các phương pháp hiện tại (như AI tóm tắt văn bản thông thường) gây rời rạc và mất kết nối với trang slide bài giảng gốc.

## 4. Bằng chứng đầu tiên
**Chuẩn A** — khảo sát Google Form, **15/20 người ngoài nhóm đã trả lời** (⚠️ đang bổ sung thêm 5 người cho đủ mốc ≥20 trước CP4):

- **86,7% (13/15)** có ôn tập/tìm lại tài liệu slide bài giảng trong 7 ngày gần đây
- **73,3% (11/15)** chọn "slide quá dài, nhiều chữ, khó nhìn ra mạch logic tổng thể" là rào cản lớn nhất
- **26,7% (4/15)** chọn "mất quá nhiều thời gian, công sức nếu phải tự ngồi vẽ sơ đồ" là rào cản lớn nhất
- **60% (9/15)** đánh giá 4-5/5 điểm cho hiệu quả của học qua mindmap so với đọc văn bản truyền thống
- **100% (15/15) sẵn sàng dùng** công cụ tự động chuyển slide dài thành sơ đồ tư duy trực quan (40% chắc chắn sẽ dùng, 60% có thể sẽ thử, 0% không có nhu cầu)
- Quote nguyên văn: **P03** — *"Slide ngắn gọn nhưng vẫn thiếu connect"*; **P07** — *"Dài quá không đọc"*

⚠️ *Dòng "100% người đọc slide đều gặp khó khăn hệ thống lại kiến thức" trong bản nháp trước đó chưa xác định được câu hỏi khảo sát gốc tương ứng — đã bỏ khỏi canvas, cần đội Evidence kiểm lại trước khi dùng số này ở đâu khác.*

*(Chi tiết đầy đủ + link tiếp tục cập nhật: xem `spec.md` §1)*

## 5. Tác động (Impact)
- **53,3% (8/15)** tự vẽ/tóm tắt được nhưng tốn rất nhiều thời gian học bài
- **46,7% (7/15)** không nắm chắc mối liên hệ giữa các phần kiến thức
- **26,7% (4/15)** bỏ cuộc giữa chừng, học thuộc vẹt từng slide rời rạc
- Tần suất: **46,7%** gặp tình trạng quá tải slide ≥3 lần/tuần (26,7% × 3-5 lần, 20% × trên 5 lần); **53,3%** gặp 1-2 lần/tuần

## 6. Lát cắt MỘT CÂU
**Học viên** đang ôn một bài giảng dài cần **thấy mạch logic và mối liên hệ giữa các khái niệm** được **AI đọc slide/transcript, trích xuất đề mục và ý chính theo cấp bậc rồi dựng thành cây sơ đồ tương tác (chủ đề → khái niệm lớn → chi tiết con)** giúp **nắm tổng quan nhanh và click vào từng node để AI giải thích sâu hơn, có dẫn số trang slide gốc**.

## 7. Automation dự kiến
**Augment** — AI chỉ đề xuất cấu trúc cây + giải thích khi được hỏi, học viên tự quyết định học/ôn phần nào tiếp. Lý do (cost-of-error): nếu AI dựng cấu trúc chưa hoàn hảo thì chỉ gây khó chịu chứ không gây hiểu sai kiến thức, miễn mỗi node vẫn link về đúng trang slide gốc để học viên tự đối chiếu.

**Điều kiện & Căn cứ (Grounding):**
- Chỉ trích xuất từ nội dung có trong tài liệu tải lên, **không tự suy diễn** ngoài văn bản
- Mỗi nút/nhánh trên sơ đồ tư duy **phải gán kèm số trang slide nguồn** tương ứng để học viên bấm đối chiếu ngữ cảnh gốc

## 8. Willing users dự kiến (≥2 người ngoài nhóm)
- [x] Dương Đạt Khang
- [x] Tạ Việt Cường

## 9. Phân công có tên
*(⚠️ vai trò dưới đây là nháp từ README, cần nhóm xác nhận lại cho hướng cây sơ đồ)*

| Họ và Tên | MSSV | Vai trò |
|---|---|---|
| Nguyễn Hoàng Việt | 2A202602602 | **Đội trưởng** · Prompt & golden set |
| Phạm Quân | 2A202602890 | Evidence — mining + khảo sát |
| Đặng Hữu Tâm | 2A202602940 | Build — dựng prototype (cây sơ đồ + lời gọi AI thật) |
| Nguyễn Đỗ Chiến Thắng | 2A202602442 | Spec & validation |

---

**Thông tin nộp form CP1:**
- Đội trưởng: Nguyễn Hoàng Việt — MSSV 2A202602602
- Link repo GitHub công khai: https://github.com/vietnh04/K4-3A-E403-BungChay
