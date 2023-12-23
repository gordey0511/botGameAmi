import math
import os
import logging
import asyncio
import time
from math import sqrt

from aiogram import Dispatcher, Bot
from aiogram.utils import executor
from aiogram.types import (
	Message, ContentType, PreCheckoutQuery, CallbackQuery, InlineKeyboardMarkup,
	InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, LabeledPrice,
)
from bson import ObjectId

import db


logging.basicConfig(level=logging.INFO)
bot = Bot(token="6926737733:AAGFyWXssPGoB9upsBPHxX8Za51tP3i4-4w")
dp = Dispatcher(bot)


base_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
# base_keyboard.add(KeyboardButton(cfg.BUTTON_MATCH))
base_keyboard.row(
	KeyboardButton("Путешествовать"),
	KeyboardButton("Продать"),
)
base_keyboard.row(
	KeyboardButton("Купить"),
	KeyboardButton("Мой инвентарь"),
)
base_keyboard.row(
	KeyboardButton("Мой персонаж"),
)



async def trigger(question_id: db.ObjectId, user: dict):
	print(question_id)
	if question_id is None:
		await bot.send_message(
			user["tid"],
			"Всем привет!",
			parse_mode='html',
			reply_markup=base_keyboard
		)
		return
	elif question_id == "CITY":
		await bot.send_message(
			user["user_id"],
			"Hello world!",
			reply_markup=base_keyboard
			)




@dp.message_handler(commands=['start'])
async def start(message: Message):
	user = db.find_user(message.from_user.id)
	await trigger(user["state"], user)


async def go_next(user_id: int, message: Message):
	user = db.find_user(user_id)
	print("GO NEXT ", user)

	if user["state"] == "NEW CITY":
		cur_city = db.get_cur_city(user["location_id"])

		if cur_city["type"] == "город":
			user["state"] = "CITY"
			db.update_user(user)
			await message.answer("Мы пришли в город!", reply_markup=base_keyboard)
		else:
			user["state"] = "DUNGEON"
			db.update_user(user)
			await message.answer("Мы пришли в подземелье!", reply_markup=base_keyboard)

			mob = db.get_random_mob()

			await message.answer(
				f"Ваш соперник"
				f"Nickname: {mob['name']}\n"
				f"HP: {mob['HP']}\n"
				f"XP: {mob['XP']}\n"
				f"req_level: {mob['req_level']}\n"
				f"attack_type: {mob['attack_type']}\n"
				f"attack: {mob['attack']}\n"
				f"magic_attack: {mob['magic_attack']}\n"
				f"armour: {mob['armour']}\n"
				f"magic_armour: {mob['magic_armour']}\n"
			)

			cur_attack = 0
			cur_armour = 0

			mob_attack = 0
			mob_armour = 0

			if mob["attack_type"] == "SIMPLE":
				cur_attack = user["attack"]
				cur_armour = user["armour"]

				mob_attack = mob["attack"]
				mob_armour = mob["armour"]
			else:
				print()

			await message.answer(
				f"Бой прошел. Ваш"
				f"Nickname: {mob['name']}\n"
				f"HP: {mob['HP']}\n"
				f"XP: {mob['XP']}\n"
				f"req_level: {mob['req_level']}\n"
				f"attack_type: {mob['attack_type']}\n"
				f"attack: {mob['attack']}\n"
				f"magic_attack: {mob['magic_attack']}\n"
				f"armour: {mob['armour']}\n"
				f"magic_armour: {mob['magic_armour']}\n"
			)
			print("MOB ", mob)

	else:
		print("ANOTHER")
		# user["state"] = question.get("next_question")


