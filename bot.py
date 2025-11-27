from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
import asyncio
import json
import os

# 🔥 تنظیمات - مستقیم در کد
TOKEN = "8319792447:AAEoexMgzT-U12GMPdyYzRx7B4U41x3qjy4"  # توکن مستقیم
ADMIN_ID = 7066426177  # آیدی مستقیم

# فایل برای ذخیره تنظیمات
SETTINGS_FILE = "settings.json"

# تنظیمات پیش‌فرض 
DEFAULT_SETTINGS = {
    "message_count": 20,  # پیش‌فرض ۲۰ پیام
    "delay_between_messages": 0.5,  # فاصله ۰.۵ ثانیه
    "auto_messages": [
        "سلام", "سلام", "سلام", "سلام", "سلام",
        "سلام", "سلام", "سلام", "سلام", "سلام",
        "سلام", "سلام", "سلام", "سلام", "سلام", 
        "سلام", "سلام", "سلام", "سلام", "سلام"
    ]
}

def load_settings():
    """بارگذاری تنظیمات از فایل"""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_SETTINGS

def save_settings(settings):
    """ذخیره تنظیمات در فایل"""
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور /start"""
    if update.message.from_user.id != ADMIN_ID:
        return
    
    settings = load_settings()
    
    welcome_text = f"""
🤖 **ربات ارسال پیام خودکار**

**راهنما:**
`/setcount عدد` - تنظیم تعداد پیام‌ها (مثال: `/setcount 20`)
`/setdelay عدد` - تنظیم فاصله بین پیام‌ها (ثانیه)
`/list` - نمایش پیام‌های فعلی
`/addmsg متن` - اضافه کردن پیام جدید
`/delmsg شماره` - حذف پیام (مثال: `/delmsg 2`)
`/clearmsg` - پاک کردن همه پیام‌ها
`/addtext متن` - اضافه کردن یک متن و تکرارش در همه پیام‌ها
`/settings` - نمایش تنظیمات فعلی

**تنظیمات فعلی:**
• تعداد پیام: {settings["message_count"]}
• فاصله زمانی: {settings["delay_between_messages"]} ثانیه
• تعداد پیام‌های ذخیره شده: {len(settings["auto_messages"])}

**نحوه استفاده:**
فقط کافیست به پیام کاربر **پاسخ (Reply)** دهید!
"""
    
    await update.message.reply_text(welcome_text)

async def set_count_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور تنظیم تعداد پیام‌ها"""
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("❌ شما دسترسی ندارید!")
        return
    
    if not context.args:
        await update.message.reply_text("❌ لطفاً عدد وارد کنید!\nمثال: `/setcount 20`")
        return
    
    try:
        count = int(context.args[0])
        if count <= 0:
            await update.message.reply_text("❌ عدد باید بزرگتر از صفر باشد!")
            return
        
        settings = load_settings()
        settings["message_count"] = count
        save_settings(settings)
        
        await update.message.reply_text(f"✅ تعداد پیام‌ها به **{count}** تنظیم شد!")
        
    except ValueError:
        await update.message.reply_text("❌ لطفاً یک عدد معتبر وارد کنید!")

async def set_delay_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور تنظیم فاصله زمانی"""
    if update.message.from_user.id != ADMIN_ID:
        return
    
    if not context.args:
        await update.message.reply_text("❌ لطفاً عدد وارد کنید!\nمثال: `/setdelay 0.5`")
        return
    
    try:
        delay = float(context.args[0])
        if delay < 0.1:
            await update.message.reply_text("❌ فاصله زمانی نمی‌تواند کمتر از ۰.۱ ثانیه باشد!")
            return
        
        settings = load_settings()
        settings["delay_between_messages"] = delay
        save_settings(settings)
        
        await update.message.reply_text(f"✅ فاصله زمانی به **{delay}** ثانیه تنظیم شد!")
        
    except ValueError:
        await update.message.reply_text("❌ لطفاً یک عدد معتبر وارد کنید!")

async def list_messages_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش لیست پیام‌ها"""
    if update.message.from_user.id != ADMIN_ID:
        return
    
    settings = load_settings()
    messages = settings["auto_messages"]
    
    if not messages:
        await update.message.reply_text("📝 هیچ پیامی ذخیره نشده است!")
        return
    
    message_list = "📋 **لیست پیام‌های ذخیره شده:**\n\n"
    for i, msg in enumerate(messages, 1):
        message_list += f"{i}. {msg}\n"
    
    await update.message.reply_text(message_list)

