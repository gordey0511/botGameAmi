class Person:
    def __init__(self, user_id, nickname, level=1, hp=100, cur_hp=100, money=0,
                 attack=10, magic_attack=10, xp=0, armour=0, magic_armour=0, location_id=1):
        self.user_id = user_id
        self.nickname = nickname
        self.level = level
        self.hp = hp
        self.cur_hp = cur_hp
        self.money = money
        self.attack = attack
        self.magic_attack = magic_attack
        self.xp = xp
        self.armour = armour
        self.magic_armour = magic_armour
        self.location_id = location_id

    def __str__(self):
        return (f"UserID: {self.user_id}, Nickname: {self.nickname}, Level: {self.level}, "
                f"HP: {self.hp}, CurHP: {self.cur_hp}, Money: {self.money}, "
                f"Attack: {self.attack}, Magic Attack: {self.magic_attack}, XP: {self.xp}, "
                f"Armour: {self.armour}, Magic Armour: {self.magic_armour}, LocationID: {self.location_id}")

class Mob:
    def __init__(self, mob_id, hp, xp, req_level, attack_type, attack, armour, magic_armour):
        self.mob_id = mob_id
        self.hp = hp
        self.xp = xp
        self.req_level = req_level
        self.attack_type = attack_type
        self.attack = attack
        self.armour = armour
        self.magic_armour = magic_armour

    def __str__(self):
        return (f"MobID: {self.mob_id}, HP: {self.hp}, XP: {self.xp}, "
                f"ReqLevel: {self.req_level}, AttackType: {self.attack_type}, "
                f"Attack: {self.attack}, Armour: {self.armour}, "
                f"Magic Armour: {self.magic_armour}")

class Location:
    def __init__(self, location_id, x_coord, y_coord, location_type):
        self.location_id = location_id
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.location_type = location_type

    def __str__(self):
        return (f"LocationID: {self.location_id}, XCoord: {self.x_coord}, "
                f"YCoord: {self.y_coord}, LocationType: {self.location_type}")


class Item:
    def __init__(self, item_id, cost, cost_to_sale, item_type, hp=0, mana=0,
                 attack=0, magic_attack=0, armour=0, magic_armour=0, req_level=1):
        self.item_id = item_id
        self.cost = cost
        self.cost_to_sale = cost_to_sale
        self.item_type = item_type
        self.hp = hp
        self.mana = mana
        self.attack = attack
        self.magic_attack = magic_attack
        self.armour = armour
        self.magic_armour = magic_armour
        self.req_level = req_level

    def __str__(self):
        return (f"ItemID: {self.item_id}, Cost: {self.cost}, CostToSale: {self.cost_to_sale}, "
                f"ItemType: {self.item_type}, HP: {self.hp}, Mana: {self.mana}, "
                f"Attack: {self.attack}, Magic Attack: {self.magic_attack}, "
                f"Armour: {self.armour}, Magic Armour: {self.magic_armour}, ReqLevel: {self.req_level}")
