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
@client.command()
async def hello(ctx):
   
   if 5 <= current_hour < 12:
        hello = 'Chào buổi sáng, tôi là ZeroBot bạn cần tôi giúp gì?'
   elif 12 <= current_hour < 18:
        hello = 'Chào buổi chiều, tôi là ZeroBot bạn cần tôi giúp gì?'
   else:
        hello = 'Chào buổi tối, tôi là ZeroBot bạn cần tôi giúp gì?!'

   await ctx.send(hello)


# goodbye command
@client.command()
async def goodbye(ctx):

    if 5 <= current_hour < 12:
        goobye = 'Chào buổi sáng, chúc chủ nhân một ngày vui vẻ!'
    elif 12 <= current_hour < 18:
        goobye = 'Chào buổi chiều, chúc chủ nhân một ngày vui vẻ!'
    else:
        goobye = 'Chào buổi tối, chúc chủ nhân một buổi tối vui vẻ!'

    await ctx.send(goobye)
 

@client.event
async def on_member_join(member):
    print("Test" + member)

client.run(botToken)

# bot này thì làmm được gì?
# ?Bot này mạnh đấy anh bạn
# con này còn làm gì được nữa không?
# ?con bot này rất ngon đấy phen