"""
Script khởi chạy máy chủ VLearn Mindmap (Hackathon Batch 04 - BungChay)
Chỉ cần chạy: python run_server.py
"""

import sys
import os
from pathlib import Path

# Add codebase to path
codebase_dir = Path(__file__).resolve().parent / "codebase"
sys.path.insert(0, str(codebase_dir))

# Ensure UTF-8 console output
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

if __name__ == "__main__":
    import uvicorn
    import dotenv
    dotenv.load_dotenv(override=True)

    key = os.getenv("GEMINI_API_KEY", "").strip()
    model = os.getenv("LLM_MODEL", "gemini-2.5-flash").strip()

    print("=" * 60)
    print("🚀 KHỞI ĐỘNG HỆ THỐNG VLEARN INTERACTIVE MINDMAP (CP3)")
    print("=" * 60)
    print(f"📌 Thư mục dự án: {Path(__file__).resolve().parent}")
    print(f"🤖 Mô hình Gemini: {model}")
    if key:
        print(f"🔑 Trạng thái API Key: ĐÃ CẤU HÌNH ({key[:6]}...{key[-4:]})")
    else:
        print(f"⚠️ Trạng thái API Key: CHƯA CÓ TRONG .env")
        print(f"   (Hệ thống vẫn phục vụ sẵn 5 ngày học đã trích xuất,")
        print(f"    bạn có thể thêm key vào file .env bất kỳ lúc nào)")
    print("-" * 60)
    print("👉 Mở trình duyệt tại: http://127.0.0.1:8000")
    print("=" * 60 + "\n")

    uvicorn.run("backend.server:app", app_dir=str(codebase_dir), host="127.0.0.1", port=8000, reload=True)
