from bots.audio_cog import AudioCog
from discord.ext import commands


class JamBot(commands.Bot):
    '''A bot that can play and manage audio in Discord.'''
    def __init__(self, **kwargs):
        super().__init__('j!', **kwargs)
        self.add_cog(AudioCog(self))
        

