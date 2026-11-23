
import telebot
import os
from dotenv import load_dotenv
from telebot import types
import random

# Завантаження токена з файлу .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

# Список із 5 футбольних запитань
questions = [
    {
        "question": "Скільки гравців однієї команди перебуває на полі?",
        "options": ["9", "10", "11", "12"],
        "answer": "11"
    },
    {
        "question": "Яка країна виграла Чемпіонат світу 2022 року?",
        "options": ["Франція", "Аргентина", "Бразилія", "Німеччина"],
        "answer": "Аргентина"
    },
    {
        "question": "Хто має прізвисько CR7?",
        "options": ["Ліонель Мессі", "Неймар", "Кріштіану Роналду", "Мбаппе"],
        "answer": "Кріштіану Роналду"
    },
    {
        "question": "Скільки хвилин триває основний час футбольного матчу?",
        "options": ["60", "80", "90", "100"],
        "answer": "90"
    },
    {
        "question": "Яка команда має прізвисько «Королівський клуб»?",
        "options": ["Барселона", "Реал Мадрид", "Челсі", "Баварія"],
        "answer": "Реал Мадрид"
    }
]

# Збереження результатів гравців
user_data = {}


# Команда старт
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "⚽ Вітаю у футбольній вікторині!\n\n"
        "Тут ти можеш перевірити свої знання про футбол.\n"
        "Натискай /quiz, щоб почати гру!"
    )


# Команда допомоги
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "📖 Правила вікторини:\n\n"
        "/start — початок роботи\n"
        "/help — допомога\n"
        "/quiz — почати вікторину\n\n"
        "Відповідай на 5 запитань і набирай бали!"
    )


# Початок вікторини
@bot.message_handler(commands=['quiz'])
def start_quiz(message):
    user_id = message.from_user.id

    user_data[user_id] = {
        "questions": random.sample(questions, len(questions)),
        "current": 0,
        "score": 0
    }

    send_question(message.chat.id, user_id)


# Надсилання запитання
def send_question(chat_id, user_id):
    data = user_data[user_id]

    if data["current"] >= len(data["questions"]):
        bot.send_message(
            chat_id,
            f"🏁 Вікторину завершено!\n\n"
            f"Твій результат: {data['score']} із 5 правильних відповідей."
        )
        del user_data[user_id]
        return

    question = data["questions"][data["current"]]

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    for option in question["options"]:
        markup.add(types.KeyboardButton(option))

    bot.send_message(
        chat_id,
        f"⚽ Запитання {data['current'] + 1}/5:\n\n"
        f"{question['question']}",
        reply_markup=markup
    )


# Перевірка відповіді
@bot.message_handler(func=lambda message: message.from_user.id in user_data)
def check_answer(message):
    user_id = message.from_user.id
    data = user_data[user_id]

    question = data["questions"][data["current"]]

    if message.text not in question["options"]:
        bot.send_message(
            message.chat.id,
            "Будь ласка, обери відповідь за допомогою кнопок."
        )
        return

    if message.text == question["answer"]:
        data["score"] += 1
        bot.send_message(message.chat.id, "✅ Правильно! Молодець!")
    else:
        bot.send_message(
            message.chat.id,
            f"❌ Неправильно! Правильна відповідь: {question['answer']}"
        )

    data["current"] += 1

    send_question(message.chat.id, user_id)


# Запуск бота
print("Футбольна вікторина запущена!")
bot.infinity_polling()

