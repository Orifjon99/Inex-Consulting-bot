"""
Admin handlers for INEX CONSULTING Bot
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from datetime import datetime
import logging
import re
import os

from states import AdminStates
from custom_calendar import get_current_month_keyboard, get_month_keyboard
from database import db
from keyboards import (
    get_admin_main_keyboard,
    get_admin_dates_management_keyboard,
    get_admin_dates_list_keyboard,
    get_back_to_admin_keyboard,
    get_cancel_keyboard,
    get_save_dates_keyboard,
    get_export_confirm_keyboard
)
from texts import get_text
from config import ADMIN_IDS
from excel_export import create_registrations_excel

logger = logging.getLogger(__name__)

router = Router()


def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id in ADMIN_IDS


# ========== ADMIN COMMAND ==========

@router.message(Command('admin'))
async def cmd_admin(message: Message, state: FSMContext):
    """Handle /admin command"""
    if not is_admin(message.from_user.id):
        await message.answer(get_text('not_admin', 'uz'))
        return

    # Get user language preference
    user = db.get_user(message.from_user.id)
    language = user['language'] if user else 'uz'

    await message.answer(
        get_text('admin_panel', language),
        reply_markup=get_admin_main_keyboard(language)
    )
    await state.set_state(AdminStates.main_menu)
    await state.update_data(language=language)


# ========== VIEW REGISTRATIONS ==========

@router.callback_query(F.data == 'admin_view_registrations')
async def view_registrations(callback: CallbackQuery, state: FSMContext):
    """View all registrations"""
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text('not_admin', 'uz'), show_alert=True)
        return

    user_data = await state.get_data()
    language = user_data.get('language', 'uz')

    registrations = db.get_registrations()

    if not registrations:
        await callback.answer(get_text('no_registrations', language), show_alert=True)
        return

    # Format registrations list
    count = len(registrations)
    message_text = get_text('registrations_list', language, count=count)

    for reg in registrations[:20]:  # Limit to 20 to avoid message too long
        message_text += get_text('registration_item', language,
                                id=reg['id'],
                                fullname=reg['fullname'],
                                phone=reg['phone'],
                                address=reg['address'],
                                company=reg['company'],
                                date=reg['meeting_date'],
                                created_at=reg['created_at'])

    if count > 20:
        message_text += f"\n\n... va yana {count - 20} ta ro'yxat"

    await callback.message.edit_text(
        message_text,
        reply_markup=get_back_to_admin_keyboard(language)
    )
    await callback.answer()


# ========== MANAGE DATES ==========

@router.callback_query(F.data == 'admin_manage_dates')
async def manage_dates(callback: CallbackQuery, state: FSMContext):
    """Show dates management menu"""
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text('not_admin', 'uz'), show_alert=True)
        return

    user_data = await state.get_data()
    language = user_data.get('language', 'uz')

    await callback.message.edit_text(
        get_text('manage_dates', language),
        reply_markup=get_admin_dates_management_keyboard(language)
    )
    await callback.answer()


# ========== ADD DATE ==========

@router.callback_query(F.data == 'admin_add_date')
async def add_date_start(callback: CallbackQuery, state: FSMContext):
    """Start adding date process with calendar"""
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text('not_admin', 'uz'), show_alert=True)
        return

    user_data = await state.get_data()
    language = user_data.get('language', 'uz')

    # Initialize selected_dates list in state
    await state.update_data(selected_dates=[])

    # Show instruction
    await callback.message.edit_text(
        get_text('admin_add_date_instruction', language)
    )

    # Show custom calendar (no locale issues!)
    calendar_keyboard = get_current_month_keyboard(language)

    await callback.message.answer(
        get_text('admin_select_date_from_calendar', language, count=0),
        reply_markup=calendar_keyboard
    )

    # Show save button below calendar
    await callback.message.answer(
        "👇 Tugash uchun:",
        reply_markup=get_save_dates_keyboard(language)
    )

    await state.set_state(AdminStates.adding_date)
    await callback.answer()


@router.callback_query(F.data.startswith('month_'), AdminStates.adding_date)
async def change_calendar_month(callback: CallbackQuery, state: FSMContext):
    """Change calendar month"""
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text('not_admin', 'uz'), show_alert=True)
        return

    user_data = await state.get_data()
    language = user_data.get('language', 'uz')

    # Parse month data: month_YYYY_MM
    parts = callback.data.split('_')
    year = int(parts[1])
    month = int(parts[2])

    # Update calendar
    calendar_keyboard = get_month_keyboard(year, month, language)

    await callback.message.edit_reply_markup(reply_markup=calendar_keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith('pickdate_'), AdminStates.adding_date)
async def pick_calendar_date(callback: CallbackQuery, state: FSMContext):
    """Pick a date from calendar"""
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text('not_admin', 'uz'), show_alert=True)
        return

    user_data = await state.get_data()
    language = user_data.get('language', 'uz')
    selected_dates = user_data.get('selected_dates', [])

    # Parse date: pickdate_DD.MM.YYYY
    formatted_date = callback.data.replace('pickdate_', '')

    # Check if date already in selected list
    if formatted_date not in selected_dates:
        selected_dates.append(formatted_date)
        await state.update_data(selected_dates=selected_dates)

        # Notify user
        await callback.answer(
            get_text('date_selected_added', language, date=formatted_date),
            show_alert=True
        )
    else:
        await callback.answer(
            get_text('date_already_exists', language, date=formatted_date),
            show_alert=True
        )


@router.callback_query(F.data == 'ignore')
async def ignore_callback(callback: CallbackQuery):
    """Ignore callback for non-interactive buttons"""
    await callback.answer()


@router.callback_query(F.data == 'admin_save_dates')
async def save_selected_dates(callback: CallbackQuery, state: FSMContext):
    """Save all selected dates to database"""
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text('not_admin', 'uz'), show_alert=True)
        return

    user_data = await state.get_data()
    language = user_data.get('language', 'uz')
    selected_dates = user_data.get('selected_dates', [])

    if not selected_dates:
        await callback.answer(get_text('no_dates_selected', language), show_alert=True)
        return

    # Add all selected dates to database
    added_count = 0
    for date_str in selected_dates:
        success = db.add_meeting_date(date_str)
        if success:
            added_count += 1

    # Show result
    if added_count > 0:
        await callback.message.edit_text(
            get_text('dates_added_successfully', language, count=added_count),
            reply_markup=get_admin_main_keyboard(language)
        )
    else:
        await callback.message.edit_text(
            get_text('admin_panel', language),
            reply_markup=get_admin_main_keyboard(language)
        )

    await state.set_state(AdminStates.main_menu)
    await callback.answer()


# ========== REMOVE DATE ==========

@router.callback_query(F.data == 'admin_remove_date')
async def remove_date_start(callback: CallbackQuery, state: FSMContext):
    """Show dates list for removal"""
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text('not_admin', 'uz'), show_alert=True)
        return

    user_data = await state.get_data()
    language = user_data.get('language', 'uz')

    dates = db.get_active_meeting_dates()

    if not dates:
        await callback.answer(get_text('no_dates_available', language), show_alert=True)
        return

    await callback.message.edit_text(
        get_text('select_date_to_remove', language),
        reply_markup=get_admin_dates_list_keyboard(dates, language)
    )
    await state.set_state(AdminStates.removing_date)
    await callback.answer()


@router.callback_query(F.data.startswith('remove_date_'))
async def process_remove_date(callback: CallbackQuery, state: FSMContext):
    """Process date removal"""
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text('not_admin', 'uz'), show_alert=True)
        return

    user_data = await state.get_data()
    language = user_data.get('language', 'uz')

    date = callback.data.replace('remove_date_', '')

    # Remove from database
    db.delete_meeting_date(date)

    await callback.answer(get_text('date_removed', language, date=date), show_alert=True)

    # Show updated dates list
    dates = db.get_active_meeting_dates()

    if dates:
        await callback.message.edit_text(
            get_text('select_date_to_remove', language),
            reply_markup=get_admin_dates_list_keyboard(dates, language)
        )
    else:
        await callback.message.edit_text(
            get_text('admin_panel', language),
            reply_markup=get_admin_main_keyboard(language)
        )
        await state.set_state(AdminStates.main_menu)


# ========== BACK BUTTON ==========

@router.callback_query(F.data == 'admin_back')
async def admin_back(callback: CallbackQuery, state: FSMContext):
    """Return to admin main menu"""
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text('not_admin', 'uz'), show_alert=True)
        return

    user_data = await state.get_data()
    language = user_data.get('language', 'uz')

    await callback.message.edit_text(
        get_text('admin_panel', language),
        reply_markup=get_admin_main_keyboard(language)
    )
    await state.set_state(AdminStates.main_menu)
    await callback.answer()


# ========== CANCEL IN ADMIN MODE ==========

@router.callback_query(F.data == 'cancel', AdminStates.adding_date)
@router.callback_query(F.data == 'cancel', AdminStates.removing_date)
@router.callback_query(F.data == 'cancel', AdminStates.replying_to_user)
async def admin_cancel(callback: CallbackQuery, state: FSMContext):
    """Cancel admin operation"""
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text('not_admin', 'uz'), show_alert=True)
        return

    user_data = await state.get_data()
    language = user_data.get('language', 'uz')

    await callback.message.edit_text(
        get_text('admin_panel', language),
        reply_markup=get_admin_main_keyboard(language)
    )
    await state.set_state(AdminStates.main_menu)
    await callback.answer()


# ========== REPLY TO USER ==========

@router.callback_query(F.data.startswith('reply_user_'))
async def start_reply_to_user(callback: CallbackQuery, state: FSMContext):
    """Start replying to a user"""
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text('not_admin', 'uz'), show_alert=True)
        return

    # Extract user_id from callback data
    user_id = int(callback.data.replace('reply_user_', ''))

    # Get admin's language preference
    admin_user = db.get_user(callback.from_user.id)
    language = admin_user['language'] if admin_user else 'uz'

    # Save user_id and language in state
    await state.update_data(reply_to_user_id=user_id, language=language)

    logger.info(f"Admin {callback.from_user.id} starting reply to user {user_id}")

    # Ask admin for message
    await callback.message.answer(
        get_text('admin_ask_reply_message', language),
        reply_markup=get_cancel_keyboard(language)
    )
    await state.set_state(AdminStates.replying_to_user)
    await callback.answer()

    logger.info(f"State set to replying_to_user for admin {callback.from_user.id}")


@router.message(AdminStates.replying_to_user)
async def process_reply_message(message: Message, state: FSMContext, bot: any):
    """Process admin's reply message and send to user"""
    user_data = await state.get_data()
    language = user_data.get('language', 'uz')
    reply_to_user_id = user_data.get('reply_to_user_id')

    logger.info(f"Admin replying to user: {reply_to_user_id}")

    if not reply_to_user_id:
        logger.error("No reply_to_user_id in state!")
        await message.answer("❌ Xatolik: Foydalanuvchi ID topilmadi!")
        await state.clear()
        return

    reply_text = message.text.strip()

    if len(reply_text) < 1:
        await message.answer(get_text('admin_ask_reply_message', language))
        return

    # Get user's language preference
    user = db.get_user(reply_to_user_id)
    user_language = user['language'] if user else 'uz'

    logger.info(f"Sending reply to user {reply_to_user_id} in {user_language}: {reply_text[:50]}")

    # Send message to user
    try:
        await bot.send_message(
            reply_to_user_id,
            get_text('admin_message_received', user_language, message=reply_text)
        )

        # Confirm to admin
        await message.answer(get_text('reply_sent_success', language))
        logger.info(f"✅ Admin {message.from_user.id} successfully sent message to user {reply_to_user_id}")

    except Exception as e:
        logger.error(f"❌ Failed to send reply to user {reply_to_user_id}: {e}", exc_info=True)
        await message.answer(get_text('reply_sent_error', language))

    # Clear state
    await state.clear()


