"""
Context Memory - Ghi nhớ ngữ cảnh và sở thích người dùng
"""
from datetime import datetime
import json
import os

class ContextMemory:
    def __init__(self, storage_file="memory_data.json"):
        """
        Khởi tạo Context Memory với persistent storage

        Args:
            storage_file: File JSON để lưu dữ liệu học được
        """
        self.storage_file = storage_file
        self.user_preferences = {}
        self.recent_actions = []

        # Trạng thái môi trường và ngữ cảnh
        self.environment_state = {
            "music_status": "stopped",  # playing/paused/stopped
            "current_song": None,  # Tên bài hát đang phát
            "otto_last_emotion": None,  # Cảm xúc gần nhất của Otto
            "otto_last_action": None,  # Hành động gần nhất
            "last_action_time": None,
        }

        # Phát hiện mood/cảm xúc của user
        self.user_mood_history = []  # Lịch sử mood: [{timestamp, mood, reason}]
        self.current_user_mood = None  # vui/buồn/tức/bình thường/hào hứng

        # Conversation context
        self.conversation_topics = []  # Các chủ đề được nhắc đến
        self.user_activities = {}  # Hoạt động user đang làm: {activity: count}

        # Load dữ liệu đã lưu (nếu có)
        self.load_from_file()

    def record_action(self, action, reason, user_input):
        """Ghi nhận hành động và lý do"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "action": action,
            "reason": reason
        }
        self.recent_actions.append(record)

        # Giữ 20 actions gần nhất (tăng từ 10)
        if len(self.recent_actions) > 20:
            self.recent_actions.pop(0)

        # Cập nhật trạng thái Otto
        if action in ['happy', 'sad', 'excited', 'confused', 'angry', 'scared', 'sleepy', 'love', 'surprised']:
            self.environment_state["otto_last_emotion"] = action
        else:
            self.environment_state["otto_last_action"] = action

        self.environment_state["last_action_time"] = datetime.now()

        # Phát hiện và ghi nhận mood của user
        self.detect_user_mood(user_input)

        # Tự động lưu sau mỗi action
        self.save_to_file()

    def learn_preference(self, activity, preferred_light_state):
        """Học sở thích: hoạt động nào thích đèn bật/tắt"""
        if activity not in self.user_preferences:
            self.user_preferences[activity] = {"on": 0, "off": 0}

        self.user_preferences[activity][preferred_light_state] += 1

        # Tự động lưu sau khi học
        self.save_to_file()

    def get_preference(self, activity):
        """Lấy sở thích đã học về một hoạt động"""
        if activity in self.user_preferences:
            prefs = self.user_preferences[activity]
            if prefs["on"] > prefs["off"]:
                return "on"
            elif prefs["off"] > prefs["on"]:
                return "off"
        return None

    def get_context_summary(self):
        """Tạo summary về context hiện tại để đưa vào prompt"""
        summary = "\n🧠 NGỮ CẢNH HIỆN TẠI:\n"

        # Trạng thái nhạc
        music_status = self.environment_state.get('music_status', 'stopped')
        current_song = self.environment_state.get('current_song')
        if music_status == 'playing' and current_song:
            summary += f"🎵 Nhạc: Đang phát '{current_song}'\n"
        elif music_status == 'paused' and current_song:
            summary += f"⏸️ Nhạc: Tạm dừng '{current_song}'\n"
        else:
            summary += f"🎵 Nhạc: Đã tắt\n"

        # Trạng thái Otto
        otto_emotion = self.environment_state.get('otto_last_emotion')
        otto_action = self.environment_state.get('otto_last_action')
        if otto_emotion:
            summary += f"🤖 Otto: Cảm xúc '{otto_emotion}' gần đây\n"
        elif otto_action:
            summary += f"🤖 Otto: Vừa thực hiện '{otto_action}'\n"

        # Mood của user
        if self.current_user_mood:
            summary += f"😊 Mood user: {self.current_user_mood}\n"

        # Hành động gần đây
        if self.recent_actions:
            summary += "\n💭 HÀNH ĐỘNG GẦN ĐÂY:\n"
            for action in self.recent_actions[-5:]:  # 5 actions gần nhất
                summary += f"  • {action['user_input'][:50]}... → {action['action']}\n"

        # Hoạt động thường làm
        if self.user_activities:
            top_activities = sorted(self.user_activities.items(), key=lambda x: x[1], reverse=True)[:3]
            summary += "\n📊 HOẠT ĐỘNG THƯỜNG LÀM:\n"
            for activity, count in top_activities:
                summary += f"  • {activity} ({count} lần)\n"

        # Mood history
        if self.user_mood_history:
            summary += "\n😌 LỊCH SỬ CẢM XÚC:\n"
            for mood_record in self.user_mood_history[-3:]:
                summary += f"  • {mood_record['mood']}: \"{mood_record['text'][:40]}...\"\n"

        summary += "\n⚡ SỬ DỤNG NGỮ CẢNH TRÊN ĐỂ TRẢ LỜI THÔNG MINH HƠN!\n"

        return summary

    def detect_user_mood(self, user_input):
        """Phát hiện mood/cảm xúc của user từ câu nói"""
        mood_keywords = {
            "vui": ["vui", "happy", "hạnh phúc", "vui vẻ", "vui quá", "tuyệt", "tốt quá", "nice", "cool"],
            "buồn": ["buồn", "sad", "khóc", "chán", "tệ", "tồi tệ", "thất vọng", "ức chế"],
            "tức giận": ["tức", "giận", "angry", "bực", "khó chịu", "mệt mỏi", "chán nản"],
            "hào hứng": ["háo hức", "hào hứng", "excited", "đỗ", "thắng", "được", "thành công", "yayyy", "yeah"],
            "mệt mỏi": ["mệt", "tired", "kiệt sức", "ngủ", "uể oải"],
            "lo lắng": ["lo", "sợ", "anxiety", "nervous", "căng thẳng", "stress"],
        }

        user_lower = user_input.lower()
        detected_mood = None

        for mood, keywords in mood_keywords.items():
            for keyword in keywords:
                if keyword in user_lower:
                    detected_mood = mood
                    break
            if detected_mood:
                break

        if detected_mood:
            self.current_user_mood = detected_mood
            self.user_mood_history.append({
                "timestamp": datetime.now().isoformat(),
                "mood": detected_mood,
                "text": user_input
            })

            # Giữ 10 mood gần nhất
            if len(self.user_mood_history) > 10:
                self.user_mood_history.pop(0)

        return detected_mood

    def update_music_status(self, status, song_name=None):
        """Cập nhật trạng thái nhạc"""
        self.environment_state["music_status"] = status  # playing/paused/stopped
        if song_name:
            self.environment_state["current_song"] = song_name
        self.save_to_file()

    def get_current_song(self):
        """Lấy bài hát đang phát"""
        return self.environment_state.get("current_song")

    def extract_activity(self, user_input):
        """Trích xuất hoạt động từ input của user"""
        activities = {
            "đọc": ["đọc", "read", "sách", "báo", "tài liệu"],
            "ngủ": ["ngủ", "sleep", "nghỉ", "rest", "buồn ngủ"],
            "làm việc": ["làm việc", "work", "code", "học", "coding", "deadline"],
            "xem phim": ["xem phim", "movie", "film", "netflix", "youtube"],
            "ăn": ["ăn", "eat", "cơm", "bữa"],
            "tập thể dục": ["tập", "gym", "chạy bộ", "workout"],
            "thư giãn": ["thư giãn", "chill", "relax", "nghỉ ngơi"],
        }

        user_input_lower = user_input.lower()
        for activity, keywords in activities.items():
            for keyword in keywords:
                if keyword in user_input_lower:
                    # Tăng counter cho activity này
                    if activity not in self.user_activities:
                        self.user_activities[activity] = 0
                    self.user_activities[activity] += 1
                    return activity
        return None

    def save_to_file(self):
        """Lưu dữ liệu vào file JSON"""
        try:
            # Chuyển datetime thành string để serialize JSON
            environment_state_serializable = {
                "music_status": self.environment_state.get("music_status", "stopped"),
                "current_song": self.environment_state.get("current_song"),
                "otto_last_emotion": self.environment_state.get("otto_last_emotion"),
                "otto_last_action": self.environment_state.get("otto_last_action"),
                "last_action_time": self.environment_state["last_action_time"].isoformat() if self.environment_state.get("last_action_time") else None,
            }

            data = {
                "user_preferences": self.user_preferences,
                "recent_actions": self.recent_actions,
                "environment_state": environment_state_serializable,
                "current_user_mood": self.current_user_mood,
                "user_mood_history": self.user_mood_history,
                "user_activities": self.user_activities,
            }

            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return True
        except Exception as e:
            print(f"⚠️  Lỗi khi lưu memory: {e}")
            return False

    def load_from_file(self):
        """Load dữ liệu từ file JSON"""
        if not os.path.exists(self.storage_file):
            print("📝 Chưa có dữ liệu học trước đó. Bắt đầu mới!")
            return False

        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.user_preferences = data.get("user_preferences", {})
            self.recent_actions = data.get("recent_actions", [])
            self.current_user_mood = data.get("current_user_mood")
            self.user_mood_history = data.get("user_mood_history", [])
            self.user_activities = data.get("user_activities", {})

            # Parse datetime từ string
            env_state = data.get("environment_state", {})
            self.environment_state = {
                "music_status": env_state.get("music_status", "stopped"),
                "current_song": env_state.get("current_song"),
                "otto_last_emotion": env_state.get("otto_last_emotion"),
                "otto_last_action": env_state.get("otto_last_action"),
                "last_action_time": datetime.fromisoformat(env_state["last_action_time"]) if env_state.get("last_action_time") else None,
            }

            print(f"✅ Đã load memory từ {self.storage_file}")
            return True
        except Exception as e:
            print(f"⚠️  Lỗi khi load memory: {e}")
            return False

    def clear_memory(self):
        """Xóa toàn bộ memory và file"""
        self.user_preferences = {}
        self.recent_actions = []
        self.environment_state = {
            "led_status": "unknown",
            "last_action_time": None,
            "last_action": None
        }

        if os.path.exists(self.storage_file):
            os.remove(self.storage_file)
            print("🗑️  Đã xóa toàn bộ memory!")
        else:
            print("🗑️  Memory đã trống!")
