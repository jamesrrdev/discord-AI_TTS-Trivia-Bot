import os
import nextcord
from config import config
from nextcord import Embed, Color
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.message_content = True

# Set command structure
bot = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)

# Replace with your Discord Bot Token
DISCORD_BOT_TOKEN = config.DISCORD_BOT_TOKEN

# Check for Cooldown Errors and Send MSG
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = Embed(title=f"AI Prompting On Cooldown", description=f"Try again in {error.retry_after:.2f}s.", color=Color.red())
        await ctx.send(embed=em)

# Check if Bot is Working
@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}")

# Integrate Cogs file
for fn in os.listdir("./cogs"):
    if fn.endswith(".py"):
        bot.load_extension(f"cogs.{fn[:-3]}")

# Load Cog Command
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    await ctx.send("Loaded cog!")

# Unlock Cog Command
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send("Unloaded cog!")

# Reload Cog Command
@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f"cogs.{extension}")
    await ctx.send("Reloaded cog!")

if __name__ == '__main__':
    bot.run(DISCORD_BOT_TOKEN)
