"""
User handlers for INEX CONSULTING Bot
"""
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import re
import logging

from states import UserRegistration
from database import db
from keyboards import (
    get_language_keyboard,
    get_channel_subscription_keyboard,
    get_meeting_dates_keyboard,
    get_cancel_keyboard,
    get_reply_to_user_keyboard
)
from texts import get_text
from config import ADMIN_IDS, CHANNEL_ID

logger = logging.getLogger(__name__)

router = Router()


# ========== START COMMAND ==========

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Handle /start command"""
    user = message.from_user

    # Add user to database
    db.add_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )

    # Ask for language selection
    await message.answer(
        get_text('select_language', 'uz'),
        reply_markup=get_language_keyboard()
    )
    await state.set_state(UserRegistration.language_selection)
    logger.info(f"User {user.id} started the bot")


# ========== LANGUAGE SELECTION ==========

@router.callback_query(F.data.startswith('lang_'))
async def process_language_selection(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Handle language selection"""
    language = callback.data.split('_')[1]  # uz or ru
    user_id = callback.from_user.id

    # Save language preference
    db.set_user_language(user_id, language)
    await state.update_data(language=language)

    await callback.answer(get_text('language_changed', language))

    # Check if user is already subscribed to channel
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            # User is already subscribed
            db.set_user_subscribed(user_id, True)
            await callback.message.edit_text(
                get_text('welcome', language)
            )
            # Show meeting date selection
            await show_meeting_dates(callback.message, state, language)
            return
    except Exception as e:
        logger.error(f"Error checking subscription: {e}")

    # User not subscribed - show subscription message
    await callback.message.edit_text(
        get_text('welcome', language) + '\n\n' + get_text('join_channel', language),
        reply_markup=get_channel_subscription_keyboard(language)
    )
    await state.set_state(UserRegistration.waiting_for_subscription)


# ========== CHANNEL SUBSCRIPTION CHECK ==========

