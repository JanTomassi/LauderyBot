#!/usr/bin/env python3
import time
from datetime import timedelta, datetime
from washingM import WashingMachine
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)


CHOOSING, TYPING_REPLY_W, CONFERM_W, STATE, TYPING_REPLY_D, CONFERM_D = range(6)

# Generate dict
machine = {
    "A": WashingMachine("Lavatrice"),
    "B": WashingMachine("Lavatrice"),
    "C": WashingMachine("Lavatrice"),
    "D": WashingMachine("Lavatrice"),
    "E": WashingMachine("Lavatrice"),
    "1": WashingMachine("D"),
    "2": WashingMachine("D"),
    "3": WashingMachine("D"),
    "4": WashingMachine("D"),
}


class Washer:
    async def lavatrice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user_data = context.user_data
        text = update.message.text

        reply_keyboard = [
            ["Lavatrice A", "Lavatrice B", "Lavatrice C"],
            ["Lavatrice D", "Lavatrice E"],
            ["Ritorna al inizio", "Reset"],
        ]
        markup = ReplyKeyboardMarkup(
            reply_keyboard, input_field_placeholder="Seleziona la lavatrice"
        )

        await update.message.reply_text("Seleziona la lavatrice", reply_markup=markup)
        return TYPING_REPLY_W

    async def ore(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user_data = context.user_data
        text = update.message.text
        user_data["washer"]["name"] = text.split(" ")[1]

        reply_keyboard = [
            ["0 ore", "1 ora"],
            ["2 ore", "3 ore"],
            ["Ritorna al inizio", "Reset"],
        ]
        markup = ReplyKeyboardMarkup(
            reply_keyboard, input_field_placeholder="Seleziona la durata in ore"
        )

        await update.message.reply_text("Seleziona la durata in ore", reply_markup=markup)
        return TYPING_REPLY_W

    async def minuti(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user_data = context.user_data
        text = update.message.text
        user_data["washer"]["hours"] = int(text.split(" ")[0])

        reply_keyboard = [
            ["0 min", "5 min", "10 min", "15 min"],
            ["20 min", "25 min", "30 min", "35 min"],
            ["40 min", "45 min", "50 min", "55 min"],
            ["Ritorna al inizio", "Reset"],
        ]
        markup = ReplyKeyboardMarkup(
            reply_keyboard, input_field_placeholder="Seleziona la durata in minuti"
        )

        await update.message.reply_text("Seleziona la durata in minuti", reply_markup=markup)
        return TYPING_REPLY_W

    async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user_data = context.user_data
        text = update.message.text
        user_data["washer"]["minuts"] = int(text.split(" ")[0])

        reply_keyboard = [["Reset", "Submit"]]
        markup = ReplyKeyboardMarkup(reply_keyboard)

        await update.message.reply_text(
            f"Questi sono i dati che ho"
            + f"\n\t- Lavatrice: {user_data['washer']['name']}"
            + f"\n\t- Durata:{user_data['washer']['hours']}h {user_data['washer']['minuts']}min",
            reply_markup=markup,
        )
        return CONFERM_W

    async def submit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user_data = context.user_data
        text = update.message.text

        machina = machine[user_data["washer"]["name"]]
        name = user_data["washer"]["name"]
        hours = user_data["washer"]["hours"]
        minuts = user_data["washer"]["minuts"]

        if machina.setnewuse(timedelta(minutes=minuts, hours=hours), update.message.from_user.id):
            reply_keyboard = [["Ritorna al inizio"], ["Seleziona un altra"], ["Stato"]]
            markup = ReplyKeyboardMarkup(reply_keyboard)
            await update.message.reply_text(
                strfstate(machina, name, True), reply_markup=markup, disable_notification=True
            )
            return CONFERM_W
        else:
            reply_keyboard = [["Ritorna al inizio"], ["Seleziona un altra"], ["Stato"]]
            markup = ReplyKeyboardMarkup(reply_keyboard)
            await update.message.reply_text(
                strfstate(machina, name, True), reply_markup=markup, disable_notification=True
            )
            return CONFERM_W


class Dryer:
    async def state1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        pass


async def state(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    for key in machine:
        await update.message.reply_text(strfstate(machine[key], key), disable_notification=True)


def strfstate(machina: WashingMachine, key: str, update: bool = False):
    if machina.hasFinished() and update:
        return (
            f"Sei riuscito a prenotare la lavatrice {key}\n"
            + f"Finira alle {machina.remaing().strftime('%d-%m-%y %H:%M')}\n"
            + f"Tra {machina.remaing() - datetime.now()}"
        )
    elif (not machina.hasFinished()) and update:
        return (
            f"Non sei riuscit a prenotare la lavatrice {key}\n"
            + f"Finira alle {machina.remaing().strftime('%d-%m-%y %H:%M')}\n"
            + f"Tra {machina.remaing() - datetime.now()}"
        )
    elif not machina.hasFinished():
        return (
            f"La {machina.mtype} {key}\n\t"
            + f"- Finira alle {machine[key].remaing().strftime('%d-%m-%y %H:%M')}\n\t"
            + f"- Tra {machine[key].remaing() - datetime.now()}"
        )
    elif machina.hasFinished():
        return f"La {machina.mtype} {key} - e' libera"
