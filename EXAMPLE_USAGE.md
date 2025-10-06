# 🎯 Ví dụ sử dụng AI Chatbot với Context Learning

## 🧠 AI tự suy luận thông minh

### Phiên chat mẫu 1: Suy luận từ hoạt động

```
Bạn: Tôi sắp đọc sách
🔧 ✅ Đã bật LED tại pin 13
💭 Lý do: Người dùng sắp đọc sách, cần ánh sáng tốt để đọc
AI: Để tôi bật đèn cho bạn đọc sách cho sáng nhé!

Bạn: Đọc xong rồi, giờ đi ngủ
🔧 ✅ Đã tắt LED tại pin 13
💭 Lý do: Người dùng chuẩn bị đi ngủ, cần môi trường tối
AI: Chúc bạn ngủ ngon! Tôi đã tắt đèn rồi 😊

Bạn: stats
📊 THỐNG KÊ AI ĐÃ HỌC:

TRẠNG THÁI HIỆN TẠI:
- Đèn: off

HÀNH ĐỘNG GẦN ĐÂY:
- Tôi sắp đọc sách → on (Người dùng sắp đọc sách, cần ánh sáng tốt để đọc)
- Đọc xong rồi, giờ đi ngủ → off (Người dùng chuẩn bị đi ngủ, cần môi trường tối)

SỞ THÍCH ĐÃ HỌC:
- Khi 'đọc': thích đèn bật
- Khi 'ngủ': thích đèn tắt
```

### Phiên chat mẫu 2: Suy luận từ cảm xúc/môi trường

```
Bạn: Trời mưa to, ảm đạm quá
🔧 ✅ Đã bật LED tại pin 13
💭 Lý do: Trời mưa tối, cần ánh sáng để tạo cảm giác ấm cúng
AI: Trời mưa tối thế này, để tôi bật đèn cho ấm cúng hơn nhé!

Bạn: Mắt mỏi quá, nhức đầu
🔧 ✅ Đã tắt LED tại pin 13
💭 Lý do: Người dùng mỏi mắt và nhức đầu, có thể do ánh sáng quá mạnh
AI: Có thể do ánh sáng quá sáng đấy. Tôi đã tắt đèn, bạn nghỉ ngơi một chút nhé!
```

### Phiên chat mẫu 3: Suy luận phức tạp

```
Bạn: Chuẩn bị làm việc, code dự án quan trọng
🔧 ✅ Đã bật LED tại pin 13
💭 Lý do: Làm việc và code cần ánh sáng tốt để tập trung
AI: Bật đèn cho bạn làm việc hiệu quả! Chúc bạn code vui vẻ 💻

Bạn: Xem phim Netflix thôi
🔧 ✅ Đã tắt LED tại pin 13
💭 Lý do: Xem phim thường tốt hơn trong môi trường tối để trải nghiệm tốt
AI: Enjoy! Tôi đã tắt đèn để bạn xem phim sướng hơn 🎬
```

## 🎓 AI học từ hành vi của bạn

### Lần đầu tiên

```
Bạn: Tôi sắp ăn cơm
AI: Bạn muốn tôi bật đèn để ăn cơm không?

Bạn: Có, bật đi
🔧 ✅ Đã bật LED tại pin 13
AI: Đã bật đèn rồi ạ!
```

### Lần thứ 2 (AI đã học)

```
Bạn: Ăn cơm nào
🔧 ✅ Đã bật LED tại pin 13
💭 Lý do: Người dùng thường bật đèn khi ăn (đã học từ lần trước)
AI: Tôi nhớ bạn thích bật đèn khi ăn cơm, đã bật rồi nha! 😊

Bạn: stats
📊 THỐNG KÊ AI ĐÃ HỌC:

SỞ THÍCH ĐÃ HỌC:
- Khi 'ăn': thích đèn bật (2 lần)
- Khi 'đọc': thích đèn bật (1 lần)
- Khi 'ngủ': thích đèn tắt (1 lần)
- Khi 'xem phim': thích đèn tắt (1 lần)
```

## 🆚 So sánh: Trước vs Sau

### ❌ TRƯỚC (Rule-based - Khớp từ khóa)

```
Bạn: Tôi sắp đọc sách
AI: Xin lỗi, tôi không hiểu. Bạn có thể nói "bật đèn" hoặc "tắt đèn" không?

Bạn: Trời mưa ảm đạm quá
AI: (Không hiểu vì không có từ "bật" hay "tối")

Bạn: Mỏi mắt quá
AI: (Không hiểu)
```

### ✅ SAU (AI Reasoning + Context Learning)

```
Bạn: Tôi sắp đọc sách
🔧 ✅ Đã bật LED
💭 Lý do: Đọc cần ánh sáng
AI: Để tôi bật đèn cho bạn đọc cho sáng!

Bạn: Trời mưa ảm đạm quá
🔧 ✅ Đã bật LED
💭 Lý do: Trời mưa tối, cần ấm cúng
AI: Trời mưa tối, để tôi bật đèn cho ấm!

Bạn: Mỏi mắt quá
🔧 ✅ Đã tắt LED
💭 Lý do: Mỏi mắt có thể do sáng quá
AI: Có thể do đèn sáng quá. Đã tắt rồi!
```

## 🌟 Các tính năng thông minh

### 1. Hiểu ngữ cảnh hoạt động
- "Đọc sách" → Cần sáng → Bật
- "Ngủ" → Cần tối → Tắt
- "Làm việc" → Cần sáng → Bật
- "Xem phim" → Thích tối → Tắt

### 2. Hiểu cảm xúc/môi trường
- "Trời tối" → Bật
- "Chói mắt" → Tắt
- "Ảm đạm" → Bật
- "Mỏi mắt" → Tắt

### 3. Học sở thích cá nhân
- Ghi nhớ bạn thích bật/tắt đèn khi làm gì
- Lần sau tự động áp dụng
- Xem thống kê bằng lệnh `stats`

### 4. Giải thích quyết định
- Mỗi hành động đều có lý do
- Trong suốt, dễ debug
- User hiểu AI đang suy luận như thế nào

## 🚀 Lệnh nâng cao

```bash
# Xem thống kê AI đã học
Bạn: stats

# Reset lịch sử chat (GIỮ NGUYÊN memory đã học)
Bạn: reset

# Thoát
Bạn: exit
```

## 💡 Tips sử dụng hiệu quả

1. **Nói tự nhiên**: Đừng cố gắng khớp từ khóa, nói như bình thường
2. **Thêm ngữ cảnh**: "Tôi sắp..." giúp AI hiểu rõ hơn
3. **Để AI học**: Dùng thường xuyên để AI học sở thích của bạn
4. **Xem stats**: Thỉnh thoảng gõ `stats` để xem AI đã học gì

## 🔥 Ví dụ sáng tạo

```
Bạn: Girlfriend sắp về, chuẩn bị romantic dinner
🔧 ✅ Đã bật LED
💭 Lý do: Bữa tối lãng mạn cần ánh sáng ấm áp
AI: Đã bật đèn cho buổi tối lãng mạn! 🕯️

Bạn: Gaming thôi!
🔧 ✅ Đã tắt LED
💭 Lý do: Chơi game thường thích môi trường tối để tập trung vào màn hình
AI: Good luck! Đã tắt đèn để bạn focus vào game 🎮

Bạn: Dọn dẹp nhà cửa
🔧 ✅ Đã bật LED
💭 Lý do: Dọn dẹp cần nhìn rõ để làm sạch hiệu quả
AI: Bật đèn cho bạn dọn dẹp cho sạch sẽ!
```
