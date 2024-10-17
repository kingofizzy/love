#
# Copyright (C) 2024 by THE-VIP-BOY-OP@Github, < https://github.com/THE-VIP-BOY-OP >.
#
# This file is part of < https://github.com/THE-VIP-BOY-OP/VIP-MUSIC > project,
# and is released under the MIT License.
# Please see < https://github.com/THE-VIP-BOY-OP/VIP-MUSIC/blob/master/LICENSE >
#
# All rights reserved.
#

import asyncio
import random

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from pyrogram.types import (
    ChatMemberUpdated,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import BANNED_USERS, adminlist
from strings import get_string
from VIPMUSIC import app
from VIPMUSIC.core.call import VIP
from VIPMUSIC.misc import SUDOERS
from VIPMUSIC.plugins import extra_plugins_enabled
from VIPMUSIC.utils.database import (
    delete_filter,
    get_assistant,
    get_cmode,
    get_lang,
    is_active_chat,
    is_commanddelete_on,
    is_maintenance,
    is_nonadmin_chat,
    set_loop,
)


@app.on_message(
    filters.command(["stop", "end", "cstop", "cend"]) & filters.group & ~BANNED_USERS
)
async def stop_music(cli, message: Message):
    if await is_maintenance() is False:
        if message.from_user.id not in SUDOERS:
            return await message.reply_text(
                "🍷 𝐶𝑢𝑡𝑒 𝐺𝑖𝑟𝑙 𝐾𝑢 𝑂𝑑𝑎𝑚𝑏𝑢 𝑆𝑎𝑟𝑖 🥺 𝑂𝑗𝑗𝑖𝑖 𝑃𝑜𝑑𝑎 𝑃𝑜𝑟𝑒𝑎𝑛 𝐴𝑝𝑚 𝑉𝑎𝑟𝑒𝑎𝑛 😻"
            )
    if not len(message.command) < 2:
        if extra_plugins_enabled:
            if not message.command[0][0] == "c" and not message.command[0][0] == "e":
                filter = " ".join(message.command[1:])
                deleted = await delete_filter(message.chat.id, filter)
                if deleted:
                    return await message.reply_text(f"**ᴅᴇʟᴇᴛᴇᴅ ғɪʟᴛᴇʀ {filter}.**")
                else:
                    return await message.reply_text("**ɴᴏ sᴜᴄʜ ғɪʟᴛᴇʀ.**")

    if await is_commanddelete_on(message.chat.id):
        try:
            await message.delete()
        except:
            pass
    try:
        language = await get_lang(message.chat.id)
        _ = get_string(language)
    except:
        _ = get_string("en")

    if message.sender_chat:
        upl = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="How to Fix this? ",
                        callback_data="AnonymousAdmin",
                    ),
                ]
            ]
        )
        return await message.reply_text(_["general_4"], reply_markup=upl)

    if message.command[0][0] == "c":
        chat_id = await get_cmode(message.chat.id)
        if chat_id is None:
            return await message.reply_text(_["setting_12"])
        try:
            await app.get_chat(chat_id)
        except:
            return await message.reply_text(_["cplay_4"])
    else:
        chat_id = message.chat.id
    if not await is_active_chat(chat_id):
        return await message.reply_text(_["general_6"])
    is_non_admin = await is_nonadmin_chat(message.chat.id)
    if not is_non_admin:
        if message.from_user.id not in SUDOERS:
            admins = adminlist.get(message.chat.id)
            if not admins:
                return await message.reply_text(_["admin_18"])
            else:
                if message.from_user.id not in admins:
                    return await message.reply_text(_["admin_19"])
    await VIP.st_stream(chat_id)
    await set_loop(chat_id, 0)
    await message.reply_text(_["admin_9"].format(message.from_user.mention))


from pyrogram import filters
from pyrogram.types import Message

from VIPMUSIC import app

photo = [
    "https://envs.sh/qeq.jpg",
    "https://envs.sh/qe0.jpg",
    "https://envs.sh/qeS.jpg",
    "https://envs.sh/qeW.jpg",
]


