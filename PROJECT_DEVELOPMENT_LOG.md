# 📝 Project Development Log

## Dự án: AI Chatbot điều khiển Arduino với Context Learning

### 🎯 Mục tiêu
Tạo chatbot AI sử dụng OpenAI API để điều khiển đèn LED Arduino thông qua ngôn ngữ tự nhiên, có khả năng học và ghi nhớ sở thích người dùng.

---

## 🏗️ Quá trình phát triển

### Phase 1: Kiến trúc cơ bản
**Yêu cầu:** Tách biệt các module để dễ quản lý

**Kết quả:**
- ✅ `config.py` - Quản lý API key và cấu hình
- ✅ `arduino_controller.py` - Điều khiển Arduino qua PyFirmata
- ✅ `function_definitions.py` - OpenAI function calling definitions
- ✅ `llm_handler.py` - Xử lý OpenAI API
- ✅ `main.py` - Entry point chính

### Phase 2: AI Reasoning nâng cao
**Vấn đề:** Rule-based matching từ khóa bị thiếu trường hợp
**Giải pháp:** Cho phép LLM tự suy luận từ ngữ cảnh

**Cải tiến:**
- Thay đổi function description từ "danh sách từ khóa" → "hãy tự quyết định dựa trên ngữ cảnh"
- Cập nhật system prompt để khuyến khích suy luận
- Thêm nhiều ví dụ phức tạp (đọc sách, ngủ, trời mưa...)

**Kết quả:**
```
"Tôi sắp đọc sách" → AI hiểu: đọc cần sáng → Bật đèn
"Mệt quá, muốn ngủ" → AI hiểu: ngủ cần tối → Tắt đèn
"Trời mưa ảm đạm" → AI hiểu: cần ánh sáng ấm → Bật đèn
```

### Phase 3: Context Learning
**Yêu cầu:** AI học và nhớ sở thích người dùng qua thời gian

**Triển khai:**
- ✅ `context_memory.py` - Module học và ghi nhớ
- ✅ Tích hợp vào `llm_handler.py`
- ✅ Inject context vào system prompt
- ✅ Học sở thích từ hoạt động (đọc → bật, ngủ → tắt)

**Tính năng:**
- Ghi nhận mỗi action với lý do
- Phát hiện hoạt động từ input
- Học pattern: "Khi đọc sách → thường bật đèn"
- Lần sau tự động áp dụng

### Phase 4: Persistent Storage
**Vấn đề:** Dữ liệu học được chỉ lưu trong RAM, tắt app là mất

**Giải pháp:** Lưu vào file JSON

**Triển khai:**
- ✅ `save_to_file()` - Serialize data ra JSON
- ✅ `load_from_file()` - Load data khi khởi động
- ✅ Auto-save sau mỗi action
- ✅ Thêm lệnh `clear` để xóa memory

**File lưu trữ:** `memory_data.json`

### Phase 5: Version Control
**Mục tiêu:** Đưa dự án lên GitHub

**Thực hiện:**
- ✅ `git init`
- ✅ Tạo `.gitignore` (loại trừ `__pycache__`, `memory_data.json`)
- ✅ Initial commit với message chi tiết
- ✅ Push lên GitHub: `namcao258/arduino-ai-chatbot`

---

## 🧠 Kiến trúc hệ thống

```
┌─────────────┐
│   User      │
│  Input      │
└──────┬──────┘
       │
       v
┌─────────────────────────────────┐
│       main.py                   │
│  (Entry point & UI)             │
└──────┬──────────────────┬───────┘
       │                  │
       v                  v
┌──────────────┐    ┌─────────────────┐
│ LLMHandler   │    │ ArduinoController│
│              │    │                  │
│ - OpenAI API │    │ - PyFirmata      │
│ - Context    │    │ - Serial Comm    │
└──────┬───────┘    └─────────────────┘
       │
       v
┌──────────────────────┐
│  ContextMemory       │
│                      │
│  - Learn patterns    │
│  - Save/Load JSON    │
└──────────────────────┘
```

