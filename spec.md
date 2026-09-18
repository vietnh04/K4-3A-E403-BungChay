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
- **[Sản phẩm 1] Google NotebookLM — tính năng Mind Map** (ra mắt 3/2025, tiếp tục mở rộng trong 2026):
  - Flow: Người dùng tải nguồn (PDF, Google Slides, video, trang web...) vào 1 "notebook" → AI tự sinh sơ đồ tư duy tương tác tóm tắt các khái niệm cốt lõi và mối liên hệ giữa chúng → có thể tải ảnh sơ đồ về.
  - Đáng học: hỗ trợ đa dạng loại nguồn (PDF/Slides/video/web), sơ đồ bám sát nội dung nguồn đã upload (grounded), miễn phí ở gói cơ bản.
  - Đáng né: giới hạn cứng số lần tạo/ngày theo gói (10 lần/ngày ở gói Standard, tối đa 1.000 ở gói cao nhất) — không phù hợp nếu học viên cần tạo lại nhiều lần khi ôn nhiều buổi; **chưa xuất hiện trên mobile app**; là công cụ tổng quát cho "nghiên cứu tài liệu" nói chung, không có cơ chế trích dẫn số trang slide gắn cứng vào từng node để đối chiếu ngược, không có khái niệm "liên kết chéo giữa các buổi học" hay "AI Tutor" hỏi đáp theo node.
  - Mình khác gì: sản phẩm của nhóm bắt buộc mọi node phải neo đúng `[Slide X]` để học viên đối chiếu 1-1 với slide gốc (PAIR ④ Explainability), có `cross_link` liên kết kiến thức giữa các Day trong cùng 1 khoá học (NotebookLM không có khái niệm "khoá học nhiều buổi liên tục"), và có panel 60/40 mở AI Tutor tương tác ngay tại node — thiết kế riêng cho luồng ôn tập của học viên VLearn, không phải công cụ nghiên cứu tài liệu đa năng.

