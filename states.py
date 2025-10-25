"""
FSM States for INEX CONSULTING Bot
"""
from aiogram.fsm.state import State, StatesGroup


class UserRegistration(StatesGroup):
    """States for user registration flow"""
    language_selection = State()
    waiting_for_subscription = State()
    selecting_date = State()
    entering_fullname = State()
    entering_phone = State()
    entering_address = State()
    entering_company = State()


class AdminStates(StatesGroup):
    """States for admin operations"""
    main_menu = State()
    adding_date = State()
    removing_date = State()
    viewing_registrations = State()
    replying_to_user = State()
