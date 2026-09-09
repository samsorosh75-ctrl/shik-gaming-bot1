import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_USERNAME = "@samansorush1"

IPV4_PRICE = "۲۰۰ هزار تومان"
IPV6_PRICE = "۲۵۰ هزار تومان"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛒 خرید DNS", callback_data="buy")],
        [InlineKeyboardButton("📞 ارتباط با پشتیبانی", callback_data="support")],
    ]

    await update.message.reply_text(
        "🎮 به فروشگاه DNS شیک گیمینگ خوش آمدید!\n\n"
        "DNSهای مخصوص گیمینگ با پشتیبانی IPv4 و IPv6\n\n"
        "یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy":
        keyboard = [
            [InlineKeyboardButton(
                f"🌐 IPv4 — {IPV4_PRICE}",
                callback_data="ipv4"
            )],
            [InlineKeyboardButton(
                f"🌐 IPv6 — {IPV6_PRICE}",
                callback_data="ipv6"
            )],
            [InlineKeyboardButton("🔙 برگشت", callback_data="back")],
        ]

        await query.edit_message_text(
            "🛒 انتخاب DNS\n\n"
            "نوع DNS موردنظر خود را انتخاب کنید:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data in ("ipv4", "ipv6"):
        dns_type = "IPv4" if query.data == "ipv4" else "IPv6"
        price = IPV4_PRICE if query.data == "ipv4" else IPV6_PRICE

        keyboard = [
            [InlineKeyboardButton(
                "💳 پرداخت و ثبت سفارش",
                callback_data=f"pay_{query.data}"
            )],
            [InlineKeyboardButton("🔙 برگشت", callback_data="buy")],
        ]

        await query.edit_message_text(
            f"📦 پلن انتخابی: {dns_type}\n"
            f"⏱ مدت: ۱ ماه\n"
            f"💰 قیمت: {price}\n\n"
            "برای ادامه روی «پرداخت و ثبت سفارش» بزنید.",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data.startswith("pay_"):
        dns_type = "IPv4" if query.data == "pay_ipv4" else "IPv6"
        price = IPV4_PRICE if dns_type == "IPv4" else IPV6_PRICE

        await query.edit_message_text(
            f"💳 ثبت سفارش {dns_type}\n\n"
            f"💰 مبلغ قابل پرداخت: {price}\n\n"
            "لطفاً مبلغ را به شماره کارت اعلام‌شده توسط پشتیبانی واریز کنید "
            "و سپس تصویر رسید را برای پشتیبانی ارسال کنید.\n\n"
            f"👤 پشتیبانی: {ADMIN_USERNAME}"
        )

    elif query.data == "support":
        await query.edit_message_text(
            "📞 پشتیبانی فروشگاه\n\n"
            f"👤 ادمین: {ADMIN_USERNAME}\n\n"
            "برای خرید یا پیگیری سفارش به ادمین پیام دهید."
        )

    elif query.data == "back":
        await start_from_query(query)


async def start_from_query(query):
    keyboard = [
        [InlineKeyboardButton("🛒 خرید DNS", callback_data="buy")],
        [InlineKeyboardButton("📞 ارتباط با پشتیبانی", callback_data="support")],
    ]

    await query.edit_message_text(
        "🎮 فروشگاه DNS شیک گیمینگ\n\n"
        "یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "لطفاً از منوی ربات استفاده کنید.\n"
        "برای شروع /start را بزنید."
    )


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN تنظیم نشده است.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_message)
    )

    app.run_polling()


if __name__ == "__main__":
    main()
