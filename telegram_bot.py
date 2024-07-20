from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import json
from datetime import datetime
import os

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = '7032217254:AAH8JfH1ekLCXL9FJDfJR-2-2VUCL9bwQqg'

# Path to the JSON file
TRANSACTIONS_FILE = 'transactions.json'

# List of allowed user IDs
ALLOWED_USERS = [1998029329]  # Replace with actual Telegram user IDs

def load_transactions():
    """Load transactions from the JSON file."""
    if os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, 'r') as file:
            return json.load(file)
    else:
        return []

def save_transactions(transactions):
    """Save transactions to the JSON file."""
    with open(TRANSACTIONS_FILE, 'w') as file:
        json.dump(transactions, file)

async def check_user(update: Update) -> bool:
    """Check if the user is in the allowed users list."""
    user_id = update.message.from_user.id
    return user_id in ALLOWED_USERS

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await check_user(update):
        await update.message.reply_text(
            'Welcome! Here are the commands you can use:\n'
            '/add <amount> - Add money to your account.\n'
            '/debit <amount> - Debit money from your account.\n'
            '/transactions <dd/mm/yy> - View transactions for a specific date.\n'
            '/total <dd/mm/yy> - Get the total amount for a specific date.\n'
            'Make sure to use the correct date format (dd/mm/yy).'
        )
    else:
        await update.message.reply_text('You are not authorized to use this bot.')

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await check_user(update):
        try:
            amount = float(context.args[0])
            transactions = load_transactions()
            transactions.append({
                'amount': amount,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'type': 'credit'
            })
            save_transactions(transactions)
            await update.message.reply_text(f'Added {amount} to your account.')
        except (IndexError, ValueError):
            await update.message.reply_text('Usage: /add <amount>')
    else:
        await update.message.reply_text('You are not authorized to use this bot.')

async def debit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await check_user(update):
        try:
            amount = float(context.args[0])
            transactions = load_transactions()
            transactions.append({
                'amount': -amount,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'type': 'debit'
            })
            save_transactions(transactions)
            await update.message.reply_text(f'Debited {amount} from your account.')
        except (IndexError, ValueError):
            await update.message.reply_text('Usage: /debit <amount>')
    else:
        await update.message.reply_text('You are not authorized to use this bot.')

async def transactions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await check_user(update):
        try:
            if len(context.args) == 1:
                date_str = context.args[0]
                date_obj = datetime.strptime(date_str, '%d/%m/%y').strftime('%Y-%m-%d')

                transactions = load_transactions()
                filtered_transactions = [
                    t for t in transactions if t['date'].startswith(date_obj)
                ]

                if filtered_transactions:
                    message = '\n'.join([f'{t["type"].capitalize()}: {t["amount"]} on {t["date"]}' for t in filtered_transactions])
                else:
                    message = f'No transactions found for {date_str}.'
            else:
                message = 'Usage: /transactions <dd/mm/yy>'

            await update.message.reply_text(message)
        except ValueError:
            await update.message.reply_text('Invalid date format. Please use dd/mm/yy.')
    else:
        await update.message.reply_text('You are not authorized to use this bot.')

async def total(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await check_user(update):
        try:
            if len(context.args) == 1:
                date_str = context.args[0]
                date_obj = datetime.strptime(date_str, '%d/%m/%y').strftime('%Y-%m-%d')

                transactions = load_transactions()
                total_amount = sum(
                    t['amount'] for t in transactions if t['date'].startswith(date_obj)
                )

                await update.message.reply_text(f'Total amount for {date_str}: {total_amount}')
            else:
                await update.message.reply_text('Usage: /total <dd/mm/yy>')
        except ValueError:
            await update.message.reply_text('Invalid date format. Please use dd/mm/yy.')
    else:
        await update.message.reply_text('You are not authorized to use this bot.')

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("debit", debit))
    application.add_handler(CommandHandler("transactions", transactions))
    application.add_handler(CommandHandler("total", total))

    application.run_polling()

if __name__ == '__main__':
    main()