@app.on_chat_member_updated(filters.group, group=6)
async def assistant_banned(client: app, member: ChatMemberUpdated):
    chat_id = member.chat.id
    userbot = await get_assistant(chat_id)
    try:
        userbot = await get_assistant(member.chat.id)
        get = await app.get_chat_member(chat_id, userbot.id)
        if get.status in [ChatMemberStatus.BANNED]:

            # Assistant bot has been banned
            remove_by = member.from_user.mention if member.from_user else "🍷 𝐔𖽪𝙺𖽡𖽙𖽮 𝐔𖾗𖽞𖽷 😻"
            chat_id = member.chat.id
            title = member.chat.title
            username = (
                f"@{member.chat.username}" if member.chat.username else "🍷 𝐏𖽷𖽹ᵥ𖽖𖾓𖽞  𝐂𖽻𖽖𖾓 😻"
            )

            # Construct message
            left_message = (
                f" **☆ . * ● ¸ . ✦ .✩○☆° :. ★ * • ○ ° ★**</b>\n\n<b>"
                f" **     🦋‌𝆺𝅥𓆩〭〬𝐂𖽪֟፝‌𖾓𖾝 ԍ𖽹𖾜֟፝𖾘 ‌𝆺𝅥😻⤍🖤 **</b>\n\n<b>"
                f" **         𝐴𝑠𝑠𝑖𝑠𝑡𝑎𝑛𝑡 𝐵𝑎𝑛𝑛𝑒𝑑 ** </b>\n\n<b>"
                f" ** ➽───────────────────❥**</b>\n\n<b>"
                f" **🍷 𝐂𖽻𖽖𖾓 😻 ** {title}</b>\n\n<b>"
                f" ** 🍷𝐀𖾗𖾗 𝐈𖽴 😻 ** {userbot.id}</b>\n\n<b>"
                f" ** 🍷 𝐍𖽖𖽧𖽞 😻 ** @{userbot.username}</b>\n\n<b>"
                f" ** 🍷 𝐁𖽖𖽡 𝐁𝚢 😻 ** {remove_by}</b>\n\n<b>"
                f" **➽───────────────────❥**</b>\n\n<b>"
                f" ** ☆ . * ● ¸ . ✦ .✩○☆° :. ★ * • ○ ° ★ **</b>\n\n<b>"
            )

            # Create keyboard for unban button
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🍷 𝐔𖽡𖽜𖽖𖽡 𝐀𖾗𖾗𖽹𖾗𖾓𖽖𖽡𖾓  😻",
                            callback_data="unban_userbot",
                        )
                    ]
                ]
            )

            # Send photo with the left message and keyboard
            await app.send_photo(
                chat_id,
                photo=random.choice(photo),
                caption=left_message,
                reply_markup=keyboard,
            )
            # Perform actions like stopping streams or loops
            await VIP.st_stream(chat_id)
            await set_loop(chat_id, 0)
            await app.unban_chat_member(chat_id, userbot.id)
            await asyncio.sleep(10)
    except UserNotParticipant:
        await VIP.st_stream(chat_id)
        await set_loop(chat_id, 0)
        await app.unban_chat_member(chat_id, userbot.id)
        await asyncio.sleep(10)
        return
    except Exception as e:
        return


@app.on_chat_member_updated(filters.group, group=-8)
async def assistant_left(client: app, member: ChatMemberUpdated):
    chat_id = member.chat.id
    try:
        userbot = await get_assistant(chat_id)
        userbot_id = userbot.id

        # Check if the leaving member is the userbot
        if (
            not member.new_chat_member
            and member.old_chat_member.user.id == userbot_id
            and member.old_chat_member.status not in {"banned", "left", "restricted"}
            and member.old_chat_member
        ):
            left_message = (
                f"**Assistant Has Left This Chat**\n\n"
                f"**Id:** `{userbot.id}`\n"
                f"**Name:** @{userbot.username}\n\n"
                f"**Invite Assistant By: /userbotjoin**"
            )
            await app.send_photo(
                chat_id,
                photo=random.choice(photo),
                caption=left_message,
                reply_markup=keyboard,
            )

            await VIP.st_stream(chat_id)
            await set_loop(chat_id, 0)
            await asyncio.sleep(10)
    except UserNotParticipant:
        left_message = (
            f"**Assistant Has Left This Chat**\n\n"
            f"**Id:** `{userbot.id}`\n"
            f"**Name:** @{userbot.username}\n\n"
            f"**Invite Assistant By: /userbotjoin**"
        )
        await app.send_photo(
            chat_id,
            photo=random.choice(photo),
            caption=left_message,
            reply_markup=keyboard,
        )
        await VIP.st_stream(chat_id)
        await set_loop(chat_id, 0)
        await asyncio.sleep(10)
    except Exception as e:
        return


@app.on_message(filters.video_chat_started & filters.group)
async def brah(_, msg):
    chat_id = msg.chat.id
    try:
        await msg.reply("**𝑉𝑎𝑛𝑡ℎ𝑢 𝐾𝑎𝑑ℎ𝑎𝑙 𝑃𝑎𝑛𝑛𝑢𝑛𝑔𝑎 𝑉𝑐 𝐿𝑎 𝐷𝑜𝑙𝑖 & 𝐷𝑜𝑙𝑎𝑛𝑠 🫶🏻🫴🏻🤍**")
        await VIP.st_stream(chat_id)
        await set_loop(chat_id, 0)
    except Exception as e:
        return await msg.reply(f"**Error {e}**")


# vc off
@app.on_message(filters.video_chat_ended & filters.group)
async def brah2(_, msg):
    chat_id = msg.chat.id
    try:
        await msg.reply("**🤧💫 𝑉𝑐 𝐸𝑣𝑎𝑛𝑑𝑎 𝐸𝑛𝑑 𝑃𝑎𝑛𝑛𝑢𝑛𝑎𝑡ℎ𝑢 🥹🤌🏻**")
        await VIP.st_stream(chat_id)
        await set_loop(chat_id, 0)
    except Exception as e:
        return await msg.reply(f"**Error {e}**")
