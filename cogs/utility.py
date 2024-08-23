from nextcord.ext import commands
import nextcord
import os

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # Stop TTS audio
    @commands.command(name="stop", help="Stop current TTS")
    async def stopTTS(self, ctx):

        vc = ctx.voice_client

        if vc.is_playing():

            # Stops VC
            vc.stop()
            print("Stopping previous VC Audio...")
            await ctx.send("Stopping TTS audio...")

            # Deletes Audio File
            if os.path.exists("ai-tts-audio.mp3"):
                os.remove("ai-tts-audio.mp3")
                print("Deleted AI file through Stop.")
            elif os.path.exists("tts-audio.mp3"):
                os.remove("tts-audio.mp3")
                print("Deleted TTS file through Stop.")
            else:
                print("No audio files found.")

        else:

            # Send Message
            await ctx.send("There is no TTS playing right now.")

def setup(bot):
    bot.add_cog(Utility(bot))