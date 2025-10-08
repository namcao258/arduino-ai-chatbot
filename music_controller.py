"""
Music Controller - Điều khiển phát nhạc trên máy tính
"""
import subprocess
import platform

class MusicController:
    def __init__(self):
        """Khởi tạo Music Controller"""
        self.system = platform.system()  # Linux, Windows, Darwin (macOS)
        self.is_playing = False

    def play(self):
        """Phát nhạc"""
        try:
            if self.system == "Linux":
                # Sử dụng playerctl (hỗ trợ Spotify, VLC, Chrome, Firefox...)
                subprocess.run(["playerctl", "play"], check=False)
                self.is_playing = True
                return "✅ Đã bật nhạc"
            elif self.system == "Windows":
                # Windows Media Control
                import keyboard
                keyboard.press_and_release('play/pause media')
                self.is_playing = True
                return "✅ Đã bật nhạc"
            elif self.system == "Darwin":  # macOS
                # AppleScript for macOS
                subprocess.run(["osascript", "-e", 'tell application "Music" to play'], check=False)
                self.is_playing = True
                return "✅ Đã bật nhạc"
            else:
                return "❌ Hệ điều hành không được hỗ trợ"
        except FileNotFoundError:
            return "❌ Không tìm thấy media player. Cài đặt: sudo apt install playerctl"
        except Exception as e:
            return f"❌ Lỗi phát nhạc: {e}"

    def pause(self):
        """Tạm dừng nhạc"""
        try:
            if self.system == "Linux":
                # Kiểm tra trạng thái trước
                status_result = subprocess.run(["playerctl", "status"], check=False, capture_output=True, text=True)
                current_status = status_result.stdout.strip()

                if current_status == "Paused":
                    return "⏸️  Nhạc đã tạm dừng rồi"
                elif current_status == "Stopped":
                    return "⏸️  Nhạc đã dừng rồi"

                # Thử playerctl trước
                result = subprocess.run(["playerctl", "pause"], check=False, capture_output=True)
                if result.returncode == 0:
                    self.is_playing = False
                    return "⏸️  Đã tạm dừng nhạc"
                else:
                    # Fallback: Hướng dẫn user
                    return "⏸️  Nhấn phím SPACE trên tab YouTube để tạm dừng nhé!"
            elif self.system == "Windows":
                import keyboard
                keyboard.press_and_release('play/pause media')
                self.is_playing = False
                return "⏸️  Đã tạm dừng nhạc"
            elif self.system == "Darwin":
                subprocess.run(["osascript", "-e", 'tell application "Music" to pause'], check=False)
                self.is_playing = False
                return "⏸️  Đã tạm dừng nhạc"
            else:
                return "❌ Hệ điều hành không được hỗ trợ"
        except FileNotFoundError:
            return "⏸️  Nhấn phím SPACE trên tab YouTube để tạm dừng nhé!"
        except Exception as e:
            return f"⏸️  Nhấn SPACE để tạm dừng (hoặc cài playerctl: sudo apt install playerctl)"

    def stop(self):
        """Dừng nhạc"""
        try:
            if self.system == "Linux":
                # Kiểm tra trạng thái trước
                status_result = subprocess.run(["playerctl", "status"], check=False, capture_output=True, text=True)
                current_status = status_result.stdout.strip()

                if current_status == "Stopped":
                    return "⏹️  Nhạc đã dừng rồi"

                result = subprocess.run(["playerctl", "stop"], check=False, capture_output=True)
                if result.returncode == 0:
                    self.is_playing = False
                    return "⏹️  Đã dừng nhạc"
                else:
                    return "⏹️  Đóng tab YouTube để dừng nhạc nhé!"
            elif self.system == "Windows":
                import keyboard
                keyboard.press_and_release('stop media')
                self.is_playing = False
                return "⏹️  Đã dừng nhạc"
            elif self.system == "Darwin":
                subprocess.run(["osascript", "-e", 'tell application "Music" to stop'], check=False)
                self.is_playing = False
                return "⏹️  Đã dừng nhạc"
            else:
                return "❌ Hệ điều hành không được hỗ trợ"
        except FileNotFoundError:
            return "⏹️  Đóng tab YouTube để dừng nhạc nhé!"
        except Exception as e:
            return f"⏹️  Đóng tab YouTube để dừng (hoặc cài: sudo apt install playerctl)"

    def volume_up(self):
        """Tăng âm lượng"""
        try:
            if self.system == "Linux":
                # Tăng 10%
                subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+10%"], check=False)
                return "🔊 Đã tăng âm lượng"
            elif self.system == "Windows":
                import keyboard
                keyboard.press_and_release('volume up')
                return "🔊 Đã tăng âm lượng"
            elif self.system == "Darwin":
                subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10)"], check=False)
                return "🔊 Đã tăng âm lượng"
            else:
                return "❌ Hệ điều hành không được hỗ trợ"
        except Exception as e:
            return f"❌ Lỗi tăng âm lượng: {e}"

    def volume_down(self):
        """Giảm âm lượng"""
        try:
            if self.system == "Linux":
                # Giảm 10%
                subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-10%"], check=False)
                return "🔉 Đã giảm âm lượng"
            elif self.system == "Windows":
                import keyboard
                keyboard.press_and_release('volume down')
                return "🔉 Đã giảm âm lượng"
            elif self.system == "Darwin":
                subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 10)"], check=False)
                return "🔉 Đã giảm âm lượng"
            else:
                return "❌ Hệ điều hành không được hỗ trợ"
        except Exception as e:
            return f"❌ Lỗi giảm âm lượng: {e}"

    def control_music(self, action):
        """
        Điều khiển nhạc theo action

        Args:
            action: "play", "pause", "stop", "volume_up", "volume_down"

        Returns:
            str: Kết quả thực hiện
        """
        actions = {
            "play": self.play,
            "pause": self.pause,
            "stop": self.stop,
            "volume_up": self.volume_up,
            "volume_down": self.volume_down
        }

        if action in actions:
            return actions[action]()
        else:
            return f"❌ Action không hợp lệ: {action}"

    def get_status(self):
        """Lấy trạng thái hiện tại"""
        try:
            if self.system == "Linux":
                result = subprocess.run(
                    ["playerctl", "status"],
                    capture_output=True,
                    text=True,
                    check=False
                )
                status = result.stdout.strip()
                return f"🎵 Trạng thái: {status}"
            else:
                return f"🎵 Trạng thái: {'Đang phát' if self.is_playing else 'Đã dừng'}"
        except Exception as e:
            return f"❌ Không thể lấy trạng thái: {e}"
