"""
Function Definitions - Định nghĩa các functions cho OpenAI Function Calling
"""

# Định nghĩa function để OpenAI biết khi nào cần gọi
FUNCTIONS = [
    {
        "name": "control_led",
        "description": """Điều khiển đèn LED trong phòng.

        HÃY TỰ QUYẾT ĐỊNH khi nào cần bật/tắt đèn dựa trên:
        - Ngữ cảnh và nhu cầu thực tế của người dùng
        - Tình huống ánh sáng (tối, sáng, mờ, chói...)
        - Hoạt động người dùng đang làm (đọc sách, ngủ, làm việc, xem phim...)
        - Cảm xúc và sở thích người dùng thể hiện

        VÍ DỤ TỰ SUY LUẬN:
        - "Tôi sắp đọc sách" → Cần ánh sáng → bật đèn
        - "Tôi muốn ngủ" → Cần tối → tắt đèn
        - "Mắt tôi mỏi" → Có thể do sáng quá → tắt đèn
        - "Chuẩn bị làm việc" → Cần môi trường sáng → bật đèn
        - "Xem phim đây" → Thường xem trong tối → tắt đèn
        - "Trời mưa ảm đạm quá" → Cần ánh sáng ấm → bật đèn

        KHÔNG CHỈ dựa vào từ khóa mà hãy HIỂU Ý ĐỊNH thực sự của người dùng.
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["on", "off"],
                    "description": "Hành động: 'on' để bật đèn, 'off' để tắt đèn"
                },
                "reason": {
                    "type": "string",
                    "description": "Giải thích WHY bạn quyết định bật/tắt đèn dựa trên ngữ cảnh"
                }
            },
            "required": ["action", "reason"]
        }
    },
    {
        "name": "control_music",
        "description": """Điều khiển phát nhạc đang phát trên máy tính (play/pause/stop/volume).

        Dùng để điều khiển nhạc ĐÃ ĐANG PHÁT (Spotify, VLC, YouTube đã mở...)

        VÍ DỤ:
        - "Tạm dừng nhạc" → pause
        - "Tắt nhạc đi" → stop
        - "To quá" → volume_down
        - "Nhỏ quá" → volume_up
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["play", "pause", "stop", "volume_up", "volume_down"],
                    "description": "Hành động điều khiển"
                },
                "reason": {
                    "type": "string",
                    "description": "Lý do"
                }
            },
            "required": ["action", "reason"]
        }
    },
    {
        "name": "play_youtube_music",
        "description": """Tự động TÌM KIẾM và PHÁT nhạc mới từ YouTube.

        Dùng khi người dùng muốn nghe bài hát CỤ THỂ hoặc nhạc theo TÂM TRẠNG.

        VÍ DỤ TỰ SUY LUẬN:
        - "Phát bài Lạc Trôi" → Tìm và phát bài "Lạc Trôi"
        - "Nghe Sơn Tùng MTP" → Tìm nhạc Sơn Tùng MTP
        - "Buồn quá, bật nhạc" → Phát nhạc buồn (mood: buồn)
        - "Nhạc vui vẻ đi" → Phát nhạc vui (mood: vui)
        - "Muốn thư giãn" → Phát nhạc thư giãn (mood: thư giãn)
        - "Nhạc EDM" → Phát nhạc EDM (genre: EDM)

        HÃY PHÂN BIỆT:
        - Có tên bài/ca sĩ cụ thể → dùng song_name/artist
        - Chỉ nói tâm trạng → dùng mood
        - Chỉ nói thể loại → dùng genre
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "song_name": {
                    "type": "string",
                    "description": "Tên bài hát (nếu có)"
                },
                "artist": {
                    "type": "string",
                    "description": "Tên ca sĩ (nếu có)"
                },
                "mood": {
                    "type": "string",
                    "enum": ["buồn", "vui", "thư giãn", "tập thể dục", "làm việc", "ngủ", "lãng mạn", "party"],
                    "description": "Tâm trạng (nếu không có bài cụ thể)"
                },
                "genre": {
                    "type": "string",
                    "description": "Thể loại nhạc: pop, rock, jazz, EDM, classical... (nếu không có mood)"
                },
                "reason": {
                    "type": "string",
                    "description": "Lý do chọn"
                }
            },
            "required": ["reason"]
        }
    }
]

# System prompt cho AI
SYSTEM_PROMPT = """Bạn là trợ lý AI thông minh có khả năng SUY LUẬN và điều khiển đèn LED + nhạc.

NGUYÊN TẮC HOẠT ĐỘNG:
🧠 HÃY SUY LUẬN THÔNG MINH như con người:
- KHÔNG chỉ khớp từ khóa, mà HIỂU ngữ cảnh và ý định
- Phân tích hoạt động, tâm trạng, môi trường người dùng
- Đưa ra quyết định hợp lý nhất cho tình huống

💡 KHI NÀO BẬT ĐÈN:
- Người dùng sắp làm việc cần ánh sáng (đọc, viết, làm việc...)
- Môi trường tối/u ám (trời tối, mưa, buồn ngủ ban ngày...)
- Cần tập trung, năng lượng, tỉnh táo
- Cảm giác không an toàn vì tối

💡 KHI NÀO TẮT ĐÈN:
- Người dùng sắp nghỉ ngơi/ngủ
- Xem phim, thư giãn (thường thích tối)
- Phàn nàn về ánh sáng (chói, mỏi mắt, đau đầu...)
- Tiết kiệm điện khi không cần

🎵 ĐIỀU KHIỂN NHẠC - QUAN TRỌNG:

**2 LOẠI LỆNH KHÁC NHAU:**

1. **play_youtube_music** - Tìm và MỞ nhạc MỚI:
   - "Phát bài [tên bài]"
   - "Nghe [ca sĩ]"
   - "Nhạc [tâm trạng/thể loại]"
   - Lần ĐẦU TIÊN người dùng yêu cầu bài hát

2. **control_music** - Điều khiển nhạc ĐANG PHÁT:
   - "Tạm dừng" / "Pause" → action: pause
   - "Tiếp tục" / "Play lại" → action: play
   - "Dừng hẳn" / "Stop" → action: stop
   - "To quá" → action: volume_down
   - "Nhỏ quá" → action: volume_up

**LƯU Ý QUAN TRỌNG:**
- YouTube không hỗ trợ "resume" sau khi dừng
- "Tiếp tục phát nhạc" SAU KHI DỪNG → Nên HỎI LẠI user muốn phát bài gì
- Chỉ dùng control_music(play) khi chắc chắn nhạc đang TẠM DỪNG (pause), chưa stop

❓ KHI KHÔNG CHẮC CHẮN:
- Hỏi lại người dùng: "Bạn muốn tôi bật đèn không?"
- KHÔNG tự ý hành động nếu không hiểu rõ

PHONG CÁCH:
- Trả lời tự nhiên, ngắn gọn bằng tiếng Việt
- Giải thích lý do quyết định nếu cần
- Chủ động đề xuất nếu phát hiện nhu cầu

VÍ DỤ SUY LUẬN:
User: "Tôi sắp đọc báo"
→ Suy luận: Đọc cần ánh sáng → Bật đèn
→ Gọi: control_led(action='on', reason='Người dùng sắp đọc báo, cần ánh sáng tốt')
→ Trả lời: "Để tôi bật đèn cho bạn đọc cho sáng nhé!"

User: "Mệt quá, muốn nằm nghỉ"
→ Suy luận: Nghỉ ngơi thường cần tối → Tắt đèn
→ Gọi: control_led(action='off', reason='Người dùng muốn nghỉ ngơi, nên tắt đèn')
→ Trả lời: "Để tôi tắt đèn cho bạn nghỉ ngơi nhé. Ngủ ngon!"

User: "Trời mưa ảm đạm quá"
→ Suy luận: Trời mưa tối, cần ánh sáng → Bật đèn
→ Gọi: control_led(action='on', reason='Trời mưa tối, cần thêm ánh sáng để không u ám')
→ Trả lời: "Trời mưa tối thế này, để tôi bật đèn cho ấm cúng hơn nhé!"
"""

# Mapping từ ngôn ngữ tự nhiên sang action (dự phòng)
ACTION_KEYWORDS = {
    "on": [
        "bật", "mở", "sáng", "tối", "turn on", "light on",
        "không nhìn thấy", "tối quá", "cần ánh sáng"
    ],
    "off": [
        "tắt", "đóng", "turn off", "light off",
        "sáng quá", "chói", "không cần đèn", "đủ sáng"
    ]
}
