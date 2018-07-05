import json
from base64 import b64decode
from hashlib import blake2s
from os import environ
from sys import argv

import jwt
from flask import Flask, jsonify, request
from telegram.ext import CommandHandler, Updater

from dataclasses import dataclass


@dataclass
class BotConfig:
    '''Class for keeping track of bot configuration.'''
    bot_token: str
    user_id: str
    chat_id: str


@dataclass
class ServiceConfig:
    '''Class for keeping track of username and password.'''
    username: str
    password: str
    secret: str


# Service app
APP = Flask(__name__)
# Config objects
BOT_CFG = BotConfig(None, None, None)
SERVICE_CFG = ServiceConfig(None, None, None)
# BOT Updater
UPDATER = None


def validate_authorization(string):
    try:
        if string.find("Basic") == -1:
            return False
    except AttributeError:
        return False
    tmp = string.replace("Basic", "").strip()
    tmp = b64decode(tmp).decode("ascii")
    username, passwd = tmp.split(":")
    passwd = blake2s(passwd.encode("ascii")).hexdigest()
    if username != SERVICE_CFG.username or passwd != SERVICE_CFG.password:
        return False
    return True


def bot_start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hi!")
    if BOT_CFG.chat_id is None and BOT_CFG.chat_id is None:
        update.message.reply_text(
            "This is your id: '{}'".format(update.message.from_user.id))
        update.message.reply_text(
            "and this is the current chat id: '{}'".format(update.message.chat.id))
    elif update.message.from_user.id != int(BOT_CFG.chat_id):
        update.message.reply_text("I don't want to speak with you. Bye!")
        update.message.chat.leave()
    else:
        update.message.reply_text("I'm at your command!")


@APP.route('/botRegister', methods=['POST', 'PUT'])
def bot_register():
    auth = request.headers.get("Authorization")
    if not validate_authorization(auth):
        return "You're not authorized!", 401

    BOT_CFG.bot_token = request.form['bot_token']

    global UPDATER
    UPDATER = Updater(BOT_CFG.bot_token)
    dispatcher = UPDATER.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", bot_start))

    UPDATER.start_polling()

    return jsonify({
        'status': "OK",
        'message': "BOT STARTED!"
    })


@APP.route('/signup', methods=['POST', 'PUT'])
def signup():
    auth = request.headers.get("Authorization")
    if not validate_authorization(auth):
        return "You're not authorized!", 401

    data = {
        'user_id': blake2s(request.form['user_id'].encode("ascii")).hexdigest(),
        'chat_id': blake2s(request.form['chat_id'].encode("ascii")).hexdigest()
    }

    BOT_CFG.user_id = data['user_id']
    BOT_CFG.chat_id = data['chat_id']

    return jsonify({
        'service_token': jwt.encode(data, SERVICE_CFG.secret, algorithm='HS256').decode("utf-8")
    })


@APP.route('/notify', methods=['POST'])
def notify():
    token = request.form['service_token']
    try:
        jwt.decode(token, SERVICE_CFG.secret, algorithms=['HS256'])
    except jwt.InvalidTokenError:
        return "You're not authorized!", 401

    message = request.form['message']

    chat_member = UPDATER.bot.get_chat_member(BOT_CFG.chat_id, BOT_CFG.user_id)
    chat_member.user.send_message(message)

    return jsonify({
        'status': "OK",
        'message_sent': message
    })


if __name__ == "__main__":
    SERVICE_CFG.username = argv[1]
    SERVICE_CFG.password = blake2s(argv[2].encode("ascii")).hexdigest()
    SERVICE_CFG.secret = argv[3]
    APP.run(port=environ.get("PORT", 5555))
