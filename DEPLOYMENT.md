# 🚀 INEX CONSULTING Bot - Render.com ga Deploy qilish

To'liq qo'llanma - step by step!

---

## 📋 Talab qilinadigan narsalar

1. **GitHub account** - https://github.com
2. **Render.com account** - https://render.com (GitHub bilan kirish mumkin)
3. **Telegram Bot Token** - @BotFather dan olingan
4. **Admin Telegram ID** - @userinfobot dan olingan

---

## 🎯 1-QADAM: GitHub Repository yaratish

### 1.1. GitHub.com ga kiring

https://github.com ga kiring yoki ro'yxatdan o'ting

### 1.2. Yangi repository yaratish

1. GitHub da **New repository** tugmasini bosing
2. Repository nomi: `inex-consulting-bot` (yoki istalgan nom)
3. **Private** yoki **Public** - istalganini tanlang
4. ✅ **Initialize this repository with a README** - BOSHMANG!
5. **Create repository** tugmasini bosing

### 1.3. Kodlaringizni GitHub ga yuklash

**Windows (Command Prompt yoki PowerShell):**

```bash
# Bot papkasiga o'ting
cd E:\OWN_Projects\loyiha_3\telegram_bot

# Git initsializatsiya
git init

# Barcha fayllarni qo'shish
git add .

# Commit yaratish
git commit -m "Initial commit: INEX CONSULTING Bot"

# GitHub repository URLini qo'shish (o'z URLingizni kiriting!)
git remote add origin https://github.com/SIZNING_USERNAME/inex-consulting-bot.git

# GitHub ga push qilish
git branch -M main
git push -u origin main
```

**Username va parol so'ralsa:**
- Username: GitHub username
- Password: **Personal Access Token** (parol emas!)

---

## 🔑 GitHub Personal Access Token yaratish (Agar kerak bo'lsa)

1. GitHub.com → Settings (profil rasmidagi menu)
2. **Developer settings** (pastki qism)
3. **Personal access tokens** → **Tokens (classic)**
4. **Generate new token** → **Generate new token (classic)**
5. Note: `Render Bot Deployment`
6. Expiration: **No expiration** yoki **90 days**
7. **repo** checkboxini belgilang
8. **Generate token** tugmasini bosing
9. **Tokenni nusxalang va saqlang!** (bir marta ko'rsatiladi)

---

## 🌐 2-QADAM: Render.com da Service yaratish

### 2.1. Render.com ga kirish

1. https://render.com ga o'ting
2. **Sign Up** yoki **Log In**
3. **Sign in with GitHub** ni tanlang (tavsiya!)
4. GitHub account bilan kiring

### 2.2. Yangi Service yaratish

1. Dashboard da **New +** tugmasini bosing
2. **Background Worker** ni tanlang (WEB SERVICE EMAS!)

### 2.3. Repository ulash

1. **Connect a repository** bo'limida
2. O'zingizning `inex-consulting-bot` repositoryni toping
3. **Connect** tugmasini bosing

**Agar repository ko'rinmasa:**
- **Configure account** ni bosing
- GitHub da Render ga access bering
- Kerakli repositoryni tanlang

### 2.4. Service sozlamalari

```
Name: inex-consulting-bot
Region: Frankfurt (EU Central) yoki Oregon (US West)
Branch: main
Root Directory: (bo'sh qoldiring)
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: python bot.py
```

**Instance Type:**
- **Free** ni tanlang ✅ (750 soat/oy tekin!)

### 2.5. Environment Variables qo'shish

**Environment** bo'limida **Add Environment Variable** tugmasini bosing:

**1-chi o'zgaruvchi:**
```
Key: BOT_TOKEN
Value: 8236382244:AAHCRDBqKpIwo9jHYgr4lA-sTjriMBjwgZs
```
(O'z bot tokeningizni kiriting!)

**2-chi o'zgaruvchi:**
```
Key: ADMIN_IDS
Value: 6368117162
```
(O'z Telegram ID ingizni kiriting!)

**Bir nechta admin bo'lsa:**
```
Value: 6368117162,123456789,987654321
```

### 2.6. Deploy qilish

1. **Create Background Worker** tugmasini bosing
2. Render avtomatik deploy qila boshlaydi
3. Loglarni kuzating:
   ```
   Installing dependencies...
   Running build command...
   Starting service...
   ```

---

## ✅ 3-QADAM: Deploy natijasini tekshirish

### 3.1. Loglarni ko'rish

Service dashboard da **Logs** tabini oching.

**Muvaffaqiyatli deploy:**
```
Bot started successfully!
Start polling
Run polling for bot @inex_consulting_official_bot
```

**Xatolik bo'lsa:**
- Environment variablelarni tekshiring
- Bot tokenni tekshiring
- Admin ID ni tekshiring

### 3.2. Botni test qilish

1. Telegram da botingizni toping
2. `/start` yuboring
3. Ishlashi kerak! ✅

---

## 🔄 4-QADAM: Kodni yangilash

Kodni o'zgartirganda, GitHub ga push qiling:

```bash
# Barcha o'zgarishlarni commit qiling
git add .
git commit -m "Yangi funksiya qo'shildi"
git push

# Render avtomatik yangi versiyani deploy qiladi!
```

**Auto Deploy o'chirilgan bo'lsa:**
- Render dashboard → Settings
- **Auto-Deploy** ni yoqing

---

## 🛠 5-QADAM: Muammolarni hal qilish

### Bot ishlamayapti?

**1. Loglarni tekshiring:**
- Render dashboard → Logs

**2. Environment variablelarni tekshiring:**
- Settings → Environment
- `BOT_TOKEN` va `ADMIN_IDS` to'g'riligini tekshiring

**3. Service qayta ishga tushiring:**
- Manual Deploy → Deploy latest commit

### Database muammosi?

Render Free tier da SQLite **yo'qoladi** har safar restart da!

**Yechim:**
- Render Disk qo'shing (pullik)
- yoki PostgreSQL ishlatng (Render da tekin!)

**PostgreSQL qo'shish:**
1. Dashboard → New → PostgreSQL
2. Free tier tanlang
3. Database URLni oling
4. Kodda SQLite o'rniga PostgreSQL ishlatng

---

## 📊 Logs va Monitoring

### Loglarni ko'rish:

**Real-time:**
- Dashboard → Logs

**Download:**
- Logs → Download logs

### Service restart qilish:

- Manual Deploy → Clear build cache & deploy

---

## 💰 Narxlar

**Free Tier:**
- ✅ 750 soat/oy (31 kun 24/7!)
- ✅ Bir nechta serviclar
- ❌ Database save yo'q (restart da o'chadi)

**Starter Plan ($7/oy):**
- ✅ Cheksiz
- ✅ Persistent disk

---

## 🎉 Tayyor!

Botingiz endi 24/7 ishlaydi! 🚀

**Foydali linklar:**
- Render Dashboard: https://dashboard.render.com
- GitHub Repo: https://github.com/SIZNING_USERNAME/inex-consulting-bot
- Telegram Bot: https://t.me/SIZNING_BOT_USERNAME

---

## 📞 Yordam kerakmi?

**Render Support:**
- https://render.com/docs
- support@render.com

**GitHub Issues:**
- Repository → Issues → New issue

**Telegram:**
- @InEx_Operations kanaliga yozing

---

**© 2024 INEX CONSULTING - Made with ❤️ by Claude Code**
