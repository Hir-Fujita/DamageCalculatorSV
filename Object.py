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
        self.value: tk.IntVar = tk.IntVar(value=1)
        self.basestatus: tk.IntVar = tk.IntVar(value=0)
        self.individual: tk.IntVar = tk.IntVar(value=31)
        self.effort: tk.IntVar = tk.IntVar(value=0)

    def reset(self):
        self.value.set(1)
        self.basestatus.set(0)
        self.individual.set(31)
        self.effort.set(0)

    def generate(self, basestatus: int):
        self.reset()
        self.basestatus.set(basestatus)
        self._status_calculation(50)

    def _status_calculation(self, level: int=50):
        base = self.basestatus.get() * 2 + self.individual.get()
        effort = math.floor(self.effort.get() / 4)
        if self.basestatus.get():
            self.value.set(math.floor(math.floor((base + effort) * level / 100) + level + 10))
        else:
            self.value.set(1)

    def status_update(self, level: int=50):
        self._status_calculation(level)

    def print(self):
        print(f"value:{self.value}\tbase:{self.basestatus}\tindividual{self.individual}\teffort{self.effort}")

class Status(StatusHP):
    def __init__(self):
        super().__init__()
        self.nature: tk.DoubleVar = tk.DoubleVar(value=1.0)

    def reset(self):
        super().reset()
        self.nature.set(1.0)

    def _status_calculation(self, level: int=50):
        base = self.basestatus.get() * 2 + self.individual.get()
        effort = math.floor(self.effort.get() / 4)
        if self.basestatus.get():
            self.value.set(math.floor(math.floor(math.floor(math.floor(math.floor(base + effort)*level) / 100) + 5) *self.nature.get()))
        else:
            self.value.set(1)

    def status_update(self, level: int=50):
        self._status_calculation(level)

    def print(self):
        print(f"value:{self.value}\tbase:{self.basestatus}\tindividual{self.individual}\teffort{self.effort}\tnature:{self.nature}")

