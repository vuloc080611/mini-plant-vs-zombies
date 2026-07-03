# 🌻 Mini Plant vs Zombies

> Bản clone thu nhỏ của tựa game huyền thoại **Plants vs. Zombies**, viết hoàn toàn bằng Python và thư viện Pygame.  
> **Đặc biệt:** Không cần bất kỳ tài nguyên hình ảnh hay âm thanh nào – tất cả đều được vẽ bằng hình học cơ bản!

---

## ✨ Tính năng nổi bật

- **4 loại cây**:
  - 🌱 **Peashooter** – bắn đậu liên tục.
  - 🌻 **Sunflower** – tạo ra mặt trời, cung cấp năng lượng.
  - 🥜 **Wallnut** – chịu đòn, làm chậm zombie.
  - 💣 **Cherry Bomb** – nổ diện rộng, tiêu diệt zombie xung quanh.

- **3 loại zombie**:
  - 🧟 Zombie thường.
  - 🪖 Zombie đội nón (nhiều máu hơn).
  - 🪣 Zombie xô sắt (cực kỳ trâu bò).

- **Hệ thống sóng (Wave)**:
  - 5 đợt tấn công, đợt cuối là **"Huge Wave"** (siêu sóng) với số lượng zombie áp đảo.

- **Công cụ hỗ trợ**:
  - 🚜 **Máy cắt cỏ (Lawnmower)** – tự động kích hoạt khi zombie đi quá xa, quét sạch hàng đó.
  - ⛏️ **Xẻng (Shovel)** – giúp nhổ bỏ cây đã trồng để lấy lại ô trống.
  - ⏳ **Cooldown** – mỗi loại cây có thời gian hồi riêng, không thể trồng liên tục.

---

## 🎮 Cách chơi

1. **Thu thập mặt trời** – click vào những mặt trời rơi từ trên trời hoặc do Sunflower tạo ra để tích lũy điểm (năng lượng).
2. **Chọn cây** – click vào biểu tượng cây trên thanh công cụ phía trên.
3. **Trồng cây** – click vào ô cỏ trống trên sân để đặt cây.
4. **Mục tiêu** – tiêu diệt toàn bộ zombie trước khi chúng băng qua mép trái sân cỏ. Đừng quên dùng máy cắt cỏ khi cấp bách!

---

## ⌨️ Điều khiển

| Hành động | Phím / Thao tác |
|-----------|----------------|
| Chọn cây (Peashooter, Sunflower, Wallnut, Cherry Bomb) | Click vào biểu tượng trên thanh menu hoặc phím **1, 2, 3, 4** |
| Trồng cây | Click vào ô đất trống |
| Nhặt mặt trời | Click chuột trái vào mặt trời |
| Kích hoạt xẻng | Click biểu tượng xẻng (hoặc phím **5**), sau đó click vào cây muốn nhổ |
| Thoát xẻng | Click chuột phải hoặc chọn lại cây khác |

---

## 💻 Cài đặt và chạy game

1. **Yêu cầu hệ thống**: Python 3.8+.

2. **Cài thư viện Pygame**:
   ```bash
   pip install -r requirements.txt

. **Chạy game**:
   ```bash
   python pvz_full.py