- **[Sản phẩm 2] Xmind AI Copilot**:
  - Flow: Người dùng nhập ý tưởng, dán link/PDF/ảnh vào tính năng "One-liner" hoặc "Outliner" → AI sinh mindmap trong vài giây → có thể dùng "Ghostwriter" viết ngược mindmap thành bài văn.
  - Đáng học: nhận đa dạng nguồn input (webpage, doc, PDF, YouTube, cả ảnh), giao diện mindmap chuyên nghiệp lâu năm, có tính năng "Grow Ideas" để AI mở rộng thêm nhánh theo yêu cầu.
  - Đáng né: là công cụ brainstorm/ghi chú đa năng cho mọi loại nội dung, không thiết kế riêng cho việc ôn tập bài giảng dài nhiều buổi; theo tìm hiểu không có cơ chế trích dẫn số trang nguồn gắn vào từng node, không có liên kết chéo giữa nhiều tài liệu/buổi học.
  - Mình khác gì: phạm vi sản phẩm nhóm hẹp và chuyên biệt hơn nhiều (1 khoá học cụ thể, nhiều Day liên tục, có Course Knowledge Index để liên kết chéo), tối ưu cho việc học viên ôn thi/đối chiếu slide thật thay vì brainstorm ý tưởng mới.

  *(Nguồn tham khảo: [NotebookLM Mind Maps guide](https://notebooklm-guide.com/notebooklm-mind-maps/), [9to5google - NotebookLM Mind Map](https://9to5google.com/2025/03/27/notebooklm-mind-map/), [Xmind AI](https://xmind.com/ai), [Xmind Copilot review](https://mindmappingsoftwareblog.com/xmind-copilot-review/) — cần đội Spec & Validation tự trải nghiệm trực tiếp 2 sản phẩm này trước khi khoá bản cuối, hiện phân tích dựa trên tài liệu công khai, chưa tự tay dùng thử.)*

## §4. Thiết kế
- Lát cắt MỘT CÂU (1 user · 1 việc · 1 quyết định AI · 1 kết quả): Học viên đang ôn tập slide bài giảng dài trên VLearn cần thấy mạch logic tổng quan và mối liên hệ kiến thức được AI trích xuất thành cây sơ đồ tương tác D3.js (tóm tắt $\le 40$ từ/node), học viên click node mở giao diện 60/40 đối chiếu trực tiếp slide gốc, trích dẫn [Slide X] và trao đổi cùng AI Tutor.
- Non-goals (≥3 thứ KHÔNG build): (1) Không vẽ gộp toàn bộ các ngày vào chung 1 cây chằng chịt gây rối mắt — hiển thị theo từng Ngày riêng biệt (Single-day view); (2) Không copy nguyên văn cả đoạn văn slide vào node — tóm tắt súc tích $\le 40$ từ; (3) Không tự động chạy vòng lặp Agent tiêu hao quota — dùng Deterministic Python Pipeline với Local Caching 0đ quota API; (4) Cây tối đa 5 cấp, tối thiểu 3 cấp (Root bài học -> Chương -> Tiểu mục -> Khái niệm cốt lõi -> Chi tiết thực hành), không phân nhánh sâu vô hạn.
- Mức prototype nhắm tới: [ ] Sketch [ ] Mock [x] Working (CP3) — phần nào mock, phần nào thật:
  - **Phật thật (100% Real Data):** Toàn bộ 5 file PDF slide bài giảng thật trong `data/` (Day 01 đến Day 05, từ 32 đến 98 trang) được trích xuất vào `codebase/storage/` với nội dung, trích dẫn [Slide X] và liên kết chéo (Cross-day links) thật 100%.
  - **Phần thật (D3.js SVG Tree Canvas):** Cây sơ đồ tương tác render bằng D3.js v7, hỗ trợ zoom, pan, thu/phóng nhánh, click node mở panel 60/40.
  - **Phần an toàn (Safe Fallback Pipeline):** Chế độ Zero Quota Offline Mode bảo vệ hạn mức 15 RPM / 500 RPD của Gemini API, có sẵn script Python gọi Gemini 2.5 Flash Structured Output khi cấp API Key.
- Automation: [x] augment [ ] conditional [ ] automate — lý do: AI đóng vai trò gia sư sư phạm (AI Tutor) và trích xuất cấu trúc kiến thức súc tích, người học hoàn toàn làm chủ hành trình ôn tập và kiểm chứng đối chiếu với slide gốc.
- §4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR, xem guide):
  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|
  | **PAIR ①: User Needs + Defining Success** | Giới hạn tóm tắt node $\le 40$ từ, mở rộng chế độ Progressive Disclosure (100% Canvas $\to$ 60/40 Split View) giải quyết đúng điểm đau "dài quá không đọc". |
  | **PAIR ④: Explainability + Trust** | Mọi node đều gắn kèm huy hiệu trích dẫn số trang chính xác `[Slide X]` và trích đoạn nguyên văn từ bài giảng của thầy cô để học viên đối chiếu 100%. |
  | **PAIR ⑤: Feedback + Control** | Học viên tự do đổi ngày (Day 01 $\to$ 05), zoom/pan, đóng/mở panel chi tiết, thu gọn các nhánh và copy lệnh thực hành. |
  | **PAIR ⑥: Errors + Graceful Failure** | Nút `⚡ Test CLARIFY` xử lý khi nội dung slide đa nghĩa (hỏi lại học viên thay vì bịa); nút `⚠️ Test LỖI` kích hoạt bộ đệm offline khi vượt hạn mức 15 RPM. |

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8)
- **Lớp 1 (Parse PDF lỗi/ảnh chụp):**
  1. Slide scan dạng ảnh (không có text layer): Tự động fallback sang text layer hoặc gợi ý tải lại bản slide vector; nếu `pypdf` trích được 0 ký tự, báo lỗi rõ ràng thay vì trả cây rỗng im lặng.
  2. File PDF nhiều cột/bảng phức tạp: `pypdf` có thể trích text sai thứ tự đọc (cột phải lẫn vào cột trái) — **tự khai hạn chế**: hiện chưa có bước kiểm tra thứ tự đọc, cần review thủ công trước khi tin tưởng 100% với slide dạng bảng dày đặc.

