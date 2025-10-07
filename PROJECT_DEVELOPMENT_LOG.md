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

## Phase 6: YouTube Music Integration - Tự động tìm và phát nhạc

**Ngày:** 2025-10-07 (Buổi sáng)

### 🎯 Yêu cầu mới
User muốn hệ thống tự động:
- Tìm kiếm nhạc trên YouTube
- Phát nhạc qua loa/tai nghe máy tính
- Điều khiển bằng giọng nói tự nhiên

### 🔧 Triển khai

#### Bước 1: Thêm YouTube Search Function
**File:** `youtube_player.py`
- Tạo class `YouTubePlayer` để tìm và phát nhạc
- Ban đầu dùng `youtube-search-python` API
- **Vấn đề:** Lỗi `post() got an unexpected keyword argument 'proxies'`
- **Giải pháp:** Đổi sang dùng `yt-dlp` để search và lấy video ID

**Code flow:**
```python
yt-dlp --get-id --get-title 'ytsearch1:query'
→ Lấy video_id
→ Tạo URL: youtube.com/watch?v={video_id}
→ webbrowser.open(url)
→ Nhạc phát qua browser
```

#### Bước 2: Thêm Function Definition
**File:** `function_definitions.py`
- Thêm function `play_youtube_music`
- Parameters: song_name, artist, mood, genre
- AI tự quyết định dựa trên:
  - Tên bài cụ thể → dùng song_name/artist
  - Tâm trạng → dùng mood (buồn, vui, thư giãn...)
  - Thể loại → dùng genre (pop, rock, EDM...)

#### Bước 3: Tích hợp vào Main
**File:** `main.py`
- Import `YouTubePlayer`
- Khởi tạo instance
- Xử lý function call `play_youtube_music`
- Logic phân loại: bài cụ thể vs mood vs genre

#### Bước 4: Xử lý Dependencies
**Vấn đề gặp phải:**

1. **ModuleNotFoundError: youtube-search-python**
   - User đang dùng conda env `AI_Agent`
   - Pip cài vào miniconda nhưng terminal dùng python3 khác
   - **Fix:** Dùng `/home/holab/miniconda3/bin/python3 main.py`

2. **pyfirmata lỗi với Python 3.12**
   - Lỗi: `module 'inspect' has no attribute 'getargspec'`
   - **Fix:** Đổi sang `pyfirmata2`
   - Sau đó đổi lại `pyfirmata` theo yêu cầu user

3. **youtube-search-python API error**
   - Lỗi: `post() got an unexpected keyword argument 'proxies'`
   - **Fix:** Đổi sang dùng `yt-dlp` để search

**Dependencies cuối cùng:**
```
openai>=1.0.0
pyfirmata>=1.1.0
pyserial>=3.5
youtube-search-python>=1.6.6  # Không dùng nữa
yt-dlp  # Dùng thay thế
```

### 🎵 Tính năng Music Control

#### Phân biệt 2 loại điều khiển:

**1. play_youtube_music** - Tìm và mở nhạc MỚI:
```
"Phát bài Lạc Trôi"
"Nghe Sơn Tùng MTP"
"Buồn quá, bật nhạc"
"Nhạc EDM đi"
```

**2. control_music** - Điều khiển nhạc ĐANG PHÁT:
```
"Tạm dừng" → pause
"Tiếp tục" → play
"Dừng hẳn" → stop
"To quá" → volume_down
```

#### Vấn đề phát hiện: Resume sau Stop

**Tình huống:**
```
User: Phát bài cause i love you
→ YouTube mở, phát nhạc ✅

User: Dừng phát
→ Stop/đóng tab ✅

User: Tiếp tục phát nhạc
→ AI gọi control_music(play)
→ Phát NHẦM media player khác ❌
```

**Nguyên nhân:**
- YouTube đã đóng tab khi stop
- `playerctl play` phát media player khác (nếu có)
- Không thể "resume" YouTube đã đóng

**Giải pháp:**
- Cập nhật system prompt: AI hiểu rõ pause vs stop
- "Tiếp tục" sau stop → AI nên HỎI LẠI user muốn phát bài gì
- Chỉ dùng `control_music(play)` khi chắc chắn đang pause

### 📊 Kết quả

#### Tính năng hoàn thành:
- ✅ Tự động tìm kiếm YouTube bằng `yt-dlp`
- ✅ Mở video đầu tiên, phát qua browser
- ✅ Hỗ trợ search theo: tên bài, ca sĩ, mood, genre
- ✅ AI tự suy luận ý định user
- ✅ Phân biệt rõ play mới vs điều khiển đang phát

#### Demo thực tế:
```
Bạn: Bật đèn và phát bài cause i love you của Noo Phước Thịnh
→ LED sáng ✅
→ (Chưa phát nhạc - AI chưa hiểu lần đầu)

Bạn: Bật nhạc đi
→ YouTube mở "Cause I Love You - Noo Phước Thịnh" ✅
→ Nhạc phát qua loa máy tính ✅

Bạn: Tắt nhạc
→ Dừng nhạc ✅

Bạn: Tiếp tục phát nhạc
→ Phát nhầm media khác ❌
→ Sau fix: AI sẽ hỏi lại ✅
```

### 🐛 Issues & Solutions

| Vấn đề | Giải pháp |
|--------|-----------|
| `youtube-search-python` lỗi API | Dùng `yt-dlp` thay thế |
| `pyfirmata` lỗi Python 3.12 | Giữ nguyên pyfirmata, hướng dẫn user |
| Conda env conflict | Dùng full path python |
| Resume sau stop | Cập nhật AI logic, hỏi lại user |
| Không điều khiển YouTube | Hướng dẫn cài `playerctl` hoặc dùng SPACE |

### 🎓 Bài học Phase 6

1. **YouTube API alternatives:**
   - `youtube-search-python`: Đơn giản nhưng dễ lỗi
   - `yt-dlp`: Ổn định, mạnh mẽ, recommended

2. **Browser automation limitations:**
   - Không thể điều khiển tab browser như native app
   - `playerctl` cần cài thêm
   - Fallback: Hướng dẫn user dùng keyboard

3. **AI function calling edge cases:**
   - Cần phân biệt rõ "play mới" vs "resume"
   - System prompt cần chi tiết về context
   - Hỏi lại user khi không chắc chắn

4. **Dependency management:**
   - Conda env vs system python
   - Version compatibility (Python 3.12)
   - Fallback strategies quan trọng

### 💡 Hướng phát triển tiếp theo

**Đã thảo luận nhưng chưa implement:**
- [ ] Download và phát offline (dùng `YouTubeDownloader` class đã viết)
- [ ] Play/pause bằng keyboard automation
- [ ] Queue management (playlist)
- [ ] Lyrics display
- [ ] Music recommendation based on mood history

**Có thể mở rộng:**
- Multiple function calls cùng lúc ("bật đèn VÀ phát nhạc")
- Smart home integration (Spotify, Apple Music...)
- Voice input (speech-to-text)

---

## 🙏 Ghi chú

Dự án được phát triển với sự hỗ trợ của Claude Code.

**Ngày khởi đầu:** 2025-10-06
**Ngày cập nhật Phase 6:** 2025-10-07
**GitHub:** https://github.com/namcao258/arduino-ai-chatbot

**Tổng số Phases hoàn thành:** 6
- Phase 1: Kiến trúc module hóa
- Phase 2: AI Reasoning nâng cao
- Phase 3: Context Learning
- Phase 4: Persistent Storage
- Phase 5: Version Control & GitHub
- Phase 6: YouTube Music Integration ⭐ NEW
