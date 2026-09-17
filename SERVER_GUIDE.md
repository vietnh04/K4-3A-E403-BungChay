# 🚀 HƯỚNG DẪN CHẠY MÁY CHỦ VLEARN INTERACTIVE MINDMAP
> **Dự án:** Mini Hackathon AI — Batch 04 · Track A (VLearn Tutor / ConceptMap)  
> **Nhóm:** BungChay · **Phòng:** E403 · **Lớp:** 3A  

Tài liệu này hướng dẫn chi tiết từng bước để bất kỳ thành viên nào trong team sau khi `git clone` hoặc `git pull` đều có thể thiết lập các thư mục/file còn thiếu và khởi chạy máy chủ web mượt mà 100%.

---

## 📂 1. Hiểu về các file & thư mục bị Git bỏ qua (Gitignored)

Vì quy định bảo mật và dung lượng repo, một số file/thư mục **không được đưa lên GitHub** (đã nằm trong `.gitignore`):

| File / Thư mục | Lý do Gitignore | Cách xử lý trên máy cá nhân |
|---|---|---|
| **`.env`** | Chứa API Key bảo mật, không được commit | Tạo từ template `.env.example` có sẵn (hướng dẫn ở mục 2). |
| **`codebase/storage/`** | Chứa cache JSON của các ngày học | **Hệ thống đã tích hợp Auto-Init:** Ngay khi khởi chạy `run_server.py`, server sẽ **tự động tạo thư mục này và nạp sẵn 5 bài giảng mẫu** từ `seed_data.py`. Bạn không cần tạo thủ công! |
| **`data/` & `data/uploads/`** | Chứa các file slide PDF bài giảng nặng | Server sẽ **tự động tạo thư mục `data/uploads/`** khi khởi chạy để nhận file PDF bạn upload lên web. |

---

## ⚡ 2. Quy trình 4 bước khởi chạy (Cực kỳ đơn giản)

### Bước 1: Cập nhật code mới nhất từ GitHub
Mở Terminal tại thư mục dự án và chạy:
```powershell
git pull origin main
```

### Bước 2: Cài đặt các thư viện phụ thuộc
Đảm bảo bạn đang ở môi trường Python (Python 3.10, 3.11 hoặc 3.12, khuyến nghị Conda `ai_workspace`):
```powershell
pip install -r requirements.txt
```
*(Các thư viện chính: `fastapi`, `uvicorn`, `pypdf`, `pydantic`, `google-genai`, `python-dotenv`, `python-multipart`)*.

