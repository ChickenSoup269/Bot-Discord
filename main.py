# improt required dependicies
from math import ceil
import discord 
import requests
import os
import json
from discord.ext import commands
from datetime import datetime, timedelta
from config.apikey import *


# improt bot token
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = "!", intents=intents)

client = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command=None)


# check giờ đã in lời chào sang,chiều,tối
current_time = datetime.now()
dt_string = current_time.strftime("%H:%M:%S")
current_hour = current_time.hour


# Nơi chứa các hàm:

# Check giờ để in lời chào sáng, chiều, tối
def get_greeting():
    if 5 <= current_hour < 12:
        return 'Chào buổi sáng, tôi là ZeroBot bạn cần tôi giúp gì?'
    elif 12 <= current_hour < 18:
        return 'Chào buổi chiều, tôi là ZeroBot bạn cần tôi giúp gì?'
    else:
        return 'Chào buổi tối, tôi là ZeroBot bạn cần tôi giúp gì?!'


def get_goodbye():
    if 5 <= current_hour < 12:
        return 'Chào buổi sáng, chúc bạn một ngày vui vẻ!'
    elif 12 <= current_hour < 18:
        return 'Chào buổi chiều, chúc bạn một buổi chiều vui vẻ!'
    else:
        return 'Chào buổi tối, chúc bạn một buổi tối vui vẻ!'

# lấy giá vàng
def get_gold_prices():
    url = "http://api.btmc.vn/api/BTMCAPI/getpricebtmc?key=3kd8ub1llcg9t45hnoh8hmn7t5kc2v"
    response = requests.get(url)
    response_json = response.json()

    data = []
    for item in response_json.get('DataList', {}).get('Data', []):
        row_number = item.get('@row')
        row_data = {
            'Name': item.get(f'@n_{row_number}'),
            'Karats': item.get(f'@k_{row_number}'),
            'Độ tinh khiết': item.get(f'@h_{row_number}'),
            'Giá mua (VND)': int(item.get(f'@pb_{row_number}', 0)),
            'Giá bán (VND)': int(item.get(f'@ps_{row_number}', 0)),
            'Thời gian cập nhật': item.get(f'@d_{row_number}')
        }
        data.append(row_data)

    return data

# Hàm để định dạng dữ liệu
def format_gold_prices(data):
    messages = []
    for item in data:
        message = (
            f"**{item['Name']}**\n"
            f"Karats: {item['Karats']}\n"
            f"Độ tinh khiết: {item['Độ tinh khiết']}\n"
            f"Giá mua (VND): {item['Giá mua (VND)']}\n"
            f"Giá bán (VND): {item['Giá bán (VND)']}\n"
            f"Thời gian cập nhật: {item['Thời gian cập nhật']}\n"
            "----------------------------------------"
        )
        messages.append(message)
    return "\n".join(messages)

# Lưu thông tin tính chi tiêu
# Dictionary to store expenses
expenses = {}

# Save expenses to a file
def save_expenses():
    with open('expenses.json', 'w') as f:
        json.dump(expenses, f)

# Load expenses from a file
def load_expenses():
    global expenses
    try:
        with open('expenses.json', 'r') as f:
            expenses = json.load(f)
    except FileNotFoundError:
        expenses = {}

# Load expenses when the bot starts
load_expenses()

# In ra chi tiêu dưới dạng bảng
def format_expenses_table(expenses_list):
    if not expenses_list:
        return "Không có chi tiêu nào trong khoảng thời gian này."

    # Tiêu đề từng hàng
    headers = f"{'Ngày':<12} {'Danh mục':<15} {'Mô tả':<25} {'Số lượng':<10} {'Số tiền (VND)':<15}\n"
    table = headers + "-" * 80 + "\n"
    
    # Chi tiết danh sách từng hàng
    total_expense = 0
    for expense in expenses_list:
        date = expense['date']
        category = expense['category']
        description = expense['description']
        quantity = expense['quantity']
        amount = f"{expense['amount']:,}"  
        total_expense += expense['amount']
        
        table += f"{date:<12} {category:<15} {description:<25} {quantity:<10} {amount:<15}\n"
    
    table += "-" * 80 + f"\n{'Tổng chi tiêu:':<64} {total_expense:,} VND"
    
    return f"```{table}```"

# Xem lịch có bao nhiêu ngày
def get_week_of_month(date):
    first_day = date.replace(day=1)
    dom = date.day
    adjusted_dom = dom + first_day.weekday()  # Adjusted day of month to consider the first day of the month
    return int(ceil(adjusted_dom / 7.0))

# =======================[NỘI DUNG TRONG ĐOẠN CHAT BOT]==================================
@client.event
async def on_ready():
    print('Bot giờ đang đã sẵn sàng sử dụng 100%...')
    print('=========================================')


# Hello command
@client.command()
async def hello(ctx):
    greeting = get_greeting()
    await ctx.send(greeting)

# Goodbye command
@client.command()
async def goodbye(ctx):
    goodbye = get_goodbye()
    await ctx.send(goodbye)


# In và lấy giá vàng
@client.command()
async def goldprices(ctx):
    data = get_gold_prices()
    formatted_message = format_gold_prices(data)
    if len(formatted_message) > 2000:
        # Chia tin nhắn nếu vượt quá giới hạn 2000 ký tự
        parts = [formatted_message[i:i+2000] for i in range(0, len(formatted_message), 2000)]
        for part in parts:
            await ctx.send(part)
    else:
        await ctx.send(formatted_message)

