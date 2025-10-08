"""
LLM Handler - Xử lý giao tiếp với OpenAI API
"""
from openai import OpenAI
import json
from config import Config
from function_definitions import FUNCTIONS, SYSTEM_PROMPT
from context_memory import ContextMemory

class LLMHandler:
    def __init__(self):
        """Khởi tạo OpenAI client"""
        Config.validate()  # Kiểm tra API key
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL
        self.context_memory = ContextMemory()  # Thêm context memory
        self.conversation_history = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]
        self.current_user_input = None  # Lưu input hiện tại để học

    def add_user_message(self, message):
        """Thêm tin nhắn người dùng vào lịch sử"""
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        self._trim_history()

    def add_assistant_message(self, message):
        """Thêm tin nhắn AI vào lịch sử"""
        self.conversation_history.append({
            "role": "assistant",
            "content": message
        })
        self._trim_history()

    def add_function_result(self, function_name, result):
        """Thêm kết quả function vào lịch sử"""
        self.conversation_history.append({
            "role": "function",
            "name": function_name,
            "content": result
        })
        self._trim_history()

    def _trim_history(self):
        """Giới hạn độ dài lịch sử hội thoại (giữ system prompt)"""
        if len(self.conversation_history) > Config.MAX_CONVERSATION_HISTORY:
            # Giữ system prompt (phần tử đầu tiên)
            self.conversation_history = [self.conversation_history[0]] + \
                                       self.conversation_history[-(Config.MAX_CONVERSATION_HISTORY - 1):]

    def _inject_context_to_system_prompt(self):
        """Inject context memory vào system prompt"""
        context_summary = self.context_memory.get_context_summary()
        enhanced_prompt = SYSTEM_PROMPT + "\n\n" + context_summary

        # Cập nhật system message
        self.conversation_history[0] = {
            "role": "system",
            "content": enhanced_prompt
        }

    def get_response(self, user_input):
        """
        Gửi tin nhắn tới OpenAI và nhận response

        Args:
            user_input: Tin nhắn từ người dùng

        Returns:
            dict: {
                "needs_function_call": bool,
                "function_name": str hoặc None,
                "function_args": dict hoặc None,
                "message": str hoặc None
            }
        """
        self.current_user_input = user_input  # Lưu lại để học
        self.add_user_message(user_input)

        # Inject context vào prompt
        self._inject_context_to_system_prompt()

        # Phát hiện từ khóa điều khiển để force function call
        user_lower = user_input.lower()

        # Từ khóa TÌM KIẾM/MỞ nhạc mới (ưu tiên cao nhất)
        play_music_keywords = ['mở bài', 'phát bài', 'bật bài', 'nghe bài', 'tìm bài', 'play bài']

        # Từ khóa điều khiển nhạc đang phát (không phải tìm bài mới)
        control_music_keywords = ['tiếp tục', 'phát tiếp', 'phát lại', 'play lại', 'pause', 'tạm dừng', 'dừng lại', 'stop', 'tắt nhạc', 'bật lại']

        # Từ khóa điều khiển Otto (chỉ khi KHÔNG liên quan nhạc)
        otto_movement_keywords = ['sang trái', 'sang phải', 'đi tới', 'đi lùi', 'chạy', 'quay', 'rẽ', 'turn', 'walk', 'moonwalk']
        otto_emotion_keywords = ['vui vẻ', 'buồn bã', 'tức giận', 'wave', 'vẫy', 'bow', 'cúi', 'nhảy']

        function_call_mode = "auto"

        # Ưu tiên 1: Nếu có từ "bài hát", "nhạc", "mở bài" → play_youtube_music
        if any(keyword in user_lower for keyword in play_music_keywords) or 'bài hát' in user_lower or ('mở' in user_lower and 'nhạc' in user_lower):
            function_call_mode = "auto"  # Để AI tự chọn play_youtube_music

        # Ưu tiên 2: Kiểm tra control_music (điều khiển nhạc đang phát)
        elif any(keyword in user_lower for keyword in control_music_keywords):
            words = user_lower.split()
            if len(words) <= 3:  # Lệnh ngắn → control_music
                function_call_mode = {"name": "control_music"}

        # Ưu tiên 3: Kiểm tra control_otto (chỉ khi rõ ràng là lệnh Otto)
        elif any(keyword in user_lower for keyword in otto_movement_keywords):
            function_call_mode = {"name": "control_otto"}
        elif any(keyword in user_lower for keyword in otto_emotion_keywords):
            # Chỉ force nếu KHÔNG có từ liên quan nhạc
            if 'nhạc' not in user_lower and 'bài' not in user_lower and 'hát' not in user_lower:
                function_call_mode = {"name": "control_otto"}

        try:
            # Nếu có từ khóa điều khiển → bắt buộc gọi function
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                functions=FUNCTIONS,
                function_call=function_call_mode
            )

            message = response.choices[0].message

            # Kiểm tra xem AI có muốn gọi function không
            if message.function_call:
                function_name = message.function_call.name

                # Parse arguments với error handling
                try:
                    function_args = json.loads(message.function_call.arguments)
                except json.JSONDecodeError as e:
                    print(f"⚠️ JSON parse error: {e}")
                    print(f"Raw arguments: {message.function_call.arguments}")
                    # Thử fix các ký tự đặc biệt
                    import re
                    fixed_args = message.function_call.arguments.replace('\n', '\\n').replace('\r', '\\r')
                    try:
                        function_args = json.loads(fixed_args)
                    except:
                        # Fallback - trả về empty dict
                        function_args = {"reason": "Không thể parse arguments"}

                return {
                    "needs_function_call": True,
                    "function_name": function_name,
                    "function_args": function_args,
                    "message": None
                }
            else:
                # AI trả lời bình thường - Text response (KHÔNG NÊN XẢY RA với lệnh điều khiển)
                ai_response = message.content

                # Cảnh báo nếu có từ khóa lệnh điều khiển mà không gọi function
                control_keywords = ['tiếp tục', 'phát', 'pause', 'tạm dừng', 'dừng', 'play', 'stop',
                                   'sang trái', 'sang phải', 'đi', 'chạy', 'nhảy', 'quay', 'rẽ',
                                   'bật nhạc', 'tắt nhạc', 'bật', 'tắt']
                user_lower = self.current_user_input.lower() if self.current_user_input else ""

                if any(keyword in user_lower for keyword in control_keywords):
                    warning = f"\n⚠️ BẠN ĐÃ NÊU LỆNH ĐIỀU KHIỂN NHƯNG CHƯA GỌI FUNCTION! User: '{self.current_user_input}'"
                    ai_response = ai_response + warning

                # Post-processing: Loại bỏ câu hỏi
                if '?' in ai_response or 'muốn' in ai_response.lower() or 'cần' in ai_response.lower() or 'tiếp theo' in ai_response.lower():
                    ai_response = "OK! 🤖"

                self.add_assistant_message(ai_response)

                return {
                    "needs_function_call": False,
                    "function_name": None,
                    "function_args": None,
                    "message": ai_response
                }

        except Exception as e:
            return {
                "needs_function_call": False,
                "function_name": None,
                "function_args": None,
                "message": f"❌ Lỗi OpenAI API: {e}"
            }

    def get_final_response(self):
        """
        Sau khi thực thi function, gọi lại OpenAI để tạo response cuối cùng

        Returns:
            str: Response từ AI
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history
            )

            final_message = response.choices[0].message.content

            # Post-processing: Loại bỏ câu hỏi nếu có
            if '?' in final_message or 'muốn' in final_message.lower() or 'cần' in final_message.lower() or 'tiếp theo' in final_message.lower():
                # Nếu AI hỏi lại, rút ngắn thành OK
                final_message = "OK! 🤖"

            self.add_assistant_message(final_message)

            return final_message

        except Exception as e:
            return f"❌ Lỗi khi tạo response: {e}"

    def record_action_to_memory(self, action, reason):
        """Ghi nhận hành động vào memory để học"""
        if self.current_user_input:
            self.context_memory.record_action(action, reason, self.current_user_input)

            # Học sở thích từ hoạt động
            activity = self.context_memory.extract_activity(self.current_user_input)
            if activity:
                self.context_memory.learn_preference(activity, action)

    def get_learned_stats(self):
        """Lấy thống kê những gì đã học"""
        return self.context_memory.get_context_summary()

    def reset_conversation(self):
        """Reset lịch sử hội thoại (giữ lại system prompt)"""
        self.conversation_history = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]
        print("🔄 Đã reset lịch sử hội thoại")