class Poke:
    def __init__(self):
        self.status_list: "list[Union[StatusHP, Status]]" = [StatusHP()] + [Status() for _ in range(5)]
        self.ability_list: "list[str]" = []
        self.name: tk.StringVar = tk.StringVar(value="")
        self.ability: tk.StringVar = tk.StringVar(value="")
        self.item: tk.StringVar = tk.StringVar(value="")
        self.terastal: tk.StringVar = tk.StringVar(value="")
        self.level: tk.IntVar = tk.IntVar(value=50)
        self.move_list: "list[tk.StringVar]" = [tk.StringVar(value="") for i in range(4)]

    def reset(self):
        [status.reset() for status in self.status_list]
        self.ability_list = []
        self.name.set("")
        self.ability.set("")
        self.item.set("")
        self.terastal.set("")
        self.level.set(0)
        [move.set("") for move in self.move_list]

    def generate(self):
        if self.name.get():
            data = Data.POKEDATA.find(self.name.get(), "name")
            [status.generate(data[5: 11][index]) for index, status in enumerate(self.status_list)]
            self.ability_list = [Data for Data in data[11: 14] if Data]
        else:
            [status.reset() for status in self.status_list]
        self.ability.set("")
        self.item.set("")
        self.terastal.set("")
        self.level.set(50)
        [move.set("") for move in self.move_list]

    def save(self) -> list[str]:
        save_data = [self.name.get(), self.level.get(), self.item.get(), self.ability.get(), self.terastal.get()]
        save_data.append("/".join([move.get() for move in self.move_list]))
        for index, status in enumerate(self.status_list):
            if index == 0:
                save_data.append(f"{str(status.individual.get())}/{str(status.effort.get())}")
            else:
                save_data.append(f"{str(status.individual.get())}/{str(status.effort.get())}/{str(status.nature.get())}")
        return save_data

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
        self.terastal_flag: tk.BooleanVar = tk.BooleanVar(value=False)
        self.rank_list: "list[tk.StringVar]" = [tk.StringVar(value="") for i in range(5)]
        self.bad_stat: tk.StringVar = tk.StringVar(value="")
        self.move_flag: tk.BooleanVar = tk.BooleanVar(value=False)
        self.ability_flag: tk.BooleanVar = tk.BooleanVar(value=False)
        self.hp_now: tk.IntVar = tk.IntVar(value=1)
        self.hp_result: tk.IntVar = tk.IntVar(value=0)
        self.memo: str = ""
        self.calc_list: list[tk.BooleanVar] = [tk.BooleanVar(value=False) for i in range(4)]
        self.pp_list: list[tk.IntVar] = [tk.IntVar(value=0) for i in range(4)]

    def get(self):
        data = SendData().get_poke(self)
        return data

    def load(self, data: Data.PokeData):
        self.name.set(data.name)
        self.generate()
        self.ability.set(data.ability)
        self.item.set(data.item)
        self.terastal.set(data.terastal)
        self.level.set(data.level)
        self.memo = "\n".join(data.memo)
        [move.set(data.move_list[index]) for index, move in enumerate(self.move_list)]
        for index, stat in enumerate(self.status_list):
            stat.individual.set(data.status[index][0])
            stat.effort.set(data.status[index][1])
            if index != 0:
                stat.nature.set(data.status[index][2])
            stat.status_update(data.level)
        self.hp_now.set(self.status_list[0].value.get())
        self.pp_set()

    def save(self) -> list[str]:
        save_data = super().save()
        [save_data.append(m) for m in self.memo.split("\n")]
        return save_data

    def generate(self):
        super().generate()
        if "そうだいしょう" in self.ability_list:
            add_list = [f"そうだいしょう+{i+1}" for i in range(5)]
            self.ability_list = self.ability_list + add_list
        self.hp_now.set(self.status_list[0].value.get())

    def re_generate(self):
        data = Data.POKEDATA.find(self.name.get(), "name")
        [status.basestatus.set((data[5: 11][index])) for index, status in enumerate(self.status_list)]
        [status.status_update() for status in self.status_list]
        self.hp_now.set(self.status_list[0].value.get())
        self.ability_list = [Data for Data in data[11: 14] if Data]

    def reset(self):
        super().reset()
        self.terastal_flag.set(value=False)
        [rank.set("") for rank in self.rank_list]
        self.bad_stat.set(value="")
        self.move_flag.set(value=False)
        self.ability_flag.set(value=False)
        self.hp_now.set(value=1)
        self.hp_result.set(value=0)
        self.memo = ""
        [lock.set(False) for lock in self.calc_list]
        [pp.set(0) for pp in self.pp_list]

    def pp_set(self):
        for i in range(4):
            pp = int(Data.MOVEDATA.find(self.move_list[i].get(), "name", "pp"))
            self.pp_list[i].set(int(pp + (pp * 0.6)))

    def copy(self):
        dic ={
            "id": self.id,
            "name": self.name.get(),
            "item": self.item.get(),
            "terastal": self.terastal.get(),
            "ability": self.ability.get(),
            "level": self.level.get(),
            "individual": [stat.individual.get() for stat in self.status_list],
            "effort": [stat.effort.get() for stat in self.status_list],
            "nature": [stat.nature.get() for stat in self.status_list[1:]],
            "move": [move.get() for move in self.move_list],
            "rank": [rank.get() for rank in self.rank_list],
            "terastal_flag": self.terastal_flag.get(),
            "ability_flag": self.ability_flag.get(),
            "move_flag": self.move_flag.get(),
            "bad_stat": self.bad_stat.get(),
            "hp_now": self.hp_now.get(),
            "hp_result": self.hp_result.get(),
            "lock": [lock.get() for lock in self.calc_list],
            "pp": [pp.get() for pp in self.pp_list]
        }
        return dic

    def paste(self, dic: dict):
        self.id = dic["id"]
        self.name.set(dic["name"])
        super().generate()
        self.item.set(dic["item"])
        self.terastal.set(dic["terastal"])
        self.ability.set(dic["ability"])
        self.level.set(dic["level"])
        for index, stat in enumerate(self.status_list):
            stat.effort.set(dic["effort"][index])
            stat.individual.set(dic["individual"][index])
            if isinstance(stat, Status):
                stat.nature.set(dic["nature"][index-1])
            stat.status_update(self.level.get())
        [move.set(dic["move"][index]) for index, move in enumerate(self.move_list)]
        [rank.set(dic["rank"][index]) for index, rank in enumerate(self.rank_list)]
        self.terastal_flag.set(dic["terastal_flag"])
        self.ability_flag.set(dic["ability_flag"])
        self.move_flag.set(dic["move_flag"])
        self.bad_stat.set(dic["bad_stat"])
        self.hp_now.set(dic["hp_now"])
        self.hp_result.set(dic["hp_result"])
        [lock.set(dic["lock"][index]) for index, lock in enumerate(self.calc_list)]
        [pp.set(dic["pp"][index]) for index, pp in enumerate(self.pp_list)]

    def print(self):
        print("-------------------------PokeDetail.Object-------------------------")
        print(f"name:{self.name.get()}\titem:{self.item.get()}\tability:{self.ability.get()}\tterastal:{self.terastal.get()}")
        print(f"move_1:{self.move_list[0].get()}\tmove_2:{self.move_list[1].get()}\tmove_3:{self.move_list[2].get()}\tmove_4:{self.move_list[3].get()}\t")
        print(f"h:{self.status_list[0].value}\ta:{self.status_list[1].value}\tb:{self.status_list[2].value}\tc:{self.status_list[3].value}\td:{self.status_list[4].value}\ts:{self.status_list[5].value}")
        print(f"rank_a:{self.rank_list[0]}\trank_b:{self.rank_list[1]}\trank_c:{self.rank_list[2]}\trank_d:{self.rank_list[3]}\trank_s:{self.rank_list[4]}")
        print(f"ability_flag:{self.ability_flag}\tterastal_flag:{self.terastal_flag}\tbad_stat:{self.bad_stat}\tmove_flag:{self.move_flag}")
        print(f"")

    def craete_any_stat(self, max: bool=False):
        poke = PokeDetail()
        poke.paste(self.copy())
        for status in poke.status_list:
            status.individual.set(31)
            status.effort.set(252 if max else 0)
            if isinstance(status, Status):
                status.nature.set(1.1 if max else 1.0)
            status.status_update()
        return poke



