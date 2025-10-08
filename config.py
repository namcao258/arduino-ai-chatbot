"""
File cấu hình - Quản lý API keys và settings
"""
import os

class Config:
    # OpenAI API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = "gpt-3.5-turbo"  # Có thể đổi sang "gpt-3.5-turbo" để tiết kiệm

    # Arduino Configuration
    ARDUINO_PORT = '/dev/ttyACM0'  # Linux: /dev/ttyACM0, Windows: COM3
    LED_PIN = 13  # Pin LED tích hợp trên Arduino Uno

    # Chatbot Configuration
    MAX_CONVERSATION_HISTORY = 20  # Giới hạn lịch sử hội thoại

    @classmethod
    def validate(cls):
        """Kiểm tra cấu hình có hợp lệ không"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY chưa được thiết lập! Chạy: export OPENAI_API_KEY='your-key'")
        return True
