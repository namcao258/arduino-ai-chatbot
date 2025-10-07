# 🎵 Hướng dẫn cài đặt Music Control

## 📋 Yêu cầu hệ thống

Music Controller hỗ trợ điều khiển media player trên **Linux**, **Windows**, và **macOS**.

---

## 🐧 Linux (Ubuntu/Debian)

### Cài đặt playerctl

```bash
# Ubuntu/Debian
sudo apt install playerctl

# Arch Linux
sudo pacman -S playerctl

# Fedora
sudo dnf install playerctl
```

### Kiểm tra

```bash
# Kiểm tra playerctl hoạt động
playerctl --version

# Xem media players đang chạy
playerctl -l
```

### Hỗ trợ media players:
- ✅ Spotify
- ✅ VLC
- ✅ Chrome/Chromium (YouTube, web players...)
- ✅ Firefox
- ✅ Rhythmbox
- ✅ Clementine
- ✅ và nhiều player khác...

---

## 🪟 Windows

### Không cần cài đặt thêm!

Windows có sẵn Media Control Keys, nhưng nếu muốn điều khiển tốt hơn:

```bash
# Cài keyboard library (optional)
pip install keyboard
```

**Lưu ý:** Chạy với quyền Administrator để `keyboard` hoạt động.

---

## 🍎 macOS

### Sử dụng AppleScript (có sẵn)

Không cần cài đặt thêm! macOS có sẵn AppleScript để điều khiển:
- Apple Music (iTunes)
- Spotify
- VLC

---

## 🎯 Cách sử dụng

### Test riêng Music Controller

```bash
cd /home/holab/Desktop/Arduino
python3
```

```python
from music_controller import MusicController

music = MusicController()

# Phát nhạc
music.play()

# Tạm dừng
music.pause()

# Dừng
music.stop()

# Tăng/giảm âm lượng
music.volume_up()
music.volume_down()

# Kiểm tra trạng thái
music.get_status()
```

### Sử dụng với AI Chatbot

```bash
python main.py
```

```
Bạn: Bật nhạc lên
🎵 ✅ Đã bật nhạc
💭 Lý do: Người dùng yêu cầu bật nhạc
AI: Đã bật nhạc cho bạn!

Bạn: Buồn quá
🎵 ✅ Đã bật nhạc
💭 Lý do: Người dùng buồn, nghe nhạc có thể giúp cải thiện tâm trạng
AI: Tôi hiểu cảm giác của bạn. Để tôi bật nhạc cho bạn!

Bạn: To quá
🎵 🔉 Đã giảm âm lượng
💭 Lý do: Âm lượng quá lớn, cần giảm
AI: Đã giảm âm lượng cho bạn rồi!
```

---

## 🐛 Troubleshooting

### Linux: "playerctl command not found"

```bash
# Cài lại playerctl
sudo apt update
sudo apt install playerctl
```

### Linux: "No players found"

Bạn cần mở một media player trước:
- Mở Spotify
- Mở VLC
- Mở YouTube trên Chrome/Firefox

### Windows: "keyboard module not found"

```bash
pip install keyboard
```

Sau đó chạy terminal với **Run as Administrator**.

### macOS: "Operation not permitted"

Cấp quyền cho Terminal/iTerm:
1. System Preferences → Security & Privacy → Privacy
2. Automation → Tick Terminal/iTerm

---

## 💡 Tips

### Linux: Điều khiển player cụ thể

```python
# Điều khiển Spotify
subprocess.run(["playerctl", "-p", "spotify", "play"])

# Điều khiển VLC
subprocess.run(["playerctl", "-p", "vlc", "play"])
```

### Thêm player khác

Chỉnh sửa [music_controller.py](music_controller.py) để thêm support cho player khác!

---

## 🎵 Các action được hỗ trợ

| Action | Mô tả | Ví dụ câu lệnh |
|--------|-------|----------------|
| `play` | Phát nhạc | "Bật nhạc", "Buồn quá" |
| `pause` | Tạm dừng | "Tạm dừng nhạc" |
| `stop` | Dừng hẳn | "Tắt nhạc", "Ồn quá" |
| `volume_up` | Tăng âm lượng | "To lên", "Nhỏ quá" |
| `volume_down` | Giảm âm lượng | "Nhỏ lại", "To quá" |

---

## 📚 Tham khảo

- [playerctl documentation](https://github.com/altdesktop/playerctl)
- [MPRIS D-Bus Interface](https://specifications.freedesktop.org/mpris-spec/latest/)