- **Lớp 2 (Slide quá nhiều chữ / quá ít chữ làm vỡ giao diện hoặc vỡ chất lượng nội dung):**
  1. Slide quá dài nhiều chữ: Giới hạn độ dài `summary <= 40 từ`, đẩy toàn bộ chi tiết vào `detail` (chỉ bắt buộc ở node lá, xem `codebase/backend/prompts.py`).
  2. Slide gần như trống (chỉ có tiêu đề chương, không nội dung — vd case `gs03` trong `eval/golden_set.json`): **tự khai hạn chế đã đo được thật** — bản prompt production hiện tại (`codebase/backend/prompts.py`, sau commit `2fdbcff` của vietnh04) chưa có field `insufficient_info` để báo "không đủ căn cứ dựng cây"; rủi ro là AI có thể ép tạo node cho nội dung gần như rỗng. Đây là hạng mục ưu tiên bổ sung ở vòng sau, đã ghi vào `eval/golden_set.json` để đo lường khi prompt được cập nhật.

- **Lớp 3 (Liên kết chéo không tồn tại hoặc trỏ sai):**
  1. Liên kết chéo trỏ tới node không tồn tại: Pipeline có script `--validate-links` tự động xác thực 17/17 liên kết chéo trước khi render.
  2. Dữ liệu ngày nguồn bị sửa/xoá sau khi đã có node khác trỏ tới (`target_node_id` mồ côi): cần ẩn badge `🔗 Kế thừa` thay vì hiển thị link chết hoặc lỗi 500 — **tự khai:** hiện xử lý ở bước validate tĩnh trước khi render, chưa có cơ chế tự sửa khi dữ liệu ngày nguồn thay đổi động sau đó.

- **Lớp 4 (Vượt rate-limit / hạ tầng bên ngoài lỗi):**
  1. Vượt rate-limit 15 RPM của Gemini: Chuyển sang đọc `codebase/storage/day_X.json` cục bộ, giữ nguyên trải nghiệm mượt mà không crash.
  2. Model/API bên thứ ba trả lỗi tạm thời (đã đo được thật khi test: NVIDIA build API trả `504 Gateway Timeout` ở case `gs14`, xem `eval/run_results.md` lượt 2): cần retry có giới hạn số lần + thông báo rõ cho người dùng thay vì client treo vô thời hạn — **tự khai:** hiện script test (`eval/run_tests.py`) có timeout cứng 350s nhưng backend production (`mindmap_service.py`) chưa có cơ chế retry/timeout tường minh cho lỗi tạm thời phía server ngoài.

## §6. Bốn đường đi của trải nghiệm
- **Happy path:** Học viên vào VLearn $\to$ Click "Cây Mindmap D3" $\to$ Xem cây kiến thức Day 01 súc tích $\to$ Click node "Local Checklist" $\to$ Panel 60/40 mở ra hiển thị các lệnh `git version`, `python --version` và quiz ôn tập.
- **Cross-day Jump path:** Học viên xem Day 03 (ReAct Agent) $\to$ Thấy badge `🔗 Kế thừa phân cấp Day 02 [Slide 3 & 69]` $\to$ Click "Chuyển sang Node liên kết" $\to$ Hệ thống tự chuyển sang Day 02 và focus vào node phân cấp Rule vs Agent.
- **Low-confidence (Clarify):** Khi slide có nội dung phân nhánh đa nghĩa $\to$ AI hiển thị gợi ý hỏi học viên muốn theo luồng lý thuyết toán hay thực hành code.
- **Failure/Rate-limit:** Khi API bị ngắt kết nối hoặc hết quota $\to$ Giao diện thông báo thân thiện và tự động tải dữ liệu từ cache `codebase/storage/`.

## §7. Kiểm thử