class PlayerField:
    def __init__(self):
        self.a_wall: tk.BooleanVar = tk.BooleanVar(value=False)
        self.c_wall: tk.BooleanVar = tk.BooleanVar(value=False)
        self.wind: tk.BooleanVar = tk.BooleanVar(value=False)
        self.help: tk.BooleanVar = tk.BooleanVar(value=False)
        self.crit: tk.BooleanVar = tk.BooleanVar(value=False)

    def get(self):
        return SendData().get_player(self)

class Field:
    def __init__(self):
        self.double: tk.BooleanVar = tk.BooleanVar(value=False)
        self.field: tk.StringVar = tk.StringVar(value="")
        self.weather: tk.StringVar = tk.StringVar(value="")
        self.ability_1: tk.StringVar = tk.StringVar(value="")
        self.ability_2: tk.StringVar = tk.StringVar(value="")
        self.gravity: tk.BooleanVar = tk.BooleanVar(value=False)
        self.magic_room: tk.BooleanVar = tk.BooleanVar(value=False)
        self.wonder_room: tk.BooleanVar = tk.BooleanVar(value=False)

    def get(self):
        return SendData().get_field(self)


class SendData:
    def get_poke(cls, poke: PokeDetail):
        cls.name = poke.name.get()
        cls.item = poke.item.get()
        cls.terastal = poke.terastal.get()
        cls.ability = poke.ability.get()
        cls.level = poke.level.get()
        cls.status = [stat.value.get() for stat in poke.status_list]
        cls.rank = [rank.get() for rank in poke.rank_list]
        cls.move_list = [move.get() for move in poke.move_list]
        cls.terastal_flag = poke.terastal_flag.get()
        cls.ability_flag = poke.ability_flag.get()
        cls.move_flag = poke.move_flag.get()
        cls.bad_stat = poke.bad_stat.get()
        cls.hp_now = poke.hp_now.get()
        return cls

    def get_player(cls, player: PlayerField):
        cls.a_wall = player.a_wall.get()
        cls.c_wall = player.c_wall.get()
        cls.wind = player.wind.get()
        cls.help = player.help.get()
        cls.crit = player.crit.get()
        return cls

    def get_field(cls, field: Field):
        cls.double = field.double.get()
        cls.field = field.field.get()
        cls.weather = field.weather.get()
        cls.ability_1 = field.ability_1.get()
        cls.ability_2 = field.ability_2.get()
        cls.gravity = field.gravity.get()
        cls.magic_room = field.magic_room.get()
        cls.wonder_room = field.wonder_room.get()
        return cls

class PokeDict:
    def __init__(self):
        self.dic: dict[str, dict[str, list[int, PokeDetail]]] = {
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
