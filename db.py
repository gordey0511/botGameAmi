import random
import datetime
from os import environ
from sys import stderr

import certifi
import pymongo as pymongo
from bson import ObjectId

# TOKEN = environ["TOKEN"][:-1].strip()  # '5791033550:AAF_2TRXtRpZa1MqG7g-53pJTQItZVLbY3c'
TOKEN = "6681679120:AAE9X_jHYVzv4t0n7MbZwVIt6qZE5Isp3Ps"
print(TOKEN, file=stderr)
client = pymongo.MongoClient(
	"mongodb+srv://gordeyzav2:AKlviZsGe4UNFYpY@cluster0.yy1upho.mongodb.net/?retryWrites=true&w=majority",
	tlsCAFile=certifi.where())
database = client["Database"]
users = database["users"]
items = database["items"]
mobs = database["mobs"]
cities = database["locations"]

def insert_user(user):
	users.insert_one(user)


def find_user(user_id: int):
	user = users.find_one({"user_id": user_id})
	# user = users.find_one({"tid": tid, "bot_id": bot_id})
	if user is None:
		user = {
			"user_id": user_id,
			"nickname": "Gordey",
			"level": 1,
			"HP": 100,
			"curHP": 100,
			"money": 0,
			"attack": 10,
			"magic_attack": 20,
			"XP":0,
			"armour": 10,
			"magic_armour": 20,
			"location_id": ObjectId("65848ab776c5a2997d5528ce"),
			"state": "CITY",
		}
		insert_user(user)
	return user

def update_user(user):
	users.update_one({"user_id": user["user_id"]}, {"$set": user})


def get_random_mob():
	random_document = mobs.aggregate([{"$sample": {"size": 1}}])

	document = None
	for doc in random_document:
		document = doc

	return document

def get_profile(user_id: int):
	user = users.find_one({"user_id": user_id})

	return user


def get_cities():
	res_cities = cities.find()

	return res_cities


async def get_city_by_name(name):
	city = cities.find_one({"name": name})

	return city


def get_cur_city(city):
	city = cities.find_one(city)

	return city



