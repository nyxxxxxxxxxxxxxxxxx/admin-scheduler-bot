import os
import discord
from discord.ext import tasks
from datetime import datetime
import pytz

TOKEN = os.getenv("DISCORD_TOKEN")

GUILD_ID = int(os.getenv("GUILD_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

SOFT_BREAK_ROLE = "💤 soft break"
UNAVAILABLE_ROLE = "🌙 unavailable today"

timezone = pytz.timezone("America/New_York")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = discord.Client(intents=intents)

SCHEDULE = {
    1:  {"role": 1450000639919783986, "vp": "-Nyx-",       "admin": "Katsu"},
    2:  {"role": 1450000712959262841, "vp": "-Nyx-",       "admin": "ZaddyNic"},
    3:  {"role": 1449999277056069706, "vp": "Triance",     "admin": "Triance"},
    4:  {"role": 1450327799956246618, "vp": "Triance",     "admin": "Skits"},
    5:  {"role": 1449999597882708089, "vp": "Mamushi",     "admin": "Mamushi"},
    6:  {"role": 1449999665109143552, "vp": "FcUeKd",      "admin": "FcUeKd"},
    8:  {"role": 1449999738182041630, "vp": "Ghosty_Kay",  "admin": "DreamStalker"},
    9:  {"role": 1449999807853756446, "vp": "Ghosty_Kay",  "admin": "Cocoa"},
    10: {"role": 1449999895300804608, "vp": "Ghosty_Kay",  "admin": "Rainaa"},
    11: {"role": 1449999973105139813, "vp": "SinfullyRae", "admin": "SinfullyRae"},
    13: {"role": 1450000047641985197, "vp": "SinfullyRae", "admin": "Yousra"},
    14: {"role": 1450000122132824135, "vp": "Ghosty_Kay",  "admin": "Ghosty_Kay"},
    15: {"role": 1450000183763927142, "vp": "Ghosty_Kay",  "admin": "Rishi"},
    17: {"role": 1450000237060952176, "vp": "-Nyx-",       "admin": "-Nyx-"},
    18: {"role": 1450000308951580823, "vp": "-Nyx-",       "admin": "SkyDaSweetyPie"},
    20: {"role": 1450000414123757608, "vp": "-Nyx-",       "admin": "N3k0Ch4nllilllllillli"},
    22: {"role": 1450000505911771220, "vp": "-Nyx-",       "admin": "ABG"},
    23: {"role": 1450000581799317614, "vp": "Patrick",    "admin": "Patrick"},
}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    hourly_ping.start()
    reset_unavailable.start()

@tasks.loop(minutes=1)
async def hourly_ping():
    now = datetime.now(timezone)
    if now.minute != 0:
        return

    hour = now.hour
    if hour not in SCHEDULE:
        return

    guild = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(CHANNEL_ID)

    data = SCHEDULE[hour]
    role = guild.get_role(data["role"])

    soft_break = discord.utils.get(guild.roles, name=SOFT_BREAK_ROLE)
    unavailable = discord.utils.get(guild.roles, name=UNAVAILABLE_ROLE)

    valid_members = [
        m for m in role.members
        if soft_break not in m.roles and unavailable not in m.roles
    ]

    if not valid_members:
        return

    message = (
        "🌸 **Admin On Duty** 🌸\n"
        f"🕒 **{hour}:00 – {hour+1}:00 ET**\n"
        f"👑 **VP:** {data['vp']}\n"
        f"🛡️ **Active:** {data['admin']}"
    )

    await channel.send(f"{role.mention}\n{message}")

@tasks.loop(minutes=1)
async def reset_unavailable():
    now = datetime.now(timezone)
    if now.hour != 0 or now.minute != 0:
        return

    guild = bot.get_guild(GUILD_ID)
    role = discord.utils.get(guild.roles, name=UNAVAILABLE_ROLE)

    for member in role.members:
        await member.remove_roles(role)

bot.run(TOKEN)
