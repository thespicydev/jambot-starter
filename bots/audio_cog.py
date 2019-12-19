from discord import utils, FFmpegPCMAudio
from discord.ext import commands

import os
import uuid
import youtube_dl


class AudioCog(commands.Cog):
    '''Manages audio related commands such as playing and stopping audio.'''
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def bye(self, ctx: commands.Context):
        '''Leaves the voice channel the user who sent the message is in.
        
        Args:
            ctx - The current context of the command.
        '''
        voice = utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.disconnect()
    
    async def _join_author_voice_channel(self, ctx:commands.Context):
        voice = utils.get(self.bot.voice_clients, guild=ctx.guild)
        channel = ctx.message.author.voice.channel
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            await channel.connect()

    @commands.command()
    async def join(self, ctx: commands.Context):
        '''Joins the voice channel the user who sent the message is in.
        
        Args:
            ctx - The current context of the command.
        '''
        await self._join_author_voice_channel(ctx)
            
    @commands.command()
    async def play(self, ctx: commands.Context, url: str):
        '''Plays the audio from one of the supported sites of youtube-dl.
        
        See: https://ytdl-org.github.io/youtube-dl/supportedsites.html.
        Also joins the voice channel the user who sent the command is in.
        
        Args:
            ctx - The current context of the command.
            url - The URL containing audio to play (e.g. YouTube).
        '''
        song_uuid = uuid.uuid4()
        ydl_opts = {
            'outtmpl': 'song-{}.%(ext)s'.format(song_uuid),
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        await self._join_author_voice_channel(ctx)
        
        def audio_finished_playing(path: str):
            '''Called when the audio stream is finished playing.
            
            Deletes the temporary file created by youtube-dl when downloading.
            '''
            def on_play_end(error: Exception):
                if error is not None:
                    ctx.send('I could not play the audio: {}'.format(error))
                os.remove(path)
            return on_play_end

        file_path = 'song-{}.mp3'.format(song_uuid)
        voice = utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice.play(
            FFmpegPCMAudio(file_path),
            after=audio_finished_playing(file_path))
        
    @commands.command()
    async def stop(self, ctx: commands.Context):
        '''Stops audio if it is currently playing.
        
        Args:
            ctx - The current context of the command.
        '''
        voice = utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice is not None:
            voice.stop()
            
    @commands.command("t")
    async def toggle(self, ctx: commands.Context):
        '''Pauses audio if playing, and plays audio if paused.
        
        Args:
            ctx - The current context of the command.
        '''
        voice = utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice is not None:
            if voice.is_paused():
                voice.resume()
            elif voice.is_playing():
                voice.pause()
            
    async def cog_check(self, ctx: commands.Context):
        '''Cog-wide check to see if the user is in a voice channel.
        
        Args:
            ctx - The current context of the command.
        '''
        return ctx.message.author.voice is not None
    
    async def cog_command_error(self, ctx: commands.Context, error: Exception):
        '''Cog-wide error handling.
        
        The only error we really care about is a CheckFailure.
        
        Args:
            ctx - The current context of the command.
            error - The exception that was thrown while command handling.
        '''
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send('You must be connected to a voice channel to use me!')