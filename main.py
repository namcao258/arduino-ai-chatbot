"""
Main Entry Point - Chương trình chính kết hợp Arduino và AI Chatbot
"""
from arduino_controller import ArduinoController
from music_controller import MusicController
from youtube_player import YouTubePlayer
from llm_handler import LLMHandler

def print_welcome():
    """In thông tin chào mừng"""
    print("=" * 60)
    print("🤖 AI CHATBOT THÔNG MINH - ĐIỀU KHIỂN ĐÈN & NHẠC")
    print("=" * 60)
    print("✨ AI có khả năng SUY LUẬN và HỌC từ bạn!")
    print("\nVí dụ:")
    print("  • 'Tôi sắp đọc sách' → AI hiểu cần sáng → Bật đèn")
    print("  • 'Buồn quá' → AI hiểu cần nhạc → Bật nhạc")
    print("  • 'Mệt quá, muốn ngủ' → AI hiểu cần tối → Tắt đèn & nhạc")
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

        # Khởi tạo Music Controller
        music = MusicController()
        print("🎵 Music Controller đã khởi tạo")

        # Khởi tạo YouTube Player
        youtube = YouTubePlayer()
        print("📺 YouTube Player đã khởi tạo")

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

                    elif function_name == "control_music":
                        action = function_args.get("action")
                        reason = function_args.get("reason", "")
                        result = music.control_music(action)

                        print(f"🎵 {result}")
                        if reason:
                            print(f"💭 Lý do: {reason}")

                        # Ghi nhận vào memory để học
                        llm.record_action_to_memory(action, reason)

                        # Thêm kết quả vào lịch sử
                        llm.add_function_result(function_name, result)

                        # Gọi lại AI để tạo response cuối cùng
                        final_response = llm.get_final_response()
                        print(f"AI: {final_response}")

                    elif function_name == "play_youtube_music":
                        song_name = function_args.get("song_name")
                        artist = function_args.get("artist")
                        mood = function_args.get("mood")
                        genre = function_args.get("genre")
                        reason = function_args.get("reason", "")

                        # Xác định cách phát nhạc
                        if song_name or artist:
                            # Phát bài hát cụ thể
                            result = youtube.play_specific_song(song_name or "", artist)
                        elif mood:
                            # Phát nhạc theo tâm trạng
                            result = youtube.play_by_mood(mood)
                        elif genre:
                            # Phát nhạc theo thể loại
                            result = youtube.play_by_genre(genre)
                        else:
                            # Tìm kiếm chung
                            query = reason if reason else "popular music 2024"
                            result = youtube.search_and_play(query)

                        print(f"🎵 {result}")
                        if reason:
                            print(f"💭 Lý do: {reason}")

                        # Ghi nhận vào memory
                        llm.record_action_to_memory("play_youtube", reason)

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