---

## 📊 Cấp độ thông minh

| Cấp độ | Phương pháp | Ví dụ | Trạng thái |
|--------|-------------|-------|-----------|
| Level 1 | Rule-based | "tối" → bật | ❌ Bỏ qua |
| Level 2 | LLM Reasoning | "đọc sách" → bật | ✅ Triển khai |
| Level 3 | Context Learning | Nhớ sở thích → tự động | ✅ Triển khai |

---

## 🔌 Giao tiếp Arduino

**Phương thức:** USB Serial Communication
**Giao thức:** Firmata Protocol
**Tốc độ:** 57600 baud

**Luồng dữ liệu:**
```
Python → PyFirmata → Serial (/dev/ttyACM0) → Arduino
                                                ↓
                                          digitalWrite(13, HIGH)
                                                ↓
                                            LED sáng 💡
```

---

## 💾 Dữ liệu học được

**Lưu trữ:** `memory_data.json`

**Cấu trúc:**
```json
{
  "user_preferences": {
    "đọc": {"on": 5, "off": 0},
    "ngủ": {"on": 0, "off": 8}
  },
  "recent_actions": [...],
  "environment_state": {...}
}
```

**Quản lý:**
- `stats` - Xem thống kê
- `reset` - Xóa chat (giữ memory)
- `clear` - Xóa toàn bộ memory

---

## 🎯 Tính năng nổi bật

### 1. Suy luận thông minh
- Không cần từ khóa cứng
- Hiểu ngữ cảnh, cảm xúc, hoạt động
- Giải thích lý do quyết định

### 2. Context Learning
- Học pattern từ hành vi
- Ghi nhớ sở thích cá nhân
- Áp dụng tự động lần sau

### 3. Persistent Storage
- Auto-save sau mỗi action
- Load tự động khi khởi động
- Không lo mất dữ liệu

### 4. Kiến trúc module
- Tách biệt rõ ràng
- Dễ mở rộng
- Dễ bảo trì

---

## 🚀 Hướng phát triển

### Đã hoàn thành ✅
- [x] Điều khiển LED cơ bản
- [x] OpenAI Function Calling
- [x] AI Reasoning
- [x] Context Learning
- [x] Persistent Storage
- [x] Module hóa kiến trúc
- [x] GitHub repository

### Có thể mở rộng 💡
- [ ] Thêm nhiều thiết bị (Servo, Relay, Sensor...)
- [ ] Voice control (Speech-to-text)
- [ ] Web interface (Flask/FastAPI)
- [ ] MQTT - Remote control
- [ ] Multi-language support
- [ ] Analytics dashboard
- [ ] Mobile app
- [ ] Home automation integration

---

## 📚 Stack công nghệ

- **Language:** Python 3.x
- **AI:** OpenAI GPT-4 API
- **Hardware:** Arduino Uno
- **Protocol:** Firmata
- **Libraries:**
  - `openai` - OpenAI API client
  - `pyfirmata` - Arduino communication
  - `pyserial` - Serial port access

---

## 🎓 Bài học rút ra

1. **LLM Reasoning > Rule-based**
   - Linh hoạt hơn nhiều
   - Bao quát được nhiều trường hợp
   - Tự nhiên hơn cho user

2. **Context là chìa khóa**
   - Inject context vào prompt rất hiệu quả
   - AI có thể học và cải thiện theo thời gian

3. **Module hóa quan trọng**
   - Dễ debug
   - Dễ mở rộng
   - Dễ maintain

4. **Persistent storage cần thiết**
   - User experience tốt hơn
   - Không mất dữ liệu khi restart

---

## 🙏 Ghi chú

Dự án được phát triển với sự hỗ trợ của Claude Code.

**Ngày hoàn thành:** 2025-10-06
**GitHub:** https://github.com/namcao258/arduino-ai-chatbot
