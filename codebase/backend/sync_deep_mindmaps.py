"""
Script đồng bộ dữ liệu Mindmap Day 1 - 5 đa tầng sâu (3-5 cấp),
bao quát toàn bộ nội dung slide mà KHÔNG gọi API Gemini thật (tiết kiệm 100% quota).
"""

import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path("c:/Users/Public/Documents/AI_BAITAP/K4-3A-E403-BungChay/codebase")
STORAGE_DIR = BASE_DIR / "storage"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# 1. DỮ LIỆU DAY 01
# ==============================================================================
DAY_1_DATA = {
  "day": 1,
  "code": "DAY_01",
  "title": "AI & LLM Foundation",
  "subtitle": "Setup & Foundation + LAB 1: LLM API Exploration",
  "pdf_file": "day01_c401.pdf",
  "total_slides": 32,
  "tree": {
    "id": "d1_root",
    "title": "Day 01: AI Foundation",
    "summary": "Nền tảng LLM, môi trường phát triển và thực hành gọi API cơ bản.",
    "slide_page": "Slide 1-5",
    "type": "root",
    "children": [
      {
        "id": "d1_c1_llm_mech",
        "title": "Cơ Chế Transformer",
        "summary": "Kiến trúc Transformer, cơ chế Self-attention và tích hợp LLM API.",
        "slide_page": "Slide 4-7",
        "type": "branch",
        "children": [
          {
            "id": "d1_c1_attention_theory",
            "title": "Kiến Trúc Self-Attention",
            "summary": "Mô hình tính toán tương quan ngữ cảnh giữa các từ trong câu.",
            "slide_page": "Slide 6",
            "type": "branch",
            "children": [
              {
                "id": "d1_self_attention",
                "title": "Self-Attention Mechanism",
                "summary": "Cân nhắc mức độ liên quan của mọi token trong ngữ cảnh.",
                "slide_page": "Slide 6",
                "type": "concept",
                "cross_link": None,
                "detail": {
                  "title": "Live Demo: Self-Attention Mechanism",
                  "slide_page": "Slide 6",
                  "excerpt": "Cơ chế Self-Attention cho phép mô hình ngôn ngữ lớn (LLM) cân nhắc mức độ liên quan của mọi token khác trong ngữ cảnh khi xử lý một token hiện tại, tạo nền tảng cho việc hiểu ngữ nghĩa sâu thay vì chỉ dịch tuần tự.",
                  "key_takeaway": "Self-attention là cốt lõi biến Transformer thành kiến trúc thống trị các mô hình ngôn ngữ hiện đại.",
                  "ai_tutor_explanation": "Khi đọc từ 'ngân hàng' trong câu 'Tôi ra bờ sông câu cá gần ngân hàng cây xanh', cơ chế Self-attention sẽ chú ý mạnh đến 'bờ sông' và 'cây xanh' để hiểu đây là dải đất ven sông.",
                  "code_snippet": None,
                  "quick_quiz": "Cơ chế nào giúp Transformer hiểu mối liên hệ ngữ nghĩa giữa các từ cách xa nhau trong câu?\nA. Convolution\nB. Self-Attention\nC. Recurrent Loop\n(Đáp án đúng: B)"
                },
                "children": [
                  {
                    "id": "d1_qkv_vectors",
                    "title": "Ma Trận Query-Key-Value",
                    "summary": "Vector biểu diễn câu hỏi, từ khóa và giá trị ngữ nghĩa.",
                    "slide_page": "Slide 6",
                    "type": "detail",
                    "cross_link": None,
                    "detail": {
                      "title": "Bộ Ba Vector Q, K, V Trong Attention",
                      "slide_page": "Slide 6",
                      "excerpt": "Mỗi token được ánh xạ thành 3 vector: Query (tìm kiếm thông tin), Key (đặc trưng đối chiếu), Value (nội dung mang theo). Tích vô hướng Q.K xác định trọng số chú ý.",
                      "key_takeaway": "Trọng số Attention là kết quả so khớp giữa Query của token hiện tại và Key của các token trước.",
                      "ai_tutor_explanation": "Tương tự như việc bạn gõ từ khóa vào thanh tìm kiếm (Query), hệ thống so khớp với tiêu đề bài viết (Key) và trả về nội dung trang (Value).",
                      "code_snippet": "# Attention(Q, K, V) = softmax(Q * K.T / sqrt(d_k)) * V",
                      "quick_quiz": "Thành phần nào trong Attention thể hiện nội dung thông tin thực tế được truyền đi?\nA. Query\nB. Key\nC. Value\n(Đáp án đúng: C)"
                    }
                  }
                ]
              }
            ]
          },
          {
            "id": "d1_c1_providers_ecosystem",
            "title": "Hệ Sinh Thái LLM API",
            "summary": "Tích hợp dịch vụ từ Google Gemini, OpenAI và Anthropic qua SDK.",
            "slide_page": "Slide 7",
            "type": "branch",
            "children": [
              {
                "id": "d1_llm_api_providers",
                "title": "Nhà Cung Cấp API",
                "summary": "Quản lý API key, format request/response và xử lý streaming.",
                "slide_page": "Slide 7",
                "type": "concept",
                "cross_link": {
                  "target_day": 3,
                  "target_node_id": "d3_llm_chatbot",
                  "label": "🔗 Nền tảng cho Chatbot Day 03 [Slide 8]"
                },
                "detail": {
                  "title": "Tổng quan Codelab: Tích Hợp 3 Nhà Cung Cấp LLM API",
                  "slide_page": "Slide 7",
                  "excerpt": "Triển khai tích hợp các dịch vụ LLM API từ 3 nhà cung cấp lớn: OpenAI (GPT-4o), Google (Gemini 2.5 Flash), Anthropic (Claude 3.5 Sonnet). Quản lý API key, format request/response, và xử lý streaming.",
                  "key_takeaway": "Nắm vững cách cấu hình client, truyền prompt và đọc câu trả lời từ các SDK chuẩn.",
                  "ai_tutor_explanation": "Mỗi nhà cung cấp có cú pháp SDK khác nhau nhưng cùng chung nguyên lý: truyền chuỗi tin nhắn và nhận về text hoặc JSON.",
                  "code_snippet": "from google import genai\n\nclient = genai.Client(api_key='GEMINI_API_KEY')\nresponse = client.models.generate_content(\n    model='gemini-2.5-flash',\n    contents='Xin chào AI!'\n)\nprint(response.text)",
                  "quick_quiz": "Khi làm việc với LLM API ở máy cá nhân, điều quan trọng nhất về bảo mật là gì?\nA. Commit API key lên GitHub\nB. Lưu key trong file .env và thêm vào .gitignore\nC. Hardcode key vào file Python\n(Đáp án đúng: B)"
                },
                "children": [
                  {
                    "id": "d1_gemini_sdk_flow",
                    "title": "Google GenAI SDK Cú Pháp",
                    "summary": "Khởi tạo Client, truyền contents và đọc response text.",
                    "slide_page": "Slide 7",
                    "type": "detail",
                    "cross_link": None,
                    "detail": {
                      "title": "Cú Pháp Chuẩn Với google-genai 2026",
                      "slide_page": "Slide 7",
                      "excerpt": "Thư viện google-genai mới thống nhất việc gọi Gemini 2.5 Flash thông qua client.models.generate_content thay vì import genai cũ.",
                      "key_takeaway": "Dùng client.models.generate_content() đồng nhất cho mọi tác vụ sinh text và multimodal.",
                      "ai_tutor_explanation": "Google đã hợp nhất SDK cũ sang google-genai để hỗ trợ đồng thời Gemini 2.0 và 2.5 Flash với hiệu năng cao hơn.",
                      "code_snippet": "from google import genai\nclient = genai.Client()\nres = client.models.generate_content(model='gemini-2.5-flash', contents='Prompt')",
                      "quick_quiz": "Model Gemini khuyến nghị dùng cho bài thực hành sinh viên là gì?\nA. gemini-1.0-ultra\nB. gemini-2.5-flash\nC. gpt-3.5-turbo\n(Đáp án đúng: B)"
                    }
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        "id": "d1_c2_env_setup",
        "title": "Chuẩn Bị Môi Trường",
        "summary": "Checklist cài đặt Git, Python chuẩn, VSCode và GitHub Classroom.",
        "slide_page": "Slide 8-17",
        "type": "branch",
        "children": [
          {
            "id": "d1_c2_checklists",
            "title": "Bộ Tiêu Chuẩn Checklist",
            "summary": "Kiểm tra quyền truy cập tài khoản và công cụ máy tính cá nhân.",
            "slide_page": "Slide 8-9",
            "type": "branch",
            "children": [
              {
                "id": "d1_global_checklist",
                "title": "Global Checklist",
                "summary": "Kiểm tra email đăng ký khóa học, GitHub Org và Discord.",
                "slide_page": "Slide 8",
                "type": "concept",
                "cross_link": None,
                "detail": {
                  "title": "Global Checklist: Quyền Truy Cập & Tài Khoản",
                  "slide_page": "Slide 8",
                  "excerpt": "● Kiểm tra email của mình đã nằm trong danh sách đăng ký khoá học.\n● Kiểm tra quyền truy cập vào GitHub Organization của lớp học.\n● Xác nhận đã tham gia kênh Discord hỗ trợ kỹ thuật.",
                  "key_takeaway": "Đảm bảo tài khoản chính xác để nhận quyền nộp bài tự động qua GitHub Classroom.",
                  "ai_tutor_explanation": "Nếu dùng sai email đã đăng ký, hệ thống chấm CI/CD không thể liên kết bài nộp với học viên.",
                  "code_snippet": None,
                  "quick_quiz": "Tài khoản nào bắt buộc trùng khớp với danh sách BTC?\nA. Email đã đăng ký\nB. Facebook cá nhân\nC. LinkedIn\n(Đáp án đúng: A)"
                }
              },
              {
                "id": "d1_local_checklist",
                "title": "Local Checklist",
                "summary": "Phiên bản Git, Python 3.11-3.13, VSCode và GitHub Extension.",
                "slide_page": "Slide 9",
                "type": "concept",
                "cross_link": {
                  "target_day": 4,
                  "target_node_id": "d4_tool_calling",
                  "label": "🔗 Môi trường cho Tool Calling Day 04 [Slide 85]"
                },
                "detail": {
                  "title": "Local Checklist: Cài Đặt Môi Trường Máy Cá Nhân",
                  "slide_page": "Slide 9",
                  "excerpt": "● Trên máy đã cài đặt Git (Mở cmd chạy `git version` để kiểm tra)\n● Trên máy đã cài đặt Python < 3.14 & > 3.11 (Mở cmd chạy `python --version` để kiểm tra)\n● Trên máy đã có IDE Visual Studio Code (VSCode).\n● Đã cài đặt Extension GitHub Classroom trên VSCode.",
                  "key_takeaway": "Môi trường chuẩn giúp chạy mượt các bài lab từ Day 1 đến Day 5 không bị xung đột.",
                  "ai_tutor_explanation": "Nên dùng Python 3.11 hoặc 3.12 để tương thích tốt nhất với pydantic và google-genai.",
                  "code_snippet": "git version\npython --version\ncode --version",
                  "quick_quiz": "Phiên bản Python nào được khuyến nghị trong bài học Day 01?\nA. Python 2.7\nB. Python > 3.11 và < 3.14\nC. Python 3.8\n(Đáp án đúng: B)"
                },
                "children": [
                  {
                    "id": "d1_verify_terminal",
                    "title": "Lệnh Kiểm Tra CLI",
                    "summary": "Chạy git version và python --version trên Terminal xác thực.",
                    "slide_page": "Slide 9",
                    "type": "detail",
                    "cross_link": None,
                    "detail": {
                      "title": "Kiểm Tra Phiên Bản Công Cụ",
                      "slide_page": "Slide 9",
                      "excerpt": "Mở Command Prompt hoặc PowerShell, chạy lần lượt git version và python --version để đảm bảo PATH đã nhận diện.",
                      "key_takeaway": "Xác nhận công cụ nhận diện trong PATH trước khi clone bài tập.",
                      "ai_tutor_explanation": "Nếu gõ python mà mở Windows Store, bạn cần tắt App Execution Aliases trong Settings của Windows.",
                      "code_snippet": "git --version\npython --version",
                      "quick_quiz": "Lỗi gõ python tự bật Microsoft Store xử lý ở đâu?\nA. Cài lại Windows\nB. Tắt App Execution Aliases trong Windows Settings\nC. Xóa Git\n(Đáp án đúng: B)"
                    }
                  }
                ]
              }
            ]
          },
          {
            "id": "d1_c2_github_flow",
            "title": "GitHub Classroom Flow",
            "summary": "Quy trình 6 bước nhận repo bài tập và mở trong VSCode.",
            "slide_page": "Slide 10-17",
            "type": "branch",
            "children": [
              {
                "id": "d1_classroom_flow",
                "title": "Quy Trình 6 Bước Lab",
                "summary": "Quét mã link Lab, đăng nhập GitHub, accept và mở VSCode.",
                "slide_page": "Slide 10-16",
                "type": "concept",
                "cross_link": None,
                "detail": {
                  "title": "Quy Trình 6 Bước Nhận Bài Tập Codelab",
                  "slide_page": "Slide 10-16",
                  "excerpt": "Bước 1: Quét mã link Lab. Bước 2: Đăng nhập vào GitHub. Bước 3: Chọn Skip to next step. Bước 4: Kiểm tra email. Bước 5: Accept assignment. Bước 6: Kéo xuống và chọn 'Open in Visual Studio Code'.",
                  "key_takeaway": "Hoàn tất luồng GitHub Classroom để chuẩn bị nộp bài tập tự động bằng Git Push.",
                  "ai_tutor_explanation": "Khi click Accept Assignment, GitHub Classroom tự tạo repository riêng từ template giảng viên.",
                  "code_snippet": "git clone https://github.com/K4-VinUni/your-assignment.git\ncd your-assignment",
                  "quick_quiz": "Nút bấm nào giúp mở trực tiếp repo bài tập vào trình soạn thảo code?\nA. Open in Terminal\nB. Open in Visual Studio Code\nC. Download ZIP\n(Đáp án đúng: B)"
                }
              }
            ]
          }
        ]
      },
      {
        "id": "d1_c3_codelab_arch",
        "title": "Cấu Trúc Codelab",
        "summary": "Template code, cấu hình file .env và bộ kiểm thử tự động.",
        "slide_page": "Slide 18-32",
        "type": "branch",
        "children": [
          {
            "id": "d1_c3_files_structure",
            "title": "Hệ Thống Files Lab",
            "summary": "Tổng quan template.py, main.py, test.py và cấu hình .env.",
            "slide_page": "Slide 18-22",
            "type": "branch",
            "children": [
              {
                "id": "d1_files_overview",
                "title": "Files & Template",
                "summary": "Cấu trúc template.py, script main.py và bộ kiểm thử test.py.",
                "slide_page": "Slide 18",
                "type": "concept",
                "cross_link": None,
                "detail": {
                  "title": "Tổng Quan Các Files Trong Bài Thực Hành",
                  "slide_page": "Slide 18",
                  "excerpt": "● template.py: File chứa khung code thực hành với các hàm TODO cần hoàn thiện.\n● main.py: Script điều khiển chính để chạy thử nghiệm các tính năng.\n● test.py: Bộ kiểm thử tự động để học viên tự đánh giá trước khi nộp.",
                  "key_takeaway": "Chỉ chỉnh sửa các vùng TODO trong template.py để đảm bảo test runner hoạt động chuẩn.",
                  "ai_tutor_explanation": "File template.py định nghĩa sẵn interface và kiểu dữ liệu trả về, bạn chỉ cần điền logic gọi API.",
                  "code_snippet": "def call_gemini(prompt: str) -> str:\n    # TODO: Khởi tạo client và gọi generate_content\n    pass",
                  "quick_quiz": "File nào chứa bộ kiểm thử tự động để bạn tự đánh giá code trước khi nộp?\nA. template.py\nB. test.py\nC. README.md\n(Đáp án đúng: B)"
                }
              },
              {
                "id": "d1_env_setup",
                "title": "Biến Môi Trường .env",
                "summary": "Thiết lập API key trong .env và bảo vệ bằng .gitignore.",
                "slide_page": "Slide 19",
                "type": "concept",
                "cross_link": None,
                "detail": {
                  "title": "Cấu Hình API Key Với File .env",
                  "slide_page": "Slide 19",
                  "excerpt": "Tạo file `.env` ở thư mục gốc repo:\nGEMINI_API_KEY=AIzaSy...\nOPENAI_API_KEY=sk-...\nANTHROPIC_API_KEY=sk-ant-...\nĐảm bảo file `.env` đã được liệt kê trong `.gitignore`.",
                  "key_takeaway": "Không bao giờ để lộ API Key công khai trên kho mã nguồn.",
                  "ai_tutor_explanation": "Nếu push nhầm API key lên GitHub công khai, bot quét sẽ vô hiệu hoá key đó trong vài phút.",
                  "code_snippet": "echo GEMINI_API_KEY=your_key_here > .env\necho .env >> .gitignore",
                  "quick_quiz": "Làm cách nào ngăn Git commit nhầm file chứa API key lên remote?\nA. Đổi tên file\nB. Thêm tên file vào .gitignore\nC. Xoá file trước khi push\n(Đáp án đúng: B)"
                }
              }
            ]
          },
          {
            "id": "d1_c3_test_runner",
            "title": "Thực Thi & Kiểm Thử",
            "summary": "Cài đặt thư viện dependencies và chạy kiểm thử tự động.",
            "slide_page": "Slide 20-32",
            "type": "branch",
            "children": [
              {
                "id": "d1_pip_install_deps",
                "title": "Cài Đặt Dependencies",
                "summary": "Cài đặt pypdf, google-genai và python-dotenv qua pip.",
                "slide_page": "Slide 20",
                "type": "concept",
                "cross_link": None,
                "detail": {
                  "title": "Cài Đặt Gói Thư Viện Thực Hành",
                  "slide_page": "Slide 20",
                  "excerpt": "Chạy lệnh pip install -r requirements.txt trong terminal VSCode để nạp toàn bộ SDK cần thiết cho bài giảng.",
                  "key_takeaway": "Cài đặt đầy đủ dependencies trong môi trường ảo trước khi chạy code.",
                  "ai_tutor_explanation": "Sử dụng pip install đảm bảo mọi thư viện đúng phiên bản yêu cầu của bài lab.",
                  "code_snippet": "pip install google-genai python-dotenv pypdf fastapi uvicorn",
                  "quick_quiz": "Lệnh nào dùng để cài đặt toàn bộ thư viện từ file cấu hình?\nA. git pull\nB. pip install -r requirements.txt\nC. python main.py\n(Đáp án đúng: B)"
                }
              }
            ]
          }
        ]
      }
    ]
  }
}

# ==============================================================================
# 2. DỮ LIỆU DAY 02
# ==============================================================================
DAY_2_DATA = {
  "day": 2,
  "code": "DAY_02",
  "title": "Xác Định Bài Toán Cho AI",
  "subtitle": "Khung Lý Thuyết 4H + Google PAIR Guidebook",
  "pdf_file": "day02.pdf",
  "total_slides": 76,
  "tree": {
    "id": "d2_root",
    "title": "Day 02: Xác Định Bài Toán",
    "summary": "Khung đánh giá bài toán, phân cấp Rule vs Agent và cẩm nang Google PAIR.",
    "slide_page": "Slide 1-8",
    "type": "root",
    "children": [
      {
        "id": "d2_c1_core_framework",
        "title": "Khung Đánh Giá Bài Toán",
        "summary": "Quy trình 4 câu hỏi trọng tâm và phân cấp giải pháp Rule-Workflow-Agent.",
        "slide_page": "Slide 3-7, 69",
        "type": "branch",
        "children": [
          {
            "id": "d2_c1_4_questions",
            "title": "4 Câu Hỏi Trọng Tâm",
            "summary": "Cần AI không? Cấp độ giải pháp? Problem Statement? Quyết định Go/No-Go?",
            "slide_page": "Slide 3",
            "type": "branch",
            "children": [
              {
                "id": "d2_4_core_questions",
                "title": "Bộ Câu Hỏi 4H",
                "summary": "Sàng lọc yêu cầu để tránh bẫy búa AI đi tìm đinh.",
                "slide_page": "Slide 3",
                "type": "concept",
                "cross_link": {
                  "target_day": 3,
                  "target_node_id": "d3_agentic_fit",
                  "label": "🔗 Cơ sở cho Agentic Fit Day 03 [Slide 10]"
                },
                "detail": {
                  "title": "Bốn Câu Hỏi Trọng Tâm Khi Thiết Kế Giải Pháp AI",
                  "slide_page": "Slide 3",
                  "excerpt": "01. Bài toán có thực sự cần AI giải quyết?\n02. Nếu có, giải pháp ở cấp độ nào: Rule, Workflow, hay Agent?\n03. Problem Statement đã đủ rõ ràng để triển khai?\n04. Khi nào quyết định: Go, Not Yet, hay No-Go?",
                  "key_takeaway": "Tránh bẫy búa AI đi tìm đinh. Chỉ áp dụng AI khi đòi hỏi xử lý ngữ nghĩa hoặc thích ứng cao.",
                  "ai_tutor_explanation": "Nhiều kỹ sư vội vã dùng LLM cho bài toán tính toán số học hoặc if/else. Câu hỏi 01 và 02 giúp xác định mức độ phức tạp tối thiểu cần thiết.",
                  "code_snippet": None,
                  "quick_quiz": "Khi bài toán có quy tắc cố định 100%, bạn nên chọn giải pháp nào?\nA. Multi-Agent System\nB. Rule-based if/else\nC. Fine-tuning LLM\n(Đáp án đúng: B)"
                },
                "children": [
                  {
                    "id": "d2_decision_go_nogo",
                    "title": "Quyết Định Go/No-Go",
                    "summary": "Tiêu chí nghiệm thu để quyết định cấp vốn hoặc dừng dự án.",
                    "slide_page": "Slide 3, 71",
                    "type": "detail",
                    "cross_link": None,
                    "detail": {
                      "title": "Khung Ra Quyết Định Go/Not Yet/No-Go",
                      "slide_page": "Slide 71",
                      "excerpt": "01 Brief mơ hồ không thay thế Problem Statement. Chỉ bấm nút 'Go' khi có dữ liệu đầu vào xác thực và baseline đo lường rõ ràng.",
                      "key_takeaway": "Một bản tóm tắt mơ hồ không thể thay thế cho Problem Statement chuẩn.",
                      "ai_tutor_explanation": "Nếu bài toán chưa có dữ liệu hoặc chưa định nghĩa được metric thành công, quyết định đúng đắn là 'Not Yet' thay vì cố build.",
                      "code_snippet": None,
                      "quick_quiz": "Khi nào nên đưa ra quyết định 'Not Yet' cho một dự án AI?\nA. Khi chưa có dữ liệu đầu vào đủ sạch và metric chưa rõ ràng\nB. Khi chưa mua GPU mới\nC. Khi chưa có chứng chỉ AI\n(Đáp án đúng: A)"
                    }
                  }
                ]
              }
            ]
          },
          {
            "id": "d2_c1_solution_tiers",
            "title": "Phân Cấp Giải Pháp",
            "summary": "So sánh 3 cấp độ: Rule cố định, Workflow tuần tự và Autonomous Agent.",
            "slide_page": "Slide 3, 69",
            "type": "branch",
            "children": [
              {
                "id": "d2_rule_workflow_agent",
                "title": "Rule vs Workflow vs Agent",
                "summary": "Phân tầng độ phức tạp giải pháp theo độ bất định của bài toán.",
                "slide_page": "Slide 69",
                "type": "concept",
                "cross_link": {
                  "target_day": 3,
                  "target_node_id": "d3_3_systems",
                  "label": "🔗 Chi tiết hoá thành 3 Kiểu Hệ Thống Day 03 [Slide 8]"
                },
                "detail": {
                  "title": "Phân Cấp: Rule vs. Workflow vs. Agent",
                  "slide_page": "Slide 69",
                  "excerpt": "● Rule: Xử lý theo logic cố định (deterministic), độ tin cậy tuyệt đối, chi phí cực thấp.\n● Workflow: Luồng nhiều bước kết hợp gọi LLM ở một số trạm xử lý văn bản.\n● Agent: Mô hình tự lập kế hoạch (Plan), tự chọn công cụ (Tool Use), tự thích ứng.",
                  "key_takeaway": "Bắt đầu với giải pháp đơn giản nhất (Rule -> Workflow), chỉ nâng lên Agent khi bất định cao.",
                  "ai_tutor_explanation": "Luôn triển khai heuristic đơn giản làm baseline trước. Nếu baseline giải quyết được 80% vấn đề với chi phí 0đ, bạn không cần dùng LLM đắt đỏ.",
                  "code_snippet": None,
                  "quick_quiz": "Theo Google và Anthropic, khi nào mới nên nâng cấp lên Agent?\nA. Khi muốn khoe công nghệ mới\nB. Khi quy tắc nghiệp vụ cố định\nC. Khi bài toán đòi hỏi tự quyết định bước đi tiếp theo dựa trên quan sát\n(Đáp án đúng: C)"
                }
              }
            ]
          }
        ]
      },
      {
        "id": "d2_c2_pair_handbook",
        "title": "Google PAIR Guidebook",
        "summary": "6 chương cẩm nang thiết kế sản phẩm AI lấy con người làm trung tâm.",
        "slide_page": "Slide 8-12",
        "type": "branch",
        "children": [
          {
            "id": "d2_c2_pair_core",
            "title": "Cẩm Nang People + AI",
            "summary": "Thiết lập kỳ vọng Mental Model, tính minh bạch và xử lý lỗi tinh tế.",
            "slide_page": "Slide 8",
            "type": "branch",
            "children": [
              {
                "id": "d2_pair_6_chapters",
                "title": "6 Trụ Cột Google PAIR",
                "summary": "User Needs, Data, Mental Models, Explainability, Feedback, Graceful Failure.",
                "slide_page": "Slide 8",
                "type": "concept",
                "cross_link": {
                  "target_day": 5,
                  "target_node_id": "d5_responsible_ai",
                  "label": "🔗 Mở rộng sang Responsible AI Day 05 [Slide 12]"
                },
                "detail": {
                  "title": "Google PAIR: People + AI Guidebook (6 Chương Cốt Lõi)",
                  "slide_page": "Slide 8",
                  "excerpt": "1. User Needs + Defining Success: Xác định giá trị thực sự cho người dùng.\n2. Data Collection + Evaluation: Thu thập và đánh giá dữ liệu.\n3. Mental Models: Định hình kỳ vọng người dùng.\n4. Explainability + Trust: Tính minh bạch và giải thích được quyết định.\n5. Feedback + Control: Trao quyền cho người dùng sửa sai.\n6. Errors + Graceful Failure: Xử lý lỗi tinh tế.",
                  "key_takeaway": "Google PAIR là kim chỉ nam giúp thiết kế trải nghiệm người dùng với AI an toàn và tin cậy.",
                  "ai_tutor_explanation": "Chương 6 (Graceful Failure) cực kỳ quan trọng: khi AI không tìm thấy tài liệu, hệ thống phải hỏi làm rõ (Clarify) thay vì bịa đặt.",
                  "code_snippet": None,
                  "quick_quiz": "Trụ cột nào trong PAIR giúp người dùng hiểu vì sao AI đưa ra gợi ý đó?\nA. Explainability + Trust\nB. Data Collection\nC. Feedback + Control\n(Đáp án đúng: A)"
                },
                "children": [
                  {
                    "id": "d2_graceful_failure_detail",
                    "title": "Graceful Failure & Clarify",
                    "summary": "Xử lý lỗi êm đẹp khi độ tin cậy thấp, kích hoạt fallback hoặc gợi ý.",
                    "slide_page": "Slide 8",
                    "type": "detail",
                    "cross_link": None,
                    "detail": {
                      "title": "Cơ Chế Graceful Failure Cho Ứng Dụng AI",
                      "slide_page": "Slide 8",
                      "excerpt": "Khi confidence score của mô hình nằm dưới ngưỡng tin cậy, UI không được báo crash 500 hay sinh hallucination mà phải hiển thị câu hỏi gợi ý làm rõ hoặc trả về dữ liệu lưu trữ sẵn.",
                      "key_takeaway": "Thiết kế vùng dung sai lỗi để người dùng luôn có lối thoát khi AI không chắc chắn.",
                      "ai_tutor_explanation": "Đây là lý do Mindmap có nút '⚡ Test CLARIFY' để kích hoạt phản hồi trợ giúp khi tài liệu không đủ dữ liệu.",
                      "code_snippet": "if confidence < 0.75:\n    return ask_clarification_question()",
                      "quick_quiz": "Hành vi nào thể hiện Graceful Failure tốt nhất?\nA. Trả về màn hình trắng tinh\nB. Hỏi làm rõ và cung cấp tài liệu tham khảo dự phòng\nC. Sinh câu trả lời bịa đặt\n(Đáp án đúng: B)"
                    }
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        "id": "d2_c3_problem_discovery",
        "title": "Problem Discovery & Sàng Lọc",
        "summary": "Khám phá điểm đau thực tế và phân loại bài toán bằng ma trận tác động.",
        "slide_page": "Slide 13-54",
        "type": "branch",
        "children": [
          {
            "id": "d2_c3_pain_points",
            "title": "Phân Tích Điểm Đau",
            "summary": "Quan sát học viên, trợ giảng và viết Problem Statement chuẩn xác.",
            "slide_page": "Slide 13-25",
            "type": "branch",
            "children": [
              {
                "id": "d2_problem_discovery",
                "title": "Problem Discovery",
                "summary": "Khảo sát lớp học 1000 học viên, tìm điểm nghẽn của TA và học viên.",
                "slide_page": "Slide 13-18",
                "type": "concept",
                "cross_link": {
                  "target_day": 5,
                  "target_node_id": "d5_prd_8_parts",
                  "label": "🔗 Điền vào Phần 1 PRD Day 05 [Slide 25]"
                },
                "detail": {
                  "title": "Problem Discovery & Phân Tích Điểm Đau (Pain Points)",
                  "slide_page": "Slide 13-18",
                  "excerpt": "Từ quan sát lớp học 1000 học viên: Trợ giảng quá tải ở khâu trả lời lặp đi lặp lại cùng một câu hỏi cài đặt môi trường. Học viên bế tắc khi gặp lỗi Git/Python mà không biết tìm slide nào hướng dẫn.",
                  "key_takeaway": "Problem Statement tốt phải chỉ rõ: Đối tượng, bối cảnh, tổn thất cụ thể và tiêu chí đo lường.",
                  "ai_tutor_explanation": "Đừng viết 'Người dùng cần AI để học nhanh hơn'. Hãy viết: 'Học viên mất trung bình 45 phút tìm kiếm slide giải thích lệnh do bài giảng dài hơn 100 trang'.",
                  "code_snippet": None,
                  "quick_quiz": "Một Problem Statement chuẩn phải bắt đầu từ yếu tố nào?\nA. Công nghệ AI xịn nhất\nB. Nỗi đau và tổn thất có thật của người dùng mục tiêu\nC. Số lượng tham số của mô hình\n(Đáp án đúng: B)"
                }
              }
            ]
          },
          {
            "id": "d2_c3_prioritization",
            "title": "Ma Trận Ưu Tiên AI",
            "summary": "Ma trận Tần suất & Tác động (Frequency vs Impact) để sàng lọc use case.",
            "slide_page": "Slide 54",
            "type": "branch",
            "children": [
              {
                "id": "d2_freq_impact_matrix",
                "title": "Ma Trận Tần Suất & Tác Động",
                "summary": "Ưu tiên bài toán có Tần suất cao và Tác động lớn để tối đa hoá ROI.",
                "slide_page": "Slide 54",
                "type": "concept",
                "cross_link": {
                  "target_day": 5,
                  "target_node_id": "d5_success_metrics",
                  "label": "🔗 Đối chiếu ROI trong Day 05 [Slide 9]"
                },
                "detail": {
                  "title": "Ma Trận Phân Loại: Tần Suất & Tác Động (Frequency vs Impact)",
                  "slide_page": "Slide 54",
                  "excerpt": "● Góc phần tư 1 (High Frequency, High Impact): Điểm vàng đầu tư AI (Core AI Use case).\n● Góc phần tư 2 (Low Frequency, High Impact): Dự phòng khủng hoảng, cần Human-in-the-loop.\n● Góc phần tư 3 (High Frequency, Low Impact): Tự động hoá bằng Rule/Macro đơn giản.\n● Góc phần tư 4 (Low Frequency, Low Impact): Bỏ qua.",
                  "key_takeaway": "Dùng ma trận để sàng lọc tính năng, tránh lãng phí chi phí phát triển AI vào use case ít giá trị.",
                  "ai_tutor_explanation": "Việc học viên tra cứu mục lục slide diễn ra hàng chục lần mỗi buổi và giảm tải 60% thời gian cho TA, thuộc góc phần tư 1.",
                  "code_snippet": None,
                  "quick_quiz": "Bài toán có tần suất xảy ra cao nhưng tác động rất nhỏ nên giải quyết bằng cách nào?\nA. Xây dựng Multi-Agent đắt tiền\nB. Viết script tự động hoá hoặc rule đơn giản\nC. Bỏ qua hoàn toàn\n(Đáp án đúng: B)"
                }
              }
            ]
          }
        ]
      }
    ]
  }
}

# ==============================================================================
# 3. DỮ LIỆU DAY 03
# ==============================================================================
DAY_3_DATA = {
  "day": 3,
  "code": "DAY_03",
  "title": "Từ Chatbot Đến Agentic Agent",
  "subtitle": "Phổ Hệ Thống + ReAct Pattern",
  "pdf_file": "day03-tu-chatbot-den-agentic-agent-react (1).pdf",
  "total_slides": 46,
  "tree": {
    "id": "d3_root",
    "title": "Day 03: ReAct Agent",
    "summary": "Phổ hệ thống AI, 4 tiêu chí Agentic Fit và kiến trúc vòng lặp ReAct.",
    "slide_page": "Slide 1-6",
    "type": "root",
    "children": [
      {
        "id": "d3_c1_spectrum",
        "title": "Phổ Hệ Thống AI",
        "summary": "So sánh chi tiết Rule-based Bot, LLM Chatbot và Autonomous Agent.",
        "slide_page": "Slide 6-9",
        "type": "branch",
        "children": [
          {
            "id": "d3_c1_comparison",
            "title": "So Sánh 3 Cấp Độ",
            "summary": "Đối chiếu về cách xử lý, bộ nhớ, công cụ, chi phí và rủi ro loop.",
            "slide_page": "Slide 7-8",
            "type": "branch",
            "children": [
              {
                "id": "d3_3_systems",
                "title": "So Sánh 3 Hệ Thống",
                "summary": "Rule-based logic cứng, Chatbot sinh text context, Agent lập kế hoạch.",
                "slide_page": "Slide 8",
                "type": "concept",
                "cross_link": {
                  "target_day": 2,
                  "target_node_id": "d2_rule_workflow_agent",
                  "label": "🔗 Kế thừa phân cấp Day 02 [Slide 3 & 69]"
                },
                "detail": {
                  "title": "Bảng So Sánh Toàn Diện: Rule-based Bot vs Chatbot vs Agent",
                  "slide_page": "Slide 8",
                  "excerpt": "Tiêu chí: Cách xử lý | Bộ nhớ | Tool use | Chi phí | Rủi ro\n● Rule-based: If/else cố định | Không | Hard-coded | Thấp nhất | Dễ kiểm soát logic\n● LLM Chatbot: Sinh text theo context | Ngắn hạn trong context | Gọi tool theo chỉ định | Trung bình | Hallucination\n● Agent: Plan -> Act -> Observe -> Adapt | Ngắn hạn + Long-term | Chủ động chọn tool | Cao hơn do loop | Loop vô tận + Tool misuse",
                  "key_takeaway": "Agent mạnh hơn nhưng chi phí cao hơn và rủi ro loop, chỉ dùng khi chatbot không giải quyết được.",
                  "ai_tutor_explanation": "Nếu bài toán chỉ là hỏi-đáp một lượt, Chatbot baseline là tối ưu. Chỉ khi hệ thống cần tự kiểm tra kết quả và thử lại mới cần Agent.",
                  "code_snippet": None,
                  "quick_quiz": "Rủi ro đặc thù lớn nhất khi triển khai Agent so với Chatbot là gì?\nA. Thiếu context window\nB. Rơi vào vòng lặp vô hạn và gọi nhầm tool\nC. Không hỗ trợ tiếng Việt\n(Đáp án đúng: B)"
                },
                "children": [
                  {
                    "id": "d3_infinite_loop_risk",
                    "title": "Rủi Ro Vòng Lặp Vô Hạn",
                    "summary": "Agent gọi tool lặp đi lặp lại làm cạn kiệt quota và token.",
                    "slide_page": "Slide 8, 35",
                    "type": "detail",
                    "cross_link": None,
                    "detail": {
                      "title": "Rủi Ro Vòng Lặp Vô Tận Trong Agent",
                      "slide_page": "Slide 35",
                      "excerpt": "Khi tool trả về lỗi liên tục mà Agent không có điều kiện dừng, Agent sẽ retry liên tiếp làm cháy quota 15 RPM chỉ trong vài chục giây.",
                      "key_takeaway": "Bắt buộc thiết lập max_iterations (thường là 3-5 bước) để chống cạn kiệt tài nguyên.",
                      "ai_tutor_explanation": "Biện pháp phòng ngừa chuẩn là gán một biến đếm bước lặp, vượt ngưỡng sẽ trả fallback.",
                      "code_snippet": "if step_count >= MAX_STEPS:\n    return 'Fallback do vượt quá số bước cho phép.'",
                      "quick_quiz": "Biện pháp kỹ thuật nào bắt buộc có để ngăn Agent chạy loop vô tận?\nA. Tăng timeout lên 1 tiếng\nB. Thiết lập max_iterations giới hạn số vòng lặp\nC. Đổi prompt dài hơn\n(Đáp án đúng: B)"
                    }
                  }
                ]
              },
              {
                "id": "d3_llm_chatbot",
                "title": "LLM Chatbot Baseline",
                "summary": "Hệ thống sinh câu trả lời theo context, đóng vai trò mốc so chuẩn.",
                "slide_page": "Slide 9",
                "type": "concept",
                "cross_link": {
                  "target_day": 1,
                  "target_node_id": "d1_llm_api_providers",
                  "label": "🔗 Sử dụng LLM API Day 01 [Slide 7]"
                },
                "detail": {
                  "title": "Xây Dựng Chatbot Baseline Trước Khi Lên Agent",
                  "slide_page": "Slide 9",
                  "excerpt": "Trong thực hành kỹ thuật, luôn xây dựng Chatbot baseline trước. Baseline cung cấp mốc đo lường về độ chính xác, tốc độ và chi phí token để so sánh xem việc nâng cấp lên ReAct Agent có thực sự đem lại giá trị vượt trội.",
                  "key_takeaway": "Không có baseline, bạn không thể chứng minh Agent của mình hiệu quả hơn hay chỉ làm tốn token.",
                  "ai_tutor_explanation": "Bài Lab 3 yêu cầu tạo 1 bot trả lời câu hỏi trước, sau đó mới tích hợp tool tra cứu và vòng lặp ReAct.",
                  "code_snippet": "response = client.models.generate_content(\n    model='gemini-2.5-flash',\n    contents=[{'role': 'user', 'parts': [{'text': user_query}]}]\n)",
                  "quick_quiz": "Mục đích quan trọng nhất của việc xây dựng Chatbot Baseline là gì?\nA. Để nộp bài cho nhanh\nB. Làm mốc đo lường đối chứng chi phí và độ chính xác trước khi lên Agent\nC. Thay thế hoàn toàn Agent\n(Đáp án đúng: B)"
                }
              }
            ]
          }
        ]
      },
      {
        "id": "d3_c2_agentic_fit",
        "title": "Agentic Fit Framework",
        "summary": "4 tiêu chí cốt lõi và ma trận chấm điểm để quyết định có cần Agent.",
        "slide_page": "Slide 10-15",
        "type": "branch",
        "children": [
          {
            "id": "d3_c2_fit_criteria",
            "title": "Bộ Tiêu Chí Đánh Giá",
            "summary": "Multi-step reasoning, tool use, dynamic decisions và environmental uncertainty.",
            "slide_page": "Slide 11-12",
            "type": "branch",
            "children": [
              {
                "id": "d3_agentic_fit",
                "title": "4 Tiêu Chí Agentic Fit",
                "summary": "4 điều kiện vàng để khẳng định một bài toán thực sự cần Agent.",
                "slide_page": "Slide 11",
                "type": "concept",
                "cross_link": {
                  "target_day": 5,
                  "target_node_id": "d5_success_metrics",
                  "label": "🔗 Xác thực bài toán trong PRD Day 05 [Slide 25]"
                },
                "detail": {
                  "title": "4 Tiêu Chí Vàng Đánh Giá Agentic Fit",
                  "slide_page": "Slide 11",
                  "excerpt": "1. Multi-step Reasoning: Suy luận chuỗi qua nhiều bước phụ thuộc nhau.\n2. Tool Use: Tương tác với môi trường ngoài (Database, API, Search).\n3. Dynamic Decisions: Bước tiếp theo phụ thuộc vào kết quả bước trước.\n4. Environmental Uncertainty: Môi trường biến thiên cao, không thể hardcode cây quyết định.",
                  "key_takeaway": "Nếu use case chỉ thoả mãn 1 trong 4 tiêu chí, thường chỉ cần Chatbot hoặc Workflow.",
                  "ai_tutor_explanation": "Tính năng tạo Mindmap tự động: đọc slide -> tạo cây khái niệm -> tìm liên kết chéo -> kiểm tra súc tích là chuỗi Multi-step điển hình.",
                  "code_snippet": None,
                  "quick_quiz": "Use case nào sau đây ĐẠT tiêu chí Agentic Fit cao nhất?\nA. Tra cứu mã bưu chính của một tỉnh\nB. Dịch một đoạn văn bản ngắn sang tiếng Anh\nC. Đặt tour du lịch tự động: kiểm tra lịch, so giá vé, gọi API book và gửi email xác nhận\n(Đáp án đúng: C)"
                }
              },
              {
                "id": "d3_anti_patterns",
                "title": "Anti-Patterns Cần Tránh",
                "summary": "Lỗi dùng Agent sai bài: bài toán 1 bước, tra FAQ đơn giản, không có feedback loop.",
                "slide_page": "Slide 13",
                "type": "concept",
                "cross_link": None,
                "detail": {
                  "title": "Anti-Patterns: Khi Dùng Agent Là Sai Bài",
                  "slide_page": "Slide 13",
                  "excerpt": "□ Bài toán 1 bước: hỏi đáp, tra FAQ, phân loại cơ bản.\n□ Quy trình đã xác định 100% không đổi: dùng workflow code thường nhanh hơn 10x và rẻ hơn 100x.\n□ Thiếu cơ chế phản hồi từ môi trường.\n□ Dùng Agent chỉ vì hiệu ứng truyền thông (FOMO công nghệ).",
                  "key_takeaway": "Dùng Agent sai bài sẽ khiến hệ thống chạy chậm, tốn token vô ích và khó debug.",
                  "ai_tutor_explanation": "Đó là lý do backend Mindmap dùng Deterministic Python Pipeline để gom slide, chỉ dùng LLM tạo JSON khái niệm.",
                  "code_snippet": None,
                  "quick_quiz": "Trường hợp nào sau đây là Anti-pattern khi dùng Agent?\nA. Viết script agent tự động duyệt và debug lỗi unit test\nB. Dùng agent để tra cứu định nghĩa một từ vựng trong từ điển\nC. Dùng agent phân tích dữ liệu nhiều nguồn và tổng hợp báo cáo\n(Đáp án đúng: B)"
                }
              }
            ]
          }
        ]
      },
      {
        "id": "d3_c3_react_pattern",
        "title": "Kiến Trúc ReAct Pattern",
        "summary": "Mô hình Reasoning + Acting: Thought -> Action -> Observation -> Final Answer.",
        "slide_page": "Slide 16-35",
        "type": "branch",
        "children": [
          {
            "id": "d3_c3_agent_arch",
            "title": "Thành Phần Cốt Lõi Agent",
            "summary": "Reasoning Core, Short-term/Long-term Memory và Tool Calling.",
            "slide_page": "Slide 17-19",
            "type": "branch",
            "children": [
              {
                "id": "d3_agent_memory",
                "title": "Bộ Nhớ Ngắn & Dài Hạn",
                "summary": "Phân biệt context window ngắn hạn và vector database dài hạn.",
                "slide_page": "Slide 18",
                "type": "concept",
                "cross_link": {
                  "target_day": 4,
                  "target_node_id": "d4_context_engineering",
                  "label": "🔗 Quản lý context trong Day 04 [Slide 50]"
                },
                "detail": {
                  "title": "Bộ Nhớ Trong Kiến Trúc Agent",
                  "slide_page": "Slide 18",
                  "excerpt": "● Short-term memory: Lưu chuỗi tin nhắn và observation trong ngữ cảnh hiện tại.\n● Long-term memory: Lưu trữ kinh nghiệm, tài liệu vector hóa để truy xuất khi cần.",
                  "key_takeaway": "Short-term memory bị giới hạn bởi context window; Long-term memory dựa vào Vector DB hoặc Cache.",
                  "ai_tutor_explanation": "Giống như RAM và Ổ cứng của máy tính: RAM xử lý tác vụ đang mở, Ổ cứng lưu file lâu dài.",
                  "code_snippet": None,
                  "quick_quiz": "Thành phần nào đóng vai trò Short-term Memory trong LLM Agent?\nA. SQLite Database\nB. Các message nằm trong prompt context hiện tại\nC. File .env\n(Đáp án đúng: B)"
                }
              }
            ]
          },
          {
            "id": "d3_c3_react_loop_flow",
            "title": "Vòng Lặp ReAct & Debug",
            "summary": "Chu trình Thought -> Action -> Observation và checklist gỡ lỗi trace.",
            "slide_page": "Slide 20-35",
            "type": "branch",
            "children": [
              {
                "id": "d3_react_loop",
                "title": "Vòng Lặp ReAct",
                "summary": "Chu trình Thought (Suy nghĩ) -> Action (Hành động) -> Observation (Quan sát).",
                "slide_page": "Slide 20-24",
                "type": "concept",
                "cross_link": {
                  "target_day": 4,
                  "target_node_id": "d4_tool_calling",
                  "label": "🔗 Thực thi Action trong Day 04 [Slide 42 & 85]"
                },
                "detail": {
                  "title": "ReAct: Synergizing Reasoning and Acting in Language Models",
                  "slide_page": "Slide 20",
                  "excerpt": "ReAct kết hợp suy luận chuỗi tư duy (Reasoning trace) với hành động cụ thể (Action execution):\n1. Thought: LLM phân tích hiện trạng và lên kế hoạch.\n2. Action: LLM xuất lệnh gọi Tool cụ thể kèm tham số.\n3. Observation: Môi trường trả về kết quả thực thi.\n4. Loop: LLM đọc kết quả và tiếp tục suy nghĩ.",
                  "key_takeaway": "Vòng lặp ReAct giúp LLM có khả năng tự sửa sai và tương tác với thế giới ngoài.",
                  "ai_tutor_explanation": "ReAct giống kỹ sư debug: Bạn nghĩ lỗi ở đâu (Thought), đặt print log (Action), đọc log (Observation), và sửa code.",
                  "code_snippet": "while steps < max_steps:\n    thought = agent.reason(context)\n    action = agent.decide_action(thought)\n    if action.is_finish:\n        return action.answer\n    obs = execute_tool(action.tool_name, action.params)\n    context.append((thought, action, obs))",
                  "quick_quiz": "Thành phần nào trong ReAct đại diện cho dữ liệu môi trường trả về sau khi gọi Tool?\nA. Thought\nB. Action\nC. Observation\n(Đáp án đúng: C)"
                }
              },
              {
                "id": "d3_debug_checklist",
                "title": "Debug Checklist Cho Agent",
                "summary": "Checklist gỡ lỗi: Xem trace trước, kiểm tra tool payload, giới hạn số vòng lặp.",
                "slide_page": "Slide 35",
                "type": "concept",
                "cross_link": None,
                "detail": {
                  "title": "Checklist Kỹ Thuật Khi Debug Hệ Thống Agent",
                  "slide_page": "Slide 35",
                  "excerpt": "● Nhìn vào trace log trước: xem Thought có hợp lý không trước khi trách Tool.\n● Kiểm tra schema input của Tool: LLM có truyền sai kiểu dữ liệu không?\n● Thiết lập `max_iterations`: luôn giới hạn số bước lặp.\n● Quan sát Observation: kết quả trả về có bị tràn context window không?",
                  "key_takeaway": "Trace log và giới hạn vòng lặp là phao cứu sinh bắt buộc trong mọi hệ thống Agent.",
                  "ai_tutor_explanation": "Nếu không đặt max_iterations, khi Tool lỗi mạng, Agent có thể retry hàng chục lần liên tục làm cháy sạch quota 15 RPM.",
                  "code_snippet": "MAX_ITERATIONS = 5\nif iteration_count >= MAX_ITERATIONS:\n    return 'Fallback: Quá số lần thử cho phép.'",
                  "quick_quiz": "Để ngăn chặn Agent gọi tool vô tận khi gặp lỗi, biện pháp bắt buộc là gì?\nA. Tăng context window lên 2M token\nB. Thiết lập tham số max_iterations giới hạn số bước\nC. Đổi model khác\n(Đáp án đúng: B)"
                }
              }
            ]
          }
        ]
      }
    ]
  }
}

# ==============================================================================
# 4. DỮ LIỆU DAY 04
# ==============================================================================
DAY_4_DATA = {
  "day": 4,
  "code": "DAY_04",
  "title": "Prompt Engineering & Tool Calling",
  "subtitle": "Kỹ Thuật RTCF & Structured Output",
  "pdf_file": "day04-prompt-engineering-tool-calling_v3.pdf",
  "total_slides": 98,
  "tree": {
    "id": "d4_root",
    "title": "Day 04: Prompt & Tools",
    "summary": "Khung viết prompt RTCF, Context Engineering, Tool Calling và phòng thủ lỗ hổng.",
    "slide_page": "Slide 1-6",
    "type": "root",
    "children": [
      {
        "id": "d4_c1_fundamentals",
        "title": "Prompt Engineering Cơ Bản",
        "summary": "Khung RTCF 4 thành phần, quy trình tinh chỉnh và quản lý token budget.",
        "slide_page": "Slide 6-17",
        "type": "branch",
        "children": [
          {
            "id": "d4_c1_rtcf",
            "title": "Khung Kỹ Thuật RTCF",
            "summary": "Role (Vai trò), Task (Nhiệm vụ), Context (Bối cảnh), Format (Định dạng).",
            "slide_page": "Slide 10-12",
            "type": "branch",
            "children": [
              {
                "id": "d4_rtcf_framework",
                "title": "4 Thành Phần RTCF",
                "summary": "Khung viết prompt chuẩn công nghiệp giúp kiểm soát hành vi mô hình.",
                "slide_page": "Slide 10",
                "type": "concept",
                "cross_link": {
                  "target_day": 5,
                  "target_node_id": "d5_prd_8_parts",
                  "label": "🔗 Chuẩn hoá format PRD trong Day 05 [Slide 25]"
                },
                "detail": {
                  "title": "Khung Viết Prompt Thực Chiến RTCF",
                  "slide_page": "Slide 10",
                  "excerpt": "● ROLE: Đóng vai trò Chuyên gia Tóm tắt Bài giảng.\n● TASK: Trích xuất cây sơ đồ tư duy từ nội dung slide.\n● CONTEXT: Dành cho sinh viên ôn tập nhanh trước kỳ thi.\n● FORMAT: Xuất ra JSON có các trường: title (2-5 từ), summary (<= 40 từ), slide_page.\nRule of thumb: Bắt đầu với Task + Format. Thêm Role và Context khi cần cải thiện độ chính xác.",
                  "key_takeaway": "Task và Format là hai yếu tố quyết định 80% chất lượng của prompt kỹ thuật.",
                  "ai_tutor_explanation": "Trong bài toán tạo Mindmap này, Format là cốt lõi: chỉ thị rõ ràng summary <= 40 từ và output JSON để không làm vỡ layout giao diện.",
                  "code_snippet": "prompt = '''\n[ROLE]: AI Study Assistant\n[TASK]: Tóm tắt khái niệm chính của slide\n[CONTEXT]: Khóa học VLearn AI Hackathon\n[FORMAT]: JSON object { \"title\": str, \"summary\": str }\n'''",
                  "quick_quiz": "Theo nguyên tắc Rule of thumb, hai thành phần nào nên bắt đầu viết đầu tiên trong RTCF?\nA. Role và Context\nB. Task và Format\nC. Role và Format\n(Đáp án đúng: B)"
                },
                "children": [
                  {
                    "id": "d4_prompt_iteration",
                    "title": "Quy Trình Tinh Chỉnh Prompt",
                    "summary": "Các bước nâng cấp prompt từ bản nháp v1 đến bản hoàn chỉnh v3.",
                    "slide_page": "Slide 12",
                    "type": "detail",
                    "cross_link": None,
                    "detail": {
                      "title": "Prompt Iteration: v1 Mơ Hồ Đến v3 Xuất Sắc",
                      "slide_page": "Slide 12",
                      "excerpt": "■ v1: Mơ hồ ('Tóm tắt bài này').\n■ v2: Có cấu trúc ('Tóm tắt slide thành 3 ý chính').\n■ v3: Có ràng buộc và ví dụ mẫu ('Trích xuất JSON gồm title <= 5 từ, summary <= 40 từ kèm slide_page').",
                      "key_takeaway": "Chuyển từ chỉ dẫn định tính sang chỉ dẫn định lượng cụ thể kèm schema.",
                      "ai_tutor_explanation": "Khi gặp output không như ý, đừng vội đổi model mà hãy bổ sung ràng buộc số từ và schema mẫu vào prompt.",
                      "code_snippet": None,
                      "quick_quiz": "Cách viết nào hiệu quả nhất để kiểm soát độ dài câu trả lời của AI?\nA. 'Xin đừng viết dài quá nhé'\nB. 'Tóm tắt nội dung chính trong tối đa 40 từ'\nC. 'Hãy trả lời thật ngắn gọn'\n(Đáp án đúng: B)"
                    }
                  }
                ]
              }
            ]
          },
          {
            "id": "d4_c1_optimization",
            "title": "Tối Ưu Token & Ranh Giới",
            "summary": "Token budget awareness, temperature sampling và negative prompting.",
            "slide_page": "Slide 14-16",
            "type": "branch",
            "children": [
              {
                "id": "d4_iteration_rules",
                "title": "Token Budget Awareness",
                "summary": "Mỗi từ trong prompt và response đều tiêu tốn chi phí và tăng độ trễ.",
                "slide_page": "Slide 15",
                "type": "concept",
                "cross_link": None,
                "detail": {
                  "title": "Ý Thức Về Ngân Sách Token (Token Budget Awareness)",
                  "slide_page": "Slide 15",
                  "excerpt": "■ Prompt dài hơn KHÔNG đồng nghĩa prompt tốt hơn.\n■ Tránh phủ định mập mờ, thay bằng chỉ thị tích cực cụ thể.\n■ Token Budget Awareness: Mỗi từ trong prompt và response đều tiêu tốn chi phí và tăng latency.",
                  "key_takeaway": "Tối ưu hoá mật độ thông tin trên mỗi token là thước đo của AI Engineer chuyên nghiệp.",
                  "ai_tutor_explanation": "Khi làm việc với free tier 15 RPM, cắt giảm 50% độ dài prompt thừa giúp tránh lỗi RateLimit và tăng gấp đôi tốc độ sinh phản hồi.",
                  "code_snippet": None,
                  "quick_quiz": "Khi muốn AI sinh câu trả lời ổn định và bám sát tài liệu nhất, nên đặt temperature khoảng bao nhiêu?\nA. 0.1 - 0.2\nB. 0.9 - 1.0\nC. 2.0\n(Đáp án đúng: A)"
                }
              }
            ]
          }
        ]
      },
      {
        "id": "d4_c2_advanced_prompts",
        "title": "Kỹ Thuật Nâng Cao & Context",
        "summary": "Few-shot prompting, cập nhật CoT 2026, Context Engineering và phòng thủ EchoLeak.",
        "slide_page": "Slide 18-56",
        "type": "branch",
        "children": [
          {
            "id": "d4_c2_context_safety",
            "title": "Context Engineering & An Toàn",
            "summary": "Cắt bỏ history thừa, đặt ranh giới dữ liệu và phòng thủ prompt injection.",
            "slide_page": "Slide 50-56",
            "type": "branch",
            "children": [
              {
                "id": "d4_context_engineering",
                "title": "Context Engineering",
                "summary": "Chỉ đưa vào context cần thiết, cắt giảm history thừa và đặt ranh giới an toàn.",
                "slide_page": "Slide 50",
                "type": "concept",
                "cross_link": {
                  "target_day": 5,
                  "target_node_id": "d5_responsible_ai",
                  "label": "🔗 Trụ cột Bảo mật Day 05 [Slide 12]"
                },
                "detail": {
                  "title": "Context Engineering: Chọn Đúng Context Cần Thiết",
                  "slide_page": "Slide 50",
                  "excerpt": "Checklist Context Engineering:\n□ Đã cắt bỏ history không liên quan đến task hiện tại?\n□ Đã nén và tóm tắt các đoạn hội thoại dài trước khi gửi lại model?\n□ Đặt ranh giới rõ ràng giữa dữ liệu người dùng và chỉ thị hệ thống.",
                  "key_takeaway": "Context ngắn gọn và chuẩn xác giúp giảm độ trễ, tiết kiệm chi phí và tăng độ tập trung của LLM.",
                  "ai_tutor_explanation": "Thay vì nhét toàn bộ 100 trang slide vào prompt mỗi lần hỏi, pipeline chỉ trích xuất phần tóm tắt mục lục và các đoạn tương ứng.",
                  "code_snippet": None,
                  "quick_quiz": "Lợi ích lớn nhất của việc cắt bỏ lịch sử chat không liên quan là gì?\nA. Giúp giao diện đẹp hơn\nB. Tiết kiệm token, giảm độ trễ và tránh làm loãng ngữ cảnh\nC. Làm tăng RAM máy chủ\n(Đáp án đúng: B)"
                },
                "children": [
                  {
                    "id": "d4_echoleak_cve",
                    "title": "Phòng Thủ EchoLeak CVE-2025",
                    "summary": "Lỗ hổng rò rỉ dữ liệu qua prompt injection gián tiếp và cách phòng ngừa.",
                    "slide_page": "Slide 54-56",
                    "type": "detail",
                    "cross_link": None,
                    "detail": {
                      "title": "Ca Thật: EchoLeak (CVE-2025-32711) & Biện Pháp Phòng Thủ",
                      "slide_page": "Slide 54",
                      "excerpt": "Microsoft 365 Copilot dính lỗ hổng prompt injection gián tiếp qua tài liệu tải lên. Kẻ tấn công nhúng chỉ thị độc hại vào văn bản để trích xuất dữ liệu nhạy cảm ra ngoài.",
                      "key_takeaway": "Luôn cách ly dữ liệu đầu vào không tin cậy bằng delimiter rõ ràng (xml tags, brackets).",
                      "ai_tutor_explanation": "Chúng ta bọc slide bằng [DỮ LIỆU SLIDE CẦN XỬ LÝ] để mô hình phân biệt rạch ròi giữa câu lệnh hệ thống và nội dung bài học.",
                      "code_snippet": "# Phân định an toàn:\n[INSTRUCTIONS]: Xử lý dữ liệu\n<user_input>{untrusted_content}</user_input>",
                      "quick_quiz": "Biện pháp nào giúp giảm thiểu rủi ro Prompt Injection từ file tài liệu tải lên?\nA. Đổi tên file sang tiếng Anh\nB. Phân định rõ ranh giới ngữ cảnh bằng thẻ đóng mở và chỉ thị hệ thống nghiêm ngặt\nC. Không cho người dùng đọc tài liệu\n(Đáp án đúng: B)"
                    }
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        "id": "d4_c3_tool_calling",
        "title": "Tool Calling & Structured Output",
        "summary": "Cơ chế LLM kích hoạt các hàm Python bên ngoài thông qua JSON Schema.",
        "slide_page": "Slide 62-85",
        "type": "branch",
        "children": [
          {
            "id": "d4_c3_flow",
            "title": "Cơ Chế Gọi Tool",
            "summary": "Mô hình sinh lời gọi hàm có cấu trúc thay vì trả lời text tự do.",
            "slide_page": "Slide 42, 85",
            "type": "branch",
            "children": [
              {
                "id": "d4_tool_calling",
                "title": "Cơ Chế Tool Calling",
                "summary": "Phân tách suy luận của LLM và quyền thực thi code của client.",
                "slide_page": "Slide 42, 85",
                "type": "concept",
                "cross_link": {
                  "target_day": 3,
                  "target_node_id": "d3_react_loop",
                  "label": "🔗 Thực thi Action trong vòng lặp ReAct Day 03 [Slide 20]"
                },
                "detail": {
                  "title": "Tool Calling: Biến LLM Thành Hệ Thống Hành Động",
                  "slide_page": "Slide 85",
                  "excerpt": "Tool Calling cho phép mô hình ngôn ngữ sinh ra JSON chỉ định tên hàm và các đối số. Ứng dụng client sẽ chạy hàm thực tế rồi trả kết quả (Observation) về cho LLM.",
                  "key_takeaway": "Tool calling phân tách an toàn giữa khả năng suy luận của LLM và quyền thực thi code.",
                  "ai_tutor_explanation": "Ví dụ cung cấp tool get_slide_content(day, page). LLM xuất {'name': 'get_slide_content', 'args': {'day': 1, 'page': 9}}. Code Python chạy hàm và trả text về.",
                  "code_snippet": "def search_slide(keyword: str) -> str:\n    '''Tìm kiếm slide chứa từ khoá'''\n    pass\n\ntools = [search_slide]\nres = client.models.generate_content(\n    model='gemini-2.5-flash',\n    contents='Tìm slide cài Git',\n    config={'tools': tools}\n)",
                  "quick_quiz": "Khi LLM kích hoạt một Tool Call, ai là người trực tiếp chạy hàm code đó?\nA. Chính máy chủ của Google/OpenAI\nB. Ứng dụng phía Client / Server của bạn\nC. Trình duyệt web của người dùng\n(Đáp án đúng: B)"
                }
              }
            ]
          },
          {
            "id": "d4_c3_structured",
            "title": "Structured Output",
            "summary": "Ép LLM trả về đúng JSON Schema bằng Pydantic hoặc Response Schema.",
            "slide_page": "Slide 69",
            "type": "branch",
            "children": [
              {
                "id": "d4_structured_output",
                "title": "Structured Output",
                "summary": "Loại bỏ hoàn toàn lỗi JSONDecodeError trong các pipeline sản phẩm.",
                "slide_page": "Slide 69",
                "type": "concept",
                "cross_link": None,
                "detail": {
                  "title": "Structured Output: Đảm Bảo 100% Khớp Schema",
                  "slide_page": "Slide 69",
                  "excerpt": "Cảnh báo kỹ thuật: Không nên dùng regex hoặc ép format bằng prompt tự do. Các model hiện đại hỗ trợ Structured Outputs với Pydantic model hoặc JSON Schema, đảm bảo JSON trả về không bao giờ bị gãy cú pháp.",
                  "key_takeaway": "Structured Output loại bỏ hoàn toàn lỗi JSONDecodeError trong các pipeline sản phẩm thực tế.",
                  "ai_tutor_explanation": "Trong pipeline tạo Mindmap của chúng ta, Pydantic class ConceptNodeSchema được truyền trực tiếp vào tham số response_schema để Gemini ép output khớp 100% với D3.js.",
                  "code_snippet": "from pydantic import BaseModel\n\nclass ConceptNode(BaseModel):\n    title: str\n    summary: str\n    slide_page: str\n\n# config={'response_mime_type': 'application/json', 'response_schema': ConceptNode}",
                  "quick_quiz": "Phương pháp nào đáng tin cậy nhất để đảm bảo LLM trả về đúng cấu trúc dữ liệu cho Frontend?\nA. Viết prompt van xin 'làm ơn chỉ trả JSON'\nB. Dùng tính năng Structured Output với JSON Schema / Pydantic\nC. Dùng hàm eval() của Python\n(Đáp án đúng: B)"
                }
              }
            ]
          }
        ]
      }
    ]
  }
}

# ==============================================================================
# 5. DỮ LIỆU DAY 05
# ==============================================================================
DAY_5_DATA = {
  "day": 5,
  "code": "DAY_05",
  "title": "AI Product Thinking & Requirements",
  "subtitle": "Product Thinking, Responsible AI & PRD",
  "pdf_file": "day05-ai-product-thinking-requirements.pdf",
  "total_slides": 44,
  "tree": {
    "id": "d5_root",
    "title": "Day 05: AI Product PRD",
    "summary": "Tư duy sản phẩm AI, Responsible AI, 8 phần PRD chuẩn và Risk Matrix.",
    "slide_page": "Slide 1-6",
    "type": "root",
    "children": [
      {
        "id": "d5_c1_product_thinking",
        "title": "Tư Duy Sản Phẩm AI",
        "summary": "Khác biệt bản chất giữa AI Product (xác suất) và Software thông thường.",
        "slide_page": "Slide 6-11",
        "type": "branch",
        "children": [
          {
            "id": "d5_c1_ai_vs_sw",
            "title": "Bản Chất AI Product",
            "summary": "Output xác suất có biến thiên, yêu cầu threshold chất lượng, SLA và fallback.",
            "slide_page": "Slide 8",
            "type": "branch",
            "children": [
              {
                "id": "d5_ai_vs_software",
                "title": "AI Product vs Software",
                "summary": "So sánh phần mềm deterministic và sản phẩm AI xác suất.",
                "slide_page": "Slide 8",
                "type": "concept",
                "cross_link": {
                  "target_day": 2,
                  "target_node_id": "d2_4_core_questions",
                  "label": "🔗 Đối chiếu bài toán cần AI Day 02 [Slide 3]"
                },
                "detail": {
                  "title": "AI Product Khác Gì Phần Mềm Truyền Thống?",
                  "slide_page": "Slide 8",
                  "excerpt": "So sánh cốt lõi:\n● Output: Phần mềm truyền thống deterministic (100% giống nhau), AI Product có tính xác suất và biến thiên.\n● Kỳ vọng User: Dễ thất vọng nếu không có Mental Model rõ ràng.\n● Definition of Done: Cần threshold chất lượng, SLA và luồng Fallback khi AI trả lời sai.\n● Vòng đời: Build -> test -> observe -> calibrate -> re-ship.",
                  "key_takeaway": "Đừng viết requirement cho AI như một form CRUD thông thường. Phải thiết kế vùng dung sai lỗi.",
                  "ai_tutor_explanation": "Vì AI có tính xác suất, chúng ta thiết kế nút '⚡ Test CLARIFY' và '⚠️ Test LỖI' trong prototype để hệ thống luôn có phương án dự phòng thân thiện.",
                  "code_snippet": None,
                  "quick_quiz": "Khái niệm nào là BẮT BUỘC khi định nghĩa tiêu chí hoàn thành (DoD) cho tính năng AI?\nA. Phải đúng 100% không bao giờ sai sót\nB. Ngưỡng chất lượng chấp nhận được (Threshold) kèm cơ chế Fallback\nC. Viết code bằng C++\n(Đáp án đúng: B)"
                },
                "children": [
                  {
                    "id": "d5_threshold_fallback",
                    "title": "Chỉ Số Threshold & Fallback SLA",
                    "summary": "Thiết lập ngưỡng tin cậy >= 90% và SLA xử lý khi AI trả lời sai.",
                    "slide_page": "Slide 8",
                    "type": "detail",
                    "cross_link": None,
                    "detail": {
                      "title": "Định Nghĩa Threshold & Fallback SLA",
                      "slide_page": "Slide 8",
                      "excerpt": "Định nghĩa rõ: Nếu độ chính xác dưới 90% hoặc thời gian phản hồi > 5s, hệ thống phải tự động kích hoạt cache hoặc thông báo bảo trì êm ái.",
                      "key_takeaway": "SLA và fallback là chốt chặn đảm bảo trải nghiệm người dùng không bị đứt gãy.",
                      "ai_tutor_explanation": "Sản phẩm AI thương mại luôn có SLA: 95% request dưới 3 giây, độ chính xác RAG trên 88%.",
                      "code_snippet": None,
                      "quick_quiz": "Mục đích của việc đặt threshold chất lượng là gì?\nA. Để đuổi bớt người dùng\nB. Để quyết định khi nào cho phép AI đưa ra câu trả lời trực tiếp\nC. Để tăng số lượng quảng cáo\n(Đáp án đúng: B)"
                    }
                  }
                ]
              }
            ]
          },
          {
            "id": "d5_c1_metrics",
            "title": "Mục Tiêu & Chỉ Số Giá Trị",
            "summary": "Jobs-to-be-Done và chỉ số North Star Metric đo lường giá trị thực tế của AI.",
            "slide_page": "Slide 9-11",
            "type": "branch",
            "children": [
              {
                "id": "d5_success_metrics",
                "title": "North Star & JTBD",
                "summary": "Người dùng không muốn dùng AI, họ muốn hoàn thành công việc nhanh hơn.",
                "slide_page": "Slide 9-11",
                "type": "concept",
                "cross_link": {
                  "target_day": 2,
                  "target_node_id": "d2_freq_impact_matrix",
                  "label": "🔗 Tác động đo lường từ Ma trận Day 02 [Slide 54]"
                },
                "detail": {
                  "title": "Jobs-to-be-Done (JTBD) và North Star Metric Cho AI Product",
                  "slide_page": "Slide 9-11",
                  "excerpt": "■ JTBD: Người dùng không muốn 'dùng AI', họ muốn hoàn thành việc nhanh hơn và bớt áp lực hơn.\n■ North Star Metric ví dụ: 'Tỷ lệ học viên tự tìm thấy câu trả lời trong slide dưới 60 giây mà không cần tag hỏi Trợ giảng'.\n■ Cảnh báo: Tránh dùng các metric ảo như 'Số lượng token đã tiêu thụ'.",
                  "key_takeaway": "Đo lường thành công của AI bằng thời gian tiết kiệm được và giá trị tạo ra cho người dùng.",
                  "ai_tutor_explanation": "Một sản phẩm AI tốt là sản phẩm giúp người dùng đạt mục đích học tập nhanh nhất, chứ không phải giữ chân người dùng chat lòng vòng.",
                  "code_snippet": None,
                  "quick_quiz": "Chỉ số nào sau đây phản ánh đúng giá trị thực tế của công cụ AI hỗ trợ học tập?\nA. Tổng số token API đã tiêu thụ\nB. Thời gian trung bình học viên nắm bắt được khái niệm cốt lõi\nC. Số lượng từ AI đã viết ra\n(Đáp án đúng: B)"
                }
              }
            ]
          }
        ]
      },
      {
        "id": "d5_c2_responsible_ai",
        "title": "Responsible AI & Đạo Đức",
        "summary": "5 trụ cột Responsible AI, giảm thiểu Bias, bảo vệ Privacy và tuân thủ EU AI Act.",
        "slide_page": "Slide 12-19",
        "type": "branch",
        "children": [
          {
            "id": "d5_c2_pillars",
            "title": "5 Trụ Cột Đạo Đức AI",
            "summary": "Công bằng, Minh bạch, Bảo mật dữ liệu, An toàn và Trách nhiệm giải trình.",
            "slide_page": "Slide 12-15",
            "type": "branch",
            "children": [
              {
                "id": "d5_responsible_ai",
                "title": "5 Trụ Cột Responsible AI",
                "summary": "Khung chuẩn mực bắt buộc cho mọi giải pháp AI đưa vào thực tế.",
                "slide_page": "Slide 13",
                "type": "concept",
                "cross_link": {
                  "target_day": 2,
                  "target_node_id": "d2_pair_6_chapters",
                  "label": "🔗 Triển khai từ Google PAIR Day 02 [Slide 8]"
                },
                "detail": {
                  "title": "5 Trụ Cột Cốt Lõi Của Responsible AI",
                  "slide_page": "Slide 13",
                  "excerpt": "1. Fairness (Công bằng): Không phân biệt đối xử hoặc thiên lệch bất công.\n2. Transparency (Minh bạch): Người dùng luôn biết nguồn gốc thông tin.\n3. Privacy & Security: Bảo mật dữ liệu cá nhân, không train model trái phép.\n4. Safety: Có rào chắn an toàn (Guardrails) ngăn chặn độc hại.\n5. Accountability: Con người luôn chịu trách nhiệm cuối cùng.",
                  "key_takeaway": "Mọi tính năng AI đưa ra thị trường đều phải có đánh giá rủi ro đạo đức và bảo mật dữ liệu.",
                  "ai_tutor_explanation": "Nguyên tắc minh bạch thể hiện qua huy hiệu trích dẫn [Slide X] trên mỗi node: học viên luôn kiểm chứng được câu trả lời từ trang slide nào.",
                  "code_snippet": None,
                  "quick_quiz": "Hành động nào thể hiện tính Minh bạch (Transparency) trong thiết kế Mindmap AI?\nA. Giấu nguồn dữ liệu\nB. Hiển thị rõ số trang slide trích dẫn [Slide X] để học viên đối chiếu\nC. Đổi tên bài giảng thành tác phẩm của AI\n(Đáp án đúng: B)"
                },
                "children": [
                  {
                    "id": "d5_eu_ai_act_pm",
                    "title": "Góc Nhìn EU AI Act Cho PM",
                    "summary": "Phân cấp rủi ro Không chấp nhận được, Cao, Hạn chế và Tối thiểu.",
                    "slide_page": "Slide 15",
                    "type": "detail",
                    "cross_link": None,
                    "detail": {
                      "title": "Đạo Luật EU AI Act 2024 Dưới Góc Nhìn Sản Phẩm",
                      "slide_page": "Slide 15",
                      "excerpt": "Không cần học thuộc luật, cần hiểu một số use case AI giáo dục hoặc tuyển dụng có thể bị xếp vào nhóm Rủi ro cao (High-risk), đòi hỏi audit dữ liệu và human-in-the-loop.",
                      "key_takeaway": "Nắm vững phân loại rủi ro pháp lý để tránh vi phạm bảo mật dữ liệu người học.",
                      "ai_tutor_explanation": "Sản phẩm giáo dục EdTech cần đảm bảo quyền riêng tư học viên và không tự động chấm điểm xếp loại tiêu cực thiếu minh bạch.",
                      "code_snippet": None,
                      "quick_quiz": "Nhóm ứng dụng nào thường bị EU AI Act xếp vào cấp rủi ro cao?\nA. Game giải trí đơn giản\nB. AI đánh giá năng lực học sinh hoặc sàng lọc hồ sơ tuyển dụng\nC. Bộ lọc thư rác email\n(Đáp án đúng: B)"
                    }
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        "id": "d5_c3_prd_and_risks",
        "title": "Kỹ Thuật Viết PRD & Rủi Ro",
        "summary": "8 phần cốt lõi của một PRD AI chuẩn, Acceptance Criteria và Risk Matrix.",
        "slide_page": "Slide 20-35",
        "type": "branch",
        "children": [
          {
            "id": "d5_c3_prd_spec",
            "title": "Cấu Trúc Bản PRD Chuẩn",
            "summary": "Tài liệu kỹ thuật đồng bộ giữa Product Manager, AI Engineer và Ban giám khảo.",
            "slide_page": "Slide 24-28",
            "type": "branch",
            "children": [
              {
                "id": "d5_prd_8_parts",
                "title": "8 Phần Của AI PRD",
                "summary": "Problem, Target User, Success Metrics, Architecture, Features, NFR, Acceptance, Risks.",
                "slide_page": "Slide 25",
                "type": "concept",
                "cross_link": {
                  "target_day": 2,
                  "target_node_id": "d2_problem_discovery",
                  "label": "🔗 Dữ liệu đầu vào từ Discovery Day 02 [Slide 15]"
                },
                "detail": {
                  "title": "Cấu Trúc Chuẩn 8 Phần Của Một Bản PRD Sản Phẩm AI",
                  "slide_page": "Slide 25",
                  "excerpt": "1. Problem: Bài toán cụ thể và nỗi đau của người dùng.\n2. Target User: Chân dung đối tượng sử dụng.\n3. Success Metrics: Các chỉ số đo lường hiệu quả.\n4. Technical Architecture: Kiến trúc pipeline (LLM, RAG, Cache, Frontend).\n5. Feature Requirements: Yêu cầu chức năng chi tiết.\n6. Non-functional Requirements (NFR): Độ trễ, chi phí token, bảo mật.\n7. Acceptance Criteria: Tiêu chuẩn nghiệm thu từng tính năng.\n8. Risk Matrix: Ma trận rủi ro và phương án ứng phó.",
                  "key_takeaway": "PRD tốt là tài liệu giúp cả team kỹ thuật, sản phẩm và giảng viên cùng chung một tầm nhìn.",
                  "ai_tutor_explanation": "Trong Checkpoint 1 và 2 vừa qua, nhóm BungChay đã xây dựng hoàn chỉnh khung này qua spec.md và canvas-cp1.md.",
                  "code_snippet": None,
                  "quick_quiz": "Phần nào trong PRD giúp xác định khi nào một tính năng AI được coi là đạt yêu cầu để đưa lên production?\nA. Technical Architecture\nB. Acceptance Criteria & Quality Thresholds\nC. Target User\n(Đáp án đúng: B)"
                }
              }
            ]
          },
          {
            "id": "d5_c3_risk_plan",
            "title": "Quản Trị Rủi Ro Vận Hành",
            "summary": "Xác định rủi ro Hallucination, trễ API, chi phí token và kế hoạch giảm thiểu.",
            "slide_page": "Slide 31-35",
            "type": "branch",
            "children": [
              {
                "id": "d5_risk_matrix",
                "title": "Ma Trận Rủi Ro (Risk Matrix)",
                "summary": "Chiến lược ứng phó với rate limit, ảo giác mô hình và nghẽn mạng.",
                "slide_page": "Slide 31",
                "type": "concept",
                "cross_link": None,
                "detail": {
                  "title": "Risk Matrix: Nhận Diện & Giảm Thiểu Rủi Ro Vận Hành AI",
                  "slide_page": "Slide 31",
                  "excerpt": "■ Rủi ro 1: Vượt hạn ngạch API (Rate Limit 15 RPM) -> Giải pháp: Caching cục bộ và giới hạn gọi batch 1 lần.\n■ Rủi ro 2: AI ảo giác (Hallucination) -> Giải pháp: Ép output kèm trích dẫn số trang slide cụ thể.\n■ Rủi ro 3: Trễ mạng khi tải -> Giải pháp: Render giao diện tức thì với local storage trước khi sync.",
                  "key_takeaway": "Không có hệ thống AI nào hoàn hảo, chỉ có hệ thống chuẩn bị sẵn kế hoạch ứng phó rủi ro tốt.",
                  "ai_tutor_explanation": "Bằng việc nạp sẵn dữ liệu trích xuất vào codebase/storage/, chúng ta triệt tiêu hoàn toàn rủi ro bị khóa API trong buổi demo trực tiếp trước ban giám khảo!",
                  "code_snippet": None,
                  "quick_quiz": "Giải pháp hiệu quả nhất để giải quyết rủi ro giới hạn 15 RPM trong buổi demo là gì?\nA. Mua thêm 100 tài khoản trả phí\nB. Áp dụng Local Caching thông minh và nạp dữ liệu trích xuất sẵn\nC. Huỷ bỏ bài thuyết trình\n(Đáp án đúng: B)"
                }
              }
            ]
          }
        ]
      }
    ]
  }
}

# ==============================================================================
# METADATA TOÀN BỘ KHÓA HỌC
# ==============================================================================
METADATA = {
  "course_title": "AI Product & Agentic Engineering (AICB-P1)",
  "institution": "VinUni / VLearn Platform",
  "team": "BungChay (Batch 04 - Track A)",
  "days": [
    {
      "day": 1,
      "code": "DAY_01",
      "title": "AI & LLM Foundation",
      "subtitle": "Setup & API Exploration",
      "pdf_file": "day01_c401.pdf",
      "total_slides": 32,
      "core_topics": [
        "Transformer & Attention",
        "LLM API Providers",
        "Local & Global Checklist",
        "Git Classroom Flow",
        "Codelab Architecture"
      ],
      "storage_file": "day_1.json"
    },
    {
      "day": 2,
      "code": "DAY_02",
      "title": "Xác Định Bài Toán Cho AI",
      "subtitle": "Khung Lý Thuyết + Google PAIR",
      "pdf_file": "day02.pdf",
      "total_slides": 76,
      "core_topics": [
        "4 Câu Hỏi Trọng Tâm",
        "Rule vs Workflow vs Agent",
        "Google PAIR Guidebook",
        "Problem Discovery",
        "Ma Trận Tần Suất & Tác Động"
      ],
      "storage_file": "day_2.json"
    },
    {
      "day": 3,
      "code": "DAY_03",
      "title": "Từ Chatbot Đến Agentic Agent",
      "subtitle": "Phổ Hệ Thống + ReAct Pattern",
      "pdf_file": "day03-tu-chatbot-den-agentic-agent-react (1).pdf",
      "total_slides": 46,
      "core_topics": [
        "Phổ 3 Hệ Thống AI",
        "Chatbot Baseline",
        "4 Tiêu Chí Agentic Fit",
        "Anti-Patterns",
        "Vòng Lặp ReAct",
        "Debug Checklist"
      ],
      "storage_file": "day_3.json"
    },
    {
      "day": 4,
      "code": "DAY_04",
      "title": "Prompt Engineering & Tool Calling",
      "subtitle": "Kỹ Thuật RTCF & Structured Output",
      "pdf_file": "day04-prompt-engineering-tool-calling_v3.pdf",
      "total_slides": 98,
      "core_topics": [
        "4 Thành Phần RTCF",
        "Prompt Iteration",
        "Context Engineering",
        "EchoLeak CVE-2025-32711",
        "Tool Calling Flow",
        "Structured Output Schema"
      ],
      "storage_file": "day_4.json"
    },
    {
      "day": 5,
      "code": "DAY_05",
      "title": "AI Product Thinking & Requirements",
      "subtitle": "Product Thinking, Responsible AI & PRD",
      "pdf_file": "day05-ai-product-thinking-requirements.pdf",
      "total_slides": 44,
      "core_topics": [
        "AI Product vs Software",
        "North Star Metric & JTBD",
        "5 Trụ Cột Responsible AI",
        "EU AI Act 2024",
        "8 Phần PRD Chuẩn",
        "Risk Matrix"
      ],
      "storage_file": "day_5.json"
    }
  ]
}

ALL_DAYS = {
  "1": DAY_1_DATA,
  "2": DAY_2_DATA,
  "3": DAY_3_DATA,
  "4": DAY_4_DATA,
  "5": DAY_5_DATA
}

def sync_all():
    print("[SYNC] Đang ghi dữ liệu vào codebase/storage/...")
    for day_num, data in ALL_DAYS.items():
        out_path = STORAGE_DIR / f"day_{day_num}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  -> Đã cập nhật: {out_path.name}")

    meta_path = STORAGE_DIR / "metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(METADATA, f, ensure_ascii=False, indent=2)
    print(f"  -> Đã cập nhật: {meta_path.name}")

    # Cập nhật seed_data.py
    seed_path = BASE_DIR / "backend" / "seed_data.py"
    seed_content = f'''"""
Seed data tự động khởi tạo mặc định cho kho lưu trữ Mindmap
Giúp đồng đội khi clone repo về máy lần đầu không bị thiếu file/thư mục.
Cập nhật: Dữ liệu phân cấp đa tầng sâu (3-5 cấp), bao quát trọn vẹn toàn bộ slide các ngày.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"

SEED_DAYS_JSON = {repr(json.dumps(ALL_DAYS, ensure_ascii=False))}
SEED_META_JSON = {repr(json.dumps(METADATA, ensure_ascii=False))}

def init_default_storage():
    """Tự động tạo thư mục và nạp 5 bài học mẫu nếu kho lưu trữ chưa tồn tại."""
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    meta_file = STORAGE_DIR / "metadata.json"
    if meta_file.exists():
        return

    print("[AUTO-INIT] Chưa phát hiện dữ liệu trong codebase/storage/. Đang khởi tạo 5 bài học mặc định...")
    days_data = json.loads(SEED_DAYS_JSON)
    for day_num_str, day_obj in days_data.items():
        day_path = STORAGE_DIR / f"day_{{day_num_str}}.json"
        with open(day_path, "w", encoding="utf-8") as f:
            json.dump(day_obj, f, ensure_ascii=False, indent=2)

    meta_obj = json.loads(SEED_META_JSON)
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(meta_obj, f, ensure_ascii=False, indent=2)

    print(f"[AUTO-INIT SUCCESS] Đã tự động tạo xong 5 bài giảng đa tầng trong {{STORAGE_DIR}}!")
'''
    with open(seed_path, "w", encoding="utf-8") as f:
        f.write(seed_content)
    print(f"  -> Đã cập nhật: {seed_path.name}")

    # Cập nhật KNOWLEDGE_BASE trong index.html
    index_path = BASE_DIR / "index.html"
    with open(index_path, "r", encoding="utf-8") as f:
        index_html = f.read()

    full_kb = {
        "metadata": METADATA,
        "days": ALL_DAYS
    }
    kb_json_str = json.dumps(full_kb, ensure_ascii=False)
    # Thay thế biến KNOWLEDGE_BASE trong index.html an toàn (dùng lambda để tránh re.sub tự ý unescape ký tự \n)
    pattern = r'const KNOWLEDGE_BASE = \{.*?\};'
    new_index_html, count = re.subn(pattern, lambda _: f'const KNOWLEDGE_BASE = {kb_json_str};', index_html, flags=re.DOTALL)
    if count > 0:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(new_index_html)
        print(f"  -> Đã cập nhật KNOWLEDGE_BASE nhúng sẵn trong: {index_path.name}")
    else:
        print(f"  [WARNING] Không tìm thấy pattern KNOWLEDGE_BASE trong {index_path.name}")

    print("[HOÀN TẤT] Tất cả dữ liệu 5 ngày đã được đồng bộ chuẩn đa tầng sâu (3-5 cấp), 0 token tiêu thụ!")

if __name__ == "__main__":
    sync_all()
