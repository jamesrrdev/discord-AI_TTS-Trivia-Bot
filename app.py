import nextcord
from nextcord.ext import commands
from gtts import gTTS

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# !hi
# Hello!
@bot.command(name="hi")
async def SendMessage(ctx):
    await ctx.send('Hello!')

@bot.command(name="tts")
async def tts(ctx, *args):
    text = " ".join(args)
    user = ctx.message.author
    if user.voice != None:
        try:
            vc = await user.voice.channel.connect()
        except:
            vc = ctx.voice_client

        sound = gTTS(text = text, lang = "en", slow = False)
        sound.save("tts-audio.mp3")

        if vc.is_playing():
            vc.stop()

        source = await nextcord.FFmpegOpusAudio.from_probe("tts-audio.mp3", method="fallback")
        vc.play(source)
    else:
        await ctx.send("You need to be in a vc to run this command!")

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}")

if __name__ == '__main__':
    bot.run("[INSERT BOT KEY HERE]")