# Tính năm nhuận
@client.command()
async def is_leap_year(ctx, year: int):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        await ctx.send(f'{year} là năm nhuận')
    else:
        await ctx.send(f'{year} không phải là năm nhuận')


# Thêm chi tiêu 
@client.command()
async def add_expense(ctx, category: str, description: str, amount: int, quantity: int = 1):
    user = str(ctx.author.id)
    date = datetime.now().strftime('%Y-%m-%d')
    
    if user not in expenses:
        expenses[user] = {}
    if date not in expenses[user]:
        expenses[user][date] = []

    total_amount = amount * quantity
    expenses[user][date].append({
        "category": category,
        "description": description,
        "amount": total_amount,
        "quantity": quantity
    })
    save_expenses()
    await ctx.send(f"Đã thêm chi tiêu: {category} - {description} - Số lượng: {quantity} - Tổng tiền: {total_amount:,} VND")

# Xem tất cả chi tiêu | [Date] để biết chi tiêu trong ngày
@client.command()
async def view_expenses(ctx, date: str = None):
    user = str(ctx.author.id)
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    if user not in expenses or date not in expenses[user]:
        await ctx.send(f"Không có chi tiêu nào vào ngày {date}.")
        return
    
    expenses_list = [
        {"date": date, "category": exp["category"], "description": exp["description"], "quantity": exp["quantity"], "amount": exp["amount"]}
        for exp in expenses[user][date]
    ]
    
    table = format_expenses_table(expenses_list)
    await ctx.send(table)

# Xem chi tiêu trong tuần
@client.command()
async def weekly_expenses(ctx):
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday

    total_weekly = 0
    for user_expenses in expenses.values():
        for date_str, items in user_expenses.items():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            if start_of_week <= date_obj <= today:  # Include up to today's date
                for item in items:
                    total_weekly += item['amount'] * item['quantity']

    week_of_month = get_week_of_month(today)
    # Inform the user that they are viewing expenses for the current week up to today
    await ctx.send(f"Tổng chi tiêu từ đầu tuần đến hôm nay (ngày thứ {today.weekday() + 1}) là {total_weekly:,} VND.")

# Chi tiêu tháng
@client.command()
async def monthly_expenses(ctx):
    today = datetime.now().date()
    total_monthly = 0

    for user_expenses in expenses.values():
        for date_str, items in user_expenses.items():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            if date_obj.year == today.year and date_obj.month == today.month:
                if date_obj <= today:  # Include up to today's date
                    for item in items:
                        total_monthly += item['amount'] * item['quantity']

    await ctx.send(f"Tổng chi tiêu từ đầu tháng đến hôm nay (ngày {today.day}) là {total_monthly:,} VND.")


# Chi tiêu năm
@client.command()
async def yearly_expenses(ctx, year: int = None):
    if year is None:
        year = datetime.now().year
    
    today = datetime.now().date()
    total_yearly = 0

    for user_expenses in expenses.values():
        for date_str, items in user_expenses.items():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            if date_obj.year == year:
                if date_obj <= today:  # Include up to today's date
                    for item in items:
                        total_yearly += item['amount'] * item['quantity']

    await ctx.send(f"Tổng chi tiêu từ đầu năm đến hôm nay (ngày {today.day}/{today.month}) là {total_yearly:,} VND.")


#  ===================================================================================================================
# In ra lời chào khi có user mới vào
@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name="general")  # Thay "general" bằng tên kênh của bạn
    if channel:
        await channel.send(f"Chào mừng {member.display_name} đã tham gia server!")


# Handle regular messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Check if message content is relevant
    if 'bot này thì làm được gì?' in message.content.lower():
        await message.channel.send('Bot này mạnh đấy anh bạn!')
    elif 'con này còn làm gì được nữa không?' in message.content.lower():
        await message.channel.send('Con bot này rất ngon đấy phen!')

    await client.process_commands(message)
    
# =======================================================[HELP]===================================================================
# Những câu lệnh được tích hợp
@client.command()
async def Help(ctx):
    help_message = (
        "Danh sách lệnh của ZeroBot:\n\n"
        "1. **!hello**\n"
        "   Gửi lời chào theo thời gian trong ngày.\n\n"
        "2. **!goodbye**\n"
        "   Gửi lời tạm biệt theo thời gian trong ngày.\n\n"
        "3. **!goldprices**\n"
        "   Hiển thị giá vàng hiện tại.\n\n"
        "4. **!is_leap_year [year]**\n"
        "   Kiểm tra xem năm [year] có phải là năm nhuận hay không.\n\n"
        "5. **!add_expense [category] [description] [amount] [quantity]**\n"
        "   Thêm một chi tiêu với số lượng và tổng tiền VND.\n\n"
        "6. **!view_expenses [date]**\n"
        "   Hiển thị các chi tiêu trong ngày [date]. Nếu không nhập [date], sẽ hiển thị chi tiêu của hôm nay.\n\n"
        "7. **!weekly_expenses**\n"
        "   Hiển thị tổng chi tiêu từ đầu tuần đến hôm nay.\n\n"
        "8. **!monthly_expenses**\n"
        "   Hiển thị tổng chi tiêu từ đầu tháng đến hôm nay.\n\n"
        "9. **!yearly_expenses [year]**\n"
        "   Hiển thị tổng chi tiêu từ đầu năm đến hôm nay. Nếu không nhập [year], sẽ hiển thị chi tiêu của năm hiện tại.\n\n"
        "10. **!help**\n"
        "    Hiển thị danh sách các lệnh có thể sử dụng với ZeroBot.\n"
    )
    await ctx.send(help_message)

client.run(botToken)