# ========== EXPORT AND CLEAR ==========

@router.callback_query(F.data == 'admin_export_and_clear')
async def export_and_clear_start(callback: CallbackQuery, state: FSMContext):
    """Show export confirmation"""
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text('not_admin', 'uz'), show_alert=True)
        return

    user_data = await state.get_data()
    language = user_data.get('language', 'uz')

    # Check if there's data to export
    registrations_count = db.get_registrations_count()

    if registrations_count == 0:
        await callback.answer(get_text('no_data_to_export', language), show_alert=True)
        return

    # Show confirmation
    await callback.message.edit_text(
        get_text('export_confirm', language),
        reply_markup=get_export_confirm_keyboard(language)
    )
    await callback.answer()


@router.callback_query(F.data == 'confirm_export_and_clear')
async def confirm_export_and_clear(callback: CallbackQuery, state: FSMContext, bot):
    """Process export and clear operation"""
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text('not_admin', 'uz'), show_alert=True)
        return

    user_data = await state.get_data()
    language = user_data.get('language', 'uz')

    # Show processing message
    await callback.message.edit_text(get_text('export_processing', language))

    try:
        # Get all registrations
        registrations = db.get_registrations()

        if not registrations:
            await callback.answer(get_text('no_data_to_export', language), show_alert=True)
            await callback.message.edit_text(
                get_text('admin_panel', language),
                reply_markup=get_admin_main_keyboard(language)
            )
            return

        # Create Excel file
        excel_file = create_registrations_excel(registrations)

        # Send Excel file to admin
        file = FSInputFile(excel_file)
        await bot.send_document(
            callback.from_user.id,
            file,
            caption=f"📊 INEX CONSULTING ro'yxatlari\n\nJami: {len(registrations)} ta"
        )

        # Delete local Excel file
        try:
            os.remove(excel_file)
            logger.info(f"Deleted temporary Excel file: {excel_file}")
        except Exception as e:
            logger.warning(f"Could not delete Excel file {excel_file}: {e}")

        # Show success message (database NOT cleared!)
        success_msg = "✅ Excel fayl yuborildi!\n\n💾 Database saqlanib qoldi." if language == 'uz' else "✅ Excel файл отправлен!\n\n💾 База данных сохранена."
        await callback.message.edit_text(
            success_msg,
            reply_markup=get_admin_main_keyboard(language)
        )

        logger.info(f"Admin {callback.from_user.id} exported {len(registrations)} registrations to Excel (database NOT cleared)")

    except Exception as e:
        logger.error(f"Error during export: {e}")
        error_msg = "❌ Excel yuklashda xatolik!" if language == 'uz' else "❌ Ошибка при экспорте Excel!"
        await callback.message.edit_text(
            error_msg,
            reply_markup=get_admin_main_keyboard(language)
        )

    await callback.answer()
