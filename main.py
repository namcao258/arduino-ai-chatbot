"""
Main Entry Point - Chương trình chính kết hợp Otto Robot và AI Chatbot
"""
from otto_controller import OttoController
from otto_movements import OttoMovements
from music_controller import MusicController
from youtube_player import YouTubePlayer
from llm_handler import LLMHandler

def print_welcome():
    """In thông tin chào mừng"""
    print("=" * 60)
    print("🤖 AI CHATBOT THÔNG MINH - ĐIỀU KHIỂN OTTO ROBOT & NHẠC")
    print("=" * 60)
    print("✨ AI có khả năng SUY LUẬN và HỌC từ bạn!")
    print("\nVí dụ:")
    print("  • 'Nhảy đi Otto' → Otto nhảy")
    print("  • 'Vui quá!' → AI hiểu cảm xúc → Otto nhảy vui")
    print("  • 'Chào bạn' → Otto vẫy tay/cúi chào")
    print("  • 'Phát nhạc EDM' → Tìm và phát nhạc EDM")
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

    # Khởi tạo Otto Controller
    try:
        otto_ctrl = OttoController()
        otto_moves = OttoMovements(otto_ctrl)
        print("🤖 Otto Robot đã sẵn sàng!")
    except Exception as e:
        print(f"❌ Không thể khởi tạo Otto Robot: {e}")
        print("   1. Arduino + PCA9685 đã kết nối chưa?")
        print("   2. I2C address đúng chưa? (0x40)")
        print("   3. Các servo đã cắm đúng chân chưa?")
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
                otto_ctrl.cleanup()
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

            # Debug: In ra response để kiểm tra
            print(f"🔍 DEBUG - needs_function_call: {response['needs_function_call']}")
            if response['needs_function_call']:
                print(f"🔍 DEBUG - function_name: {response['function_name']}")
                print(f"🔍 DEBUG - function_args: {response['function_args']}")

            # Kiểm tra xem có cần gọi function không
            if response["needs_function_call"]:
                function_name = response["function_name"]
                function_args = response["function_args"]

                # Thực thi function tương ứng
                if function_name == "control_otto":
                    action = function_args.get("action")
                    emotion = function_args.get("emotion")
                    steps = function_args.get("steps")
                    reason = function_args.get("reason", "")

                    # Thực hiện động tác
                    try:
                        if emotion:
                            # Thực hiện theo cảm xúc
                            emotion_method = getattr(otto_moves, emotion, None)
                            if emotion_method:
                                result = emotion_method()
                            else:
                                result = f"❌ Cảm xúc '{emotion}' không hợp lệ"
                        elif action:
                            # Thực hiện động tác cụ thể
                            action_method = getattr(otto_moves, action, None)
                            if action_method:
                                # List các động tác cần tham số steps
                                movements_with_steps = [
                                    'walk_forward', 'walk_backward', 'turn_left', 'turn_right',
                                    'run', 'jump', 'moonwalk_left', 'moonwalk_right',
                                    'swing', 'crusaito', 'flapping', 'tiptoe_swing',
                                    'jitter', 'shake_leg', 'updown'
                                ]

                                if action in movements_with_steps and steps:
                                    result = action_method(steps)
                                elif action in movements_with_steps:
                                    # Dùng default steps
                                    result = action_method()
                                else:
                                    result = action_method()
                            else:
                                result = f"❌ Động tác '{action}' không hợp lệ"
                        else:
                            result = "❌ Không có action hoặc emotion được chỉ định"

                        print(f"🤖 {result}")
                        if reason:
                            print(f"💭 Lý do: {reason}")

                        # Ghi nhận vào memory
                        llm.record_action_to_memory(action or emotion, reason)

                        # Thêm kết quả vào lịch sử
                        llm.add_function_result(function_name, result)

                        # Gọi lại AI để tạo response cuối cùng
                        final_response = llm.get_final_response()
                        print(f"AI: {final_response}")

                    except Exception as e:
                        print(f"❌ Lỗi khi thực hiện động tác: {e}")

                elif function_name == "control_music":
                    action = function_args.get("action")
                    reason = function_args.get("reason", "")
                    result = music.control_music(action)

                    # Cập nhật music status vào context memory
                    if action == "play":
                        llm.context_memory.update_music_status("playing")
                    elif action == "pause":
                        llm.context_memory.update_music_status("paused")
                    elif action == "stop":
                        llm.context_memory.update_music_status("stopped")

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
                        full_song_name = f"{song_name} - {artist}" if artist else song_name
                    elif mood:
                        # Phát nhạc theo tâm trạng
                        result = youtube.play_by_mood(mood)
                        full_song_name = f"Nhạc {mood}"
                    elif genre:
                        # Phát nhạc theo thể loại
                        result = youtube.play_by_genre(genre)
                        full_song_name = f"Nhạc {genre}"
                    else:
                        # Tìm kiếm chung
                        query = reason if reason else "popular music 2024"
                        result = youtube.search_and_play(query)
                        full_song_name = query

                    # Cập nhật vào context memory
                    llm.context_memory.update_music_status("playing", full_song_name)

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
        print("🔌 Đang dọn dẹp Otto Robot...")
        otto_ctrl.cleanup()

if __name__ == "__main__":
    main()
