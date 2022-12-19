from telegram.ext import (Updater, CommandHandler, CallbackContext)
from telegram import (Update)

import GamesController
import MsgController
import roles
import random
import os
import logging

update = Update
context = CallbackContext
commands = ["/help - Gives you information about the available commands.",
            "/claim - Maintains a list of werewolf roles claimed by everyone in the group",
            "/claims - View the list of all claimed roles.",
            "/reset - Clears the list of claims in a group.",
            "/flip - Flips a coin.",
            "/ping - Pings the bot."]

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
                                                                                                                
logger = logging.getLogger(__name__)

class Player(object):
    def __init__(self, name, uid, claim):
        self.name = name
        self.uid = uid
        self.claim = claim

class Game(object):
    def __init__(self, cid, initiator):
        self.playerlist = {}
        self.cid = cid
        self.initiator = initiator

    def add_player(self, uid, player):
        self.playerlist[uid] = player

    def remove_player(self, uid):
        self.playerlist.pop(uid)

    def print_claims(self):
        rtext = ""

        for p in self.playerlist:
            rtext += "[" + self.playerlist[p].name + "](tg://user?id=" + str(self.playerlist[p].uid) + ") claims "
            rtext += "_" + self.playerlist[p].claim + "_\n"
        return rtext

class Message(object):
    def __init__(self, cid, msg):
        self.cid = cid
        self.msg = msg

    def get_msg(self, cid):
        return self.msg


def get_emoji(claim):
    if claim.lower() in roles.vg:
        return "\U0001F471 " + claim
    elif claim.lower() in roles.drunk:
        return "\U0001F37B " + claim
    elif claim.lower() in roles.seer:
        return "\U0001F473 " + claim
    elif claim.lower() in roles.harlot:
        return "\U0001F48B " + claim
    elif claim.lower() in roles.bh:
        return "\U0001F441 " + claim
    elif claim.lower() in roles.gunner:
        return "\U0001F52B " + claim
    elif claim.lower() in roles.ga:
        return "\U0001F47C " + claim
    elif claim.lower() in roles.fool:
        return "\U0001F0CF " + claim
    elif claim.lower() in roles.mason:
        return "\U0001F477 " + claim
    elif claim.lower() in roles.dete:
        return "\U0001F575 " + claim
    elif claim.lower() in roles.apps:
        return "\U0001F647 " + claim
    elif claim.lower() in roles.ch:
        return "\U0001F482 " + claim
    elif claim.lower() in roles.cupid:
        return "\U0001F3F9 " + claim
    elif claim.lower() in roles.th:
        return "\U0001F3AF " + claim
    elif claim.lower() in roles.cg:
        return "\U0001F915 " + claim
    elif claim.lower() in roles.bs:
        return "\U00002692 " + claim 
    elif claim.lower() in roles.prince:
        return "\U0001F48D " + claim
    elif claim.lower() in roles.mayor:
        return "\U0001F396 " + claim
    elif claim.lower() in roles.oracle:
        return "\U0001F300 " + claim
    elif claim.lower() in roles.monarch:
        return "\U0001F451 " + claim
    elif claim.lower() in roles.paci:
        return "\U0000262E " + claim
    elif claim.lower() in roles.we:
        return "\U0001F4DA " + claim
    elif claim.lower() in roles.sm:
        return "\U0001F4A4 " + claim
    elif claim.lower() in roles.wolfman:
        return "\U0001F471\U0001F31A " + claim
    elif claim.lower() in roles.martyr:
        return "\U0001F530 " + claim
    elif claim.lower() in roles.alche:
        return "\U0001F375 " + claim
    elif claim.lower() in roles.squire:
        return "\U0001F6E1 " + claim
    elif claim.lower() in roles.beauty:
        return "\U0001F485 " + claim
    elif claim.lower() in roles.sb:
        return "\U0001F329 " + claim
    elif claim.lower() in roles.traitor:
        return "\U0001F595 " + claim
    elif claim.lower() in roles.wc:
        return "\U0001F476 " + claim
    elif claim.lower() in roles.cursed:
        return "\U0001F63E " + claim
    elif claim.lower() in roles.ww:
        return "\U0001F43A " + claim
    elif claim.lower() in roles.sorc:
        return "\U0001F52E " + claim
    elif claim.lower() in roles.alpha:
        return "\U000026A1 " + claim
    elif claim.lower() in roles.wolfcub:
        return "\U0001F436 " + claim
    elif claim.lower() in roles.lycan:
        return "\U0001F43A\U0001F31D " + claim
    elif claim.lower() in roles.prowl:
        return "\U0001F989 " + claim
    elif claim.lower() in roles.mystic:
        return "\U00002604 " + claim
    elif claim.lower() in roles.trickster:
        return "\U0001F411 " + claim
    elif claim.lower() in roles.fa:
        return "\U0001F47C\U0001F43A " + claim
    elif claim.lower() in roles.arso:
        return "\U0001F525 " + claim
    elif claim.lower() in roles.tanner:
        return "\U0001F47A " + claim
    elif claim.lower() in roles.cult:
        return "\U0001F464 " + claim
    elif claim.lower() in roles.thief:
        return "\U0001F608 " + claim
    elif claim.lower() in roles.ppm:
        return "\U0001F574 " + claim
    elif claim.lower() in roles.dg:
        return "\U0001F3AD " + claim
    elif claim.lower() in roles.sk:
        return "\U0001F52A " + claim
    elif claim.lower() in roles.bw:
        return "\U0001F43A\U0001F311 " + claim
    elif claim.lower() in roles.necro:
        return "\U000026B0 " + claim
    else:
        return claim
    
