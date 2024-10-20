# Copyright (C) 2024 by THE-VIP-BOY-OP@Github, < https://github.com/THE-VIP-BOY-OP >.
#
# This file is part of < https://github.com/THE-VIP-BOY-OP/VIP-MUSIC > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/THE-VIP-BOY-OP/VIP-MUSIC/blob/master/LICENSE >
#
# All rights reserved.
#

import uvloop

uvloop.install()

import pyrogram
import pyromod.listen  # noqa
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (
    BotCommand,
    BotCommandScopeAllChatAdministrators,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

import config

from ..logging import LOGGER


class VIPBot(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot")
        super().__init__(
            "VIPMUSIC",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.mention = self.me.mention

        # Create the button
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="๏ ᴀᴅᴅ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ ๏",
                        url=f"https://t.me/{self.username}?startgroup=true",
                    )
                ]
            ]
        )

        # Try to send a message to the logger group
        if config.LOG_GROUP_ID:
            try:
                await self.send_photo(
                    config.LOG_GROUP_ID,
                    photo=config.START_IMG_URL,
                    caption=f"╔════❰𝐖𝐄𝐋𝐂𝐎𝐌𝐄❱════❍⊱❁۪۪\n║\n║┣⪼🥀𝐁𝐨𝐭 𝐒𝐭𝐚𝐫𝐭𝐞𝐝 𝐁𝐚𝐛𝐲🎉\n║\n║┣⪼ {self.name}\n║\n║┣⪼🎈𝐈𝐃:- `{self.id}` \n║\n║┣⪼🎄@{self.username} \n║ \n║┣⪼💖𝐓𝐡𝐚𝐧𝐤𝐬 𝐅𝐨𝐫 𝐔𝐬𝐢𝐧𝐠😍\n║\n╚════════════════❍⊱❁",
                    reply_markup=button,
                )
            except pyrogram.errors.ChatWriteForbidden as e:
                LOGGER(__name__).error(f"Bot cannot write to the log group: {e}")
                try:
                    await self.send_message(
                        config.LOG_GROUP_ID,
                        f"╔═══❰𝐖𝐄𝐋𝐂𝐎𝐌𝐄❱═══❍⊱❁۪۪\n║\n║┣⪼🥀𝐁𝐨𝐭 𝐒𝐭𝐚𝐫𝐭𝐞𝐝 𝐁𝐚𝐛𝐲🎉\n║\n║◈ {self.name}\n║\n║┣⪼🎈𝐈𝐃:- `{self.id}` \n║\n║┣⪼🎄@{self.username} \n║ \n║┣⪼💖𝐓𝐡𝐚𝐧𝐤𝐬 𝐅𝐨𝐫 𝐔𝐬𝐢𝐧𝐠😍\n║\n╚══════════════❍⊱❁",
                        reply_markup=button,
                    )
                except Exception as e:
                    LOGGER(__name__).error(f"Failed to send message in log group: {e}")
            except Exception as e:
                LOGGER(__name__).error(
                    f"Unexpected error while sending to log group: {e}"
                )
        else:
            LOGGER(__name__).warning(
                "LOG_GROUP_ID is not set, skipping log group notifications."
            )

        # Setting commands
        if config.SET_CMDS:
            try:
                await self.set_bot_commands(
                    commands=[
                        BotCommand("start", "𝑆𝑡𝑎𝑟𝑡 𝑡ℎ𝑒 𝑏𝑜𝑡"),
                        BotCommand("help", "𝐺𝑒𝑡 𝑡ℎ𝑒 ℎ𝑒𝑙𝑝 𝑚𝑒𝑛𝑢"),
                        BotCommand("ping", "𝐶ℎ𝑒𝑐𝑘 𝑖𝑓 𝑡ℎ𝑒 𝑏𝑜𝑡 𝑖𝑠 𝑎𝑙𝑖𝑣𝑒 𝑜𝑟 𝑑𝑒𝑎𝑑"),
                    ],
                    scope=BotCommandScopeAllPrivateChats(),
                )
                await self.set_bot_commands(
                    commands=[
                        BotCommand("play", "𝑆𝑡𝑎𝑟𝑡 𝑝𝑙𝑎𝑦𝑖𝑛𝑔 𝑟𝑒𝑞𝑢𝑒𝑠𝑡𝑒𝑑 𝑠𝑜𝑛𝑔"),
                        BotCommand("stop", "𝑆𝑡𝑜𝑝 𝑡ℎ𝑒 𝑐𝑢𝑟𝑟𝑒𝑛𝑡 𝑠𝑜𝑛𝑔"),
                        BotCommand("pause", "𝑃𝑎𝑢𝑠𝑒 𝑡ℎ𝑒 𝑐𝑢𝑟𝑟𝑒𝑛𝑡 𝑠𝑜𝑛𝑔"),
                        BotCommand("resume", "𝑅𝑒𝑠𝑢𝑚𝑒 𝑡ℎ𝑒 𝑝𝑎𝑢𝑠𝑒𝑑 𝑠𝑜𝑛𝑔"),
                        BotCommand("queue", "𝐶ℎ𝑒𝑐𝑘 𝑡ℎ𝑒 𝑞𝑢𝑒𝑢𝑒 𝑜𝑓 𝑠𝑜𝑛𝑔𝑠"),
                        BotCommand("skip", "𝑆𝑘𝑖𝑝 𝑡ℎ𝑒 𝑐𝑢𝑟𝑟𝑒𝑛𝑡 𝑠𝑜𝑛𝑔"),
                        BotCommand("volume", "𝐴𝑑𝑗𝑢𝑠𝑡 𝑡ℎ𝑒 𝑚𝑢𝑠𝑖𝑐 𝑣𝑜𝑙𝑢𝑚𝑒"),
                        BotCommand("lyrics", "𝐺𝑒𝑡 𝑙𝑦𝑟𝑖𝑐𝑠 𝑜𝑓 𝑡ℎ𝑒 𝑠𝑜𝑛𝑔"),
                    ],
                    scope=BotCommandScopeAllGroupChats(),
                )
                await self.set_bot_commands(
                    commands=[
                        BotCommand("start", "𝑆𝑡𝑎𝑟𝑡 𝑡ℎ𝑒 𝑏𝑜𝑡"),
                        BotCommand("ping", "𝐶ℎ𝑒𝑐𝑘 𝑡ℎ𝑒 𝑝𝑖𝑛𝑔"),
                        BotCommand("help", "𝐺𝑒𝑡 ℎ𝑒𝑙𝑝"),
                        BotCommand("vctag", "𝑇𝑎𝑔 𝑎𝑙𝑙 𝑓𝑜𝑟 𝑣𝑜𝑖𝑣𝑒 𝑐ℎ𝑎𝑡"),
                        BotCommand("stopvctag", "𝑆𝑡𝑜𝑝 𝑡𝑎𝑔𝑔𝑖𝑛𝑔 𝑓𝑜𝑟 𝑉𝑐"),
                        BotCommand("tagall", "𝑇𝑎𝑔 𝑎𝑙𝑙 𝑚𝑒𝑚𝑏𝑒𝑟𝑠 𝑏𝑦 𝑡𝑒𝑥𝑡"),
                        BotCommand("cancel", "𝐶𝑎𝑛𝑐𝑒𝑙 𝑡ℎ𝑒 𝑡𝑎𝑔𝑔𝑖𝑛𝑔"),
                        BotCommand("settings", "𝐺𝑒𝑡 𝑡ℎ𝑒 𝑠𝑒𝑡𝑡𝑖𝑛𝑔𝑠"),
                        BotCommand("reload", "𝑅𝑒𝑙𝑜𝑎𝑑 𝑡ℎ𝑒 𝑏𝑜𝑡"),
                        BotCommand("play", "𝑃𝑙𝑎𝑦 𝑡ℎ𝑒 𝑟𝑒𝑞𝑢𝑒𝑠𝑡𝑒𝑑 𝑠𝑜𝑛𝑔"),
                        BotCommand("vplay", "𝑃𝑙𝑎𝑦 𝑣𝑖𝑑𝑒𝑜 𝑎𝑙𝑜𝑛𝑔 𝑤𝑖𝑡ℎ 𝑚𝑢𝑠𝑖𝑐"),
                        BotCommand("end", "𝐸𝑚𝑝𝑡𝑦 𝑡ℎ𝑒 𝑞𝑢𝑒𝑢𝑒"),
                        BotCommand("playlist", "𝐺𝑒𝑡 𝑡ℎ𝑒 𝑝𝑙𝑎𝑦𝑙𝑖𝑠𝑡"),
                        BotCommand("stop", "𝑆𝑡𝑜𝑝 𝑡ℎ𝑒 𝑠𝑜𝑛𝑔"),
                        BotCommand("lyrics", "𝐺𝑒𝑡 𝑡ℎ𝑒 𝑠𝑜𝑛𝑔 𝑙𝑦𝑟𝑖𝑐𝑠"),
                        BotCommand("song", "𝐷𝑜𝑤𝑛𝑙𝑜𝑎𝑑 𝑡ℎ𝑒 𝑟𝑒𝑞𝑢𝑒𝑠𝑡𝑒𝑑"),
                        BotCommand("video", "𝐷𝑜𝑤𝑛𝑙𝑜𝑎𝑑 𝑡ℎ𝑒 𝑟𝑒𝑞𝑢𝑒𝑠𝑡𝑒𝑑 𝑣𝑖𝑑𝑒𝑜 𝑠𝑜𝑛𝑔"),
                        BotCommand("gali", "𝑅𝑒𝑝𝑙𝑦 𝑤𝑖𝑡ℎ 𝑓𝑢𝑛"),
                        BotCommand("shayri", "𝐺𝑒𝑡 𝑎 𝑠ℎ𝑎𝑦𝑎𝑟𝑖"),
                        BotCommand("love", "𝐺𝑒𝑡 𝑎 𝑙𝑜𝑣𝑒 𝑠ℎ𝑎𝑦𝑎𝑟𝑖"),
                        BotCommand("sudolist", "𝐶ℎ𝑒𝑐𝑘 𝑡ℎ𝑒 𝑠𝑢𝑑𝑜 𝑙𝑖𝑠𝑡"),
                        BotCommand("owner", "𝐶ℎ𝑒𝑐𝑘 𝑡ℎ𝑒 𝑜𝑤𝑛𝑒𝑟"),
                        BotCommand("update", "𝑈𝑝𝑑𝑎𝑡𝑒 𝑏𝑜𝑡 "),
                        BotCommand("gstats", "𝐺𝑒𝑡 𝑠𝑡𝑎𝑡𝑠 𝑜𝑓 𝑡ℎ𝑒 𝑏𝑜𝑡"),
                        BotCommand("repo", "𝐶ℎ𝑒𝑐𝑘 𝑡ℎ𝑒 𝑟𝑒𝑝𝑜"),
                    ],
                    scope=BotCommandScopeAllChatAdministrators(),
                )
            except Exception as e:
                LOGGER(__name__).error(f"Failed to set bot commands: {e}")

        # Check if bot is an admin in the logger group
        if config.LOG_GROUP_ID:
            try:
                chat_member_info = await self.get_chat_member(
                    config.LOG_GROUP_ID, self.id
                )
                if chat_member_info.status != ChatMemberStatus.ADMINISTRATOR:
                    LOGGER(__name__).error(
                        "Please promote Bot as Admin in Logger Group"
                    )
            except Exception as e:
                LOGGER(__name__).error(f"Error occurred while checking bot status: {e}")

        LOGGER(__name__).info(f"MusicBot Started as {self.name}")
