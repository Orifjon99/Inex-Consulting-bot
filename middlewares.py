"""
Middlewares for INEX CONSULTING Bot
"""
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram import Bot
from config import CHANNEL_ID
import logging

logger = logging.getLogger(__name__)


class ChannelSubscriptionMiddleware(BaseMiddleware):
    """
    Middleware to check if user is subscribed to channel
    Only applies to specific handlers (not /start and not admin commands)
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Get user
        if isinstance(event, Message):
            user = event.from_user
        elif isinstance(event, CallbackQuery):
            user = event.from_user
        else:
            return await handler(event, data)

        # Skip check for /start, /admin commands and subscription check callback
        if isinstance(event, Message):
            if event.text and (event.text.startswith('/start') or event.text.startswith('/admin')):
                return await handler(event, data)

        if isinstance(event, CallbackQuery):
            if event.data in ['check_subscription', 'lang_uz', 'lang_ru']:
                return await handler(event, data)
            # Skip for admin callbacks
            if event.data.startswith('admin_'):
                return await handler(event, data)

        # Check subscription
        bot: Bot = data.get('bot')
        try:
            member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user.id)
            if member.status in ['member', 'administrator', 'creator']:
                data['is_subscribed'] = True
                return await handler(event, data)
            else:
                data['is_subscribed'] = False
                return await handler(event, data)
        except Exception as e:
            logger.error(f"Error checking subscription for user {user.id}: {e}")
            # If error, allow to proceed
            data['is_subscribed'] = True
            return await handler(event, data)
