#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from typing import Union
import tkinter as tk
import random, string
import Data

def random_id(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

class StatusHP:
    def __init__(self):
        self.value = 1
        self.basestatus = 0
        self.individual = 31
        self.effort = 0

    def reset(self):
        self.value = 1
        self.basestatus = 0
        self.individual = 31
        self.effort = 0

    def generate(self, basestatus: int):
        self.basestatus = int(basestatus)
        self._status_calculation(50)

    def _status_calculation(self, level: int=50):
        base = self.basestatus * 2 + self.individual
        effort = math.floor(self.effort / 4)
        if self.basestatus:
            self.value = math.floor(math.floor((base + effort) * level / 100) + level + 10)
        else:
            self.value = 1

    def status_update(self, effort: int=0, individual: int=31, level: int=50):
        self.effort = effort
        self.individual = individual
        self._status_calculation(level)

    def print(self):
        print(f"value:{self.value}\tbase:{self.basestatus}\tindividual{self.individual}\teffort{self.effort}")

class Status(StatusHP):
    def __init__(self):
        super().__init__()
        self.nature = 1

    def reset(self):
        super().reset()
        self.nature = 1

    def _status_calculation(self, level: int=50):
        base = self.basestatus * 2 + self.individual
        effort = math.floor(self.effort / 4)
        if self.basestatus:
            self.value = math.floor(math.floor(math.floor(math.floor(math.floor(base + effort)*level) / 100) + 5) *self.nature)
        else:
            self.value = 1

    def status_update(self, effort: int=0, individual: int=31, nature: float=1.0, level: int=50):
        self.effort = effort
        self.individual = individual
        self.nature = nature
        self._status_calculation(level)

    def print(self):
        print(f"value:{self.value}\tbase:{self.basestatus}\tindividual{self.individual}\teffort{self.effort}\tnature:{self.nature}")

class StatusHPDetail(StatusHP):
    def __init__(self):
        super().__init__()
        self.value_now = 1

    def generate(self, basestatus: int):
        self.basestatus = int(basestatus)
        self._status_calculation(50)
        self.value_now = self.value

    def _status_calculation(self, level: int=50) -> int:
        base = self.basestatus * 2 + self.individual
        effort = math.floor(self.effort / 4)
        if self.basestatus:
            self.value = math.floor(math.floor((base + effort) * level / 100) + level + 10)
        else:
            self.value = 1
        self.value_now = self.value

    def set_now(self, value: int):
        if value < 1:
            value = 1
        self.value_now = value

    def print(self):
        print(f"value:{self.value}\tbase:{self.basestatus}\tindividual{self.individual}\teffort{self.effort}\tnow:{self.value_now}")

class Poke:
    def __init__(self,):
        self.status_list: "list[Union[StatusHP, Status]]" = [StatusHP()] + [Status() for _ in range(5)]
        self.ability_list: "list[str]" = []
        self.name: str = ""
        self.ability: str = ""
        self.item: str = ""
        self.terastal: str = ""
        self.level: int = 50
        self.move_list: "list[str]" = ["", "", "", ""]
        self.dic: dict[str, tk.Variable | "list[tk.Variable]"] = {}

    def set_dic(self, key, value):
        self.dic[key] = value

    def generate(self, name: str=""):
        self.name = name
        if self.name:
            data = Data.POKEDATA.find(self.name, "name")
            [status.generate(data[5: 11][index]) for index, status in enumerate(self.status_list)]
            self.ability_list = [Data for Data in data[11: 14] if Data]
            if "そうだいしょう" in self.ability_list:
                add_list = [f"そうだいしょう+{i+1}" for i in range(5)]
                self.ability_list = self.ability_list + add_list
        else:
            [status.reset() for status in self.status_list]
        self.ability = ""
        self.item = ""
        self.terastal = ""
        self.level = 50
        self.move_list = ["", "", "", ""]

    def update(self):
        self.level = self.dic["level"].get() if "level" in self.dic else 50
        self.item = self.dic["item"].get() if "item" in self.dic else ""
        self.ability = self.dic["ability"].get() if "ability" in self.dic else ""
        self.terastal = self.dic["terastal"].get() if "terastal" in self.dic else ""
        self.move_list = []
        for i in range(4):
            if  "move" in self.dic:
                self.move_list.append(self.dic["move"][i].get())
            else:
                self.move_list.append("")
        for i in range(6):
            if i == 0:
                self.status_list[i].status_update(
                    self.dic["effort"][i].get(),
                    self.dic["individual"][i].get(),
                    self.level
                )
            else:
                self.status_list[i].status_update(
                    self.dic["effort"][i].get(),
                    self.dic["individual"][i].get(),
                    self.dic["nature"][i-1].get(),
                    self.level
                )

    def find_any_stats(self, stats_index: int, individual: int, effort: int, nature: float=1):
        copy_individual = self.status_list[stats_index].individual
        copy_effort = self.status_list[stats_index].effort
        if stats_index != 0:
            copy_nature = self.status_list[stats_index].nature
            [stat.status_update(effort, individual, nature, self.level) for stat in self.status_list]
        else:
            [stat.status_update(effort, individual, self.level) for stat in self.status_list]
        value = self.status_list[stats_index].value
        if stats_index != 0:
            copy_nature = self.status_list[stats_index].nature
            [stat.status_update(copy_effort, copy_individual, copy_nature, self.level) for stat in self.status_list]
        else:
            [stat.status_update(copy_effort, copy_individual, self.level) for stat in self.status_list]
        return value

class PokeDetail(Poke):
    def __init__(self):
        super().__init__()
        self.id = random_id(10)
        self.terastal_flag: bool = False
        self.rank_list: "list[str]" = ["", "", "", "", ""]
        self.bad_stat: str = ""
        self.move_flag: bool = False
        self.ability_flag: bool = False
        self.hp_now: int = 1
        self.hp_result: int = 0

    def generate(self, name: str = ""):
        super().generate(name)
        self.hp_now = self.status_list[0].value
        self.hp_result = 0

    def re_init(self, data: Data.PokeData=None):
        """
        バナーセット時や手持ちのリセット時
        """
        super().__init__()
        if data:
            self.generate(data.name)
            self.item = data.item
            self.terastal = data.terastal
            self.ability = data.ability
            self.move_list = data.move_list.copy()

    def reset(self):
        self.re_init()

    def update(self):
        super().update()
        self.rank_list = []
        for i in range(5):
            if "rank" in self.dic:
                self.rank_list.append(self.dic["rank"][i].get())
            else:
                self.rank_list.append("")
        self.terastal_flag = self.dic["terastal_flag"].get() if "terastal_flag" in self.dic else False
        self.move_flag = self.dic["move_flag"].get() if "move_flag" in self.dic else False
        self.bad_stat = self.dic["bad_stat"].get() if "bad_stat" in self.dic else ""
        self.ability_flag = self.dic["ability_flag"].get() if "ability_flag" in self.dic else False

    def copy(self):
        dic ={
            "id": self.id,
            "name": self.name,
            "item": self.item,
            "terastal": self.terastal,
            "ability": self.ability,
            "level": self.level,
            "individual": [stat.individual for stat in self.status_list],
            "effort": [stat.effort for stat in self.status_list],
            "nature": [stat.nature for stat in self.status_list[1:]],
            "move": [move for move in self.move_list],
            "rank": [rank for rank in self.rank_list],
            "terastal_flag": self.terastal_flag,
            "ability_flag": self.ability_flag,
            "move_flag": self.move_flag,
            "bad_stat": self.bad_stat,
            "hp_now": self.hp_now,
            "hp_result": self.hp_result
        }
        return dic

    def paste(self, dic: dict):
        self.id = dic["id"]
        super().generate(dic["name"])
        self.item = dic["item"]
        self.terastal = dic["terastal"]
        self.ability = dic["ability"]
        self.level = dic["level"]
        for index, stat in enumerate(self.status_list):
            if index == 0:
                stat.status_update(dic["effort"][index], dic["individual"][index], self.level)
            else:
                stat.status_update(dic["effort"][index], dic["individual"][index], dic["nature"][index-1], self.level)
        self.move_list = dic["move"]
        self.rank_list = dic["rank"]
        self.terastal_flag = dic["terastal_flag"]
        self.ability_flag = dic["ability_flag"]
        self.move_flag = dic["move_flag"]
        self.bad_stat = dic["bad_stat"]
        self.hp_now = dic["hp_now"]
        self.hp_result = dic["hp_result"]

    def print(self):
        print("-------------------------PokeDetail.Object-------------------------")
        print(f"name:{self.name}\titem:{self.item}\tability:{self.ability}\tterastal:{self.terastal}")
        print(f"h:{self.status_list[0].value}\ta:{self.status_list[1].value}\tb:{self.status_list[2].value}\tc:{self.status_list[3].value}\td:{self.status_list[4].value}\ts:{self.status_list[5].value}")
        print(f"rank_a:{self.rank_list[0]}\trank_b:{self.rank_list[1]}\trank_c:{self.rank_list[2]}\trank_d:{self.rank_list[3]}\trank_s:{self.rank_list[4]}")
        print(f"ability_flag:{self.ability_flag}\tterastal_flag:{self.terastal_flag}\tbad_stat:{self.bad_stat}\tmove_flag:{self.move_flag}")
        print(f"")

class PlayerField:
    def __init__(self):
        self.a_wall: bool = False
        self.c_wall: bool = False
        self.wind: bool = False
        self.help: bool = False
        self.crit: bool = False

    def config(self,
            a_wall_variable: tk.BooleanVar,
            c_wall_variable: tk.BooleanVar,
            wind_variable: tk.BooleanVar,
            help_variable: tk.BooleanVar,
            crit_variable: tk.BooleanVar
        ):
        self.a_wall_variable = a_wall_variable
        self.c_wall_variable = c_wall_variable
        self.wind_variable = wind_variable
        self.help_variable = help_variable
        self.crit_variable = crit_variable

    def update(self):
        self.a_wall = self.a_wall_variable.get()
        self.c_wall = self.c_wall_variable.get()
        self.wind = self.wind_variable.get()
        self.help = self.help_variable.get()
        self.crit = self.crit_variable.get()

class Field:
    def __init__(self):
        self.double: bool = False
        self.field: str = ""
        self.weather: str = ""
        self.ability_1: str = ""
        self.ability_2: str = ""

    def config(
            self,
            double_variable: tk.BooleanVar,
            field_variable: tk.StringVar,
            weather_variable: tk.StringVar,
            ability_1_variable: tk.StringVar,
            ability_2_variable: tk.StringVar
    ):
        self.double_variable = double_variable
        self.field_variable = field_variable
        self.weather_variable = weather_variable
        self.ability_1_variable = ability_1_variable
        self.ability_2_variable = ability_2_variable

    def reset(self):
        self.__init__()

    def update(self):
        self.double = self.double_variable.get()
        self.field = self.field_variable.get()
        self.weather = self.weather_variable.get()
        self.ability_1 = self.ability_1_variable.get()
        self.ability_2 = self.ability_2_variable.get()

    def print(self):
        print("-------------------------Field.Object-------------------------")
        print(f"double: {self.double}\tfield: {self.field}\tweather: {self.weather}\t")
        print(f"ability_1: {self.ability_1}\tability_2: {self.ability_2}")

from typing import Dict, List
class PokeDict:
    def __init__(self):
        self.dic: Dict[str, Dict[str, List[int, PokeDetail]]] = {
            tk.LEFT: {},
            tk.RIGHT: {}
        }

    def access(self, side: Union[tk.LEFT, tk.RIGHT], move_index: int, poke: PokeDetail) -> bool:
        if poke["id"] in self.dic[side].keys():
            if move_index in self.dic[side][poke["id"]]:
                self.dic[side][poke["id"]].remove(move_index)
                if len(self.dic[side][poke["id"]]) == 1:
                    del self.dic[side][poke["id"]]
                return False
            else:
                self.dic[side][poke["id"]].append(move_index)
                return True
        else:
            self.dic[side][poke["id"]] = [poke, move_index]
            return True

    def move_index_check(self, side: Union[tk.LEFT, tk.RIGHT], key: str) -> "list[int]":
        result = []
        for dic_key in self.dic[side].keys():
            if key in dic_key:
                result = [res for res in self.dic[side][key][1:]]
        return result

    def key_check(self, side: str, key:str) -> bool:
        for dic_key in self.dic[side].keys():
            if key in dic_key:
                return True
        return False