### Bước 3: Tạo file cấu hình môi trường `.env`
Nhóm đã chuẩn bị sẵn mẫu cấu hình chuẩn trong file [`.env.example`](file:///.env.example). Bạn chỉ cần copy thành `.env`:

- **Trên Windows PowerShell:**
  ```powershell
  Copy-Item .env.example .env
  ```
- **Hoặc trên Linux / macOS / Git Bash:**
  ```bash
  cp .env.example .env
  ```

Sau đó, mở file `.env` bằng VSCode hoặc Notepad và điền API Key của bạn:
```env
# Google Gemini API Key (Lấy miễn phí tại Google AI Studio)
GEMINI_API_KEY=AIzaSy...điền_key_của_bạn_vào_đây...
LLM_MODEL=gemini-2.5-flash
```
*(Nếu chưa có API Key, bạn vẫn có thể để trống; server vẫn chạy bình thường với 5 bài học mẫu có sẵn).*

### Bước 4: Khởi chạy Server
Chạy lệnh khởi động duy nhất:
```powershell
python run_server.py
```

Khi Terminal xuất hiện thông báo:
```text
============================================================
🚀 KHỞI ĐỘNG HỆ THỐNG VLEARN INTERACTIVE MINDMAP (CP3)
============================================================
👉 Mở trình duyệt tại: http://127.0.0.1:8000
============================================================
```

👉 Mở trình duyệt bất kỳ (Chrome, Edge) và truy cập: **`http://127.0.0.1:8000`**

---

## 🖥️ 3. Thao tác trên giao diện Web

Khi giao diện web mở ra tại `http://127.0.0.1:8000`:

1. **Khám phá Cây Mindmap (D3.js SVG Tree):**
   - Dùng chuột để **kéo di chuyển (Pan)** hoặc **lăn chuột để phóng to/thu nhỏ (Zoom)**.
   - Nhấp vào nút tròn xanh trên mỗi nhánh để **thu gọn / mở rộng** nhánh đó.
   - Nhấp vào bất kỳ Node khái niệm nào để mở **Drawer chi tiết 60/40 bên phải** (xem trích đoạn slide gốc, lời giải thích từ AI Tutor, lệnh terminal và câu hỏi Quick Quiz).
2. **Chuyển đổi giữa các ngày học:**
   - Bấm vào các nút tab: `Day 01: Setup & API`, `Day 02: Xác Định Bài Toán`, `Day 03: ReAct Agent`, `Day 04: Prompt & Tools`, `Day 05: Product PRD`.
3. **Liên kết chéo liên ngày (Cross-Day Links):**
   - Các node có biểu tượng `🔗 Từ Day X` mang ý nghĩa kế thừa kiến thức. Khi mở chi tiết, bấm nút **"Chuyển sang Node liên kết"** để nhảy trực tiếp sang bài học đó.
4. **Tải lên Slide bài giảng mới (Upload PDF):**
   - Bấm nút **"Upload Slide (PDF)"** trên thanh header.
   - Kéo thả file PDF bài giảng mới vào ô upload $\to$ Bấm **"Bắt Đầu Xử Lý Với Gemini API"**.
   - Server sẽ dùng `pypdf` đọc text, gửi đến Gemini trích xuất cây tư duy và tự động mở bài giảng mới (Day 06) lên màn hình!
5. **Xoá bài giảng / slide tải nhầm:**
   - Chọn bài giảng muốn xoá trên thanh tab $\to$ Bấm nút đỏ **"Xoá Slide Này"** $\to$ Bấm xác nhận để dọn sạch dữ liệu.

---

## 🛠️ 4. Xử lý các lỗi thường gặp (Troubleshooting)

### Lỗi 1: `ModuleNotFoundError: No module named 'fastapi'` hoặc `uvicorn`
- **Nguyên nhân:** Bạn đang chạy trên Python mặc định chưa cài thư viện.
- **Cách sửa:** Kiểm tra xem đã kích hoạt đúng môi trường chưa (ví dụ `conda activate ai_workspace`) rồi chạy lại:
  ```powershell
  pip install -r requirements.txt
  ```

### Lỗi 2: `[WinError 10048] Only one usage of each socket address is normally permitted (Port 8000)`
- **Nguyên nhân:** Có một tiến trình Python hoặc server cũ đang chiếm cổng 8000.
- **Cách sửa:**
  - Tắt cửa sổ Terminal cũ đang chạy server.
  - Hoặc tắt tiến trình qua lệnh PowerShell:
    ```powershell
    Get-Process python | Stop-Process
    ```
  - Sau đó chạy lại `python run_server.py`.

### Lỗi 3: Báo `⚠️ Chưa có GEMINI_API_KEY trong .env` khi bấm Upload
- **Nguyên nhân:** File `.env` chưa có key hoặc chưa lưu file.
- **Cách sửa:** Mở file `.env`, dán key vào `GEMINI_API_KEY=...` và bấm **Save (Ctrl+S)**. Hệ thống đã cài chế độ tự động nhận diện (Hot-reload), bạn **không cần khởi động lại server**, chỉ cần bấm nút thử lại trên web.

### Lỗi 4: Thư mục `codebase/storage/` bị xoá hoặc thiếu file
- **Cách sửa:** Đừng lo! Hệ thống có file `codebase/backend/seed_data.py`. Mỗi khi bạn chạy `python run_server.py`, nếu phát hiện thiếu `storage/`, server sẽ **tự động phục hồi lại toàn bộ 5 bài học mẫu** ngay lập tức.
