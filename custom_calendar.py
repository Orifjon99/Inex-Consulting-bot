"""
Custom date picker without locale dependencies
Simple and reliable date selection
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime, timedelta
from typing import List, Tuple


def get_month_keyboard(year: int, month: int, language: str = 'uz') -> InlineKeyboardMarkup:
    """
    Generate calendar keyboard for a specific month
    Returns inline keyboard with dates
    """
    builder = InlineKeyboardBuilder()

    # Month names in Uzbek and Russian
    month_names_uz = [
        "Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun",
        "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"
    ]
    month_names_ru = [
        "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
        "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ]

    month_names = month_names_uz if language == 'uz' else month_names_ru

    # Header with month and year
    builder.row(
        InlineKeyboardButton(
            text=f"📅 {month_names[month-1]} {year}",
            callback_data="ignore"
        )
    )

    # Get first day of month and number of days
    first_day = datetime(year, month, 1)
    if month == 12:
        last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = datetime(year, month + 1, 1) - timedelta(days=1)

    num_days = last_day.day

    # Create buttons for dates (3 per row)
    date_buttons = []
    for day in range(1, num_days + 1):
        date_str = f"{day:02d}.{month:02d}.{year}"
        date_buttons.append(
            InlineKeyboardButton(
                text=f"{day}",
                callback_data=f"pickdate_{date_str}"
            )
        )

    # Arrange in rows of 7 (week view)
    for i in range(0, len(date_buttons), 7):
        row = date_buttons[i:i+7]
        builder.row(*row)

    # Navigation buttons
    prev_text = "⬅️ Oldingi" if language == 'uz' else "⬅️ Назад"
    next_text = "Keyingi ➡️" if language == 'uz' else "Вперёд ➡️"

    nav_buttons = []

    # Previous month
    if month == 1:
        prev_month, prev_year = 12, year - 1
    else:
        prev_month, prev_year = month - 1, year

    nav_buttons.append(
        InlineKeyboardButton(
            text=prev_text,
            callback_data=f"month_{prev_year}_{prev_month}"
        )
    )

    # Next month
    if month == 12:
        next_month, next_year = 1, year + 1
    else:
        next_month, next_year = month + 1, year

    nav_buttons.append(
        InlineKeyboardButton(
            text=next_text,
            callback_data=f"month_{next_year}_{next_month}"
        )
    )

    builder.row(*nav_buttons)

    return builder.as_markup()


def get_current_month_keyboard(language: str = 'uz') -> InlineKeyboardMarkup:
    """Get keyboard for current month"""
    now = datetime.now()
    return get_month_keyboard(now.year, now.month, language)
