from nextcord.ext import commands
import nextcord
import asyncio
import os
from open_ai import OpenAiManager
from config import config
from gtts import gTTS

# Declare the OpenAI class
openai_manager = OpenAiManager()
print("OpenAI manager created.")

cooldown_time = config.ai_prompt_command_cooldown
cooldown_msgs_per = config.ai_msgs_per_cooldown

# Sends the initial message
openai_manager.chat_history.append(config.first_message)

class Prompts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Send a prompt to AI and get a MSG response
    @commands.cooldown(cooldown_msgs_per, cooldown_time)
    @commands.command(name="p", help="prompt the ai and get a msg back")
    async def Prompt(self, ctx, *args):

        print("Prompt")

        # Add user text to User_Answer variable
        text = " ".join(args)

        # Send prompt to AI and save to variable
        ai_response = openai_manager.chat(text)

        if (len(ai_response) < 2000):
            await ctx.send(ai_response)
        else:
            await ctx.send("This response exceeds Discord's 2000 character limit!")

    # Send a prompt to AI and get a MSG response
    @commands.cooldown(cooldown_msgs_per, cooldown_time)
    @commands.command(name="ptts", help="prompt the ai and get a tts back in vc")
    async def PromptTTS(self, ctx, *args):

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

            # Send prompt to AI and save to variable
            ai_response = openai_manager.chat(text)

            # Turn AI's response to TTS and store as mp3
            tts_response = gTTS(text = ai_response, lang = "en", slow = False)
            tts_response.save("ai-tts-audio.mp3")

            # Stop Bot's previous voice
            if vc.is_playing():
                vc.stop()
                print("Stopping previous VC Audio...")

            # Play User Input mp3 file
            source = await nextcord.FFmpegOpusAudio.from_probe("ai-tts-audio.mp3", method="fallback")
            vc.play(source)
            print("Playing User Input Audio...")

            # Wait for Audio to finish playing
            while vc.is_playing():
                await asyncio.sleep(1)

            # Delete file
            if os.path.exists("ai-tts-audio.mp3"):
                os.remove("ai-tts-audio.mp3")
                print("Deleted Audio File.")

        else:
                await ctx.send("You need to be in a vc to run this command!")

    # Answer to the Trivia Question
    @commands.cooldown(cooldown_msgs_per, cooldown_time)
    @commands.command(name="ans", help="answer the trivia question")
    async def Answer(self, ctx, *args):

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

                # Wait for Audio to finish playing
                while vc.is_playing():
                    await asyncio.sleep(1)

                # Delete file
                if os.path.exists("ai-tts-audio.mp3"):
                    os.remove("ai-tts-audio.mp3")
                    print("Deleted Audio File.")


            else:
                await ctx.send("You need to be in a vc to run this command!")
        

    # Text to Speech Command
    @commands.cooldown(cooldown_msgs_per, cooldown_time)
    @commands.command(name="top", help="submit a topic to ai for trivia")
    async def Topic(self, ctx, *args):

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

            # Wait for Audio to finish playing
            while vc.is_playing():
                await asyncio.sleep(1)

            # Delete file
            if os.path.exists("tts-audio.mp3"):
                os.remove("tts-audio.mp3")
                print("Deleted Audio File.")

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
                await asyncio.sleep(1)
                print("Waiting for TTS to finish...")

            # Play mp3 in voice channel
            source = await nextcord.FFmpegOpusAudio.from_probe("ai-tts-audio.mp3", method="fallback")
            vc.play(source)
            print("Playing AI response TTS...")

            # Wait for Audio to finish playing
            while vc.is_playing():
                await asyncio.sleep(1)

            # Delete file
            if os.path.exists("ai-tts-audio.mp3"):
                os.remove("ai-tts-audio.mp3")
                print("Deleted Audio File.")

        else:
            await ctx.send("You need to be in a vc to run this command!")

def setup(bot):
    bot.add_cog(Prompts(bot))