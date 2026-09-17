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
- Lát cắt MỘT CÂU (1 user · 1 việc · 1 quyết định AI · 1 kết quả): Học viên đang ôn tập slide bài giảng dài trên VLearn cần thấy mạch logic tổng quan và mối liên hệ kiến thức được AI trích xuất thành cây sơ đồ tương tác D3.js (tóm tắt $\le 15$ từ/node), học viên click node mở giao diện 60/40 đối chiếu trực tiếp slide gốc, trích dẫn [Slide X] và trao đổi cùng AI Tutor.
- Non-goals (≥3 thứ KHÔNG build): (1) Không vẽ gộp toàn bộ các ngày vào chung 1 cây chằng chịt gây rối mắt — hiển thị theo từng Ngày riêng biệt (Single-day view); (2) Không copy nguyên văn cả đoạn văn slide vào node — tóm tắt súc tích $\le 15$ từ; (3) Không tự động chạy vòng lặp Agent tiêu hao quota — dùng Deterministic Python Pipeline với Local Caching 0đ quota API; (4) Cây tối đa 3 cấp (Root bài học -> Chương nhánh -> Khái niệm chi tiết).
- Mức prototype nhắm tới: [ ] Sketch [ ] Mock [x] Working (CP3) — phần nào mock, phần nào thật:
  - **Phật thật (100% Real Data):** Toàn bộ 5 file PDF slide bài giảng thật trong `data/` (Day 01 đến Day 05, từ 32 đến 98 trang) được trích xuất vào `codebase/storage/` với nội dung, trích dẫn [Slide X] và liên kết chéo (Cross-day links) thật 100%.
  - **Phần thật (D3.js SVG Tree Canvas):** Cây sơ đồ tương tác render bằng D3.js v7, hỗ trợ zoom, pan, thu/phóng nhánh, click node mở panel 60/40.
  - **Phần an toàn (Safe Fallback Pipeline):** Chế độ Zero Quota Offline Mode bảo vệ hạn mức 15 RPM / 500 RPD của Gemini API, có sẵn script Python gọi Gemini 2.5 Flash Structured Output khi cấp API Key.
- Automation: [x] augment [ ] conditional [ ] automate — lý do: AI đóng vai trò gia sư sư phạm (AI Tutor) và trích xuất cấu trúc kiến thức súc tích, người học hoàn toàn làm chủ hành trình ôn tập và kiểm chứng đối chiếu với slide gốc.
- §4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR, xem guide):
  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|
  | **PAIR ①: User Needs + Defining Success** | Giới hạn tóm tắt node $\le 15$ từ, mở rộng chế độ Progressive Disclosure (100% Canvas $\to$ 60/40 Split View) giải quyết đúng điểm đau "dài quá không đọc". |
  | **PAIR ④: Explainability + Trust** | Mọi node đều gắn kèm huy hiệu trích dẫn số trang chính xác `[Slide X]` và trích đoạn nguyên văn từ bài giảng của thầy cô để học viên đối chiếu 100%. |
  | **PAIR ⑤: Feedback + Control** | Học viên tự do đổi ngày (Day 01 $\to$ 05), zoom/pan, đóng/mở panel chi tiết, thu gọn các nhánh và copy lệnh thực hành. |
  | **PAIR ⑥: Errors + Graceful Failure** | Nút `⚡ Test CLARIFY` xử lý khi nội dung slide đa nghĩa (hỏi lại học viên thay vì bịa); nút `⚠️ Test LỖI` kích hoạt bộ đệm offline khi vượt hạn mức 15 RPM. |

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8)
- Lớp 1 (Parse PDF lỗi/ảnh chụp): Tự động fallback sang text layer hoặc gợi ý tải lại bản slide vector.
- Lớp 2 (Slide quá nhiều chữ làm vỡ giao diện): Giới hạn độ dài `summary <= 15 từ`, đẩy toàn bộ chi tiết vào drawer bên phải.
- Lớp 3 (Liên kết chéo không tồn tại): Pipeline có script `--validate-links` tự động xác thực 17/17 liên kết chéo trước khi render.
- Lớp 4 (Vượt rate-limit 15 RPM): Chuyển sang đọc `codebase/storage/day_X.json` cục bộ, giữ nguyên trải nghiệm mượt mà không crash.

## §6. Bốn đường đi của trải nghiệm
- **Happy path:** Học viên vào VLearn $\to$ Click "Cây Mindmap D3" $\to$ Xem cây kiến thức Day 01 súc tích $\to$ Click node "Local Checklist" $\to$ Panel 60/40 mở ra hiển thị các lệnh `git version`, `python --version` và quiz ôn tập.
- **Cross-day Jump path:** Học viên xem Day 03 (ReAct Agent) $\to$ Thấy badge `🔗 Kế thừa phân cấp Day 02 [Slide 3 & 69]` $\to$ Click "Chuyển sang Node liên kết" $\to$ Hệ thống tự chuyển sang Day 02 và focus vào node phân cấp Rule vs Agent.
- **Low-confidence (Clarify):** Khi slide có nội dung phân nhánh đa nghĩa $\to$ AI hiển thị gợi ý hỏi học viên muốn theo luồng lý thuyết toán hay thực hành code.
- **Failure/Rate-limit:** Khi API bị ngắt kết nối hoặc hết quota $\to$ Giao diện thông báo thân thiện và tự động tải dữ liệu từ cache `codebase/storage/`.

## §7. Kiểm thử
- **Độ chính xác liên kết chéo:** 17/17 (100%) liên kết chéo giữa các ngày hợp lệ (`mindmap_pipeline.py --validate-links`).
- **Độ cô đọng tóm tắt:** 100% các node trên cây sơ đồ tuân thủ tiêu chí $\le 15$ từ.
- **Khả năng tương thích:** Render chuẩn trên mọi trình duyệt với D3.js v7 và Tailwind CSS (chạy offline `file:///` không phụ thuộc backend server).

## §8. Phân công & kế hoạch
- **Spec & Design:** Nhóm BungChay (Khảo sát nhu cầu học viên, thiết kế UX Progressive Disclosure).
- **Pipeline & Parser:** `codebase/pipeline/mindmap_pipeline.py` (Trích xuất PDF bằng `pypdf`, xử lý cấu trúc JSON và rate limiting).
- **Frontend Visualization:** `codebase/index.html` (D3.js SVG Tree, Pan/Zoom, Day switcher, Split View).
- **Willing users:** Dương Đạt Khang, Tạ Việt Cường (Học viên lớp K4-3A test đối chiếu slide và giải quiz).

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
|---|---|---|
| 16/9 (CP1) | Khởi tạo Canvas & Spec A2 cho học viên | Dựa trên kết quả khảo sát 15 học viên thật gặp khó khăn khi học slide dài |
| 16/9 (CP2) | Xây dựng Mockup giao diện và 4 đường trải nghiệm | Chốt luồng click node mở 60/40, bổ sung nút Test CLARIFY và Test LỖI |
| 17/9 (CP3) | Hoàn thiện Working Prototype với 100% dữ liệu slide thật | Tích hợp D3.js, nạp 5 ngày học từ `data/`, xây dựng pipeline offline bảo vệ quota 15 RPM |

