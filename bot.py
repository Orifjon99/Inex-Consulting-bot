"""
INEX CONSULTING Telegram Bot
Main application file
"""
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import user, admin
from middlewares import ChannelSubscriptionMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


async def main():
    """Main function to start the bot"""
    # Initialize bot and dispatcher
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Use memory storage for FSM
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Register middlewares
    # Note: Subscription check middleware is optional and can be enabled if needed
    # dp.message.middleware(ChannelSubscriptionMiddleware())
    # dp.callback_query.middleware(ChannelSubscriptionMiddleware())

    # Register routers
    # IMPORTANT: Admin router must be first to handle admin states correctly
    dp.include_router(admin.router)
    dp.include_router(user.router)

    logger.info("Bot started successfully!")

    # Start polling
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"Error during polling: {e}")
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


