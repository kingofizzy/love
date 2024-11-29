from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ChatMembersFilter
from pyrogram.types import (
    CallbackQuery,
    ChatJoinRequest,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from VIPMUSIC import app

def build_keyboard(buttons):
    keyboard = [
        [InlineKeyboardButton(text, callback_data=data) for text, data in buttons.items()]
    ]
    return InlineKeyboardMarkup(keyboard)

@app.on_chat_join_request(filters.group)
async def handle_join_request(client, request: ChatJoinRequest):
    chat = request.chat
    user = request.from_user

    text = (
        f"**Join Request:**\n"
        f"User: {user.mention}\n"
        f"Requested to join the group: {chat.title}\n\n"
        f"Admins can approve or decline the request."
    )

    buttons = {
        "✅ Approve": f"approve_{user.id}",
        "❌ Decline": f"decline_{user.id}",
    }
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text, callback_data=data) for text, data in buttons.items()]]
    )

    await app.send_message(
        chat_id=chat.id,
        text=text,
        reply_markup=keyboard
    )
    
@app.on_callback_query(filters.regex("^(approve|decline)_(.*)"))
async def handle_approval(client, cb: CallbackQuery):
    chat = cb.message.chat
    admin_id = cb.from_user.id
    member = await chat.get_member(admin_id)

    if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        if member.privileges.can_restrict_members:
            action, user_id = cb.data.split("_", 1)
            user_id = int(user_id)

            if action == "approve":
                await client.approve_chat_join_request(chat.id, user_id)
                await cb.message.edit_text(f"User approved by {cb.from_user.mention}")
            elif action == "decline":
                await client.decline_chat_join_request(chat.id, user_id)
                await cb.message.edit_text(f"User declined by {cb.from_user.mention}")
        else:
            await cb.answer("You don't have the required permissions.", show_alert=True)
    else:
        await cb.answer("Only admins can perform this action.", show_alert=True)

