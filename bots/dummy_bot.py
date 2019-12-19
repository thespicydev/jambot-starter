from discord.ext import commands
from discord import abc, Member, Message, User
from typing import Union

import datetime


class DummyBot(commands.Bot):
    '''A bot that literally does nothing. Give this bot some life!'''

    def __init__(self, command_prefix: str='!'):
        '''Constructor.
        
        Arguments:
            command_prefix: How users will invoke your bot's commands.
                Example: typing '!slurp' to invoke the 'slurp' command.
        '''
        super().__init__(command_prefix='!')

    async def on_ready(self):
        '''Called when the client is done preparing the data from Discord.
        
        This is usually after the bot login is successful.
        NOTE: Not guaranteed to be the first event called or only called once.
        '''
        pass
    
    async def on_member_join(self, member: Member):
        '''Called when a Member joins a Guild.
        
        Args:
            member - The Member that joined.
        '''
        pass
    
    async def on_member_remove(self, member: Member):
        '''Called when a Member leaves a Guild.
        
        Args:
            member - The member that left.
        '''
        pass

    async def on_message(self, message: Message):
        '''Called when a Message is created and sent.
        
        NOTE: Bot messages are also handled by this event. Be careful to
        check the user IDs to handle bot messages separately. Otherwise,
        it's possible that your bot messages will infinitely recurse handling
        their own, or other bot's automatic messages.
        
        Args:
            message - The message sent.
        '''
        pass
    
    async def on_error(self, event: str, *args, **kwargs):
        '''Exception handler for exceptions raised during event handling.
        
        The default behavior is for the traceback of an exception to be written
        to stderr and then ignored. The 'on_error' handler allows you to
        customize error handling more.
        
        Args:
            event - The name of the event that raised the exception.
            args - Positional args for the event that raised the exception.
            kwargs - Keyword args for the event that raised the exception.
        '''
        pass
    
    async def on_typing(self, channel: abc.Messageable,
                        user: Union[User, Member], when: datetime.datetime):
        '''Called when someone begins typing a message.
        
        An abc.Messageable instance is either a TextChannel, GroupChannel,
        or DMCChannel.
        
        Args:
            channel - The location where the typing originated from.
            user - The user that started typing. If 'channel' is a TextChannel,
                then 'user' is a Member. Otherwise, 'user' is a User.
            when - When the typing started as a naive datetime in UTC.
        '''
        pass