@dp.message_handler()
async def message_trigger(message: Message):
	user = db.find_user(message.from_user.id)
	if user["state"] is None:
		await go_next(message.from_user.id, message, message.text)
	elif message.text == "Путешествовать":
		cities = db.get_cities()
		cur_city = db.get_cur_city(user['location_id'])

		next_cities = []
		inline_kb = InlineKeyboardMarkup(row_width=2)
		print("Путешествовать", cur_city)

		for city in cities:
			print(city)
			if city["_id"] == cur_city["_id"]: continue

			if sqrt(pow((cur_city["x"]-city["x"]), 2) + pow((cur_city["y"]-city["y"]), 2)) <= 10:
				next_cities.append(city)
				button = InlineKeyboardButton(city["name"], callback_data=f"WAY {city['name']}")
				inline_kb.add(button)

		await message.answer(
			text="Путешествовать",
			reply_markup=inline_kb
		)
	elif message.text == "Купить":
		items = db.get_items()

		inline_kb = InlineKeyboardMarkup(row_width=2)

		for item in items:
			print(item)

			button = InlineKeyboardButton(f"{item['name']} – цена: {item['cost']}", callback_data=f"BUY {item['name']}")
			inline_kb.add(button)

		await message.answer(
			text="Что купим?",
			reply_markup=inline_kb
		)
	elif message.text == "Продать":
		items = db.get_my_items(user["user_id"])

		inline_kb = InlineKeyboardMarkup(row_width=2)

		for item_id, item_count in items.items():
			my_item = db.get_item(item_id)
			print(my_item, item_id, item_count)

			button = InlineKeyboardButton(f"{my_item['name']} – количество: {item_count}, цена продажи: {my_item['cost_to_sale']}", callback_data=f"SEL {my_item['name']}")
			inline_kb.add(button)

		await message.answer(
			text="Что продадим?",
			reply_markup=inline_kb
		)
	elif message.text == "Мой инвентарь":
		items = db.get_my_items(user["user_id"])
		text_inventar = "Инвентарь:\n"

		for item_id, item_count in items.items():
			my_item = db.get_item(item_id)
			print(my_item, item_id, item_count)
			if item_count > 0:
				text_inventar = text_inventar + f"{my_item['name']} – количество: {item_count}"

		await message.answer(
			text=text_inventar
		)
	elif message.text == "Мой персонаж":
		person = db.get_profile(message.from_user.id)
		print("TEST", person)

		text_person = f"Nickname: {person['nickname']}\n" \
					  f"Level: {person['level']}\n" \
					  f"HP: {person['HP']}\n" \
					  f"CurHP: {person['curHP']}\n" \
					  f"Money: {person['money']}\n" \
					  f"Attack: {person['attack']}\n" \
					  f"Magic Attack: {person['magic_attack']}\n" \
					  f"XP: {person['XP']}\n" \
					  f"Armour: {person['armour']}\n" \
					  f"Magic Armour: {person['magic_armour']}\n" \
					  f"Location: {db.get_cur_city(person['location_id'])['name']}\n"
		await message.answer(
			text = text_person,
			reply_markup=base_keyboard,
		)



@dp.callback_query_handler()
async def button_trigger(call: CallbackQuery):
	await bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
	user = db.find_user(call.from_user.id)

	if call.data[0:3] == "WAY":
		data = call.data[4:]
		city = await db.get_city_by_name(data)
		cur_city = db.get_cur_city(user["location_id"])

		distance = sqrt(pow((city["x"]-cur_city["x"]), 2) + pow((city["y"]-cur_city["y"]), 2))
		sent_message = await call.message.answer("идем...")
		print("City ", data, city, cur_city, distance)
		await asyncio.sleep(distance)

		await bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)

		user["location_id"] = ObjectId(city["_id"])
		user["state"] = "NEW CITY"
		db.update_user(user)
	elif call.data[0:3] == "BUY":
		data = call.data[4:]
		item = await db.get_item_by_name(data)
		my_items = db.get_my_items(user["user_id"])
		print("DATA ", data, my_items)

		check = True

		if item["item_type"] != "зелье":
			for my_item_id, my_item_count in my_items.items():
				item_data = db.get_item(my_item_id)
				if my_item_count > 0:
					if my_item_id != str(item["_id"]):
						check = False

		print("RESULT", check)
		if not check:
			await call.message.answer("Вы уже купили другое оружие!")
		else:
			if item["cost"] > user["money"]:
				await call.message.answer("У вас нету денег!")
			else:
				await call.message.answer("Купили!")
				user["money"] -= item["cost"]

				if str(item["_id"]) not in user["items"].keys():
					user["items"][str(item["_id"])] = 1
				else:
					user["items"][str(item["_id"])] += 1

				print(user)

				db.update_user(user)
	elif call.data[0:3] == "SEL":
		data = call.data[4:]
		item = await db.get_item_by_name(data)
		my_items = db.get_my_items(user["user_id"])
		print("DATA ", data, my_items)

		if my_items[str(item["_id"])] == 0:
			await call.message.answer("Он и так уже продан!")
		else:
			user["items"][str(item["_id"])] -= 1
			user["money"] += item["cost_to_sale"]

			print(user)

			db.update_user(user)

			await call.message.answer("Продали!")

	await go_next(call.from_user.id, call.message)


if __name__ == '__main__':
	try:
		executor.start_polling(dp, skip_updates=True)
	except Exception as exc:
		logging.error(exc)
		os._exit(0)
