# 📺 Hướng dẫn cài đặt YouTube Music Player

## 🎯 Tính năng

AI tự động:
- 🔍 Tìm kiếm nhạc trên YouTube
- 🎵 Phát nhạc theo tên bài/ca sĩ
- 😊 Phát nhạc theo tâm trạng (buồn, vui, thư giãn...)
- 🎸 Phát nhạc theo thể loại (pop, rock, EDM...)

---

## 📦 Cài đặt

### 1. Cài đặt thư viện Python

```bash
cd /home/holab/Desktop/Arduino
pip install youtube-search-python
```

### 2. Đảm bảo có browser

YouTube sẽ mở trên browser, cần có một trong các browser:
- Google Chrome / Chromium ✅
- Firefox ✅
- Microsoft Edge ✅

---

## 🎮 Cách sử dụng

### Ví dụ chat với AI:

```
Bạn: Phát bài Lạc Trôi
🔍 Đang tìm kiếm: Lạc Trôi official audio...
🎵 Đã tìm thấy: Sơn Tùng M-TP - LẠC TRÔI | Official Music Video
✅ Đang phát: Sơn Tùng M-TP - LẠC TRÔI
💭 Lý do: Người dùng yêu cầu phát bài Lạc Trôi
AI: Đang phát bài Lạc Trôi cho bạn!
```

```
Bạn: Buồn quá
🔍 Đang tìm kiếm: sad emotional music playlist...
🎵 Đã tìm thấy: Sad Songs Playlist 2024
✅ Đang phát: Sad Songs Playlist 2024
💭 Lý do: Người dùng buồn, phát nhạc buồn giúp thư giãn
AI: Tôi hiểu cảm giác của bạn. Đang bật nhạc buồn!
```

```
Bạn: Muốn nghe nhạc EDM
🔍 Đang tìm kiếm: EDM music playlist 2024...
🎵 Đã tìm thấy: Best EDM Mix 2024
✅ Đang phát: Best EDM Mix 2024
AI: EDM đây! Enjoy!
```

---

## 🎵 Các loại yêu cầu hỗ trợ

### 1. Bài hát cụ thể

```
"Phát bài [tên bài]"
"Nghe bài See Tình"
"Play Shape of You"
```

### 2. Ca sĩ cụ thể

```
"Nghe Sơn Tùng MTP"
"Phát nhạc Ed Sheeran"
"Bài của Taylor Swift"
```

### 3. Tâm trạng

| Tâm trạng | Ví dụ câu lệnh |
|-----------|----------------|
| **buồn** | "Buồn quá", "Tôi đang buồn" |
| **vui** | "Vui vẻ đi", "Nhạc sôi động" |
| **thư giãn** | "Thư giãn thôi", "Chill chill" |
| **tập thể dục** | "Tập gym", "Workout music" |
| **làm việc** | "Cần focus", "Nhạc tập trung" |
| **ngủ** | "Muốn ngủ", "Sleep music" |
| **lãng mạn** | "Nhạc lãng mạn", "Love songs" |
| **party** | "Nhạc party", "Dance music" |

### 4. Thể loại

```
"Nhạc pop"
"Rock music"
"Jazz chill"
"EDM sôi động"
"Classical piano"
```

---

## 🔧 Cách hoạt động

### Luồng xử lý:

```
User: "Phát bài Lạc Trôi"
    ↓
AI nhận diện: song_name="Lạc Trôi"
    ↓
YouTubePlayer.search_and_play("Lạc Trôi official audio")
    ↓
Tìm trên YouTube API
    ↓
Lấy link video đầu tiên
    ↓
Mở browser với link
    ↓
YouTube phát nhạc qua tai nghe! 🎧
```

---

## 💡 Tips

### 1. Tối ưu search

AI tự động thêm "official audio" hoặc "playlist" để kết quả tốt hơn:
```python
"Lạc Trôi" → "Lạc Trôi official audio"
"sad music" → "sad emotional music playlist"
```

### 2. Đóng tab cũ

Browser sẽ mở tab mới mỗi lần phát nhạc. Bạn có thể:
- Đóng tab cũ thủ công
- Hoặc để nhiều tab (multi-tasking)

### 3. Volume control

Sau khi mở YouTube, dùng lệnh:
```
"To quá" → Giảm âm lượng hệ thống
"Nhỏ quá" → Tăng âm lượng hệ thống
```

---

## 🚀 Nâng cao: Download và phát offline

Nếu muốn chất lượng cao hơn (không cần browser), dùng `YouTubeDownloader`:

### Cài đặt

```bash
# Cài yt-dlp
sudo apt install yt-dlp

# Cài mpv hoặc vlc
sudo apt install mpv
# hoặc
sudo apt install vlc
```

### Sử dụng trong code

```python
from youtube_player import YouTubeDownloader

downloader = YouTubeDownloader()
downloader.download_and_play("Lạc Trôi Sơn Tùng MTP")
```

**Ưu điểm:**
- ✅ Chất lượng audio cao (MP3 320kbps)
- ✅ Phát qua mpv/vlc (nhẹ hơn browser)
- ✅ Lưu cache, không tải lại

**Nhược điểm:**
- ❌ Download mất thời gian lần đầu
- ❌ Tốn dung lượng ổ cứng

---

## 🐛 Troubleshooting

### Lỗi: "No module named 'youtubesearchpython'"

```bash
pip install youtube-search-python
```

### Lỗi: "No browser found"

Cài browser:
```bash
sudo apt install chromium-browser
# hoặc
sudo apt install firefox
```

### Video không phát

- Kiểm tra kết nối Internet
- Thử search keyword khác
- Có thể video bị chặn ở khu vực của bạn

---

## 📚 Tham khảo

- [youtube-search-python docs](https://github.com/alexmercerind/youtube-search-python)
- [yt-dlp docs](https://github.com/yt-dlp/yt-dlp)
