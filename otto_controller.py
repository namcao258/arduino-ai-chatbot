"""
Otto Robot Controller
Điều khiển Otto robot qua PCA9685 I2C PWM driver sử dụng PyFirmata
"""
import time
import pyfirmata
import otto_config as config

class OttoController:
    """
    Controller chính để điều khiển Otto robot qua PyFirmata I2C
    """
    def __init__(self, port='/dev/ttyACM0'):
        """
        Khởi tạo kết nối Arduino và PCA9685

        Args:
            port: Cổng serial Arduino (mặc định /dev/ttyACM0)
        """
        try:
            # Kết nối Arduino
            self.board = pyfirmata.Arduino(port)
            time.sleep(2)  # Đợi Arduino khởi động

            print("🔌 Đã kết nối Arduino")

            # Bật I2C mode
            self.board.send_sysex(0x78, [0])  # I2C_CONFIG
            time.sleep(0.1)

            print("📡 Đã bật I2C mode")

            # Khởi tạo PCA9685
            self._init_pca9685()

            # Lưu trạng thái góc hiện tại của các servo
            self.current_angles = config.NEUTRAL_POSITIONS.copy()

            # Đưa tất cả servo về vị trí neutral
            self.reset_to_neutral()

            print("✅ Otto Controller đã khởi tạo thành công!")

        except Exception as e:
            print(f"❌ Lỗi khởi tạo Otto Controller: {e}")
            raise

    def _init_pca9685(self):
        """
        Khởi tạo PCA9685: Set frequency = 50Hz cho servo
        """
        addr = config.PCA9685_ADDRESS

        # PCA9685 MODE1 register = 0x00
        # Sleep mode để set frequency
        self._i2c_write(addr, 0x00, 0x10)
        time.sleep(0.005)

        # Set prescale cho 50Hz
        # prescale = round(25MHz / (4096 * 50Hz)) - 1 = 121
        prescale = 121
        self._i2c_write(addr, 0xFE, prescale)
        time.sleep(0.005)

        # Wake up, auto-increment
        self._i2c_write(addr, 0x00, 0x20)
        time.sleep(0.005)

        print(f"🎛️  PCA9685 đã set frequency = {config.SERVO_FREQ}Hz")

    def _i2c_write(self, device_address, register, value):
        """
        Ghi 1 byte vào I2C device

        Args:
            device_address: Địa chỉ I2C (0x40 cho PCA9685)
            register: Register address
            value: Giá trị cần ghi
        """
        # I2C_REQUEST format:
        # [slave_address, mode, register_low, register_high, data_low, data_high]
        # mode: 0x00 = WRITE
        data = [
            device_address,
            0x00,  # I2C_WRITE mode
            register & 0x7F,
            (register >> 7) & 0x7F,
            value & 0x7F,
            (value >> 7) & 0x7F
        ]
        self.board.send_sysex(0x76, data)  # 0x76 = I2C_REQUEST
        time.sleep(0.001)

    def _set_pwm(self, channel, on_time, off_time):
        """
        Set PWM cho một channel trên PCA9685

        Args:
            channel: Channel number (0-15)
            on_time: Thời điểm bật (0-4095)
            off_time: Thời điểm tắt (0-4095)
        """
        addr = config.PCA9685_ADDRESS

        # LED0_ON_L register = 0x06 + 4*channel
        base_reg = 0x06 + (4 * channel)

        # Ghi 4 bytes: ON_L, ON_H, OFF_L, OFF_H
        self._i2c_write(addr, base_reg, on_time & 0xFF)
        self._i2c_write(addr, base_reg + 1, (on_time >> 8) & 0xFF)
        self._i2c_write(addr, base_reg + 2, off_time & 0xFF)
        self._i2c_write(addr, base_reg + 3, (off_time >> 8) & 0xFF)

    def set_servo_angle(self, pin, angle, smooth=False, speed=None):
        """
        Đặt góc cho một servo

        Args:
            pin: Chân servo trên PCA9685 (0-15)
            angle: Góc mục tiêu (0-180)
            smooth: Di chuyển mượt hay nhảy thẳng
            speed: Tốc độ di chuyển (ms giữa mỗi bước)
        """
        # Giới hạn góc
        angle = max(config.SERVO_MIN, min(config.SERVO_MAX, angle))

        if not smooth:
            # Di chuyển trực tiếp
            pulse = config.angle_to_pulse(angle)
            self._set_pwm(pin, 0, pulse)
            self.current_angles[pin] = angle
        else:
            # Di chuyển mượt
            current_angle = self.current_angles.get(pin, config.NEUTRAL_POSITIONS[pin])
            step_speed = speed if speed else config.DEFAULT_SPEED
            step_size = 1 if angle > current_angle else -1

            for a in range(int(current_angle), int(angle), step_size):
                pulse = config.angle_to_pulse(a)
                self._set_pwm(pin, 0, pulse)
                time.sleep(step_speed / 1000.0)

            # Đặt góc cuối cùng
            pulse = config.angle_to_pulse(angle)
            self._set_pwm(pin, 0, pulse)
            self.current_angles[pin] = angle

    def set_multiple_servos(self, angles_dict, smooth=False, speed=None):
        """
        Đặt góc cho nhiều servo cùng lúc

        Args:
            angles_dict: Dict {pin: angle}
            smooth: Di chuyển mượt
            speed: Tốc độ di chuyển
        """
        if smooth:
            # Tính toán số bước cần thiết cho mỗi servo
            current_angles = {}
            target_angles = {}
            max_steps = 0

            for pin, target in angles_dict.items():
                current = self.current_angles.get(pin, config.NEUTRAL_POSITIONS[pin])
                current_angles[pin] = current
                target_angles[pin] = target
                steps = abs(target - current)
                max_steps = max(max_steps, steps)

            # Di chuyển từng bước
            step_speed = speed if speed else config.DEFAULT_SPEED
            for step in range(int(max_steps) + 1):
                for pin, target in target_angles.items():
                    current = current_angles[pin]
                    progress = step / max_steps if max_steps > 0 else 1
                    new_angle = current + (target - current) * progress
                    pulse = config.angle_to_pulse(new_angle)
                    self._set_pwm(pin, 0, pulse)
                time.sleep(step_speed / 1000.0)

            # Update current angles
            for pin, angle in target_angles.items():
                self.current_angles[pin] = angle
        else:
            # Đặt trực tiếp
            for pin, angle in angles_dict.items():
                pulse = config.angle_to_pulse(angle)
                self._set_pwm(pin, 0, pulse)
                self.current_angles[pin] = angle

    def reset_to_neutral(self):
        """
        Đưa tất cả servo về vị trí neutral (đứng yên)
        """
        print("🤖 Otto đang reset về vị trí neutral...")
        self.set_multiple_servos(config.NEUTRAL_POSITIONS, smooth=True, speed=config.SLOW_SPEED)
        time.sleep(0.5)

    def get_current_angles(self):
        """
        Lấy góc hiện tại của tất cả servo
        """
        return self.current_angles.copy()

    def execute_movement_sequence(self, sequence, speed=None):
        """
        Thực hiện một chuỗi động tác

        Args:
            sequence: List of dicts [{servo_angles}, delay_ms]
            speed: Tốc độ di chuyển

        Example:
            sequence = [
                ({config.RIGHT_ARM: 120}, 500),  # Giơ tay phải, đợi 500ms
                ({config.RIGHT_ARM: 90}, 500)    # Hạ tay, đợi 500ms
            ]
        """
        for move in sequence:
            angles_dict = move[0]
            delay = move[1] if len(move) > 1 else 500

            self.set_multiple_servos(angles_dict, smooth=True, speed=speed)
            time.sleep(delay / 1000.0)

    def cleanup(self):
        """
        Dọn dẹp khi kết thúc
        """
        try:
            self.reset_to_neutral()
            self.board.exit()
            print("👋 Otto Controller đã dọn dẹp xong")
        except:
            pass
