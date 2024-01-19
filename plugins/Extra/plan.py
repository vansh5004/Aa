from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from telegram.ext.dispatcher import run_async
from datetime import datetime, timedelta

# Define your token here
TOKEN = "6726031505:AAEM2q-VJOqql7_LYBX-uRtcQMtg5b0lA2U"
updater = Updater(token=TOKEN, use_context=True)

# Replace with the actual admin user ID
ADMIN_USER_ID = 2020224264  # Replace with the admin's user ID

# Dictionary to store plans and purchase time for each user
user_plans = {}

# Available plans with their durations in days
plans = {
    "1day": {"price": 10, "duration": 1},
    "7day": {"price": 20, "duration": 7},
    "1month": {"price": 100, "duration": 30}
}

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! Use /plan to see available plans.")

def plan(update: Update, context: CallbackContext) -> None:
    # Display available plans
    plan_text = "Available plans:\n"
    photo_url = 'https://graph.org/file/f8c26a2bda2c9ca9c6871.jpg'
    for plan_name, plan_details in plans.items():
        plan_text += f"{plan_name} - {plan_details['price']}rs\n"
    update.message.reply_text(photo=photo_url, plan_text)

def buy_plan(update: Update, context: CallbackContext) -> None:
    # Get the user's input after the /buyplan command
    plan_name = context.args[0]

    # Check if the plan is valid
    if plan_name in plans:
        user_id = update.message.from_user.id
        plan_price = plans[plan_name]["price"]
        plan_duration = plans[plan_name]["duration"]
        
        # Save the plan and purchase time for the user
        purchase_time = datetime.now()
        expiration_time = purchase_time + timedelta(days=plan_duration)
        user_plans[user_id] = {"plan_name": plan_name, "plan_price": plan_price, "expiration_time": expiration_time}

        update.message.reply_text(f"Plan purchased: {plan_name} - {plan_price}rs. Expires on {expiration_time}")
    else:
        update.message.reply_text("Invalid plan. Use /plan to see available plans.")

@run_async
def add_premium(update: Update, context: CallbackContext) -> None:
    # Check if the user is an admin
    if update.message.from_user.id == ADMIN_USER_ID:
        # Ask for user ID
        update.message.reply_text("Please provide the Telegram user ID of the user you want to add to the premium plan.")
        context.user_data['admin_step'] = 'get_user_id'
    else:
        update.message.reply_text("You don't have permission to use this command.")

def get_user_id(update: Update, context: CallbackContext) -> None:
    # Retrieve user ID from the admin's input
    user_id = context.message.text.strip()

    if user_id.isdigit():
        # Ask for the desired plan
        context.user_data['user_id'] = int(user_id)
        update.message.reply_text("Please select the plan for the user (1day/7day/1month).")
        context.user_data['admin_step'] = 'get_plan'
    else:
        update.message.reply_text("Invalid user ID. Please provide a valid numerical user ID.")

def get_plan(update: Update, context: CallbackContext) -> None:
    # Retrieve the selected plan from the admin's input
    plan_name = context.message.text.strip()

    # Check if the plan is valid
    if plan_name in plans:
        user_id = context.user_data['user_id']
        plan_price = plans[plan_name]["price"]
        plan_duration = plans[plan_name]["duration"]

        # Save the plan and purchase time for the user
        purchase_time = datetime.now()
        expiration_time = purchase_time + timedelta(days=plan_duration)
        user_plans[user_id] = {"plan_name": plan_name, "plan_price": plan_price, "expiration_time": expiration_time}

        # Send a confirmation message to the user
        update.message.reply_text(f"You are subscribed to the premium plan ({plan_name} - {plan_price}rs). Expires on {expiration_time}")
    else:
        update.message.reply_text("Invalid plan. Please select a valid plan (1day/7day/1month).")

def myplan(update: Update, context: CallbackContext) -> None:
    # Retrieve the user's plan and check expiration
    user_id = update.message.from_user.id
    user_plan = user_plans.get(user_id)

    if user_plan:
        plan_name = user_plan["plan_name"]
        plan_price = user_plan["plan_price"]
        expiration_time = user_plan["expiration_time"]

        if expiration_time and datetime.now() > expiration_time:
            update.message.reply_text("Your plan has expired. Use /plan to see available plans.")
            del user_plans[user_id]  # Remove expired plan
            # Notify the user about plan expiration
            update.message.reply_text("Your Subscription has expired. Renew Premium plan.")
        else:
            update.message.reply_text(f"Your plan: {plan_name} - {plan_price}rs. Expires on {expiration_time}")
    else:
        update.message.reply_text("No plan purchased. Use /plan to see available plans.")

def userpremium(update: Update, context: CallbackContext) -> None:
    # Check if the user is an admin
    if update.message.from_user.id == ADMIN_USER_ID:
        premium_users = [user_id for user_id, user_plan in user_plans.items() if user_plan and datetime.now() < user_plan["expiration_time"]]
        if premium_users:
            premium_info = "\n".join([f"User ID: {user_id}, Plan: {user_plans[user_id]['plan_name']}, Expires on: {user_plans[user_id]['expiration_time']}" for user_id in premium_users])
            update.message.reply_text(f"Users with active premium plans:\n{premium_info}")
        else:
            update.message.reply_text("No users have active premium plans.")
    else:
        update.message.reply_text("You don't have permission to use this command.")

def main() -> None:
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("plan", plan))
    dp.add_handler(CommandHandler("buyplan", buy_plan, pass_args=True))
    dp.add_handler(CommandHandler("addpremium", add_premium))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, get_user_id, run_async=True))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, get_plan, run_async=True))
    dp.add_handler(CommandHandler("myplan", myplan))
    dp.add_handler(CommandHandler("userpremium", userpremium))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