def command_claim(update, context):
    cid = update.message.chat_id
    fname = update.message.from_user.first_name
    message = update.message.text
    claim = message.split(" ", 1)
    game = GamesController.games.get(cid, None)
    msg = MsgController.msg.get(cid, None)
    
    if game:
        if len(claim) == 2:
            uid = update.message.from_user.id
            
            player = Player(fname, uid, get_emoji(claim[1]))
            game.add_player(uid, player)
            msg.get_msg(cid).delete()
            msg = context.bot.send_message(cid, game.print_claims(), parse_mode="Markdown")
            MsgController.msg[cid] = Message(cid, msg)

    else:
        GamesController.games[cid] = Game(cid, update.message.from_user.id)
        if len(claim) == 2:
            game = GamesController.games.get(cid, None)
            uid = update.message.from_user.id
            player = Player(fname, uid, get_emoji(claim[1]))
            game.add_player(uid, player)

            msg = context.bot.send_message(cid, game.print_claims(), parse_mode="Markdown")
            MsgController.msg[cid] = Message(cid, msg)

def command_claims(update, context):
    cid = update.message.chat_id
    game = GamesController.games.get(cid, None)
    msg = MsgController.msg.get(cid, None)
    if game:
        if len(game.playerlist) == 0:
            
            msg = update.message.reply_text("There are no claims yet!")
            MsgController.msg[cid] = Message(cid, msg)
        else:
            msg = context.bot.send_message(cid, game.print_claims(), parse_mode="Markdown")
            MsgController.msg[cid] = Message(cid, msg)
    else:
        msg = update.message.reply_text("There are no claims yet!")
        MsgController.msg[cid] = Message(cid, msg)

def command_reset(update, context):
    cid = update.message.chat_id
    msg = MsgController.msg.get(cid, None)
    game = GamesController.games.get(cid, None)

    if game:
        if len(game.playerlist) > 0:
            game.playerlist.clear()
            msg = update.message.reply_text("Reset claims list.")
            MsgController.msg[cid] = Message(cid, msg)
        else:
            msg.get_msg(cid).delete()
            msg = update.message.reply_text("There are no claims yet!")
            MsgController.msg[cid] = Message(cid, msg)
    else:
        msg = update.message.reply_text("There are no claims yet!")
        MsgController.msg[cid] = Message(cid, msg)

def command_unclaim(update, context):
    cid = update.message.chat_id
    msg = MsgController.msg.get(cid, None)
    game = GamesController.games.get(cid, None)

    if game:
        uid = update.message.from_user.id
        if uid in game.playerlist:
            game.remove_player(uid)
            msg.get_msg(cid).delete()
            if len(game.playerlist) == 0:
                msg = update.message.reply_text("There are no claims yet!")
                MsgController.msg[cid] = Message(cid, msg)
            else:
                msg = context.bot.send_message(cid, game.print_claims(), parse_mode="Markdown")
                MsgController.msg[cid] = Message(cid, msg)

def command_ping(update, context):
    update.message.reply_text("Pong!")

def command_coin(update, context):
    coin = ["Heads.", "Tails."]
    update.message.reply_text(random.choice(coin))

def command_help(update, context):
    cid = update.message.chat_id
    help_text = "The following commands are available:\n"
    for i in commands:
        help_text += i + "\n"
    context.bot.send_message(cid, help_text)

def main():
    GamesController.init()
    MsgController.init()

    updater = Updater("1384431621:AAH_HQnrZFJIA5F7WgmltLBUpBmQE1xNzPg", use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("ping", command_ping))
    dp.add_handler(CommandHandler("claim", command_claim))
    dp.add_handler(CommandHandler("claims", command_claims))
    dp.add_handler(CommandHandler("reset", command_reset))
    dp.add_handler(CommandHandler("flip", command_coin))
    dp.add_handler(CommandHandler("help", command_help))
    dp.add_handler(CommandHandler("unclaim", command_unclaim))

    updater.start_polling()

    updater.idle()

if __name__ == "__main__":
    main()