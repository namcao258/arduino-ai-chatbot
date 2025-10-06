"""
Arduino Controller - Quản lý kết nối và điều khiển Arduino
"""
from pyfirmata import Arduino, util
from config import Config

class ArduinoController:
    def __init__(self, port=None, led_pin=None):
        """
        Khởi tạo kết nối Arduino

        Args:
            port: Cổng serial (mặc định từ Config)
            led_pin: Chân LED (mặc định từ Config)
        """
        self.port = port or Config.ARDUINO_PORT
        self.led_pin = led_pin or Config.LED_PIN
        self.board = None
        self.is_connected = False

    def connect(self):
        """Kết nối với Arduino"""
        try:
            self.board = Arduino(self.port)
            self.is_connected = True
            print(f"✅ Đã kết nối Arduino tại {self.port}")
            return True
        except Exception as e:
            print(f"❌ Lỗi kết nối Arduino: {e}")
            print(f"   Kiểm tra: ls /dev/tty* để xem cổng khả dụng")
            self.is_connected = False
            return False

    def turn_on_led(self):
        """Bật LED"""
        if not self.is_connected:
            return "❌ Arduino chưa kết nối"

        try:
            self.board.digital[self.led_pin].write(1)
            return f"✅ Đã bật LED tại pin {self.led_pin}"
        except Exception as e:
            return f"❌ Lỗi bật LED: {e}"

    def turn_off_led(self):
        """Tắt LED"""
        if not self.is_connected:
            return "❌ Arduino chưa kết nối"

        try:
            self.board.digital[self.led_pin].write(0)
            return f"✅ Đã tắt LED tại pin {self.led_pin}"
        except Exception as e:
            return f"❌ Lỗi tắt LED: {e}"

    def control_led(self, action):
        """
        Điều khiển LED theo action

        Args:
            action: "on" hoặc "off"

        Returns:
            str: Kết quả thực hiện
        """
        if action == "on":
            return self.turn_on_led()
        elif action == "off":
            return self.turn_off_led()
        else:
            return f"❌ Action không hợp lệ: {action}"

    def disconnect(self):
        """Ngắt kết nối Arduino"""
        if self.board:
            self.board.exit()
            self.is_connected = False
            print("🔌 Đã ngắt kết nối Arduino")

    def __enter__(self):
        """Context manager - tự động kết nối"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager - tự động ngắt kết nối"""
        self.disconnect()
