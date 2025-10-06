from pyfirmata import Arduino, util
import time

# Cổng kết nối Arduino (ví dụ: COM3 trên Windows hoặc /dev/ttyACM0 trên Ubuntu)
board = Arduino('/dev/ttyACM0')

print("Kết nối Arduino thành công!")

led_pin = 13  # chân LED tích hợp sẵn trên Arduino Uno

try:
    while True:
        print("Bật LED")
        board.digital[led_pin].write(1)  # bật LED
        time.sleep(1)

        print("Tắt LED")
        board.digital[led_pin].write(0)  # tắt LED
        time.sleep(1)

except KeyboardInterrupt:
    print("Kết thúc chương trình.")
    board.exit()
