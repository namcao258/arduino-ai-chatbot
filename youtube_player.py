"""
YouTube Player - Tự động tìm và phát nhạc YouTube
"""
import subprocess
import platform
from youtubesearchpython import VideosSearch
import webbrowser
import os

class YouTubePlayer:
    def __init__(self):
        """Khởi tạo YouTube Player"""
        self.system = platform.system()
        self.current_url = None

    def search_and_play(self, query, max_results=1):
        """
        Tìm kiếm và phát nhạc từ YouTube

        Args:
            query: Từ khóa tìm kiếm (tên bài hát, ca sĩ...)
            max_results: Số kết quả tìm kiếm (mặc định 1)

        Returns:
            str: Kết quả thực hiện
        """
        try:
            # Tìm kiếm và lấy URL video đầu tiên bằng yt-dlp
            print(f"🔍 Đang tìm kiếm: {query}...")

            # Dùng yt-dlp để tìm kiếm
            result = subprocess.run(
                ['yt-dlp', '--get-id', '--get-title', f'ytsearch1:{query}'],
                capture_output=True,
                text=True,
                check=True
            )

            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                video_title = lines[0]
                video_id = lines[1]
                video_url = f"https://www.youtube.com/watch?v={video_id}"

                print(f"🎵 Đã tìm thấy: {video_title}")

                # Mở video trực tiếp
                webbrowser.open(video_url)

                self.current_url = video_url
                return f"✅ Đang phát: {video_title}"
            else:
                return f"❌ Không tìm thấy kết quả cho: {query}"

        except subprocess.CalledProcessError:
            # Fallback: Mở trang tìm kiếm nếu yt-dlp lỗi
            print("⚠️  yt-dlp không khả dụng, dùng tìm kiếm thông thường")
            import urllib.parse
            search_query = urllib.parse.quote(query)
            search_url = f"https://www.youtube.com/results?search_query={search_query}"
            webbrowser.open(search_url)
            return f"✅ Đã mở YouTube tìm kiếm: {query} (bạn click vào video đầu tiên nhé)"

        except Exception as e:
            return f"❌ Lỗi tìm kiếm YouTube: {e}"

    def _play_url(self, url, title):
        """
        Phát URL YouTube

        Args:
            url: YouTube URL
            title: Tiêu đề video

        Returns:
            str: Kết quả
        """
        try:
            if self.system == "Linux":
                # Thử các browser theo thứ tự ưu tiên
                browsers = [
                    'google-chrome',
                    'chromium-browser',
                    'firefox',
                    'microsoft-edge'
                ]

                for browser in browsers:
                    try:
                        # Mở browser ở chế độ nền (không focus)
                        subprocess.Popen(
                            [browser, '--new-window', url],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                        return f"✅ Đang phát: {title}"
                    except FileNotFoundError:
                        continue

                # Fallback: dùng webbrowser
                webbrowser.open(url)
                return f"✅ Đang phát: {title}"

            else:
                # Windows & macOS
                webbrowser.open(url)
                return f"✅ Đang phát: {title}"

        except Exception as e:
            return f"❌ Lỗi phát video: {e}"

    def play_specific_song(self, song_name, artist=None):
        """
        Phát bài hát cụ thể

        Args:
            song_name: Tên bài hát
            artist: Tên ca sĩ (optional)

        Returns:
            str: Kết quả
        """
        if artist:
            query = f"{song_name} {artist} official audio"
        else:
            query = f"{song_name} official audio"

        return self.search_and_play(query)

    def play_by_mood(self, mood):
        """
        Phát nhạc theo tâm trạng

        Args:
            mood: Tâm trạng (buồn, vui, thư giãn, tập thể dục...)

        Returns:
            str: Kết quả
        """
        mood_playlists = {
            "buồn": "sad emotional music playlist",
            "vui": "happy upbeat music playlist",
            "thư giãn": "relaxing chill music playlist",
            "tập thể dục": "workout gym music playlist",
            "làm việc": "focus study music playlist",
            "ngủ": "sleep meditation music",
            "lãng mạn": "romantic love songs playlist",
            "party": "party dance music playlist"
        }

        query = mood_playlists.get(mood.lower(), f"{mood} music playlist")
        return self.search_and_play(query)

    def play_by_genre(self, genre):
        """
        Phát nhạc theo thể loại

        Args:
            genre: Thể loại (pop, rock, jazz, classical...)

        Returns:
            str: Kết quả
        """
        query = f"{genre} music playlist 2024"
        return self.search_and_play(query)

    def get_current_playing(self):
        """Lấy thông tin bài hát đang phát"""
        if self.current_url:
            return f"🎵 Đang phát: {self.current_url}"
        else:
            return "❌ Chưa có bài hát nào đang phát"


# Optional: YouTube downloader và phát offline
class YouTubeDownloader:
    """
    Download YouTube audio và phát bằng local player
    (Chất lượng tốt hơn, không cần browser)
    """

    def __init__(self, download_dir="./music_cache"):
        """
        Khởi tạo YouTube Downloader

        Args:
            download_dir: Thư mục lưu nhạc
        """
        self.download_dir = download_dir
        os.makedirs(download_dir, exist_ok=True)

    def download_and_play(self, query):
        """
        Download audio và phát bằng mpv/vlc

        Args:
            query: Từ khóa tìm kiếm

        Returns:
            str: Kết quả
        """
        try:
            # Tìm kiếm YouTube
            videos_search = VideosSearch(query, limit=1)
            results = videos_search.result()

            if not results['result']:
                return f"❌ Không tìm thấy: {query}"

            video_url = results['result'][0]['link']
            video_title = results['result'][0]['title']

            print(f"⬇️  Đang tải: {video_title}...")

            # Download audio bằng yt-dlp
            output_path = os.path.join(self.download_dir, '%(title)s.%(ext)s')
            subprocess.run([
                'yt-dlp',
                '-x',  # Extract audio
                '--audio-format', 'mp3',
                '--audio-quality', '0',  # Best quality
                '-o', output_path,
                video_url
            ], check=True)

            # Phát bằng mpv hoặc vlc
            audio_file = os.path.join(self.download_dir, f"{video_title}.mp3")

            # Thử mpv trước (nhẹ hơn)
            try:
                subprocess.Popen(['mpv', '--no-video', audio_file])
                return f"✅ Đang phát: {video_title}"
            except FileNotFoundError:
                # Fallback: vlc
                subprocess.Popen(['vlc', '--intf', 'dummy', audio_file])
                return f"✅ Đang phát: {video_title}"

        except subprocess.CalledProcessError:
            return "❌ Lỗi download. Cài đặt: pip install yt-dlp"
        except Exception as e:
            return f"❌ Lỗi: {e}"
