# AI SPEC — Cây sơ đồ tư duy tương tác từ slide bài giảng · Nhóm BungChay · Zone 1
Hướng: [x] A — VLearn  [ ] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [ ] Tối ưu tính năng có sẵn (A1)  [x] Tính năng mới (A2 — cho học viên)

> ✅ **Nhóm chốt lại (16/9, sau khảo sát thật):** đổi từ "bản đồ điểm nghẽn cho giảng viên" sang **cây sơ đồ tư duy tương tác cho học viên**, vẫn thuộc A2 (tính năng AI mới trên VLearn), chỉ đổi đối tượng từ giảng viên sang học viên. Bản A2-giảng viên cũ giữ lại trong §2 làm ứng viên đã cân nhắc.

## §1. User & Job
- Job executor + workflow: Học viên đang ôn tập/tổng hợp kiến thức từ slide bài giảng dài (PDF/PowerPoint nhiều trang) trên VLearn. Hiện tại: đọc lướt từng slide và tự ghi chép gạch đầu dòng, hoặc tự tay vẽ sơ đồ tư duy ra giấy/phần mềm, hoặc dùng AI tóm tắt thành văn bản — nhưng vẫn phải tự ngồi vẽ lại quan hệ giữa các phần.
- Core JTBD: Nắm nhanh mạch logic và mối liên hệ giữa các khái niệm trong một bài giảng dài, để ôn tập/tổng hợp hiệu quả hơn so với đọc tuần tự từng trang.
- Problem statement (KHÔNG chữ AI): Khi tài liệu bài giảng dài nhiều trang chữ, học viên khó nhìn ra mạch logic tổng thể và mối liên hệ giữa các phần kiến thức — dẫn đến mất nhiều thời gian tự vẽ/tóm tắt lại, hoặc bỏ cuộc giữa chừng và học thuộc vẹt từng slide rời rạc.
- Evidence (**Chuẩn A** — khảo sát nội bộ Google Form, 15 người ngoài nhóm đã trả lời; ⚠️ **cần bổ sung thêm ≥5 người để đủ mốc ≥20 theo yêu cầu spec**):
  - **73,3% (11/15)** chọn "Slide quá dài và nhiều chữ, khó nhìn ra mạch logic tổng thể" là khó khăn lớn nhất khi tổng hợp kiến thức
  - **46,7% (7/15)** kết quả cuối cùng là "Không nắm chắc mối liên hệ giữa các phần kiến thức"; **53,3% (8/15)** "tự vẽ/tóm tắt được nhưng mất rất nhiều thời gian"; **26,7% (4/15)** "bỏ cuộc giữa chừng, học thuộc vẹt từng slide rời rạc"
  - **86,7% (13/15)** đã phải đọc lại file slide bài giảng nhiều trang trong 7 ngày qua để ôn bài/làm bài tập; trong đó 60% để "nắm tổng quan trước khi đi sâu chi tiết", 13,3% để "tìm mối liên kết giữa các khái niệm/chương mục để ôn thi"
  - **100% (15/15) sẵn sàng dùng** công cụ tự động chuyển slide dài thành sơ đồ tư duy trực quan nếu có (40% "chắc chắn sẽ dùng" + 60% "có thể sẽ thử", 0% "không có nhu cầu")
  - **60% (9/15)** đánh giá 4-5/5 điểm cho hiệu quả học qua mindmap so với đọc văn bản truyền thống
  - Tương quan củng cố: 53,3% (8/15) hiện đã dùng AI tóm tắt thành **text**, nhưng nỗi đau lớn nhất vẫn là thiếu **mạch logic trực quan** — cho thấy tóm tắt dạng chữ chưa giải quyết đúng vấn đề, cần dạng sơ đồ
  - Quote nguyên văn (câu tự luận "Khó khăn lớn nhất"), hiện có **2/5**:
    - **P03**: *"Slide ngắn gọn nhưng vẫn thiếu connect"*
    - **P07**: *"Dài quá không đọc"*
  - **[CẦN LÀM — tự khai thiếu, chưa giấu]** Còn thiếu ≥3 quote nguyên văn nữa và ≥5 phản hồi khảo sát (đủ ≥20) — có 1 câu tự luận khác trong form bị cắt chữ trên biểu đồ tổng hợp ("Tóm tắt xong thì bị ngắt kết nối với slide gốc, không biết ý đó n...") chưa xác nhận được văn bản đầy đủ, cần mở tab "Câu trả lời riêng lẻ" hoặc Google Sheet gốc của form để lấy nguyên văn chính xác trước khi trích vào spec

