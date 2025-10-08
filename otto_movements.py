"""
Otto Robot Movements Library
Thư viện các động tác cơ bản cho Otto robot
Sử dụng oscillation-based movement để chuyển động mượt mà
"""
import time
import math
import otto_config as config

class OttoMovements:
    """
    Thư viện động tác cho Otto
    """
    def __init__(self, controller):
        """
        Args:
            controller: Instance của OttoController
        """
        self.otto = controller

    def _oscillate(self, A, O, T, phase_diff):
        """
        Tạo chuyển động dao động mượt mà cho các servo

        Args:
            A: List amplitude (biên độ dao động) cho mỗi servo [4]
            O: List offset (độ lệch trung tâm) cho mỗi servo [4]
            T: Period (chu kỳ dao động) tính bằng ms
            phase_diff: List phase difference (độ lệch pha) cho mỗi servo [4] (radian)

        Công thức: angle = O + A * sin(2π * t/T + phase)
        """
        ref_time = time.time()
        end_time = ref_time + (T / 1000.0)

        while time.time() < end_time:
            elapsed = (time.time() - ref_time) * 1000  # ms

            angles = {}
            for i, pin in enumerate([config.RIGHT_ARM, config.LEFT_ARM,
                                     config.RIGHT_HIP, config.LEFT_HIP,
                                     config.RIGHT_FOOT, config.LEFT_FOOT][:4]):
                # Tính góc theo hàm sin
                angle = O[i] + A[i] * math.sin(2 * math.pi * elapsed / T + phase_diff[i])
                angle = 90 + angle  # Offset về neutral position
                angles[pin] = angle

            # Set tất cả servo cùng lúc
            self.otto.set_multiple_servos(angles, smooth=False)
            time.sleep(0.02)  # ~50Hz update rate

    # ===========================
    # Động tác cơ bản
    # ===========================

    def home_position(self):
        """Về vị trí đứng yên"""
        print("🏠 Otto về vị trí home")
        self.otto.reset_to_neutral()
        return "✅ Otto đã về vị trí home"

    def bow(self):
        """Cúi chào"""
        print("🙇 Otto cúi chào...")

        # Cúi xuống
        self.otto.set_multiple_servos({
            config.RIGHT_HIP: 110,
            config.LEFT_HIP: 70
        }, smooth=True, speed=config.SLOW_SPEED)
        time.sleep(1)

        # Đứng lên
        self.otto.reset_to_neutral()
        return "✅ Otto đã cúi chào"

    def wave_right(self):
        """Vẫy tay phải"""
        print("👋 Otto vẫy tay phải...")

        for _ in range(3):
            # Giơ tay
            self.otto.set_servo_angle(config.RIGHT_ARM, 130, smooth=True)
            time.sleep(0.3)
            # Hạ tay
            self.otto.set_servo_angle(config.RIGHT_ARM, 60, smooth=True)
            time.sleep(0.3)

        # Reset về neutral
        self.otto.set_servo_angle(config.RIGHT_ARM, 90, smooth=True)
        return "✅ Otto đã vẫy tay phải"

    def wave_left(self):
        """Vẫy tay trái"""
        print("👋 Otto vẫy tay trái...")

        for _ in range(3):
            self.otto.set_servo_angle(config.LEFT_ARM, 130, smooth=True)
            time.sleep(0.3)
            self.otto.set_servo_angle(config.LEFT_ARM, 60, smooth=True)
            time.sleep(0.3)

        self.otto.set_servo_angle(config.LEFT_ARM, 90, smooth=True)
        return "✅ Otto đã vẫy tay trái"

    def wave_both(self):
        """Vẫy cả 2 tay"""
        print("🙌 Otto vẫy cả 2 tay...")

        for _ in range(3):
            self.otto.set_multiple_servos({
                config.RIGHT_ARM: 130,
                config.LEFT_ARM: 130
            }, smooth=True)
            time.sleep(0.3)
            self.otto.set_multiple_servos({
                config.RIGHT_ARM: 60,
                config.LEFT_ARM: 60
            }, smooth=True)
            time.sleep(0.3)

        self.otto.reset_to_neutral()
        return "✅ Otto đã vẫy cả 2 tay"

    # ===========================
    # Động tác di chuyển
    # ===========================

    def walk_forward(self, steps=4, T=1000):
        """
        Đi bộ về phía trước (oscillation-based)

        Args:
            steps: Số bước đi
            T: Thời gian mỗi bước (ms), mặc định 1000ms
        """
        print(f"🚶 Otto đi bộ tiến {steps} bước...")

        # Mapping: [RIGHT_ARM, LEFT_ARM, RIGHT_HIP, LEFT_HIP]
        # Nhưng Otto chỉ dùng HIP và FOOT
        # Code gốc: RR(chân phải), RL(chân trái), YR(hông phải), YL(hông trái)
        # Map: [RR, RL, YR, YL]

        A = [15, 15, 30, 30]  # Biên độ: chân=15°, hông=30°
        O = [0, 0, 0, 0]       # Offset = 0 (dao động quanh neutral)
        phase_diff = [0, 0, math.pi/2, math.pi/2]  # Chân lệch pha 90° với hông

        # Thực hiện oscillation
        for _ in range(steps):
            self._oscillate_walk(A, O, T, phase_diff)

        return f"✅ Otto đã đi tiến {steps} bước"

    def _oscillate_walk(self, A, O, T, phase_diff):
        """
        Oscillation cho walk - mapping đúng servo pins
        [RR, RL, YR, YL] -> [RIGHT_FOOT, LEFT_FOOT, RIGHT_HIP, LEFT_HIP]
        """
        ref_time = time.time()
        end_time = ref_time + (T / 1000.0)

        while time.time() < end_time:
            elapsed = (time.time() - ref_time) * 1000

            # Map đúng servo pins
            pins = [config.RIGHT_FOOT, config.LEFT_FOOT, config.RIGHT_HIP, config.LEFT_HIP]
            angles = {}

            for i, pin in enumerate(pins):
                angle = O[i] + A[i] * math.sin(2 * math.pi * elapsed / T + phase_diff[i])
                angles[pin] = 90 + angle

            self.otto.set_multiple_servos(angles, smooth=False)
            time.sleep(0.02)

    def walk_backward(self, steps=4, T=1000):
        """Đi bộ lùi lại (oscillation-based)"""
        print(f"🔙 Otto đi bộ lùi {steps} bước...")

        A = [15, 15, 30, 30]
        O = [0, 0, 0, 0]
        phase_diff = [0, 0, -math.pi/2, -math.pi/2]  # Đảo ngược pha để đi lùi

        for _ in range(steps):
            self._oscillate_walk(A, O, T, phase_diff)

        return f"✅ Otto đã đi lùi {steps} bước"

    def turn_left(self, steps=2, T=3000):
        """Rẽ trái (oscillation-based)"""
        print(f"↪️  Otto rẽ trái {steps} bước...")

        A = [20, 20, 10, 30]  # Hông trái lớn hơn để rẽ trái
        O = [0, 0, 0, 0]
        phase_diff = [0, 0, math.pi/2, math.pi/2]

        for _ in range(steps):
            self._oscillate_walk(A, O, T, phase_diff)

        return f"✅ Otto đã rẽ trái {steps} bước"

    def turn_right(self, steps=2, T=3000):
        """Rẽ phải (oscillation-based)"""
        print(f"↩️  Otto rẽ phải {steps} bước...")

        A = [20, 20, 30, 10]  # Hông phải lớn hơn để rẽ phải
        O = [0, 0, 0, 0]
        phase_diff = [0, 0, math.pi/2, math.pi/2]

        for _ in range(steps):
            self._oscillate_walk(A, O, T, phase_diff)

        return f"✅ Otto đã rẽ phải {steps} bước"

    def moonwalk_left(self, steps=4, T=1000):
        """Moonwalk sang trái (Michael Jackson style)"""
        print(f"🕺 Otto moonwalk trái {steps} bước...")

        A = [25, 25, 0, 0]  # Chỉ chân dao động
        O = [-15, 15, 0, 0]  # Offset để tạo hiệu ứng trượt
        phase_diff = [0, math.pi + math.pi*2/3, math.pi/2, math.pi/2]

        for _ in range(steps):
            self._oscillate_walk(A, O, T, phase_diff)

        return f"✅ Otto đã moonwalk trái {steps} bước"

    def moonwalk_right(self, steps=4, T=1000):
        """Moonwalk sang phải"""
        print(f"🕺 Otto moonwalk phải {steps} bước...")

        A = [25, 25, 0, 0]
        O = [-15, 15, 0, 0]
        phase_diff = [0, math.pi - math.pi*2/3, math.pi/2, math.pi/2]

        for _ in range(steps):
            self._oscillate_walk(A, O, T, phase_diff)

        return f"✅ Otto đã moonwalk phải {steps} bước"

    def swing(self, steps=4, T=1000):
        """Lắc lư trai phải"""
        print(f"🎵 Otto đang lắc lư {steps} lần...")

        A = [25, 25, 0, 0]
        O = [-15, 15, 0, 0]
        phase_diff = [0, 0, math.pi/2, math.pi/2]

        for _ in range(steps):
            self._oscillate_walk(A, O, T, phase_diff)

        return f"✅ Otto đã lắc lư {steps} lần"

    def crusaito(self, steps=1, T=1000):
        """Bước crusaito (bước chéo)"""
        print(f"💃 Otto đang crusaito {steps} bước...")

        A = [25, 25, 30, 30]
        O = [-15, 15, 0, 0]
        phase_diff = [0, math.pi + math.pi*2/3, math.pi/2, math.pi/2]

        for _ in range(steps):
            self._oscillate_walk(A, O, T, phase_diff)

        return f"✅ Otto đã crusaito {steps} bước"

    def flapping(self, steps=4, T=1000):
        """Vỗ cánh"""
        print(f"🦅 Otto đang vỗ cánh {steps} lần...")

        A = [15, 15, 8, 8]
        O = [-15, 15, 0, 0]
        phase_diff = [0, math.pi, math.pi/2, -math.pi/2]

        for _ in range(steps):
            self._oscillate_walk(A, O, T, phase_diff)

        return f"✅ Otto đã vỗ cánh {steps} lần"

    # ===========================
    # Động tác cảm xúc
    # ===========================

    def happy(self):
        """Biểu hiện vui vẻ - nhảy nhót"""
        print("😊 Otto đang vui...")

        for _ in range(4):
            # Nhảy lên
            self.otto.set_multiple_servos({
                config.RIGHT_FOOT: 110,
                config.LEFT_FOOT: 70,
                config.RIGHT_ARM: 120,
                config.LEFT_ARM: 120
            }, smooth=True, speed=config.FAST_SPEED)
            time.sleep(0.2)

            # Nhảy xuống
            self.otto.set_multiple_servos({
                config.RIGHT_FOOT: 90,
                config.LEFT_FOOT: 90,
                config.RIGHT_ARM: 90,
                config.LEFT_ARM: 90
            }, smooth=True, speed=config.FAST_SPEED)
            time.sleep(0.2)

        return "✅ Otto đang vui vẻ!"

    def sad(self):
        """Biểu hiện buồn - cúi đầu"""
        print("😢 Otto đang buồn...")

        # Cúi đầu xuống
        self.otto.set_multiple_servos({
            config.RIGHT_HIP: 120,
            config.LEFT_HIP: 60,
            config.RIGHT_ARM: 70,
            config.LEFT_ARM: 70
        }, smooth=True, speed=config.SLOW_SPEED)
        time.sleep(2)

        # Về lại
        self.otto.reset_to_neutral()
        return "✅ Otto đang buồn..."

    def excited(self):
        """Biểu hiện hào hứng - vẫy tay nhanh"""
        print("🤩 Otto đang hào hứng...")

        for _ in range(5):
            self.otto.set_multiple_servos({
                config.RIGHT_ARM: 140,
                config.LEFT_ARM: 140
            }, smooth=False)
            time.sleep(0.1)
            self.otto.set_multiple_servos({
                config.RIGHT_ARM: 40,
                config.LEFT_ARM: 40
            }, smooth=False)
            time.sleep(0.1)

        self.otto.reset_to_neutral()
        return "✅ Otto rất hào hứng!"

    def confused(self):
        """Biểu hiện bối rối - lắc đầu"""
        print("🤔 Otto đang bối rối...")

        for _ in range(3):
            self.otto.set_servo_angle(config.RIGHT_HIP, 110, smooth=True)
            time.sleep(0.3)
            self.otto.set_servo_angle(config.RIGHT_HIP, 70, smooth=True)
            time.sleep(0.3)

        self.otto.reset_to_neutral()
        return "✅ Otto đang bối rối"

    def dance(self):
        """Nhảy múa"""
        print("💃 Otto đang nhảy...")

        # Sequence nhảy đơn giản
        for _ in range(2):
            # Bước 1
            self.otto.set_multiple_servos({
                config.RIGHT_ARM: 130,
                config.LEFT_ARM: 50,
                config.RIGHT_HIP: 110
            }, smooth=True, speed=config.FAST_SPEED)
            time.sleep(0.3)

            # Bước 2
            self.otto.set_multiple_servos({
                config.RIGHT_ARM: 50,
                config.LEFT_ARM: 130,
                config.LEFT_HIP: 70
            }, smooth=True, speed=config.FAST_SPEED)
            time.sleep(0.3)

            # Bước 3
            self.otto.set_multiple_servos({
                config.RIGHT_FOOT: 110,
                config.LEFT_FOOT: 70
            }, smooth=True, speed=config.FAST_SPEED)
            time.sleep(0.3)

            # Reset
            self.otto.reset_to_neutral()
            time.sleep(0.2)

        return "✅ Otto đã nhảy xong!"

    # ===========================
    # Advanced Movements
    # ===========================

    def run(self, steps=4, T=500):
        """Chạy nhanh"""
        print(f"🏃 Otto đang chạy {steps} bước...")

        A = [10, 10, 10, 10]  # Biên độ nhỏ hơn, tốc độ nhanh hơn
        O = [0, 0, 0, 0]
        phase_diff = [0, 0, math.pi/2, math.pi/2]

        for _ in range(steps):
            self._oscillate_walk(A, O, T, phase_diff)

        return f"✅ Otto đã chạy {steps} bước"

    def jump(self, steps=1):
        """Nhảy lên"""
        print(f"🦘 Otto đang nhảy {steps} lần...")

        for _ in range(steps):
            # Nhảy lên
            self.otto.set_multiple_servos({
                config.RIGHT_FOOT: 140,
                config.LEFT_FOOT: 40
            }, smooth=True, speed=1)
            time.sleep(0.1)

            # Hạ xuống
            self.otto.set_multiple_servos({
                config.RIGHT_FOOT: 90,
                config.LEFT_FOOT: 90
            }, smooth=True, speed=1)
            time.sleep(0.2)

        return f"✅ Otto đã nhảy {steps} lần"

    def tiptoe_swing(self, steps=4, T=900):
        """Lắc lư trên mũi chân"""
        print(f"🩰 Otto đang lắc mũi chân {steps} lần...")

        A = [0, 0, 25, 25]  # Chỉ hông dao động
        O = [10, -10, 0, 0]  # Nâng nhẹ chân lên
        phase_diff = [0, 0, 0, math.pi]

        for _ in range(steps):
            self._oscillate_walk(A, O, T, phase_diff)

        return f"✅ Otto đã lắc mũi chân {steps} lần"

    def jitter(self, steps=4, T=500):
        """Run rẩy (jitter)"""
        print(f"😰 Otto đang run {steps} lần...")

        A = [20, 20, 10, 10]  # Chuyển động nhanh, nhỏ
        O = [0, 0, 0, 0]
        phase_diff = [0, math.pi, math.pi/2, -math.pi/2]

        for _ in range(steps):
            self._oscillate_walk(A, O, T, phase_diff)

        return f"✅ Otto đã run {steps} lần"

    def shake_leg(self, steps=4, direction=1):
        """Lắc chân trái/phải"""
        print(f"🦵 Otto đang lắc chân {steps} lần...")

        for _ in range(steps):
            if direction == 1:  # Lắc chân phải
                self.otto.set_multiple_servos({
                    config.RIGHT_HIP: 110,
                    config.LEFT_HIP: 70
                }, smooth=True, speed=3)
                time.sleep(0.15)
            else:  # Lắc chân trái
                self.otto.set_multiple_servos({
                    config.RIGHT_HIP: 70,
                    config.LEFT_HIP: 110
                }, smooth=True, speed=3)
                time.sleep(0.15)

            self.otto.reset_to_neutral()
            time.sleep(0.15)

        return f"✅ Otto đã lắc chân {steps} lần"

    def updown(self, steps=4, T=1000):
        """Chuyển động lên xuống"""
        print(f"⬆️⬇️  Otto đang chuyển động lên xuống {steps} lần...")

        A = [25, 25, 0, 0]
        O = [-15, 15, 0, 0]
        phase_diff = [math.pi, 0, math.pi*3/2, math.pi*3/2]

        for _ in range(steps):
            self._oscillate_walk(A, O, T, phase_diff)

        return f"✅ Otto đã chuyển động lên xuống {steps} lần"

    # ===========================
    # More Emotional Expressions
    # ===========================

    def angry(self):
        """Biểu hiện tức giận"""
        print("😠 Otto đang tức giận...")

        for _ in range(3):
            # Dậm chân
            self.otto.set_multiple_servos({
                config.RIGHT_FOOT: 120,
                config.RIGHT_HIP: 110
            }, smooth=False)
            time.sleep(0.1)
            self.otto.set_multiple_servos({
                config.RIGHT_FOOT: 90,
                config.RIGHT_HIP: 90
            }, smooth=False)
            time.sleep(0.1)

        # Giơ tay lên giận dữ
        self.otto.set_multiple_servos({
            config.RIGHT_ARM: 140,
            config.LEFT_ARM: 140
        }, smooth=True, speed=2)
        time.sleep(0.5)

        self.otto.reset_to_neutral()
        return "✅ Otto đang tức giận!"

    def scared(self):
        """Biểu hiện sợ hãi - co rúm lại"""
        print("😨 Otto đang sợ...")

        # Co rúm lại
        self.otto.set_multiple_servos({
            config.RIGHT_HIP: 70,
            config.LEFT_HIP: 110,
            config.RIGHT_FOOT: 120,
            config.LEFT_FOOT: 60,
            config.RIGHT_ARM: 60,
            config.LEFT_ARM: 60
        }, smooth=True, speed=config.SLOW_SPEED)
        time.sleep(1.5)

        # Run rẩy
        for _ in range(5):
            self.otto.set_multiple_servos({
                config.RIGHT_HIP: 75,
                config.LEFT_HIP: 105
            }, smooth=False)
            time.sleep(0.05)
            self.otto.set_multiple_servos({
                config.RIGHT_HIP: 70,
                config.LEFT_HIP: 110
            }, smooth=False)
            time.sleep(0.05)

        self.otto.reset_to_neutral()
        return "✅ Otto đang sợ hãi"

    def sleepy(self):
        """Biểu hiện buồn ngủ - ngáp và cúi đầu"""
        print("😴 Otto đang buồn ngủ...")

        # Ngáp (giơ tay lên)
        self.otto.set_multiple_servos({
            config.RIGHT_ARM: 140,
            config.LEFT_ARM: 140
        }, smooth=True, speed=config.SLOW_SPEED)
        time.sleep(1)

        # Hạ tay xuống
        self.otto.set_multiple_servos({
            config.RIGHT_ARM: 90,
            config.LEFT_ARM: 90
        }, smooth=True, speed=config.SLOW_SPEED)
        time.sleep(0.5)

        # Cúi đầu buồn ngủ
        self.otto.set_multiple_servos({
            config.RIGHT_HIP: 110,
            config.LEFT_HIP: 70
        }, smooth=True, speed=config.SLOW_SPEED)
        time.sleep(2)

        self.otto.reset_to_neutral()
        return "✅ Otto đang buồn ngủ"

    def love(self):
        """Biểu hiện yêu thương - vẽ hình trái tim"""
        print("❤️  Otto đang thể hiện tình yêu...")

        # Vẫy tay nhẹ nhàng
        for _ in range(3):
            self.otto.set_multiple_servos({
                config.RIGHT_ARM: 120,
                config.LEFT_ARM: 120
            }, smooth=True, speed=config.SLOW_SPEED)
            time.sleep(0.3)
            self.otto.set_multiple_servos({
                config.RIGHT_ARM: 100,
                config.LEFT_ARM: 100
            }, smooth=True, speed=config.SLOW_SPEED)
            time.sleep(0.3)

        # Lắc lư nhẹ nhàng (swing)
        self.swing(2, 1200)

        self.otto.reset_to_neutral()
        return "✅ Otto đang thể hiện tình yêu"

    def surprised(self):
        """Biểu hiện ngạc nhiên - nhảy lùi"""
        print("😲 Otto đang ngạc nhiên...")

        # Giật mình
        self.otto.set_multiple_servos({
            config.RIGHT_FOOT: 120,
            config.LEFT_FOOT: 60,
            config.RIGHT_ARM: 140,
            config.LEFT_ARM: 140
        }, smooth=False)
        time.sleep(0.2)

        # Nhảy lùi
        self.walk_backward(2, 800)

        self.otto.reset_to_neutral()
        return "✅ Otto đang ngạc nhiên!"

    # ===========================
    # Utility
    # ===========================

    def get_available_actions(self):
        """
        Trả về danh sách tất cả các động tác có thể thực hiện
        """
        return {
            "basic": ["home_position", "bow", "wave_right", "wave_left", "wave_both"],
            "movement": ["walk_forward", "walk_backward", "turn_left", "turn_right",
                        "run", "jump", "moonwalk_left", "moonwalk_right"],
            "dance": ["dance", "swing", "crusaito", "flapping", "tiptoe_swing",
                     "jitter", "shake_leg", "updown"],
            "emotion": ["happy", "sad", "excited", "confused", "angry", "scared",
                       "sleepy", "love", "surprised"]
        }
