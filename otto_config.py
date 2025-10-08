"""
Otto Robot Configuration
Cấu hình servo pins, góc, và I2C address cho PCA9685
"""

# ===========================
# I2C Configuration
# ===========================
PCA9685_ADDRESS = 0x40  # Địa chỉ I2C mặc định (không hàn jumper)
SERVO_FREQ = 50         # Tần số PWM cho servo (50Hz)

# ===========================
# Servo Pin Mapping trên PCA9685
# ===========================
# Tay
RIGHT_ARM = 0   # Tay phải
LEFT_ARM = 4    # Tay trái

# Chân phải
RIGHT_HIP = 1   # Hông phải
RIGHT_FOOT = 2  # Bàn chân phải

# Chân trái
LEFT_HIP = 5    # Hông trái
LEFT_FOOT = 6   # Bàn chân trái

# ===========================
# Servo Angle Limits
# ===========================
# Góc tối thiểu và tối đa cho mỗi servo (để bảo vệ servo)
SERVO_MIN = 0
SERVO_MAX = 180

# ===========================
# Neutral Positions (góc đứng yên)
# ===========================
NEUTRAL_POSITIONS = {
    RIGHT_ARM: 90,
    LEFT_ARM: 90,
    RIGHT_HIP: 90,
    RIGHT_FOOT: 90,
    LEFT_HIP: 90,
    LEFT_FOOT: 90
}

# ===========================
# PWM Range for SG90 Servo
# ===========================
# SG90 thường hoạt động ở xung 1ms (0°) đến 2ms (180°)
# Với tần số 50Hz (chu kỳ 20ms), mỗi chu kỳ chia thành 4096 bước
SERVO_MIN_PULSE = 150   # Xung tương ứng 0° (~1ms)
SERVO_MAX_PULSE = 600   # Xung tương ứng 180° (~2ms)

# ===========================
# Movement Speed
# ===========================
DEFAULT_SPEED = 10      # Tốc độ di chuyển mặc định (ms giữa các bước)
SLOW_SPEED = 30         # Chậm
FAST_SPEED = 5          # Nhanh

# ===========================
# Helper Functions
# ===========================
def angle_to_pulse(angle):
    """
    Chuyển đổi góc (0-180) sang giá trị PWM pulse (150-600)
    """
    if angle < SERVO_MIN:
        angle = SERVO_MIN
    if angle > SERVO_MAX:
        angle = SERVO_MAX

    pulse = SERVO_MIN_PULSE + (angle / 180.0) * (SERVO_MAX_PULSE - SERVO_MIN_PULSE)
    return int(pulse)

def get_all_servos():
    """
    Trả về list tất cả servo pins
    """
    return [RIGHT_ARM, LEFT_ARM, RIGHT_HIP, RIGHT_FOOT, LEFT_HIP, LEFT_FOOT]