## §2. Impact & quyết định chọn
- Bảng impact (≥3 ứng viên, số liệu từ mining ở trên):

  | Ứng viên | Bao nhiêu người gặp | Tần suất | Tốn gì mỗi lần | Build nổi không | Chọn? |
  |---|---|---|---|---|---|
  | Cây sơ đồ tư duy tương tác từ slide (A2 — học viên) | 100% khảo sát (15/15) muốn dùng; 73,3% (11/15) thấy đây là khó khăn lớn nhất | mỗi lần ôn bài/tổng hợp — 86,7% phải làm việc này trong 7 ngày qua | mất nhiều thời gian tự vẽ lại (53,3%) hoặc bỏ cuộc, học vẹt rời rạc (26,7%) | Vừa sức nếu giới hạn phạm vi: AI trích xuất cấu trúc khái niệm từ 1 slide/transcript → dựng cây, học viên click node để hỏi thêm | ✅ Chọn |
  | Giảng viên không biết lớp đang kẹt ở đâu (A2 — giảng viên) | 127 học viên K4 cùng vướng ở bài Day01 (23,1% câu hỏi thật) | mỗi buổi học | ôn sai trọng tâm buổi sau, học viên hổng kiến thức nền không được lấp | Vừa sức nếu giới hạn phạm vi: tổng hợp + xếp hạng theo bài giảng, không cần real-time | Loại — nhóm đổi hướng sang phục vụ trực tiếp học viên sau khi có khảo sát; bằng chứng mining (§1 bản cũ, script `evidence/mining_chatlog_a2.py`) vẫn giữ, có thể tái dùng làm nguồn "concept nào nhiều người hỏi" cho cây sơ đồ |
  | Tutor không trích dẫn khi trả lời (không nói rõ ranh giới tài liệu, A1) | 32,8% lượt hỏi thật của K4 (838/2.555) | mỗi lần hỏi ngoài phạm vi tài liệu đang mở | học viên không biết tin hay không, có thể học nhầm kiến thức ngoài khoá | Có — sửa logic quyết định trung tâm (conditional response), phạm vi hẹp nhất trong 3 ứng viên | Loại — nhóm ưu tiên hướng có khảo sát thật + insight độc đáo hơn (mindmap) |
  | Tutor không hỏi lại khi câu hỏi mơ hồ | chỉ 6/3.097 lượt K4 có hỏi lại | hiếm | trả lời sai hướng, học viên phải hỏi lại | Có, nhưng cần thêm logic phân loại mơ hồ — phạm vi rộng hơn | Loại — ít bằng chứng định lượng trực tiếp về hậu quả hơn |

- Ứng viên ĐÃ LOẠI + vì sao: "Tutor không hỏi lại khi mơ hồ" — ít bằng chứng hậu quả trực tiếp. "Tutor không trích dẫn (A1)" — dễ build nhất nhưng ít khác biệt, chỉ dựa mining chatlog chứ chưa có khảo sát trực tiếp người dùng. "Giảng viên không biết lớp kẹt ở đâu (A2 cũ)" — bằng chứng mining mạnh (87,1% review_concept, Day01 chiếm 23,1%) nhưng đối tượng nghiệm thu (giảng viên) khó tiếp cận làm willing user hơn học viên; nhóm quyết định pivot sang phục vụ học viên trực tiếp sau khi khảo sát cho tín hiệu rõ hơn.
- Ứng viên CHỌN + vì sao (bằng số): Cây sơ đồ tư duy tương tác cho học viên (A2) — vì 100% người khảo sát (15/15) muốn dùng, 73,3% xác nhận đây là khó khăn lớn nhất khi ôn tập, và 86,7% gặp tình huống này thường xuyên (trong 7 ngày qua). Có thể tái dùng bằng chứng mining chatlog cũ (khái niệm nào bị hỏi lại nhiều — `review_concept`) làm tín hiệu tô đậm node "khó" trên cây sơ đồ, kết hợp cả Chuẩn A và Chuẩn B.
- ⚠️ **Lưu ý rủi ro (tự khai):** (1) khảo sát mới có 15/20 phản hồi, cần bổ sung gấp trước khi khoá spec ở CP4; (2) dựng cây sơ đồ tương tác (parse cấu trúc + UI graph) tốn công hơn một quyết định trả lời đơn — cần thu hẹp phạm vi kỹ ở §4 Non-goals (ví dụ: chỉ 1 bài giảng mẫu, cây 2 cấp, không cần kéo-thả).

## §3. Giải pháp tương tự đã nghiên cứu
- [Sản phẩm 1]: flow / đáng học / đáng né / mình khác gì
- [Sản phẩm 2]: ...

## §4. Thiết kế
- Lát cắt MỘT CÂU (1 user · 1 việc · 1 quyết định AI · 1 kết quả) — **[NHÁP, cần nhóm chốt]**: Học viên đang ôn một bài giảng dài cần thấy mạch logic và mối liên hệ giữa các khái niệm được AI đọc slide/transcript rồi trích xuất cấu trúc khái niệm thành cây sơ đồ tương tác giúp nắm tổng quan nhanh và click vào từng node để AI giải thích sâu hơn.
- Non-goals (≥3 thứ KHÔNG build) — **[NHÁP]**: (1) không tự dựng cây cho toàn bộ khoá học, chỉ 1 bài giảng/slide đang mở; (2) không cho kéo-thả/chỉnh sửa cây thủ công, chỉ xem + click; (3) không cần đồng bộ real-time với tiến độ học; (4) cây tối đa 2 cấp (chủ đề lớn → khái niệm con), không lồng sâu hơn.
- Mức prototype nhắm tới: [ ] Sketch [ ] Mock [ ] Working — phần nào mock, phần nào thật:
- Automation: [x] augment [ ] conditional [ ] automate — **[NHÁP]** lý do: AI chỉ đề xuất cấu trúc/giải thích, học viên tự quyết định học gì tiếp — cost-of-error thấp (sai cấu trúc chỉ gây khó chịu, không gây hiểu sai kiến thức nếu vẫn link về đúng trang slide gốc).
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
- Phân công có tên: spec / evidence / prompt / code / demo — xem `TEAMMATES.md` (⚠️ cần xác nhận lại vai trò cho hướng cây sơ đồ)
- Willing users (≥2 tên): **Dương Đạt Khang**, **Tạ Việt Cường** + kế hoạch vòng validation *(bonus, nếu làm)*: *(cần bổ sung task cụ thể giao cho họ ở CP5)*
- Multi-prototype (nếu làm): trục khác biệt của ≥2 phương án + lý do chọn:

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
|---|---|---|
