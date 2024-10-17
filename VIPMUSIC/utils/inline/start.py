from pyrogram.types import InlineKeyboardButton

import config
from config import SUPPORT_GROUP
from VIPMUSIC import app


def start_pannel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="🍷 𝐂𖾘𖽹𖽝ᴋ 𝐇𖽞𖽖𖽞 𝐓𖽙 𝐀𖽴𖽴 𝐌𖽞 😻",
                url=f"https://t.me/{app.username}?startgroup=true",
            ),
        ],
        [
            InlineKeyboardButton(text="🍷 𝐇𖽞𖾘𖽳 😻", callback_data="settings_back_helper"),
            InlineKeyboardButton(text="🍷 𝐒𖽞𖾓 😻", callback_data="settings_helper"),
        ],
        [
            InlineKeyboardButton(text="🍷 𝐆𖽷𖽙𖽪𖽳 😻", url=config.SUPPORT_GROUP),
        ],
    ]
    return buttons


def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="🍷 𝐂𖾘𖽹𖽝ᴋ 𝐇𖽞𖽖𖾖 𝐓𖽙 𝐀𖽴𖽴 𝐌𖽞 😻",
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(text="🍷 𝐆𖽷𖽙𖽪𖽳 😻", url=config.SUPPORT_GROUP),
            InlineKeyboardButton(text="🍷 𝐌𖽙𖽷𖽞 😻", url=config.SUPPORT_CHANNEL),
        ],
        [
            InlineKeyboardButton(
                text="🍷 𝐅𖽞𖽖𖾓𖽪𖽷𖽞𖾗 😻", callback_data="settings_back_helper"
            )
        ],
    ]
    return buttons


def alive_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="🍷 𝐀𖽴𖽴 𝐌𖽞 😻", url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text=_["S_B_3"], url=f"{SUPPORT_GROUP}"),
        ],
    ]
    return buttons


def music_start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="🍷 𝐂𖾘𖽹𖽝ᴋ 𝐇𖽞𖽖𖽞 𝐓𖽙 𝐀𖽴𖽴 𝐌𖽞 😻",
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(text="🍷 𝐀𖽜𖽙𖽪𖾓 😻", callback_data="about"),
            InlineKeyboardButton(text="🍷 𝐒𖽪𖽳𖽳𖽙𖽷𖾓 😻", callback_data="support"),
        ],
        [InlineKeyboardButton(text="🍷 𝐅𖽞𖽖𖾓𖽪𖽷𖽞𖾗 😻", callback_data="feature")],
    ]
    return buttons
