import os # Remove this if not using Windows Environment Variables
import nextcord
import time
from open_ai import OpenAiManager
from config import config
from nextcord.ext import commands
from gtts import gTTS

# Declare the OpenAI along with the initial message
openai_manager = OpenAiManager()
openai_manager.chat_history.append(config.first_message)


intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Replace with your Discord Bot Token
DISCORD_BOT_TOKEN = os.environ.get("TRIVIA_BOT_TOKEN")

question = "question"
answer = "answer"
user_answer = "user_answer"

# See Commands
@bot.command(name="h")
async def SendMessage(ctx):
    await ctx.send("!top : submit a topic ~~~ !ans : answer the question")

# Answer to the Trivia Question
@bot.command(name="ans")
async def changeAnswer(ctx, *args):

        user = ctx.message.author
        
        if user.voice != None:
            try:
                vc = await user.voice.channel.connect()
            except:
                vc = ctx.voice_client

            text = " ".join(args)
            global user_answer
            user_answer = text

            ans_check = "Is '" + user_answer + "' a reasonable answer to your previous question?"

            openai_check = openai_manager.chat_with_history(ans_check)

            openai_check_response_tts = gTTS(text = openai_check, lang = "en", slow = False)
            openai_check_response_tts.save("ai-tts-audio.mp3")

            source = await nextcord.FFmpegOpusAudio.from_probe("ai-tts-audio.mp3", method="fallback")
            vc.play(source)


        else:
            await ctx.send("You need to be in a vc to run this command!")
    

# Text to Speech Command
@bot.command(name="top")
async def tts(ctx, *args):
    text = " ".join(args)
    user = ctx.message.author
    if user.voice != None:
        try:
            vc = await user.voice.channel.connect()
        except:
            vc = ctx.voice_client

        sound = gTTS(text = text, lang = "es", slow = False)
        sound.save("tts-audio.mp3")

        if vc.is_playing():
            vc.stop()

        source = await nextcord.FFmpegOpusAudio.from_probe("tts-audio.mp3", method="fallback")
        vc.play(source)

        openai_result = openai_manager.chat_with_history(text)

        global question
        question = openai_result

        response = gTTS(text = openai_result, lang = "en", slow = False)
        response.save("ai-tts-audio.mp3")

        while vc.is_playing():
            time.sleep(1)

        source = await nextcord.FFmpegOpusAudio.from_probe("ai-tts-audio.mp3", method="fallback")
        vc.play(source)

    else:
        await ctx.send("You need to be in a vc to run this command!")


# Check if Bot is Working
@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}")

if __name__ == '__main__':
    bot.run(DISCORD_BOT_TOKEN)
