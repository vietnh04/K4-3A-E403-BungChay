# AI SPEC — Tutor nói rõ khi không có căn cứ · Nhóm BungChay · Zone 1
Hướng: [x] A — VLearn  [ ] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [x] Tối ưu tính năng có sẵn (A1)  [ ] Tính năng mới

> ⚠️ **[NHÁP — chờ nhóm xác nhận]** Job executor và hướng A1 dưới đây là đề xuất dựa trên mining chatlog, chưa được cả nhóm chốt. Sửa lại nếu nhóm chọn hướng khác.

## §1. User & Job
- Job executor + workflow: Học viên đang xem bài giảng trong trang học VLearn, bôi đen một đoạn tài liệu/slide hoặc gõ câu hỏi để hỏi tutor ngay trong lúc học.
- Core JTBD: Hiểu ngay một khái niệm trong bài đang xem mà không phải dừng lại tự tra cứu nơi khác.
- Problem statement (KHÔNG chữ AI): Khi học viên hỏi về nội dung chưa có sẵn trong tài liệu đang mở (ví dụ video chưa được chuyển thành văn bản), câu trả lời nhận được không nói rõ đây là kiến thức ngoài khoá — học viên không biết khi nào nên tin, khi nào cần tự kiểm lại.
- Evidence (chuẩn B — mining `data/vlearn-pack/chatlog/tutor_turns.csv`, phương pháp: lọc `is_preset=False` rồi đếm `has_citation=False` bằng pandas, script lưu tại `evidence/mining_chatlog.py`):
  - **34,6% câu hỏi thật không được trích dẫn nguồn** (3.609/10.427 lượt, toàn khoá); riêng khoá K4 hiện tại: **32,8%** (838/2.555)
  - Tutor gần như không hỏi lại khi câu hỏi mơ hồ: `ask_probing_question` chỉ 28/13.494 lượt (0,2%); K4 chỉ 6/3.097
  - ≥5 quote nguyên văn (turn_id dẫn nguồn trong `tutor_turns.csv`):
    - `[T10424]` Q: "LLM là gì" → A: *"thầy hiện chưa có lời giảng chi tiết từ video để trích xuất nội dung bài học cho em, nhưng anh có thể giúp em hiểu khái niệm này theo kiến thức nền tảng của khóa học."*
    - `[T10405]` Q: "LLM là gì" (học viên khác, cùng bài) → A: *"Vì nội dung của đoạn video em đang xem chưa có dạng văn bản, anh chưa thể trích xuất chính xác định nghĩa từ tài liệu bài giảng cho em."*
    - `[T13311]` Q: "tỉ lệ LLM trả lời dùng một tool không có trong tool schema là bao nhiêu %?" → A: trả lời chung chung, không trích dẫn, không nói rõ đây là ước lượng ngoài tài liệu khoá
    - `[T13469]` Q: hỏi cách tính keyframe trung bình mỗi track trong bài lab → A: hướng dẫn tự suy luận, không trích dẫn tài liệu
    - `[T10341]` Q: "Tôi nên bắt đầu từ đâu" → A: trả lời có cấu trúc nhưng không trích trang cụ thể
  - **[CHƯA LÀM — cần nhóm]** Chuẩn A: khảo sát ≥20 học viên ngoài nhóm, ≥50% xác nhận, log câu hỏi + trả lời nguyên văn

## §2. Impact & quyết định chọn
- Bảng impact (≥3 ứng viên, số liệu từ mining ở trên):

  | Ứng viên | Bao nhiêu người gặp | Tần suất | Tốn gì mỗi lần | Build nổi không | Chọn? |
  |---|---|---|---|---|---|
  | Tutor không trích dẫn khi trả lời (không nói rõ ranh giới tài liệu) | 32,8% lượt hỏi thật của K4 (838/2.555) | mỗi lần hỏi ngoài phạm vi tài liệu đang mở | học viên không biết tin hay không, có thể học nhầm kiến thức ngoài khoá | Có — sửa logic quyết định trung tâm (conditional response) | ✅ Chọn |
  | Tutor không hỏi lại khi câu hỏi mơ hồ | chỉ 6/3.097 lượt K4 có hỏi lại | hiếm | trả lời sai hướng, học viên phải hỏi lại | Có, nhưng cần thêm logic phân loại mơ hồ — phạm vi rộng hơn | Loại — ít bằng chứng định lượng trực tiếp về hậu quả hơn |
  | Giảng viên không biết lớp đang kẹt ở đâu (A2) | cả lớp mỗi buổi | mỗi buổi học | ôn sai trọng tâm buổi sau | Khó hơn trong thời gian sự kiện — cần tổng hợp nhiều lượt | Loại — build nặng hơn, ít thời gian |

- Ứng viên ĐÃ LOẠI + vì sao: "Tutor không hỏi lại khi mơ hồ" và "bản đồ lỗ hổng cho giảng viên (A2)" — cả hai đều khả thi nhưng ứng viên được chọn có bằng chứng định lượng trực tiếp mạnh hơn (32,8% là con số lớn, có quote cụ thể lặp lại ở nhiều học viên) và phạm vi sửa hẹp hơn (một quyết định: có căn cứ → trả lời kèm trích dẫn; không có căn cứ → nói rõ + gợi ý tìm ở đâu), phù hợp build trong thời gian sự kiện.
- Ứng viên CHỌN + vì sao (bằng số): Tutor nói rõ khi không có căn cứ trong tài liệu — vì đây là pattern xảy ra ở gần 1/3 số lượt hỏi thật, có bằng chứng lặp lại trên nhiều học viên khác nhau (không phải cá biệt), và sửa được bằng một quyết định AI duy nhất (có căn cứ hay không) khớp đúng lát cắt MỘT CÂU.

## §3. Giải pháp tương tự đã nghiên cứu
- [Sản phẩm 1]: flow / đáng học / đáng né / mình khác gì
- [Sản phẩm 2]: ...

## §4. Thiết kế
- Lát cắt MỘT CÂU (1 user · 1 việc · 1 quyết định AI · 1 kết quả):
- Non-goals (≥3 thứ KHÔNG build):
- Mức prototype nhắm tới: [ ] Sketch [ ] Mock [ ] Working — phần nào mock, phần nào thật:
- Automation: [ ] augment [ ] conditional [ ] automate — lý do theo cost-of-error:
- §4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR, xem guide):
  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8) [bảng theo guide §2.5]

## §6. Bốn đường đi của trải nghiệm
- Happy path: · Low-confidence (②): · Failure/không căn cứ (①): · Correction (user sửa):
- Khi bị đòi ngoài phạm vi (③): · Case đặc thù domain (④):

## §7. Kiểm thử
- Chiều chất lượng + định nghĩa kiểm chứng được:
- Golden set (≥20 case theo cơ cấu trong guide §2.6, file trong eval/):
- Quality bar (chốt từ hạn chốt spec của khoá, giữ nguyên sau đó): "Đạt khi ≥ ___% qua bộ, và ___"
- Kết quả các lượt chạy (bảng % — cập nhật đến trước CP6):

## §8. Phân công & kế hoạch
- Phân công có tên: spec / evidence / prompt / code / demo
- Willing users (≥2 tên) + kế hoạch vòng validation *(bonus, nếu làm)*:
- Multi-prototype (nếu làm): trục khác biệt của ≥2 phương án + lý do chọn:

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
|---|---|---|
