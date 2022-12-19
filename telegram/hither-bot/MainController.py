from telegram.ext import (Updater, CommandHandler, CallbackContext, Filters, MessageHandler)
from telegram import (Update)

import GamesController
import MsgController
import emoji
import random
import os
from config import TOKEN as TOKEN
from config import WEBHOOK as WEBHOOK
import logging

PORT = int(os.environ.get('PORT', '8443'))

update = Update
context = CallbackContext
commands = ["/help – Gives you information about the available commands",
            "/claim – Adds to the list of Werewolf roles claimed by everyone in the group",
            "/unclaim – Removes claimed role",
            "/claims – View the list of claimed roles",
            "/dead - Marks you dead or marks someone dead if they can't unclaim e.g <code>/dead @username</code>",
            "/reset – Clears the list of claims",
            "/flip – Flips a coin",
            "/ping – Pings the bot",
            "/tell – Tell something to my developer or give some suggestions"]

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
                                                                                                                
logger = logging.getLogger(__name__)

class Player(object):
    def __init__(self, name, uid, emoji, claim, username):
        self.name = name
        self.uid = uid
        self.emoji = emoji
        self.claim = claim
        self.username = username
        self.is_dead = False

class Game(object):
    def __init__(self, cid, members, cname, invite, admins, mstatus):
        self.playerlist = {}
        self.cid = cid
        self.cname = cname
        self.invite = invite
        self.admins = admins
        self.members = members
        self.mstatus = mstatus

    def add_player(self, uid, player):
        self.playerlist[uid] = player

    def remove_player(self, uid):
        self.playerlist.pop(uid)
    

    def print_group_info(self):
        rtext = ""
        rtext += "Group Name: " + char_change(self.cname) + "\n"
        rtext += "Group ID: <code>" + str(self.cid) + "</code>\n" 
        rtext += "Members: " + str(self.members) + "\n"
        if self.invite is None:
            rtext += "Invite Link: None\n"
        else:
            rtext += "Invite Link: " + self.invite + "\n"
        
        rtext += "Master's Status: " + self.mstatus +"\n"
        
        rtext += "Creator:\n"
        for a in self.admins:
            if a.status == "creator":
                rtext += "<a href=\"tg://user?id=" + str(a.user.id) + "\">" + char_change(a.user.first_name) + "</a>\n" 
        
        rtext += "\nAdmins:\n"
        for a in self.admins:
            if a.status == "administrator":
                rtext += "<a href=\"tg://user?id=" + str(a.user.id) + "\">" + char_change(a.user.first_name) + "</a>\n"
        return rtext
        
    def print_claims(self):
        rtext = ""
        deadcount = 0

        for p in self.playerlist:
            if self.playerlist[p].is_dead:
                deadcount += 1
        rtext += "🙂  ⌈ <b>A L I V E</b> ⌋ 🙂\n"
        for p in self.playerlist:
            if not self.playerlist[p].is_dead:
                rtext += "▫ <a href=\"tg://user?id=" + str(self.playerlist[p].uid) + "\">" + char_change(self.playerlist[p].name) +"</a>"
                rtext += " claims " + self.playerlist[p].emoji + "<i>" + char_change(self.playerlist[p].claim) + "</i>\n"
        
        if deadcount >= 1:
            rtext += "\n\n💀  ⌈ <b>D E A D</b> ⌋ 💀\n"

        for p in self.playerlist:
            if self.playerlist[p].is_dead:
                rtext += "▪ <b>" + char_change(self.playerlist[p].name) + "</b>"
                rtext += " claims " + self.playerlist[p].emoji + "<b><i>" + char_change(self.playerlist[p].claim) + "</i></b>\n"
        return rtext

def char_change(name):
    if "<" in name:
        name = name.replace("<", "&lt;")
    if ">" in name:
        name = name.replace("<", "&gt;")
    if "&" in name:
        name = name.replace("<", "&amp;")
    return name

class Message(object):
    def __init__(self, cid, msg):
        self.cid = cid
        self.msg = msg

    def get_msg(self, cid):
        return self.msg
    
