from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery
# from aiogram.utils import executor
from aiogram import executor
from info import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Dictionary to store user payment requests
payment_requests = {}


@dp.message_handler(commands=['buy_repo'])
async def buy_repo(message: types.Message):
    user_id = message.from_user.id

    # Generate QR code and UPI details (replace with your logic)
    qr_code_url = "https://graph.org/file/187cd4a45be90ef91d261.jpg"
    upi_details = "vansh009@fam"

    # Store payment details in the dictionary
    payment_requests[user_id] = {"qr_code_url": qr_code_url, "upi_details": upi_details}

    # Create an inline keyboard with "Payment Done" button
    keyboard = [[InlineKeyboardButton("Payment Done", callback_data='payment_done')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the QR code and UPI details to the user
    await message.reply_text(f"Scan the QR code or use the provided UPI details for payment:", reply_markup=reply_markup)


@dp.callback_query_handler(lambda c: c.data == 'payment_done')
async def payment_done(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    # Inform the admin about the payment request
    admin_user_id = "2020224264"  # Replace with the actual admin user ID
    admin_message = f"Payment request received from user {user_id}. Click 'Received' if payment is received or 'Not Receive' otherwise."
    keyboard = [
        [InlineKeyboardButton("Received", callback_data='payment_received')],
        [InlineKeyboardButton("Not Receive", callback_data='not_received')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await bot.send_message(chat_id=admin_user_id, text=admin_message, reply_markup=reply_markup)


@dp.callback_query_handler(lambda c: c.data == 'not_received')
async def not_received(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    # Send a message to the user indicating that the admin did not receive the payment
    user_message = "Your payment request was not received by the admin. Please contact the admin for further assistance."
    await bot.send_message(chat_id=user_id, text=user_message)


@dp.callback_query_handler(lambda c: c.data == 'payment_received')
async def payment_received(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    # Send the GitHub link to the user
    github_link = "https://github.com/htmlboss123/PiroAutoFilterBot/"
    await bot.send_message(chat_id=user_id, text=f"Congratulations! 🔥 GitHub link: {github_link}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
