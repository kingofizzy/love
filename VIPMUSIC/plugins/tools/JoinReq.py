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
from VIPMUSIC.core.mongo import mongodb
from VIPMUSIC.misc import SUDOERS

approvaldb = mongodb.autoapprove


def build_keyboard(buttons):
    keyboard = [
        [InlineKeyboardButton(text, callback_data=data) for text, data in buttons.items()]
    ]
    return InlineKeyboardMarkup(keyboard)


@app.on_message(filters.command("autoapprove") & filters.group)
async def approval_command(client, message: Message):
    chat_id = message.chat.id
    admin = await client.get_chat_member(chat_id, message.from_user.id)

    if admin.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER] or not admin.privileges.can_restrict_members:
        return await message.reply_text("You don't have permission to do this.")

    chat_data = await approvaldb.find_one({"chat_id": chat_id})
    mode = chat_data.get("mode", "manual") if chat_data else "manual"
    new_mode = "automatic" if mode == "manual" else "manual"

    buttons = {f"Switch to {new_mode.upper()}": f"approval_{new_mode}"}
    keyboard = build_keyboard(buttons)

    if chat_data:
        await approvaldb.update_one({"chat_id": chat_id}, {"$set": {"mode": new_mode}})
    else:
        await approvaldb.insert_one({"chat_id": chat_id, "mode": new_mode})

    await message.reply_text(
        f"Auto-approval for this group is now set to <b>{new_mode.upper()}</b>.",
        reply_markup=keyboard,
    )


@app.on_callback_query(filters.regex(r"approval_(.*)"))
async def approval_cb(client, cb: CallbackQuery):
    chat_id = cb.message.chat.id
    admin = await client.get_chat_member(chat_id, cb.from_user.id)

    if admin.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER] or not admin.privileges.can_restrict_members:
        return await cb.answer("You don't have permission to do this.", show_alert=True)

    new_mode = cb.data.split("_")[1]
    await approvaldb.update_one(
        {"chat_id": chat_id},
        {"$set": {"mode": new_mode}},
        upsert=True,
    )
    await cb.edit_message_text(
        f"Auto-approval for this group is now set to <b>{new_mode.upper()}</b>."
    )


@app.on_chat_join_request(filters.group)
async def accept_join_request(client, request: ChatJoinRequest):
    chat_id = request.chat.id
    user_id = request.from_user.id

    chat_data = await approvaldb.find_one({"chat_id": chat_id})
    if not chat_data or chat_data.get("mode", "manual") == "manual":
        # Manual mode: Notify admins
        pending_users = chat_data.get("pending_users", [])
        if user_id not in pending_users:
            await approvaldb.update_one(
                {"chat_id": chat_id},
                {"$addToSet": {"pending_users": user_id}},
                upsert=True,
            )
        admin_message = (
            f"User {request.from_user.mention} has requested to join.\n"
            f"Admins can approve or decline."
        )
        buttons = {
            "Approve": f"manual_approve_{user_id}",
            "Decline": f"manual_decline_{user_id}",
        }
        keyboard = build_keyboard(buttons)
        admin_list = [
            admin.user.id
            async for admin in client.get_chat_members(
                chat_id, filter=ChatMembersFilter.ADMINISTRATORS
            )
            if not admin.user.is_bot and not admin.user.is_deleted
        ]
        for admin_id in admin_list:
            await client.send_message(admin_id, admin_message, reply_markup=keyboard)
    else:
        # Automatic mode: Approve immediately
        await client.approve_chat_join_request(chat_id, user_id)


@app.on_callback_query(filters.regex(r"manual_(approve|decline)_(\d+)"))
async def manual_action(client, cb: CallbackQuery):
    action, user_id = cb.data.split("_")[1:]
    user_id = int(user_id)
    chat_id = cb.message.chat.id

    admin = await client.get_chat_member(chat_id, cb.from_user.id)
    if admin.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER] or not admin.privileges.can_restrict_members:
        return await cb.answer("You don't have permission to do this.", show_alert=True)

    if action == "approve":
        await client.approve_chat_join_request(chat_id, user_id)
    elif action == "decline":
        await client.decline_chat_join_request(chat_id, user_id)

    await approvaldb.update_one(
        {"chat_id": chat_id},
        {"$pull": {"pending_users": user_id}},
    )
    await cb.message.delete()
