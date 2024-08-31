# BOT DISCORD [![My Skills](https://skillicons.dev/icons?i=discord)](https://skillicons.dev)

Đây là bot discord tính chi phí tiêu dùng hàng ngày do người dùng nhập vào xuất ra tổng chi phí tiêu dùng trong ngày, tháng, năm, mỗi ngày xuất ra hôm nay bạn tiêu được bao nhiêu tiền, tuần này bạn đã chi ra bao nhiêu, tháng, năm...

## Cách hệ thống hoạt động

Chi tiêu hôm nay của bạn bao gồm là gì? | mời bạn chọn số để hệ thống có thể tính được chi tiêu và số tiền bạn thường chi tiêu cho khoảng nào nhiều nhất:

- Đồ dùng học tập [1]
- Thức ăn & nước uống [2]
- Giải trí [3]
- Tiền wifi, cáp, tivi [4]
- Tiền điện & nước [5]
-
-

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`API_KEY`
-> how to get https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token

`BotToken`: API_KEY



## Chức năng của bot [BETA - ĐANG PHÁT TRIỂN THÊM]
 
| Command | Description                |
| :-------- |  :------------------------- |
| `!hello` |  Gửi lời chào theo thời gian trong ngày. |
| `!goodbye` | Gửi lời tạm biệt theo thời gian trong ngày. |
| `!goldprices` |  Hiển thị giá vàng hiện tại.  |
| `!is_leap_year [year]` |  Kiểm tra xem năm [year] có phải là năm nhuận hay không. |
| `!add_expense [category] [description] [amount] [quantity]` | Thêm một chi tiêu với số lượng và tổng tiền VND. |
| `!view_expenses [date]` |  Hiển thị các chi tiêu trong ngày [date]. Nếu không nhập [date], sẽ hiển thị chi tiêu của hôm nay. |
| `!weekly_expenses` | Hiển thị tổng chi tiêu từ đầu tuần đến hôm nay.  |
| `!monthly_expenses` |Hiển thị tổng chi tiêu từ đầu tháng đến hôm nay. |
| `!yearly_expenses [year]` | *Hiển thị tổng chi tiêu từ đầu năm đến hôm nay. Nếu không nhập [year], sẽ hiển thị chi tiêu của năm hiện tại. |
| `!Help` | Hiển thị danh sách các lệnh có thể sử dụng với ZeroBot. |

# Pip
### Linux/macOS
```bash
  python3 -m pip install -U discord.py
```
### Windows
```bash
 py -3 -m pip install -U discord.py
```
## Run Locally

Clone the project

```bash
  git clone https://github.com/ChickenSoup269/Bot-Discord.git
```

Go to the project directory

```bash
  cd [your-project]
```

Start 

```bash
  python main.py
```
## Screenshots

![App Screenshot](https://github.com/ChickenSoup269/Bot-Discord/blob/main/Screenshots/Screenshot%202024-08-15%20201704.png)

![App Screenshot](https://github.com/ChickenSoup269/Bot-Discord/blob/main/Screenshots/Screenshot%202024-08-15%20215019.png)

![App Screenshot](https://github.com/ChickenSoup269/Bot-Discord/blob/main/Screenshots/Screenshot%202024-08-15%20215043.png)

![App Screenshot](https://github.com/ChickenSoup269/Bot-Discord/blob/main/Screenshots/image.png)

