import os
from openai import OpenAI
from pyfirmata import Arduino, util
import time
import json

# Khởi tạo OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Kết nối Arduino
board = Arduino('/dev/ttyACM0')
led_pin = 13

print("🤖 AI Chatbot điều khiển đèn Arduino đã sẵn sàng!")
print("Ví dụ: 'bật đèn', 'tắt đèn', 'tối quá', 'sáng quá'\n")

# Định nghĩa functions cho OpenAI
functions = [
    {
        "name": "control_led",
        "description": "Điều khiển đèn LED bật hoặc tắt. Gọi hàm này khi người dùng muốn bật/tắt đèn hoặc phàn nàn về ánh sáng (tối/sáng)",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["on", "off"],
                    "description": "Hành động: 'on' để bật đèn, 'off' để tắt đèn"
                }
            },
            "required": ["action"]
        }
    }
]

# Hàm điều khiển LED thực tế
def control_led(action):
    if action == "on":
        board.digital[led_pin].write(1)
        return "Đã bật đèn ✅"
    elif action == "off":
        board.digital[led_pin].write(0)
        return "Đã tắt đèn ✅"
    else:
        return "Lệnh không hợp lệ"

# Lịch sử hội thoại
conversation_history = [
    {
        "role": "system",
        "content": """Bạn là trợ lý AI điều khiển đèn thông minh.
        - Khi người dùng nói 'tối quá', 'tối', 'bật đèn', 'mở đèn' -> gọi control_led với action='on'
        - Khi người dùng nói 'sáng quá', 'chói quá', 'tắt đèn', 'tắt giúp tôi' -> gọi control_led với action='off'
        - Trả lời thân thiện bằng tiếng Việt"""
    }
]

try:
    while True:
        # Nhận input từ người dùng
        user_input = input("Bạn: ")

        if user_input.lower() in ['thoát', 'exit', 'quit']:
            print("Tạm biệt! 👋")
            break

        # Thêm tin nhắn người dùng vào lịch sử
        conversation_history.append({
            "role": "user",
            "content": user_input
        })

        # Gọi OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=conversation_history,
            functions=functions,
            function_call="auto"
        )

        message = response.choices[0].message

        # Kiểm tra xem AI có muốn gọi function không
        if message.function_call:
            function_name = message.function_call.name
            function_args = json.loads(message.function_call.arguments)

            # Thực thi function
            if function_name == "control_led":
                result = control_led(function_args["action"])
                print(f"🔧 {result}")

                # Thêm kết quả function vào lịch sử
                conversation_history.append({
                    "role": "function",
                    "name": function_name,
                    "content": result
                })

                # Gọi lại API để AI tạo response cuối cùng
                second_response = client.chat.completions.create(
                    model="gpt-4",
                    messages=conversation_history
                )

                final_message = second_response.choices[0].message.content
                print(f"AI: {final_message}")

                conversation_history.append({
                    "role": "assistant",
                    "content": final_message
                })
        else:
            # AI trả lời bình thường không cần gọi function
            ai_response = message.content
            print(f"AI: {ai_response}")

            conversation_history.append({
                "role": "assistant",
                "content": ai_response
            })

except KeyboardInterrupt:
    print("\n\nĐã dừng chương trình.")
finally:
    board.exit()
