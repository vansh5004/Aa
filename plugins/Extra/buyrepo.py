from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from pyrogram import Client, filters

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
# updater = Updater(token='YOUR_BOT_TOKEN', use_context=True)

# Dictionary to store user payment requests
payment_requests = {}

@updater.message_handler(filters.private & filters.command(["buy_repo"]))
def buy_repo_command_handler(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    # Generate QR code and UPI details (replace with your logic)
    qr_code_url = "https://graph.org/file/187cd4a45be90ef91d261.jpg"
    upi_details = "vansh009@fam"

    # Store payment details in the dictionary
    payment_requests[user_id] = {"qr_code_url": qr_code_url, "upi_details": upi_details}

    # Create an inline keyboard with "Payment Done" button
    keyboard = [[InlineKeyboardButton("Payment Done", callback_data='payment_done')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the QR code and UPI details to the user
    update.message.reply_text(f"Scan the QR code or use the provided UPI details for payment:", reply_markup=reply_markup)

    # Show an alert to the user
    # Note: The context.bot method is used directly instead of update.callback_query
    context.bot.answer_callback_query(update.callback_query.id, text="Payment request sent. Please wait for admin approval.")

def payment_done_command_handler(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    # Inform the admin about the payment request
    admin_user_id = "2020224264"  # Replace with the actual admin user ID
    admin_message = f"Payment request received from user {user_id}. Click 'Received' if payment is received or 'Not Receive' otherwise."
    keyboard = [
        [InlineKeyboardButton("Received", callback_data='payment_received')],
        [InlineKeyboardButton("Not Receive", callback_data='not_received')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=admin_user_id, text=admin_message, reply_markup=reply_markup)

def not_received_command_handler(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    # Send a message to the user indicating that the admin did not receive the payment
    user_message = "Your payment request was not received by the admin. Please contact the admin for further assistance."
    context.bot.send_message(chat_id=user_id, text=user_message)

def payment_received_command_handler(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    # Send the GitHub link to the user
    github_link = "https://github.com/htmlboss123/PiroAutoFilterBot/"
    update.message.reply_text(f"Congratulations! 🔥 GitHub link: {github_link}")

# Command handlers
updater.dispatcher.add_handler(buy_repo_command_handler)

# Callback query handlers
# Note: Callback query handlers should be added separately using CallbackQueryHandler
updater.dispatcher.add_handler(CallbackQueryHandler(payment_done_command_handler, pattern='payment_done'))
updater.dispatcher.add_handler(CallbackQueryHandler(not_received_command_handler, pattern='not_received'))
updater.dispatcher.add_handler(CallbackQueryHandler(payment_received_command_handler, pattern='payment_received'))

# Start the bot
# updater.start_polling()
# updater.idle()
