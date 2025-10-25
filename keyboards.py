"""
Inline keyboards for INEX CONSULTING Bot
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List
from config import CHANNEL_URL
from texts import get_text


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Language selection keyboard"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz"),
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")
    )
    return builder.as_markup()


def get_channel_subscription_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Channel subscription keyboard"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="📢 INEX CONSULTING",
            url=CHANNEL_URL
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text('check_subscription', lang),
            callback_data="check_subscription"
        )
    )
    return builder.as_markup()


def get_meeting_dates_keyboard(dates: List[str], lang: str = 'uz') -> InlineKeyboardMarkup:
    """Meeting dates selection keyboard"""
    builder = InlineKeyboardBuilder()

    for date in dates:
        builder.row(
            InlineKeyboardButton(
                text=f"📅 {date}",
                callback_data=f"date_{date}"
            )
        )

    return builder.as_markup()


def get_admin_main_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Admin main menu keyboard"""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=get_text('view_registrations', lang),
            callback_data="admin_view_registrations"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text('manage_dates', lang),
            callback_data="admin_manage_dates"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text('export_and_clear', lang),
            callback_data="admin_export_and_clear"
        )
    )

    return builder.as_markup()


def get_admin_dates_management_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Admin dates management keyboard"""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=get_text('add_date', lang),
            callback_data="admin_add_date"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text('remove_date', lang),
            callback_data="admin_remove_date"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text('back', lang),
            callback_data="admin_back"
        )
    )

    return builder.as_markup()


def get_admin_dates_list_keyboard(dates: List[str], lang: str = 'uz') -> InlineKeyboardMarkup:
    """Admin dates list for removal"""
    builder = InlineKeyboardBuilder()

    for date in dates:
        builder.row(
            InlineKeyboardButton(
                text=f"🗑 {date}",
                callback_data=f"remove_date_{date}"
            )
        )

    builder.row(
        InlineKeyboardButton(
            text=get_text('back', lang),
            callback_data="admin_manage_dates"
        )
    )

    return builder.as_markup()


def get_cancel_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Cancel keyboard"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=get_text('cancel', lang),
            callback_data="cancel"
        )
    )
    return builder.as_markup()


def get_back_to_admin_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Back to admin panel keyboard"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=get_text('back', lang),
            callback_data="admin_back"
        )
    )
    return builder.as_markup()


def get_save_dates_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Keyboard to save selected dates"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=get_text('finish_adding_dates', lang),
            callback_data="admin_save_dates"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text('cancel', lang),
            callback_data="cancel"
        )
    )
    return builder.as_markup()


def get_reply_to_user_keyboard(user_id: int, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Keyboard with reply button for admin notification"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=get_text('reply_to_user', lang),
            callback_data=f"reply_user_{user_id}"
        )
    )
    return builder.as_markup()


def get_export_confirm_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Keyboard to confirm export and clear operation"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=get_text('confirm_export', lang),
            callback_data="confirm_export_and_clear"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text('cancel', lang),
            callback_data="admin_back"
        )
    )
    return builder.as_markup()
