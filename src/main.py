#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging
import os
from typing import Dict
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from State import (
    Washer,
    Dryer,
    state,
    CHOOSING,
    TYPING_REPLY_D,
    TYPING_REPLY_W,
    CONFERM_W,
    CONFERM_D,
    STATE,
)

reply_keyboard = [
    ["Lavatrice", "Asciugartrice", "Stato"],
    ["Number of siblings", "Something else..."],
    ["Done"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["washer"] = {"name": None, "hours": None, "minuts": None}
    context.user_data["dryer"] = {"name": None, "hours": None, "minuts": None}

    """Start the conversation and ask user for input."""
    reply_keyboard = [["Lavatrice"], ["Asciugartrice"], ["Stato"]]
    markup = ReplyKeyboardMarkup(
        reply_keyboard,
        input_field_placeholder="Seleziona dalla tastiera",
    )

    await update.message.reply_text(
        "Seleziona dalla tastiera",
        reply_markup=markup,
    )
    return CHOOSING


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = (
        Application.builder().concurrent_updates(True).token(os.environ.get("TOKEN")).build()
    )
    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                MessageHandler(filters.Regex("^Lavatrice$"), Washer.lavatrice),
                MessageHandler(filters.Regex("^Asciugatrice$"), Dryer.state1),
                MessageHandler(filters.Regex("^Stato$"), state),
            ],
            TYPING_REPLY_W: [
                MessageHandler(filters.Regex("^Lavatrice [ABCDE]"), Washer.ore),
                MessageHandler(filters.Regex("^[0-4] or[ae]$"), Washer.minuti),
                MessageHandler(filters.Regex("^[0-5][0-9]? min$"), Washer.end),
                MessageHandler(filters.Regex("^Ritorna al inizio$"), start),
                MessageHandler(filters.Regex("^Reset$"), Washer.lavatrice),
            ],
            CONFERM_W: [
                MessageHandler(filters.Regex("^Stato$"), state),
                MessageHandler(filters.Regex("^Submit$"), Washer.submit),
                MessageHandler(filters.Regex("^Ritorna al inizio$"), start),
                MessageHandler(filters.Regex("^(Reset|Seleziona un altra)$"), Washer.lavatrice),
            ],
            STATE: [],
            TYPING_REPLY_D: [],
            CONFERM_D: [],
        },
        fallbacks=[CommandHandler("start", start)],
        block=False,
    )
    application.add_handler(conv_handler)
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