### Định nghĩa kiểm thử theo từng chiều chất lượng
| Chiều chất lượng | Cách đo | Công cụ |
|---|---|---|
| Cấu trúc đúng (structural validity) | JSON hợp lệ, cây sâu 3-5 cấp, mọi node có `slide_page` | `eval/run_tests.py` chấm theo `scoring_rules` trong `eval/golden_set.json` |
| Bám nguồn / không bịa (grounding) | Không chứa `forbidden_terms` của từng case trong `title`/`summary`/`detail` | `eval/golden_set.json` (20 case, đủ 4 lớp taxonomy chỗ khó) |
| Trích dẫn đúng trang | Mọi số trang trong `must_cover_pages` phải xuất hiện trong `slide_page` của cây trả về | `eval/golden_set.json` |
| Liên kết chéo hợp lệ | 17/17 (100%) liên kết chéo giữa các ngày hợp lệ | `mindmap_pipeline.py --validate-links` |
| Độ cô đọng | 100% node tuân thủ `summary <= 40 từ` | Kiểm tra thủ công + rule trong prompt |
| Khả năng tương thích | Render chuẩn trên mọi trình duyệt | `codebase/index.html` chạy offline `file:///`, D3.js v7 + Tailwind |

### Quality Bar (ngưỡng chất lượng — đóng băng tại CP4, 17/9/2026 21:00)
Sản phẩm được coi là **ĐẠT** khi thoả đồng thời:
1. **≥ 90% tổng số case** trong `eval/golden_set.json` (20 case) đạt Pass theo `scoring_rules` (JSON hợp lệ, cấu trúc 3-5 cấp, trích dẫn đúng trang, không bịa nội dung ngoài `forbidden_terms`).
2. **100% case thuộc lớp ③ Ngoài phạm vi/thẩm quyền** (trang bìa, đề thi, thông báo hành chính, ảnh không chữ) phải được AI xử lý an toàn — đây là ngưỡng cứng riêng vì đây là lớp rủi ro cao nhất (AI dựng cây giả cho nội dung không phải kiến thức).
3. Liên kết chéo: 100% (17/17) hợp lệ, không có `target_node_id` mồ côi.

**Kết quả đo thật tính đến 17/9/2026 15:40** (xem chi tiết từng case tại `eval/run_results.md`):
- Tổng thể: **19/20 (95%)** — ĐẠT ngưỡng 1 (≥90%).
- Lớp ① Nguồn sự thật: 6/6 (100%). Lớp ② Mơ hồ/thiếu thông tin: 4/4 (100%). Lớp ④ Đặc thù nghiệp vụ: 6/6 (100%).
- **Lớp ③ Ngoài phạm vi: 3/4 (75%) — CHƯA đạt ngưỡng cứng 100% (ngưỡng 2).** Case `gs14` (đề trắc nghiệm không đáp án) fail vì lỗi hạ tầng bên thứ ba (`504 Gateway Timeout` từ NVIDIA build API khi test) — không phải lỗi logic prompt (bug logic ban đầu đã được xác định và sửa ở lượt 1). Cần chạy lại xác nhận, chưa kịp trước giờ khoá spec.

### Tự khai báo hạng mục chưa xử lý kịp (không giấu)
- Case `gs14` chưa xác nhận lại được (mục trên).
- Prompt production hiện tại (`codebase/backend/prompts.py`) **chưa có field `insufficient_info`** để AI báo "không đủ căn cứ dựng cây" cho slide gần như rỗng (xem §5 Lớp 2, kịch bản 2) — bộ `eval/golden_set.json` đã thiết kế sẵn case cho hành vi này, chờ prompt bổ sung để đo được đầy đủ.
- 20 case của golden set là **dữ liệu tự sinh**, chưa có case trích trực tiếp từ slide thật của khoá VLearn — cần bổ sung trước khi dùng Quality Bar này làm căn cứ nghiệm thu chính thức ở vòng sau.
- Model dùng để đo Quality Bar ở trên là `deepseek-ai/deepseek-v4-flash-0731` qua NVIDIA build API (chưa có Gemini API key thật để test qua đúng model production `gemini-2.5-flash`) — số liệu là bằng chứng chất lượng PROMPT, cần đo lại khi có key Gemini thật.

## §8. Phân công & kế hoạch

