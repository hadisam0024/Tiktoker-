from telegram.ext import Updater, CommandHandler
import requests
from bs4 import BeautifulSoup

# 🔐 Your Telegram Bot Token
TOKEN = "7911567511:AAHIfmdh_AWm7csYZBkwv4Nw11VCEVwniDg"

def start(update, context):
    update.message.reply_text("🤖 Bot is Active!\nUse /check <tiktok_username> to get info.")

def check(update, context):
    args = context.args
    if not args:
        update.message.reply_text("❌ Usage: /check <username>")
        return

    username = args[0].replace("@", "").strip()
    url = f"https://www.tiktok.com/@{username}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 404 or "Couldn't find this account" in res.text:
            update.message.reply_text(f"@{username} ❌ Not found")
            return

        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text().lower()

        passkey = "✅" if "passkey" not in text else "❌"
        links = "✅" if "http" not in text else "❌"
        email = "✅" if "gmail.com" not in text and "email" not in text else "❌"
        phone = "✅" if "+92" not in text and "phone" not in text else "❌"

        message = (
            f"👤 Account: @{username}\n"
            f"🔐 Passkey not found: {passkey}\n"
            f"🔗 External links: {links}\n"
            f"📧 Email hidden: {email}\n"
            f"📱 Phone hidden: {phone}"
        )
        update.message.reply_text(message)

    except Exception as e:
        update.message.reply_text(f"⚠️ Error: {str(e)}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("check", check))

    print("✅ Bot started...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
