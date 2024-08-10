import os # Remove this if not using Windows Environment Variables
import nextcord
import time
from open_ai import OpenAiManager
from config import config
from nextcord.ext import commands
from gtts import gTTS

# Declare the OpenAI class
openai_manager = OpenAiManager()

# Change this if you want to change personality
openai_manager.chat_history.append(config.first_message)

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Replace with your Discord Bot Token
DISCORD_BOT_TOKEN = os.environ.get("TRIVIA_BOT_TOKEN")

# Call Question and Answer Variables
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

            # Try connecting to voice channel
            try:
                vc = await user.voice.channel.connect()
                print(vc)
                print("Joining Voice...")
            except:
                vc = ctx.voice_client

            # Add user text to User_Answer variable
            text = " ".join(args)
            global user_answer
            user_answer = text

            # Create prompt for AI that confirms the Answer
            ans_check = "Is '" + user_answer + "' a reasonable answer to your previous question?"

            # Send the prompt to the AI and store response in variable
            openai_check = openai_manager.chat_with_history(ans_check)

            # Turn AI's response to TTS and store as mp3
            openai_check_response_tts = gTTS(text = openai_check, lang = "en", slow = False)
            openai_check_response_tts.save("ai-tts-audio.mp3")

            # Stop Bot's previous voice
            if vc.is_playing():
                vc.stop()
                print("Stopping previous VC Audio...")

            # Play mp3 in voice channel
            source = await nextcord.FFmpegOpusAudio.from_probe("ai-tts-audio.mp3", method="fallback")
            vc.play(source)
            print("Playing AI TTS")


        else:
            await ctx.send("You need to be in a vc to run this command!")
    

# Text to Speech Command
@bot.command(name="top")
async def tts(ctx, *args):

    # Store user text to variable
    text = " ".join(args)
    user = ctx.message.author


    if user.voice != None:

        # Connect to voice channel
        try:
            vc = await user.voice.channel.connect()
            print(vc)
            print("Joining Voice...")
            
        except:
            vc = ctx.voice_client
            print(vc)

        # Create mp3 TTS file of user's input
        sound = gTTS(text = text, lang = "es", slow = False)
        sound.save("tts-audio.mp3")

        # Stop Bot's previous voice
        if vc.is_playing():
            vc.stop()
            print("Stopping previous VC Audio...")

        # Play User Input mp3 file
        source = await nextcord.FFmpegOpusAudio.from_probe("tts-audio.mp3", method="fallback")
        vc.play(source)
        print("Playing User Input Audio...")

        # Send User's Input to AI and store to variable
        openai_result = openai_manager.chat_with_history(text)

        # Save AI's question to variable
        global question
        question = openai_result

        # Turn AI's response to TTS and store as mp3
        response = gTTS(text = openai_result, lang = "en", slow = False)
        response.save("ai-tts-audio.mp3")

        # Wait for bot to finish playing previous mp3 file
        while vc.is_playing():
            time.sleep(1)
            print("Waiting for TTS to finish...")

        # Play mp3 in voice channel
        source = await nextcord.FFmpegOpusAudio.from_probe("ai-tts-audio.mp3", method="fallback")
        vc.play(source)
        print("Playing AI response TTS...")

    else:
        await ctx.send("You need to be in a vc to run this command!")


# Check if Bot is Working
@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}")

if __name__ == '__main__':
    bot.run(DISCORD_BOT_TOKEN)
