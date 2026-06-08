import os
from dotenv import load_dotenv
from walledeval.llms import OpenAILLM # Giả sử bạn dùng OpenAI theo mẫu của thư viện
from walledeval.judges import OpenAILLMJudge

# 1. Tự động tìm và nạp các biến trong file .env vào hệ thống
load_dotenv() 

# 2. Lúc này hệ thống đã có KEY, bạn gọi ra kiểm tra thử (Tùy chọn)
if not os.getenv("OPENAI_API_KEY"):
    print("❌ Lỗi: Chưa tìm thấy API Key trong file .env rồi!")
else:
    print("✅ Đã nạp API Key thành công. Sẵn sàng test!")

# 3. Đoạn code mẫu từ GitHub WalledEval của bạn sẽ tiếp tục ở đây...
# Ví dụ:
# llm = OpenAILLM(model_name="gpt-3.5-turbo")
# judge = OpenAILLMJudge(model_name="gpt-4")
# ... tiếp tục các bước test jailbreak ...