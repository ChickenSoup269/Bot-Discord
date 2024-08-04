# improt required dependicies
import discord 
import requests
from discord.ext import commands
from datetime import datetime
from config.apikey import *


# improt bot token
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = "!", intents=intents)

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

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
    

client.run(botToken)