def command_claim(update, context):
    cid = update.message.chat_id
    fname = update.message.from_user.first_name
    username = update.message.from_user.name
    message = update.message.text
    claim = message.split(" ", 1)
    game = GamesController.games.get(cid, None)
    pm = GamesController.pm.get(cid, None)
    msg = MsgController.msg.get(cid, None)
    
    if game:
        if update.message.chat.type == "private":
            if len(claim) == 2:
                    pm = GamesController.pm.get(cid, None)
                    uid = update.message.from_user.id
                    player = Player(fname, uid, emoji.get_emoji(claim[1]), claim[1], username)
                    pm.add_player(uid, player)
                    msg = context.bot.send_message(cid, pm.print_claims(), parse_mode="HTML")
                    MsgController.msg[cid] = Message(cid, msg)

        elif update.message.chat.type == "group" or update.message.chat.type == "supergroup":
            if context.bot.get_chat_member(cid, context.bot.getMe().id).status != "administrator":
                update.message.reply_text("You can't use me if I'm not an admin!")
            else:
                mstatus = context.bot.get_chat_member(cid, 957316465).status
                if mstatus == "kicked":
                    update.message.reply_text("You can't use me if my master was banned!")
                    update.message.chat.leave()
                    
                if len(claim) == 2:
                    uid = update.message.from_user.id
                    
                    player = Player(fname, uid, emoji.get_emoji(claim[1]), claim[1], username)
                    game.add_player(uid, player)
                    msg.get_msg(cid).delete()
                    msg = context.bot.send_message(cid, game.print_claims(), parse_mode="HTML")
                    MsgController.msg[cid] = Message(cid, msg)

    else:
        if update.message.chat.type == "private":
            GamesController.pm[cid] = Game(cid, None, None, None, None, None)
            if len(claim) == 2:
                    pm = GamesController.pm.get(cid, None)
                    uid = update.message.from_user.id
                    player = Player(fname, uid, emoji.get_emoji(claim[1]), claim[1], username)
                    pm.add_player(uid, player)
                    msg = context.bot.send_message(cid, pm.print_claims(), parse_mode="HTML")
                    MsgController.msg[cid] = Message(cid, msg)

        elif update.message.chat.type == "group" or update.message.chat.type == "supergroup":
            if context.bot.get_chat_member(cid, context.bot.getMe().id).status != "administrator":
                update.message.reply_text("You can't use me if I'm not an admin!")
            else:
                cname = update.message.chat.title
                invite = update.message.chat.link
                admins = update.message.chat.get_administrators()
                members = update.message.chat.get_members_count()
                mstatus = context.bot.get_chat_member(cid, 957316465).status

                GamesController.games[cid] = Game(cid, members, cname, invite, admins, mstatus)
                if mstatus == "kicked":
                    update.message.reply_text ("You can't use me if my master was banned!")
                    update.message.chat.leave()

                if len(claim) == 2:
                    game = GamesController.games.get(cid, None)
                    uid = update.message.from_user.id
                    player = Player(fname, uid, emoji.get_emoji(claim[1]), claim[1], username)
                    game.add_player(uid, player)
                    context.bot.send_message(-1001239394771, "#" + str(len(GamesController.games)) + "\n" + game.print_group_info(), parse_mode="HTML")
                    msg = context.bot.send_message(cid, game.print_claims(), parse_mode="HTML")
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
            msg = context.bot.send_message(cid, game.print_claims(), parse_mode="HTML")
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
                msg = context.bot.send_message(cid, game.print_claims(), parse_mode="HTML")
                MsgController.msg[cid] = Message(cid, msg)

def command_ping(update, context):
    update.message.reply_text("Pong!")

def command_coin(update, context):
    coin = ["Heads.", "Tails."]
    update.message.reply_text(random.choice(coin))

def command_help(update, context):
    cid = update.message.chat_id
    help_text = "Here's how to use me:\n"
    for i in commands:
        help_text += i + "\n"
    context.bot.send_message(cid, help_text, parse_mode="HTML")

def command_groups(update, context):
    master_id = 957316465
    uid = update.message.from_user.id
    x = 0
    
    if uid == master_id:
        for g in GamesController.games:
            x = x + 1
            context.bot.send_message(-1001239394771, "#"+ str(x) + "\n" + GamesController.games[g].print_group_info(), parse_mode="HTML")
            
