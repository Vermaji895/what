import random
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace these with your credentials
BOT_TOKEN = "7880370045:AAH90gZ-84ZwcNoqzNK6AjgGoGKQ_ye-rk4"
ADMIN_ID = 7417113479  # Replace with your Telegram user ID


def luhn_algorithm(card_number):
    """
    Validate a credit card number using the Luhn algorithm.
    """
    digits = [int(d) for d in str(card_number)][::-1]
    checksum = 0
    for i, digit in enumerate(digits):
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0


def check_card_approval(card_number, expiry_month, expiry_year, cvv):
    """
    Simulates checking if a credit card is approved for payment.
    """
    if not card_number.isdigit() or not expiry_month.isdigit() or not expiry_year.isdigit() or not cvv.isdigit():
        return "❌ Invalid input. Please ensure all fields are numeric."

    if not luhn_algorithm(card_number):
        return "❌ Card declined. Invalid card number."

    if int(expiry_month) not in range(1, 13):
        return "❌ Card declined. Invalid expiry month."

    if int(expiry_year) < 2025:  # Replace with current year in production
        return "❌ Card declined. Card has expired."

    if len(cvv) != 3:
        return "❌ Card declined. Invalid CVV."

    # Random approval simulation
    if random.choice([True, False]):
        return "✅ Card approved for payment."
    else:
        return "❌ Card declined. Insufficient funds or blocked."


def start(update: Update, context: CallbackContext):
    """
    Handles the /start command.
    """
    if update.effective_user.id == ADMIN_ID:
        update.message.reply_text("Welcome Admin! Send the card details as: \n\n"
                                  "CardNumber|MM|YYYY|CVV")
    else:
        update.message.reply_text("🚫 Access Denied. You are not authorized to use this bot.")


def check_card(update: Update, context: CallbackContext):
    """
    Handles card details sent by the admin.
    """
    if update.effective_user.id != ADMIN_ID:
        update.message.reply_text("🚫 Access Denied. You are not authorized to use this bot.")
        return

    # Parse the card details
    message = update.message.text
    try:
        card_number, expiry_month, expiry_year, cvv = message.split("|")
        result = check_card_approval(card_number.strip(), expiry_month.strip(), expiry_year.strip(), cvv.strip())
        update.message.reply_text(result)
    except ValueError:
        update.message.reply_text("❌ Invalid format. Send the details as:\nCardNumber|MM|YYYY|CVV")


def main():
    """
    Main function to run the bot.
    """
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    # Command handler for /start
    dp.add_handler(CommandHandler("start", start))

    # Message handler for card details
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, check_card))

    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()