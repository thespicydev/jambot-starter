'''Entry point for our Discord bot.

Make sure your .env file in the same directory contains the environment
variable DISCORD_TOKEN. Example:

# .env file
DISCORD_TOKEN=whatever_your_token_is
'''
from bots import dummy_bot, jam_bot
from dotenv import load_dotenv

import argparse
import logging
import os


def main():
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    spicy_bot = jam_bot.JamBot()
    spicy_bot.run(token)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--log",
        dest="log_level",
        choices=[
            'DEBUG','INFO', 'WARNING', 'ERROR', 'CRITICAL'
        ],
        default='INFO',
        help="Set the logging level")

    args = parser.parse_args()
    if args.log_level:
        logging.basicConfig(level=logging.getLevelName(args.log_level))
    main()