async def add_message_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """اضافه کردن پیام جدید"""
    if update.message.from_user.id != ADMIN_ID:
        return
    
    if not context.args:
        await update.message.reply_text("❌ لطفاً متن پیام را وارد کنید!\nمثال: `/addmsg هر متنی که می‌خواهی`")
        return
    
    new_message = " ".join(context.args)
    settings = load_settings()
    settings["auto_messages"].append(new_message)
    save_settings(settings)
    
    await update.message.reply_text(f"✅ پیام جدید اضافه شد:\n`{new_message}`")

async def delete_message_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """حذف پیام"""
    if update.message.from_user.id != ADMIN_ID:
        return
    
    if not context.args:
        await update.message.reply_text("❌ لطفاً شماره پیام را وارد کنید!\nمثال: `/delmsg 2`")
        return
    
    try:
        index = int(context.args[0]) - 1
        settings = load_settings()
        
        if index < 0 or index >= len(settings["auto_messages"]):
            await update.message.reply_text("❌ شماره پیام معتبر نیست!")
            return
        
        deleted_message = settings["auto_messages"].pop(index)
        save_settings(settings)
        
        await update.message.reply_text(f"✅ پیام حذف شد:\n`{deleted_message}`")
        
    except ValueError:
        await update.message.reply_text("❌ لطفاً یک عدد معتبر وارد کنید!")

async def clear_messages_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پاک کردن همه پیام‌ها"""
    if update.message.from_user.id != ADMIN_ID:
        return
    
    settings = load_settings()
    settings["auto_messages"] = []
    save_settings(settings)
    
    await update.message.reply_text("✅ همه پیام‌ها پاک شدند!")

async def add_text_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """اضافه کردن یک متن و تکرارش"""
    if update.message.from_user.id != ADMIN_ID:
        return
    
    if not context.args:
        await update.message.reply_text("❌ لطفاً متن را وارد کنید!\nمثال: `/addtext متن دلخواه`")
        return
    
    text = " ".join(context.args)
    settings = load_settings()
    
    # پاک کردن پیام‌های قبلی و اضافه کردن متن جدید به تعداد message_count
    settings["auto_messages"] = [text] * settings["message_count"]
    save_settings(settings)
    
    await update.message.reply_text(f"✅ متن تنظیم شد:\n`{text}`\n\nاین متن {settings['message_count']} بار تکرار خواهد شد.")

async def show_settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش تنظیمات فعلی"""
    if update.message.from_user.id != ADMIN_ID:
        return
    
    settings = load_settings()
    
    settings_text = f"""
⚙️ **تنظیمات فعلی ربات:**

• تعداد پیام ارسالی: **{settings['message_count']}**
• فاصله بین پیام‌ها: **{settings['delay_between_messages']}** ثانیه
• تعداد پیام‌های ذخیره شده: **{len(settings['auto_messages'])}**

**پیام اول:** {settings['auto_messages'][0] if settings['auto_messages'] else 'هیچ'}

از دستور `/start` برای راهنما استفاده کنید.
"""
    
    await update.message.reply_text(settings_text)

async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پردازش زمانی که ادمین به پیامی پاسخ می‌دهد"""
    if (update.message and 
        update.message.from_user.id == ADMIN_ID and 
        update.message.reply_to_message):
        
        target_user_id = update.message.reply_to_message.from_user.id
        settings = load_settings()
        message_count = settings["message_count"]
        delay = settings["delay_between_messages"]
        auto_messages = settings["auto_messages"]
        
        if not auto_messages:
            await update.message.reply_text("❌ هیچ پیامی تنظیم نشده است! از /addmsg استفاده کنید.")
            return
        
        sent_count = 0
        for i in range(min(message_count, len(auto_messages))):
            await context.bot.send_message(
                chat_id=target_user_id,
                text=auto_messages[i]
            )
            sent_count += 1
            await asyncio.sleep(delay)
        
        await update.message.reply_text(
            f"✅ **{sent_count}** پیام ارسال شد!",
            reply_to_message_id=update.message.message_id
        )

def main():
    """تابع اصلی"""
    application = Application.builder().token(TOKEN).build()
    
    # افزودن هندلرهای دستورات
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("setcount", set_count_command))
    application.add_handler(CommandHandler("setdelay", set_delay_command))
    application.add_handler(CommandHandler("list", list_messages_command))
    application.add_handler(CommandHandler("addmsg", add_message_command))
    application.add_handler(CommandHandler("delmsg", delete_message_command))
    application.add_handler(CommandHandler("clearmsg", clear_messages_command))
    application.add_handler(CommandHandler("addtext", add_text_command))
    application.add_handler(CommandHandler("settings", show_settings_command))
    
    # هندلر برای تشخیص ریپلای ادمین
    application.add_handler(
        MessageHandler(filters.REPLY, handle_admin_reply)
    )
    
    print("🤖 ربات فعال شد...")
    print("📝 از دستور /start برای راهنما استفاده کنید")
    application.run_polling()

if __name__ == "__main__":
    main()
