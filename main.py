# improt required dependicies
import discord 
from discord.ext import commands
from datetime import datetime

# improt bot token
from apikey import *
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = "!", intents=intents)

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# check giờ đã in lời chào sang,chiều,tối
current_time = datetime.now()
dt_string = current_time.strftime("%H:%M:%S")
current_hour = current_time.hour

@client.event
async def on_ready():
    print('Bot giờ đang đã sẵn sàng sử dụng 100%...')
    print('=========================================')

# hello command
# Check giờ để in lời chào sáng, chiều, tối
def get_greeting():
    current_time = datetime.now()
    current_hour = current_time.hour

    if 5 <= current_hour < 12:
        return 'Chào buổi sáng, tôi là ZeroBot bạn cần tôi giúp gì?'
    elif 12 <= current_hour < 18:
        return 'Chào buổi chiều, tôi là ZeroBot bạn cần tôi giúp gì?'
    else:
        return 'Chào buổi tối, tôi là ZeroBot bạn cần tôi giúp gì?!'

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
    if 5 <= current_hour < 12:
        return 'Chào buổi sáng, chúc bạn một ngày vui vẻ!'
    elif 12 <= current_hour < 18:
        return 'Chào buổi chiều, chúc bạn một buổi chiều vui vẻ!'
    else:
        return 'Chào buổi tối, chúc bạn một buổi tối vui vẻ!'


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
