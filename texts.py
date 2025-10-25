"""
Bilingual texts for INEX CONSULTING Bot (Uzbek/Russian)
"""

TEXTS = {
    # Language selection
    'select_language': {
        'uz': "Tilni tanlang / Выберите язык",
        'ru': "Tilni tanlang / Выберите язык"
    },

    # Welcome messages
    'welcome': {
        'uz': """👋 Assalomu alaykum!

🎯 INEX CONSULTING ning rasmiy botiga xush kelibsiz!

Biz bilan uchrashuv tashkil qilish uchun davom etishingiz mumkin.""",
        'ru': """👋 Здравствуйте!

🎯 Добро пожаловать в официальный бот INEX CONSULTING!

Вы можете продолжить для организации встречи с нами."""
    },

    # Channel subscription
    'join_channel': {
        'uz': """📢 Davom etish uchun bizning rasmiy Telegram kanaliga a'zo bo'ling:

👉 INEX CONSULTING rasmiy kanali

A'zo bo'lganingizdan so'ng "✅ A'zoman" tugmasini bosing.""",
        'ru': """📢 Для продолжения подпишитесь на наш официальный Telegram канал:

👉 Официальный канал INEX CONSULTING

После подписки нажмите кнопку "✅ Подписан"."""
    },

    'check_subscription': {
        'uz': "✅ A'zoman",
        'ru': "✅ Подписан"
    },

    'not_subscribed': {
        'uz': "❌ Siz hali kanalga a'zo bo'lmagansiz. Iltimos, avval kanalga a'zo bo'ling!",
        'ru': "❌ Вы еще не подписаны на канал. Пожалуйста, сначала подпишитесь!"
    },

    'must_subscribe_to_use': {
        'uz': "⛔️ Botdan foydalanish uchun avval kanalga a'zo bo'lishingiz SHART!\n\n👇 Quyidagi tugmani bosing:",
        'ru': "⛔️ Для использования бота необходимо ОБЯЗАТЕЛЬНО подписаться на канал!\n\n👇 Нажмите кнопку ниже:"
    },

    'subscription_confirmed': {
        'uz': "✅ Ajoyib! Kanalga a'zo bo'lganingiz uchun rahmat!",
        'ru': "✅ Отлично! Спасибо за подписку на канал!"
    },

    # Meeting date selection
    'select_date': {
        'uz': """📅 Uchrashuv sanasini tanlang:

Quyidagi mavjud sanalardan birini tanlang:""",
        'ru': """📅 Выберите дату встречи:

Выберите одну из доступных дат:"""
    },

    'no_dates_available': {
        'uz': "❌ Hozircha mavjud uchrashuv sanalari yo'q. Iltimos, keyinroq qayta urinib ko'ring.",
        'ru': "❌ В данный момент нет доступных дат для встреч. Пожалуйста, попробуйте позже."
    },

    'date_selected': {
        'uz': "✅ Siz tanlagan sana: {date}",
        'ru': "✅ Вы выбрали дату: {date}"
    },

    'date_already_booked': {
        'uz': "❌ Kechirasiz, bu sana allaqachon band qilingan. Iltimos, boshqa sanani tanlang.",
        'ru': "❌ Извините, эта дата уже занята. Пожалуйста, выберите другую дату."
    },

    # User information collection
    'ask_fullname': {
        'uz': """👤 Ism va familiyangizni kiriting:

Masalan: Ahmadov Aziz""",
        'ru': """👤 Введите ваше имя и фамилию:

Например: Ахмедов Азиз"""
    },

    'ask_phone': {
        'uz': """📱 Telefon raqamingizni kiriting:

Masalan: +998901234567 yoki 901234567""",
        'ru': """📱 Введите ваш номер телефона:

Например: +998901234567 или 901234567"""
    },

    'invalid_phone': {
        'uz': """❌ Telefon raqam noto'g'ri formatda!

Iltimos, quyidagi formatda kiriting:
+998901234567 yoki 901234567""",
        'ru': """❌ Неверный формат номера телефона!

Пожалуйста, введите в формате:
+998901234567 или 901234567"""
    },

    'ask_address': {
        'uz': """📍 Manzilingizni kiriting:

Masalan: Toshkent shahar, Yunusobod tumani""",
        'ru': """📍 Введите ваш адрес:

Например: г. Ташкент, Юнусабадский район"""
    },

    'ask_company': {
        'uz': """🏢 Korxonangiz nomini kiriting:

Masalan: "InnoTech" MCHJ""",
        'ru': """🏢 Введите название вашей компании:

Например: ООО "ИнноТех" """
    },

    # Registration confirmation
    'registration_complete': {
        'uz': """✅ Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!

📋 Ma'lumotlaringiz:
👤 Ism-Familiya: {fullname}
📱 Telefon: {phone}
📍 Manzil: {address}
🏢 Korxona: {company}
📅 Uchrashuv sanasi: {date}

Tez orada siz bilan bog'lanamiz. Rahmat! 🤝""",
        'ru': """✅ Регистрация успешно завершена!

📋 Ваши данные:
👤 Имя-Фамилия: {fullname}
📱 Телефон: {phone}
📍 Адрес: {address}
🏢 Компания: {company}
📅 Дата встречи: {date}

Мы свяжемся с вами в ближайшее время. Спасибо! 🤝"""
    },

    # Admin messages
    'admin_panel': {
        'uz': """👨‍💼 Admin Panel

Quyidagi amallardan birini tanlang:""",
        'ru': """👨‍💼 Админ Панель

Выберите одно из действий:"""
    },

    'view_registrations': {
        'uz': "📋 Ro'yxatlarni ko'rish",
        'ru': "📋 Просмотр регистраций"
    },

    'manage_dates': {
        'uz': "📅 Sanalarni boshqarish",
        'ru': "📅 Управление датами"
    },

    'export_and_clear': {
        'uz': "📊 Excel yuklab olish va tozalash",
        'ru': "📊 Скачать Excel и очистить"
    },

    'add_date': {
        'uz': "➕ Sana qo'shish",
        'ru': "➕ Добавить дату"
    },

    'remove_date': {
        'uz': "➖ Sanani o'chirish",
        'ru': "➖ Удалить дату"
    },

    'back': {
        'uz': "⬅️ Ortga",
        'ru': "⬅️ Назад"
    },

    'cancel': {
        'uz': "❌ Bekor qilish",
        'ru': "❌ Отмена"
    },

    'admin_add_date_instruction': {
        'uz': """➕ Yangi uchrashuv sanalarini qo'shish

📅 Kalendardan kerakli sanalarni tanlang

Bir nechta sanalarni tanlashingiz mumkin!
Tugagach "✅ Saqlash" tugmasini bosing.""",
        'ru': """➕ Добавление новых дат встреч

📅 Выберите нужные даты из календаря

Вы можете выбрать несколько дат!
По завершении нажмите кнопку "✅ Сохранить"."""
    },

    'admin_select_date_from_calendar': {
        'uz': """📅 Kalendardan sanalarni tanlang:

Tanlangan sanalar: {count} ta""",
        'ru': """📅 Выбирайте даты из календаря:

Выбрано дат: {count} шт."""
    },

    'date_selected_added': {
        'uz': "✅ Sana qo'shildi: {date}",
        'ru': "✅ Дата добавлена: {date}"
    },

    'date_already_exists': {
        'uz': "⚠️ Sana allaqachon mavjud: {date}",
        'ru': "⚠️ Дата уже существует: {date}"
    },

    'finish_adding_dates': {
        'uz': "✅ Saqlash",
        'ru': "✅ Сохранить"
    },

    'dates_added_successfully': {
        'uz': "✅ {count} ta sana muvaffaqiyatli qo'shildi!",
        'ru': "✅ {count} дат успешно добавлено!"
    },

    'no_dates_selected': {
        'uz': "❌ Hech qanday sana tanlanmadi!",
        'ru': "❌ Не выбрано ни одной даты!"
    },

    'date_added': {
        'uz': "✅ Sana muvaffaqiyatli qo'shildi: {date}",
        'ru': "✅ Дата успешно добавлена: {date}"
    },

    'invalid_date_format': {
        'uz': """❌ Sana formati noto'g'ri!

Iltimos, quyidagi formatda kiriting:
DD.MM.YYYY HH:MM

Masalan: 25.12.2024 14:00""",
        'ru': """❌ Неверный формат даты!

Пожалуйста, введите в формате:
DD.MM.YYYY HH:MM

Например: 25.12.2024 14:00"""
    },

    'select_date_to_remove': {
        'uz': "O'chirish uchun sanani tanlang:",
        'ru': "Выберите дату для удаления:"
    },

    'date_removed': {
        'uz': "✅ Sana o'chirildi: {date}",
        'ru': "✅ Дата удалена: {date}"
    },

    'no_registrations': {
        'uz': "❌ Hozircha ro'yxatdan o'tganlar yo'q.",
        'ru': "❌ Пока нет регистраций."
    },

    'registrations_list': {
        'uz': "📋 Ro'yxatdan o'tganlar ({count} ta):",
        'ru': "📋 Список регистраций ({count} шт.):"
    },

    'registration_item': {
        'uz': """
━━━━━━━━━━━━━━━━━
🆔 ID: {id}
👤 {fullname}
📱 {phone}
📍 {address}
🏢 {company}
📅 {date}
🕐 {created_at}""",
        'ru': """
━━━━━━━━━━━━━━━━━
🆔 ID: {id}
👤 {fullname}
📱 {phone}
📍 {address}
🏢 {company}
📅 {date}
🕐 {created_at}"""
    },

    # New registration notification for admin
    'new_registration_admin': {
        'uz': """🔔 Yangi ro'yxatdan o'tish!

👤 Ism-Familiya: {fullname}
📱 Telefon: {phone}
📍 Manzil: {address}
🏢 Korxona: {company}
📅 Uchrashuv sanasi: {date}
🆔 Foydalanuvchi ID: {user_id}""",
        'ru': """🔔 Новая регистрация!

👤 Имя-Фамилия: {fullname}
📱 Телефон: {phone}
📍 Адрес: {address}
🏢 Компания: {company}
📅 Дата встречи: {date}
🆔 ID пользователя: {user_id}"""
    },

    'not_admin': {
        'uz': "❌ Bu buyruq faqat adminlar uchun!",
        'ru': "❌ Эта команда только для администраторов!"
    },

    # Reply to user
    'reply_to_user': {
        'uz': "💬 Javob berish",
        'ru': "💬 Ответить"
    },

    'admin_ask_reply_message': {
        'uz': """💬 Foydalanuvchiga javob berish

Javob xabaringizni yozing:""",
        'ru': """💬 Ответ пользователю

Напишите ваше сообщение:"""
    },

    'reply_sent_success': {
        'uz': "✅ Xabar foydalanuvchiga yuborildi!",
        'ru': "✅ Сообщение отправлено пользователю!"
    },

    'reply_sent_error': {
        'uz': "❌ Xabar yuborishda xatolik yuz berdi!",
        'ru': "❌ Ошибка при отправке сообщения!"
    },

    'admin_message_received': {
        'uz': """📨 INEX CONSULTING dan xabar:

{message}""",
        'ru': """📨 Сообщение от INEX CONSULTING:

{message}"""
    },

    # User message to admin
    'user_message_to_admin': {
        'uz': """💬 Foydalanuvchidan yangi xabar!

👤 Foydalanuvchi: {username}
🆔 ID: {user_id}
📝 Xabar:

{message}""",
        'ru': """💬 Новое сообщение от пользователя!

👤 Пользователь: {username}
🆔 ID: {user_id}
📝 Сообщение:

{message}"""
    },

    'message_sent_to_admin': {
        'uz': """✅ Xabaringiz adminga yuborildi!

Tez orada javob berishadi.""",
        'ru': """✅ Ваше сообщение отправлено администратору!

Вам ответят в ближайшее время."""
    },

    # Export and clear
    'export_confirm': {
        'uz': """⚠️ Diqqat!

Siz ro'yxatlarni Excel faylga yuklab olmoqchisiz va bazani tozalamoqchisiz.

Bu amalni bajarilgandan so'ng:
✅ Barcha ro'yxatlar Excel faylga yuklanadi
❌ Bazadan barcha ro'yxatlar o'chiriladi
❌ Barcha uchrashuv sanalari o'chiriladi

Davom etasizmi?""",
        'ru': """⚠️ Внимание!

Вы хотите скачать регистрации в Excel и очистить базу.

После выполнения этой операции:
✅ Все регистрации будут выгружены в Excel
❌ Все регистрации будут удалены из базы
❌ Все даты встреч будут удалены

Продолжить?"""
    },

    'confirm_export': {
        'uz': "✅ Ha, davom etaman",
        'ru': "✅ Да, продолжить"
    },

    'export_processing': {
        'uz': "⏳ Excel fayl tayyorlanmoqda...",
        'ru': "⏳ Подготовка Excel файла..."
    },

    'export_success': {
        'uz': """✅ Muvaffaqiyatli bajarildi!

📊 Excel fayl yuborildi
🗑 {registrations_count} ta ro'yxat o'chirildi
🗑 {dates_count} ta sana o'chirildi

Baza tozalandi!""",
        'ru': """✅ Успешно выполнено!

📊 Excel файл отправлен
🗑 {registrations_count} регистраций удалено
🗑 {dates_count} дат удалено

База очищена!"""
    },

    'no_data_to_export': {
        'uz': "❌ Export qilish uchun ma'lumotlar yo'q!",
        'ru': "❌ Нет данных для экспорта!"
    },

    'export_error': {
        'uz': "❌ Excel yaratishda xatolik yuz berdi!",
        'ru': "❌ Ошибка при создании Excel файла!"
    },

    'language_changed': {
        'uz': "✅ Til o'zgartirildi!",
        'ru': "✅ Язык изменен!"
    }
}


def get_text(key: str, lang: str = 'uz', **kwargs) -> str:
    """Get text by key and language with formatting support"""
    text = TEXTS.get(key, {}).get(lang, TEXTS.get(key, {}).get('uz', ''))
    if kwargs:
        text = text.format(**kwargs)
    return text
