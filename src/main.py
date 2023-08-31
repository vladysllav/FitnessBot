import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler
from dotenv import load_dotenv
from user_service import UserService
from csv_file_handler import CSVFileHandler


from .db import engine, SessionLocal
from .models import Base, User
from sqlalchemy.orm import Session  # Import Session

Base.metadata.create_all(bind=engine)


"""
example of a function to create a user

def create_user(username: str, email: str):
    db = SessionLocal()
    db_user = User(username=username, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user
"""




load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")


class FitnessBot:

    def __init__(self, token):
        self.app = Application.builder().token(token).build()
        self.user_service = UserService()
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CallbackQueryHandler(self.handle_type_options, pattern='^type_.*$'))
        self.app.add_handler(CallbackQueryHandler(self.handle_coach_options, pattern='^coach_.*$'))
        self.app.add_handler(CallbackQueryHandler(self.handle_athlete_options, pattern='^athlete_.*$'))

    async def start(self, update: Update, context: CallbackContext) -> None:
        user_id = update.message.from_user.id
        user_data = self.user_service.get_user_by_id(user_id)

        if user_data:
            username = user_data['username']
            first_name = user_data['first_name']
            last_name = user_data['last_name']
            user_type = user_data['user_type']
            await update.message.reply_text(f"Hello {first_name} {last_name}, {user_type}")
        else:
            keyboard = [
                [
                    InlineKeyboardButton("Coach", callback_data='type_coach'),
                    InlineKeyboardButton("Athlete", callback_data='type_athlete')
                ]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("Please choose your type:", reply_markup=reply_markup)

    async def handle_coach_options(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query_data = query.data
        user_type = query_data.split('_')[1]

        await query.edit_message_text(user_type)

    async def handle_athlete_options(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query_data = query.data
        user_type = query_data.split('_')[1]

        await query.edit_message_text(user_type)

    async def handle_type_options(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query_data = query.data
        user_type = query_data.split('_')[1]

        try:
            if query.from_user.last_name is None:
                UserService.add_user(id=query.from_user.id,
                                     username=query.from_user.username,
                                     first_name=has_emoji(query.from_user.first_name),
                                     last_name='',
                                     user_type=user_type)
            else:
                UserService.add_user(id=query.from_user.id,
                                     username=query.from_user.username,
                                     first_name=has_emoji(query.from_user.first_name),
                                     last_name=has_emoji(query.from_user.last_name),
                                     user_type=user_type)
        except Exception as e:
            print(f"An exception occurred: {e}")

        if user_type == 'coach':
            coach_keyboard = [
                [
                    InlineKeyboardButton("Show my athletes", callback_data='coach_show_athletes'),
                    InlineKeyboardButton("Add workout program", callback_data='coach_add_program')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(coach_keyboard)
            await query.edit_message_text("Choose an option:", reply_markup=reply_markup)
        elif user_type == 'athlete':
            athlete_keyboard = [
                [
                    InlineKeyboardButton("Show WOD", callback_data='athlete_show_wod'),
                    InlineKeyboardButton("Write result of WOD", callback_data='athlete_write_result_wod'),
                ],
                [
                    InlineKeyboardButton("Show statistics", callback_data='athlete_show_statistic')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(athlete_keyboard)
            await query.edit_message_text("Choose an option:", reply_markup=reply_markup)
        else:
            await query.edit_message_text("Invalid type. Please choose either 'Coach' or 'Athlete'.")

    def run(self):
        self.app.run_polling()


if __name__ == '__main__':
    bot = FitnessBot(TOKEN)
    bot.run()