@router.callback_query(F.data == 'check_subscription')
async def check_subscription(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Check if user subscribed to channel"""
    user_id = callback.from_user.id
    user_data = await state.get_data()
    language = user_data.get('language', 'uz')

    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)

        if member.status in ['member', 'administrator', 'creator']:
            # User is subscribed
            db.set_user_subscribed(user_id, True)
            await callback.answer()  # No alert

            await callback.message.edit_text(
                get_text('subscription_confirmed', language)
            )

            # Show meeting date selection
            await show_meeting_dates(callback.message, state, language)

        else:
            # User not subscribed - edit existing message
            await callback.answer()  # Close loading
            await callback.message.edit_text(
                get_text('welcome', language) + '\n\n' + get_text('not_subscribed', language),
                reply_markup=get_channel_subscription_keyboard(language)
            )

    except Exception as e:
        logger.error(f"Error checking subscription for user {user_id}: {e}")
        await callback.answer()  # Close loading
        # Try to edit, if fails then send new message
        try:
            await callback.message.edit_text(
                get_text('welcome', language) + '\n\n' + get_text('not_subscribed', language),
                reply_markup=get_channel_subscription_keyboard(language)
            )
        except:
            await callback.message.answer(
                get_text('not_subscribed', language),
                reply_markup=get_channel_subscription_keyboard(language)
            )


# ========== MEETING DATE SELECTION ==========

async def show_meeting_dates(message: Message, state: FSMContext, language: str):
    """Show all meeting dates with visual indicators (available and booked)"""
    all_dates = db.get_active_meeting_dates()
    booked_dates = db.get_booked_meeting_dates()

    if not all_dates:
        await message.answer(get_text('no_dates_available', language))
        # Clear state so user can send messages freely
        await state.clear()
        return

    # Create message with legend
    legend = "📌 ✅ - Mavjud sanalar\n📌 🔒 - Band qilingan sanalar" if language == 'uz' else "📌 ✅ - Доступные даты\n📌 🔒 - Забронированные даты"
    message_text = get_text('select_date', language) + "\n\n" + legend

    await message.answer(
        message_text,
        reply_markup=get_meeting_dates_keyboard(all_dates, booked_dates, language)
    )
    await state.set_state(UserRegistration.selecting_date)


@router.callback_query(F.data.startswith('date_booked_'))
async def process_booked_date_click(callback: CallbackQuery, state: FSMContext):
    """Handle click on booked date - show alert"""
    user_data = await state.get_data()
    language = user_data.get('language', 'uz')

    # Show alert that date is booked
    alert_text = "⚠️ Bu sana allaqachon band qilingan!\nIltimos, boshqa sana tanlang." if language == 'uz' else "⚠️ Эта дата уже забронирована!\nПожалуйста, выберите другую дату."
    await callback.answer(alert_text, show_alert=True)


@router.callback_query(F.data.startswith('date_'))
async def process_date_selection(callback: CallbackQuery, state: FSMContext):
    """Handle meeting date selection"""
    date = callback.data.replace('date_', '')
    user_data = await state.get_data()
    language = user_data.get('language', 'uz')

    # Check if date is still available
    available_dates = db.get_available_meeting_dates()
    if date not in available_dates:
        await callback.answer(get_text('date_already_booked', language), show_alert=True)

        # Show updated available dates
        await show_meeting_dates(callback.message, state, language)
        return

    await state.update_data(meeting_date=date)

    await callback.answer()
    await callback.message.edit_text(
        get_text('date_selected', language, date=date)
    )

    # Ask for fullname
    await callback.message.answer(
        get_text('ask_fullname', language),
        reply_markup=get_cancel_keyboard(language)
    )
    await state.set_state(UserRegistration.entering_fullname)


# ========== USER INFORMATION COLLECTION ==========

@router.message(UserRegistration.entering_fullname)
async def process_fullname(message: Message, state: FSMContext):
    """Handle fullname input"""
    user_data = await state.get_data()
    language = user_data.get('language', 'uz')

    fullname = message.text.strip()

    if len(fullname) < 3:
        await message.answer(get_text('ask_fullname', language))
        return

    await state.update_data(fullname=fullname)

    # Ask for phone
    await message.answer(
        get_text('ask_phone', language),
        reply_markup=get_cancel_keyboard(language)
    )
    await state.set_state(UserRegistration.entering_phone)


@router.message(UserRegistration.entering_phone)
async def process_phone(message: Message, state: FSMContext):
    """Handle phone input"""
    user_data = await state.get_data()
    language = user_data.get('language', 'uz')

    phone = message.text.strip()

    # Clean phone number
    phone = re.sub(r'[^\d+]', '', phone)

    # Add +998 if not present
    if not phone.startswith('+'):
        if phone.startswith('998'):
            phone = '+' + phone
        else:
            phone = '+998' + phone

    # Validate phone format (Uzbekistan)
    if not re.match(r'^\+998\d{9}$', phone):
        await message.answer(get_text('invalid_phone', language))
        return

    await state.update_data(phone=phone)

    # Ask for address
    await message.answer(
        get_text('ask_address', language),
        reply_markup=get_cancel_keyboard(language)
    )
    await state.set_state(UserRegistration.entering_address)


@router.message(UserRegistration.entering_address)
async def process_address(message: Message, state: FSMContext):
    """Handle address input"""
    user_data = await state.get_data()
    language = user_data.get('language', 'uz')

    address = message.text.strip()

    if len(address) < 5:
        await message.answer(get_text('ask_address', language))
        return

    await state.update_data(address=address)

    # Ask for company
    await message.answer(
        get_text('ask_company', language),
        reply_markup=get_cancel_keyboard(language)
    )
    await state.set_state(UserRegistration.entering_company)


@router.message(UserRegistration.entering_company)
async def process_company(message: Message, state: FSMContext, bot: Bot):
    """Handle company input and complete registration"""
    user_data = await state.get_data()
    language = user_data.get('language', 'uz')

    company = message.text.strip()

    if len(company) < 2:
        await message.answer(get_text('ask_company', language))
        return

    # Save registration to database
    user_id = message.from_user.id
    fullname = user_data.get('fullname')
    phone = user_data.get('phone')
    address = user_data.get('address')
    meeting_date = user_data.get('meeting_date')

    registration_id = db.add_registration(
        user_id=user_id,
        fullname=fullname,
        phone=phone,
        address=address,
        company=company,
        meeting_date=meeting_date
    )

    logger.info(f"Registration completed: ID {registration_id}, User {user_id}")

    # Send confirmation to user
    await message.answer(
        get_text('registration_complete', language,
                fullname=fullname,
                phone=phone,
                address=address,
                company=company,
                date=meeting_date)
    )

    # Notify admins
    admin_message = get_text('new_registration_admin', language,
                            fullname=fullname,
                            phone=phone,
                            address=address,
                            company=company,
                            date=meeting_date,
                            user_id=user_id)

    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(
                admin_id,
                admin_message,
                reply_markup=get_reply_to_user_keyboard(user_id, language)
            )
        except Exception as e:
            logger.error(f"Failed to send notification to admin {admin_id}: {e}")

    # Clear state
    await state.clear()


# ========== CANCEL CALLBACK ==========

@router.callback_query(F.data == 'cancel')
async def process_cancel(callback: CallbackQuery, state: FSMContext):
    """Handle cancel button"""
    user_data = await state.get_data()
    language = user_data.get('language', 'uz')

    await state.clear()
    await callback.message.edit_text(get_text('cancel', language))
    await callback.answer()


# ========== GENERAL MESSAGE HANDLER ==========

@router.message(F.text)
async def handle_user_message(message: Message, state: FSMContext, bot: Bot):
    """Handle any text message from user and forward to admin"""
    # Check if user is in registration process (but NOT in waiting_for_subscription or language_selection)
    current_state = await state.get_state()

    # List of states where user is actively filling registration form
    registration_states = [
        'UserRegistration:selecting_date',
        'UserRegistration:entering_fullname',
        'UserRegistration:entering_phone',
        'UserRegistration:entering_address',
        'UserRegistration:entering_company'
    ]

    if current_state in registration_states:
        # User is filling registration form, don't handle here
        return

    user = message.from_user
    user_id = user.id

    # Get user language
    language = db.get_user_language(user_id)

    # Check if user is subscribed to channel
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        logger.info(f"User {user_id} channel status: {member.status}")

        if member.status not in ['member', 'administrator', 'creator']:
            # User is not subscribed - block and force subscription
            await message.answer(
                get_text('must_subscribe_to_use', language),
                reply_markup=get_channel_subscription_keyboard(language)
            )
            logger.info(f"🚫 User {user_id} BLOCKED - not subscribed. Status: {member.status}. Message: {message.text[:30]}")
            return
        else:
            logger.info(f"✅ User {user_id} is subscribed. Forwarding message to admin.")
    except Exception as e:
        logger.error(f"❌ Error checking subscription for user {user_id}: {e}")
        # If error checking, show subscription message to be safe
        await message.answer(
            get_text('must_subscribe_to_use', language),
            reply_markup=get_channel_subscription_keyboard(language)
        )
        return

    # Prepare username display
    username = user.username if user.username else f"{user.first_name or ''} {user.last_name or ''}".strip()
    if not username:
        username = f"User {user_id}"

    # Prepare admin notification
    admin_notification = get_text('user_message_to_admin', language,
                                  username=username,
                                  user_id=user_id,
                                  message=message.text)

    # Send to all admins
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(
                admin_id,
                admin_notification,
                reply_markup=get_reply_to_user_keyboard(user_id, language)
            )
        except Exception as e:
            logger.error(f"Failed to forward message to admin {admin_id}: {e}")

    # Confirm to user
    await message.answer(get_text('message_sent_to_admin', language))
    logger.info(f"User {user_id} sent message to admin: {message.text[:50]}...")
