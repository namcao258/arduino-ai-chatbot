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
        self.environment_state = {
            "led_status": "unknown",  # on/off/unknown
            "last_action_time": None,
            "last_action": None
        }

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

        # Giữ 10 actions gần nhất
        if len(self.recent_actions) > 10:
            self.recent_actions.pop(0)

        # Cập nhật trạng thái hiện tại
        self.environment_state["led_status"] = action
        self.environment_state["last_action_time"] = datetime.now()
        self.environment_state["last_action"] = action

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
        summary = f"""
TRẠNG THÁI HIỆN TẠI:
- Đèn: {self.environment_state['led_status']}
"""

        if self.recent_actions:
            summary += "\nHÀNH ĐỘNG GẦN ĐÂY:\n"
            for action in self.recent_actions[-3:]:  # 3 actions gần nhất
                summary += f"- {action['user_input']} → {action['action']} ({action['reason']})\n"

        if self.user_preferences:
            summary += "\nSỞ THÍCH ĐÃ HỌC:\n"
            for activity, prefs in self.user_preferences.items():
                preferred = "bật" if prefs["on"] > prefs["off"] else "tắt"
                summary += f"- Khi '{activity}': thích đèn {preferred}\n"

        return summary

    def extract_activity(self, user_input):
        """Trích xuất hoạt động từ input của user (đơn giản)"""
        activities = {
            "đọc": ["đọc", "read", "sách", "báo"],
            "ngủ": ["ngủ", "sleep", "nghỉ", "rest"],
            "làm việc": ["làm việc", "work", "code", "học"],
            "xem phim": ["xem phim", "movie", "film", "netflix"],
            "ăn": ["ăn", "eat", "cơm"],
        }

        user_input_lower = user_input.lower()
        for activity, keywords in activities.items():
            for keyword in keywords:
                if keyword in user_input_lower:
                    return activity
        return None

    def save_to_file(self):
        """Lưu dữ liệu vào file JSON"""
        try:
            # Chuyển datetime thành string để serialize JSON
            environment_state_serializable = {
                "led_status": self.environment_state["led_status"],
                "last_action_time": self.environment_state["last_action_time"].isoformat() if self.environment_state["last_action_time"] else None,
                "last_action": self.environment_state["last_action"]
            }

            data = {
                "user_preferences": self.user_preferences,
                "recent_actions": self.recent_actions,
                "environment_state": environment_state_serializable
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

            # Parse datetime từ string
            env_state = data.get("environment_state", {})
            self.environment_state = {
                "led_status": env_state.get("led_status", "unknown"),
                "last_action_time": datetime.fromisoformat(env_state["last_action_time"]) if env_state.get("last_action_time") else None,
                "last_action": env_state.get("last_action")
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