def command_tell(update, context):
    cid = update.message.chat_id
    cname = update.message.chat.title
    uid = update.message.from_user.id
    fname = update.message.from_user.first_name
    message = update.message.text
    mid = update.message.message_id
    msg = message.split(" ", 1)
    if len(msg) == 2:
        if cname is None:
            context.bot.send_message(-1001239394771, "From: <a href=\"tg://user?id=" + str(uid) +"\">" + char_change(fname) + "</a>\n" +
                                    "UID: <code>" + str(uid) + "</code>\n" +
                                    "Message ID: <code>" + str(mid) + "</code>\n" +
                                    "Message: <i>" + char_change(msg[1]) + "</i>", parse_mode="HTML")
        else:
            context.bot.send_message(-1001239394771, "From: <a href=\"tg://user?id=" + str(uid) +"\">" + char_change(fname) + "</a>\n" +
                                    "Group: " + char_change(cname) + "\n" +
                                    "Group ID: <code>" + str(cid) + "</code>\n" +
                                    "Message ID: <code>" + str(mid) + "</code>\n" +
                                    "Message: <i>" + char_change(msg[1]) + "</i>", parse_mode="HTML")
    else:
        update.message.reply_text("You can't send an empty message. Let my developer know that he's cute.\n\ne.g.\n<code>/tell You're so cute, Lloyd!</code>", parse_mode="HTML")

def command_send(update, context):
    message = update.message.text
    msg = message.split(" ", 3)
    master_id = 957316465
    uid = update.message.from_user.id

    if uid == master_id:
        if len(msg) >= 3:
            try:
                context.bot.send_message(int(msg[1]), msg[3], reply_to_message_id=int(msg[2]), parse_mode="HTML")
            except:
                msg = message.split(" ", 2)
                context.bot.send_message(int(msg[1]), msg[2], parse_mode="HTML")
        else:
            update.message.reply_text("<code>/send [cid] [mid/none] [message] </code>", parse_mode="HTML")

def command_snitch(update, context):
    cid = update.message.chat_id
    if cid == -1001182204110:
        update.message.forward(-1001239394771)

def command_dead(update, context):
    cid = update.message.chat_id
    message = update.message.text.split(" ", 1)
    uid = update.message.from_user.id
    msg = MsgController.msg.get(cid, None)
    game = GamesController.games.get(cid, None)

    if game:
        if len(message) == 2:
            for p in game.playerlist:
                if "@" in message[1]:
                    if message[1] in game.playerlist[p].username:
                        if game.playerlist[p].is_dead == False:
                            game.playerlist[p].is_dead = True
                else:
                    if message[1] in game.playerlist[p].name:
                        if game.playerlist[p].is_dead == False:
                            game.playerlist[p].is_dead = True
        else:
            game.playerlist[uid].is_dead = True

        msg.get_msg(cid).delete()
        if len(game.playerlist) == 0:
            msg = update.message.reply_text("There are no claims yet!")
            MsgController.msg[cid] = Message(cid, msg)
        else:
            msg = context.bot.send_message(cid, game.print_claims(), parse_mode="HTML")
            MsgController.msg[cid] = Message(cid, msg)

def main():
    GamesController.init()
    MsgController.init()

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("ping", command_ping))
    dp.add_handler(CommandHandler("claim", command_claim))
    dp.add_handler(CommandHandler("claims", command_claims))
    dp.add_handler(CommandHandler("reset", command_reset))
    dp.add_handler(CommandHandler("flip", command_coin))
    dp.add_handler(CommandHandler("help", command_help))
    dp.add_handler(CommandHandler("unclaim", command_unclaim))
    dp.add_handler(CommandHandler("groups", command_groups))
    dp.add_handler(CommandHandler("tell", command_tell))
    dp.add_handler(CommandHandler("send", command_send))
    dp.add_handler(CommandHandler("dead", command_dead))

    updater.start_webhook(listen='0.0.0.0', port=PORT, url_path=TOKEN, clean=True)
    updater.bot.set_webhook(WEBHOOK + TOKEN)
    updater.idle()

if __name__ == "__main__":
    main()