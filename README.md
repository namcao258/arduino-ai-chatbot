# AI Chatbot điều khiển Arduino

Chatbot AI sử dụng OpenAI API để điều khiển đèn LED qua Arduino với kiến trúc module hóa.

## 📁 Cấu trúc dự án

```
Arduino/
├── config.py                  # Cấu hình API key và settings
├── function_definitions.py    # Định nghĩa OpenAI function calling
├── llm_handler.py            # Xử lý OpenAI API
├── arduino_controller.py     # Điều khiển Arduino
├── main.py                   # Entry point chính
├── test_blink.py             # Test blink cơ bản
└── requirements.txt          # Dependencies
```

## 🔧 Vai trò từng file

| File | Chức năng |
|------|-----------|
| **config.py** | Quản lý API key, cổng Arduino, cấu hình hệ thống |
| **function_definitions.py** | Định nghĩa functions cho OpenAI, system prompts |
| **llm_handler.py** | Giao tiếp với OpenAI API, quản lý hội thoại |
| **arduino_controller.py** | Kết nối và điều khiển Arduino qua PyFirmata |
| **main.py** | Kết hợp tất cả modules, chạy chatbot |

## 🚀 Cài đặt

### Bước 1: Upload Firmata lên Arduino
```bash
# Mở Arduino IDE -> File -> Examples -> Firmata -> StandardFirmata
# Chọn Board (Arduino Uno, Mega, ...) và Port
# Click Upload
```

### Bước 2: Cài đặt dependencies Python
```bash
pip install -r requirements.txt
```

### Bước 3: Thiết lập OpenAI API Key
```bash
export OPENAI_API_KEY='sk-your-api-key-here'
```

### Bước 4: Cấu hình (tùy chọn)
Mở [config.py](config.py) và chỉnh sửa:
- `ARDUINO_PORT`: Cổng serial của Arduino
- `LED_PIN`: Chân LED (mặc định 13)
- `OPENAI_MODEL`: Model OpenAI (mặc định gpt-4)

## 🎮 Sử dụng

### Test kết nối Arduino
```bash
python test_blink.py
```

### Chạy AI Chatbot
```bash
python main.py
```

## 💬 Ví dụ chat

```
🤖 AI CHATBOT ĐIỀU KHIỂN ĐÈN ARDUINO
============================================================

Bạn: tối quá
🔧 ✅ Đã bật LED tại pin 13
AI: Để tôi bật đèn cho bạn ngay nhé!

Bạn: sáng rồi, tắt đi
🔧 ✅ Đã tắt LED tại pin 13
AI: Đã tắt đèn cho bạn rồi ạ!

Bạn: không nhìn thấy gì hết
🔧 ✅ Đã bật LED tại pin 13
AI: Tôi vừa bật đèn lên rồi, bây giờ bạn có thấy rõ hơn không?

Bạn: chói mắt quá
🔧 ✅ Đã tắt LED tại pin 13
AI: Xin lỗi bạn! Tôi đã tắt đèn rồi.
```

## 🎯 Tính năng

- ✅ Hiểu ngôn ngữ tự nhiên (tiếng Việt & tiếng Anh)
- ✅ OpenAI Function Calling thông minh
- ✅ Kiến trúc module hóa, dễ mở rộng
- ✅ Quản lý lịch sử hội thoại
- ✅ Context manager tự động ngắt kết nối Arduino
- ✅ Error handling đầy đủ

## 🔌 Kết nối phần cứng

### LED tích hợp
- Arduino Uno: Pin 13 (có sẵn LED onboard)

### LED ngoài
```
Arduino Pin 13 → Điện trở 220Ω → LED (+) → LED (-) → GND
```

## 🛠️ Mở rộng

### Thêm function mới
1. Mở [function_definitions.py](function_definitions.py)
2. Thêm function definition vào list `FUNCTIONS`
3. Mở [arduino_controller.py](arduino_controller.py)
4. Implement method điều khiển
5. Mở [main.py](main.py)
6. Thêm logic xử lý function call

### Ví dụ: Thêm điều khiển servo
```python
# function_definitions.py
{
    "name": "control_servo",
    "description": "Điều khiển góc quay servo motor",
    "parameters": {
        "type": "object",
        "properties": {
            "angle": {"type": "number", "minimum": 0, "maximum": 180}
        }
    }
}
```

## 🐛 Troubleshooting

### Lỗi: Permission denied /dev/ttyACM0
```bash
sudo usermod -a -G dialout $USER
# Logout và login lại
```

### Lỗi: Arduino không kết nối
```bash
# Kiểm tra cổng khả dụng
ls /dev/tty*

# Thử cổng khác trong config.py
ARDUINO_PORT = '/dev/ttyUSB0'  # hoặc COM3 trên Windows
```

### Lỗi: OpenAI API key không hợp lệ
```bash
# Kiểm tra biến môi trường
echo $OPENAI_API_KEY

# Set lại
export OPENAI_API_KEY='sk-...'
```

## 💾 Lưu trữ dữ liệu học

### Tự động lưu
- Mọi hành động và sở thích được **tự động lưu** vào file `memory_data.json`
- Khi khởi động lại, AI sẽ **nhớ tất cả** những gì đã học
- File JSON dễ đọc, có thể chỉnh sửa bằng tay

### Quản lý memory
```bash
# Xem thống kê
Bạn: stats

# Xóa lịch sử chat (GIỮ NGUYÊN memory đã học)
Bạn: reset

# Xóa TOÀN BỘ memory đã học
Bạn: clear
```

### Ví dụ file memory_data.json
```json
{
  "user_preferences": {
    "đọc": {"on": 5, "off": 0},
    "ngủ": {"on": 0, "off": 8},
    "làm việc": {"on": 10, "off": 1}
  },
  "recent_actions": [...],
  "environment_state": {
    "led_status": "off",
    "last_action_time": "2025-10-06T22:30:45.123456",
    "last_action": "off"
  }
}
```

## 📝 Lưu ý

- Arduino phải upload **StandardFirmata** sketch
- OpenAI API **có phí** (khoảng $0.03/1K tokens cho GPT-4)
- Dùng `gpt-3.5-turbo` trong [config.py](config.py) để tiết kiệm chi phí
- Giới hạn lịch sử hội thoại: 20 tin nhắn (có thể thay đổi trong config)
- Memory được lưu tự động, không lo mất dữ liệu khi tắt app

## 📚 Tài liệu tham khảo

- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [PyFirmata Documentation](https://pypi.org/project/pyFirmata/)
- [Arduino Firmata Protocol](https://github.com/firmata/protocol)
