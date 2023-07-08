import asyncio
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import aioschedule as schedule, os,logging
from dotenv import load_dotenv


load_dotenv('.env')
bot = Bot(os.environ.get('token'))
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)




class Task(StatesGroup):
    title = State()
    time = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Я ToDo List Bot. Чтобы добавить дело, используй команду /add.")


@dp.message_handler(commands=['add'])
async def add_task(message: types.Message):
    await message.reply("Введите название дела:")
    await Task.title.set()


@dp.message_handler(state=Task.title)
async def set_time(message: types.Message, state: FSMContext):
    title = message.text
    await state.update_data(title=title)

    await message.reply("Введите время выполнения дела (в формате HH:MM):")
    await Task.time.set()


@dp.message_handler(state=Task.time)
async def add_task_to_db(message: types.Message, state: FSMContext):
    time = message.text
    await state.update_data(time=time)
    data = await state.get_data()
    title = data['title']

    

    await state.finish()
    await message.reply(f"Дело '{title}' добавлено.")


@dp.message_handler(commands=['delete'])
async def delete_task(message: types.Message):
    await message.reply("Дело удалено.")


async def send_task_list():
   

    tasks = ["Task 1", "Task 2", "Task 3"]  # Пример списка дел

    if tasks:
        for task in tasks:
            await bot.send_message(chat_id=USER_CHAT_ID, text=task)
    else:
        await bot.send_message(chat_id=USER_CHAT_ID, text="Список дел пуст.")


async def schedule_jobs():
    schedule.every().day.at("09:00").do(send_task_list)  

    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)

executor.start_polling(dp, skip_updates=True)