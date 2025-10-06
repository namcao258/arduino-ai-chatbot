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

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                functions=FUNCTIONS,
                function_call="auto"
            )

            message = response.choices[0].message

            # Kiểm tra xem AI có muốn gọi function không
            if message.function_call:
                function_name = message.function_call.name
                function_args = json.loads(message.function_call.arguments)

                return {
                    "needs_function_call": True,
                    "function_name": function_name,
                    "function_args": function_args,
                    "message": None
                }
            else:
                # AI trả lời bình thường
                ai_response = message.content
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