| Đầu việc | Người phụ trách | Sản phẩm bàn giao | Kế hoạch kiểm thử thực tế |
|---|---|---|---|
| Nhóm trưởng — Backend pipeline & quản trị repo | **Nguyễn Hoàng Việt** | `codebase/backend/` (`mindmap_service.py`, `prompts.py`, `server.py`), `codebase/pipeline/mindmap_pipeline.py`, quản trị GitHub repo | Chạy server thật (`run_server.py`), xác thực liên kết chéo bằng `mindmap_pipeline.py --validate-links` (17/17), review code trước khi merge, kiểm tra không lộ API key |
| Kỹ sư prompt — System Prompt v1/v2 | **Nguyễn Đỗ Chiến Thắng** | Rule bám nguồn, phân rã cấu trúc, xử lý 4 lớp chỗ khó trong prompt | Nhận danh sách case fail từ Task 4 (`eval/run_results.md`), phân tích nguyên nhân gốc rễ (ảo giác, thiếu thông tin, gãy cú pháp, sai phân cấp), cập nhật prompt theo bằng chứng đo được |
| Golden set & taxonomy | **Đặng Hữu Tâm** | `eval/golden_set.json` (20 case, đủ 4 lớp taxonomy chỗ khó, tiêu chí Pass/Fail định lượng) | Tự kiểm tra bằng `eval/run_tests.py` trước khi bàn giao, đối chiếu với schema thật của `prompts.py` trước khi khoá case |
| Đo lường, báo cáo & demo | **Phạm Quân** | `eval/run_tests.py`, `eval/run_results.md`, video demo 30s thao tác thực tế | Chạy 20 case qua backend thật, ghi kết quả Pass/Fail theo taxonomy vào `eval/run_results.md`, quay video tải slide → gửi request → AI sinh Mindmap thời gian thực |
| Willing users (kiểm thử người dùng thật) | Dương Đạt Khang, Tạ Việt Cường (học viên K4-3A) | Phản hồi UX | Test đối chiếu slide gốc và giải quiz thật trên giao diện `codebase/index.html` |

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
|---|---|---|
| 16/9 (CP1) | Khởi tạo Canvas & Spec A2 cho học viên | Dựa trên kết quả khảo sát 15 học viên thật gặp khó khăn khi học slide dài |
| 16/9 (CP2) | Xây dựng Mockup giao diện và 4 đường trải nghiệm | Chốt luồng click node mở 60/40, bổ sung nút Test CLARIFY và Test LỖI |
| 17/9 (CP3) | Hoàn thiện Working Prototype với 100% dữ liệu slide thật | Tích hợp D3.js, nạp 5 ngày học từ `data/`, xây dựng pipeline offline bảo vệ quota 15 RPM |
| 17/9 (CP3) | Nâng Non-goal §4(4) từ "tối đa 3 cấp" lên "tối thiểu 3, tối đa 5 cấp" | `codebase/backend/prompts.py` (SLIDE_MINDMAP_EXTRACTION_PROMPT) thực tế bắt buộc 3-5 cấp để giữ nguyên tắc Zero Knowledge Loss (§4b) cho các slide dài 32-98 trang — nén về đúng 3 cấp làm mất chi tiết kỹ thuật (code mẫu, tham số, bước thực hiện). Cập nhật spec cho khớp code thay vì để lệch ngầm; `eval/golden_set.json` (Task 3) đã cập nhật theo đúng biên 3-5 cấp này |
| 17/9 (CP4) | Hoàn thiện đủ 8 phần spec.md và đóng băng Quality Bar: viết §3 (phân tích NotebookLM + Xmind AI), mở rộng §5 lên 8 kịch bản, thêm công thức Quality Bar + liên kết `eval/` vào §7, điền tên thật §8 | Khoá ngưỡng nghiệm thu trước 21:00 theo yêu cầu CP4 — Quality Bar dựa trên số đo thật `eval/run_results.md` (19/20 = 95%, lớp ③ 3/4 = 75% chưa đạt ngưỡng cứng do lỗi hạ tầng khi test), tự khai rõ các hạng mục chưa xử lý kịp (field `insufficient_info` chưa có trong prompt production, chưa test qua Gemini thật) |

