"""
FastAPI Server phục vụ Giao diện VLearn và API Upload Slide chạy thật
Team: BungChay | Hackathon Batch 04 | Track A
"""

import os
import sys
import shutil
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import dotenv

# Load environment
dotenv.load_dotenv(override=True)

# Add parent path for imports
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.mindmap_service import (
    get_api_config,
    process_uploaded_slide,
    STORAGE_DIR,
    UPLOAD_DIR
)

app = FastAPI(
    title="VLearn Mindmap Backend Service",
    description="Hệ thống tự động trích xuất slide và dựng Mindmap D3.js bằng Gemini API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Phục vụ file giao diện chính."""
    index_file = BASE_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="index.html not found")
    with open(index_file, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/api/status")
async def get_system_status():
    """Kiểm tra trạng thái cấu hình API và số lượng ngày học hiện có."""
    cfg = get_api_config()
    meta_path = STORAGE_DIR / "metadata.json"
    days_count = 0
    if meta_path.exists():
        import json
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
                days_count = len(meta.get("days", []))
        except Exception:
            pass

    return {
        "status": "online",
        "has_api_key": cfg["has_key"],
        "model": cfg["model"],
        "total_days": days_count,
        "api_key_masked": f"{cfg['api_key'][:6]}...{cfg['api_key'][-4:]}" if len(cfg["api_key"]) > 10 else ("Configured" if cfg["has_key"] else "Missing")
    }


@app.get("/api/days")
async def get_all_days():
    """Lấy danh sách tất cả các ngày học và metadata."""
    meta_path = STORAGE_DIR / "metadata.json"
    if not meta_path.exists():
        return {"days": []}
    import json
    with open(meta_path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/api/day/{day_num}")
async def get_day_data(day_num: int):
    """Lấy dữ liệu chi tiết của một ngày học."""
    day_file = STORAGE_DIR / f"day_{day_num}.json"
    if not day_file.exists():
        raise HTTPException(status_code=404, detail=f"Không tìm thấy dữ liệu cho Day {day_num}")
    import json
    with open(day_file, "r", encoding="utf-8") as f:
        return json.load(f)


@app.delete("/api/day/{day_num}")
async def delete_day(day_num: int):
    """
    ENDPOINT XOÁ: Xoá bài giảng (slide & mindmap) theo số thứ tự ngày.
    """
    try:
        from backend.mindmap_service import delete_day_data
        result = delete_day_data(day_num)
        return {
            "success": True,
            "message": f"Đã xoá thành công bài học Day {day_num} và cây Mindmap tương ứng.",
            "data": result
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi xoá: {str(e)}")


@app.post("/api/upload")
async def upload_slide_deck(
    file: UploadFile = File(...),
    custom_title: Optional[str] = Form(None)
):
    """
    ENDPOINT CHÍNH: Nhận file slide PDF upload thật,
    trích xuất text và gọi Gemini API để sinh cây Mindmap D3.js.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Hệ thống hiện chỉ hỗ trợ định dạng slide PDF (.pdf)."
        )

    # 1. Lưu file upload tạm
    save_path = UPLOAD_DIR / file.filename
    try:
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi lưu file: {e}")

    # 2. Kiểm tra API Key
    cfg = get_api_config()
    if not cfg["has_key"]:
        raise HTTPException(
            status_code=400,
            detail=(
                "CHƯA TÌM THẤY GEMINI_API_KEY!\n\n"
                "Bạn cần mở file '.env' ở thư mục gốc dự án và điền: GEMINI_API_KEY=AIzaSy...\n"
                "Sau đó bấm nút Thử lại."
            )
        )

    # 3. Gọi xử lý thật với Gemini API
    try:
        result = process_uploaded_slide(save_path, custom_title)
        return {
            "success": True,
            "message": f"Đã trích xuất và tạo Mindmap thành công cho: {file.filename}",
            "data": result
        }
    except Exception as e:
        print(f"[ERROR IN UPLOAD] {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi trong quá trình AI phân tích slide: {str(e)}"
        )


def start():
    """Khởi động Uvicorn server."""
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "127.0.0.1")
    print(f"\n========================================================")
    print(f"🚀 VLEARN MINDMAP SERVER ĐANG CHẠY TẠI: http://{host}:{port}")
    print(f"👉 Mở trình duyệt truy cập: http://{host}:{port}")
    print(f"========================================================\n")
    uvicorn.run("backend.server:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    start()

