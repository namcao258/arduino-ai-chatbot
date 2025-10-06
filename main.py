"""
Main Entry Point - Chương trình chính kết hợp Arduino và AI Chatbot
"""
from arduino_controller import ArduinoController
from llm_handler import LLMHandler

def print_welcome():
    """In thông tin chào mừng"""
    print("=" * 60)
    print("🤖 AI CHATBOT THÔNG MINH - ĐIỀU KHIỂN ĐÈN ARDUINO")
    print("=" * 60)
    print("✨ AI có khả năng SUY LUẬN và HỌC từ bạn!")
    print("\nVí dụ:")
    print("  • 'Tôi sắp đọc sách' → AI hiểu cần sáng → Bật đèn")
    print("  • 'Mệt quá, muốn ngủ' → AI hiểu cần tối → Tắt đèn")
    print("  • 'Trời mưa ảm đạm' → AI hiểu cần ấm → Bật đèn")
    print("\nLệnh đặc biệt:")
    print("  • 'stats' - Xem AI đã học được gì")
    print("  • 'reset' - Xóa lịch sử hội thoại")
    print("  • 'clear' - Xóa toàn bộ memory đã học")
    print("  • 'exit' - Thoát")
    print("=" * 60)
    print()

def main():
    """Hàm chính"""
    print_welcome()

    # Khởi tạo Arduino Controller với context manager
    with ArduinoController() as arduino:
        if not arduino.is_connected:
            print("❌ Không thể kết nối Arduino. Vui lòng kiểm tra:")
            print("   1. Arduino đã cắm USB chưa?")
            print("   2. Đã upload StandardFirmata chưa?")
            print("   3. Cổng serial đúng chưa? (kiểm tra: ls /dev/tty*)")
            return

        # Khởi tạo LLM Handler
        try:
            llm = LLMHandler()
        except ValueError as e:
            print(f"❌ {e}")
            return

        print("✅ Hệ thống sẵn sàng! Hãy chat với AI...\n")

        # Main loop
        try:
            while True:
                # Nhận input từ người dùng
                user_input = input("Bạn: ").strip()

                if not user_input:
                    continue

                # Xử lý lệnh đặc biệt
                if user_input.lower() in ['exit', 'quit', 'thoát']:
                    print("👋 Tạm biệt!")
                    break

                if user_input.lower() == 'reset':
                    llm.reset_conversation()
                    continue

                if user_input.lower() == 'stats':
                    print("\n📊 THỐNG KÊ AI ĐÃ HỌC:")
                    print(llm.get_learned_stats())
                    continue

                if user_input.lower() == 'clear':
                    confirm = input("⚠️  Xóa toàn bộ memory đã học? (yes/no): ")
                    if confirm.lower() in ['yes', 'y']:
                        llm.context_memory.clear_memory()
                    else:
                        print("Đã hủy!")
                    continue

                # Gửi tin nhắn tới AI
                response = llm.get_response(user_input)

                # Kiểm tra xem có cần gọi function không
                if response["needs_function_call"]:
                    function_name = response["function_name"]
                    function_args = response["function_args"]

                    # Thực thi function tương ứng
                    if function_name == "control_led":
                        action = function_args.get("action")
                        reason = function_args.get("reason", "")
                        result = arduino.control_led(action)

                        print(f"🔧 {result}")
                        if reason:
                            print(f"💭 Lý do: {reason}")

                        # Ghi nhận vào memory để học
                        llm.record_action_to_memory(action, reason)

                        # Thêm kết quả vào lịch sử
                        llm.add_function_result(function_name, result)

                        # Gọi lại AI để tạo response cuối cùng
                        final_response = llm.get_final_response()
                        print(f"AI: {final_response}")
                    else:
                        print(f"❌ Function không xác định: {function_name}")
                else:
                    # AI trả lời bình thường
                    print(f"AI: {response['message']}")

                print()  # Dòng trống để dễ đọc

        except KeyboardInterrupt:
            print("\n\n⚠️  Đã nhận Ctrl+C - Đang thoát...")
        except Exception as e:
            print(f"\n❌ Lỗi không mong đợi: {e}")
        finally:
            print("🔌 Đang ngắt kết nối Arduino...")

if __name__ == "__main__":
    main()
