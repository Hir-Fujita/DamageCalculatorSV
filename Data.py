#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Union
import pickle
import csv
import configparser
import os
from tkinter import filedialog

FOLDER = f"{os.getcwd()}\DamageCalculatorSV"

def open_file(path):
    with open(path, "rb") as f:
        data = pickle.load(f)
    return data

def save_file(path, data):
    with open(path, "wb") as f:
        pickle.dump(data, f)

def save_filedialogwindow(save_name: str, title: str, parent_folder: str, filetypes: "tuple[str, str]") -> str:
    save_folder = f"{FOLDER}/Data/{parent_folder}/"
    filepath = filedialog.asksaveasfilename(
        title=title,
        initialfile=save_name,
        defaultextension=f".txt",
        filetypes=[filetypes],
        initialdir=save_folder
    )
    return filepath

def open_filedialogwindow(title: str, parent_folder: str, filetypes: "tuple[str, str]") -> str:
    load_folder = f"{FOLDER}/Data/{parent_folder}"
    filepath = filedialog.askopenfilename(
        title=title,
        multiple=False,
        initialdir=load_folder,
        filetypes=[filetypes]
    )
    return filepath


class Setting:
    def __init__(self, path: str):
        self.setting_ini = configparser.ConfigParser()
        self.setting_ini.read(path, encoding="utf-8")
        self.setting = self.setting_ini["USER_SETTING"]

class Text:
    def __init__(self, path: str):
        with open(path, "r", encoding="UTF-8") as f:
            datalist = f.readlines()
            self.data = [row.replace("\n", "") for row in datalist]

    def poke_item(self):
        data = [tuple(d.split(":")) for d in self.data]
        return data

class PokeData:
    '''
    テキストファイルから読み込んで、ポケモンのデータを管理する
    '''
    def __init__(self, path: Union[str, "list[str]"]):
        if isinstance(path, list):
            data = path
        else:
            with open(path, "r", encoding="utf-8") as f:
                data = f.readlines()
            data = [d.replace("\n", "") for d in data]
        self.name: str = data[0]
        self.level: int = int(data[1])
        self.item: str  = data[2]
        self.ability: str = data[3]
        self.terastal: str = data[4]
        self.move_list: "list[str]" = data[5].split("/")
        status = data[6:12]
        self.status = []
        for index, s in enumerate(status):
            stat = s.split("/")
            if index == 0:
                self.status.append((int(stat[0]), int(stat[1])))
            else:
                self.status.append((int(stat[0]), int(stat[1]), float(stat[2])))
        self.memo = [d for d in data[12:] if d != ""]

    def save(self):
        data = [self.name, self.level, self.item, self.ability, self.terastal, "/".join(self.move_list)]
        for s in self.status:
            s = list(map(str, s))
        [data.append("/".join(list(map(str, s)))) for s in self.status]
        return data + self.memo

class CSV:
    def __init__(self, path: str):
        self.kana = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもらりるれろやゆよわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽゔぁぃぅぇぉゃゅょっｎー"
        self.kata = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモラリルレロヤユヨワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポヴァィゥェォャュョッンー"
        with open(path, encoding="utf-8") as f:
            reader = csv.reader(f)
            self.data = [row for row in reader]
        self.key = self.data.pop(0)
        self.name_list = [data[self.key_index("name")] for data in self.data]
        self.name_list_plus = [data for data in self.data if not "+" in data]
        if "kata" in self.key:
            self.kata_list = [data[self.key_index("kata")] for data in self.data]

    def key_index(self, key: str):
        return self.key.index(key)

    def find(self, value: str, key: str, return_key: str="") -> str:
        if not value:
            return "0"
        else:
            value_list = [data[self.key_index(key)] for data in self.data]
            index = value_list.index(value)
            data = self.data[index]
            if return_key:
                data = data[self.key_index(return_key)]
            return data

    def autocomplete(self, text: str) -> "list[str]":
        if not text:
            return self.name_list
        else:
            result = [self.kata[self.kana.index(t)] if t in self.kana else t for t in text]
            result = "".join(result)
            if "kata" in self.key:
                results = [self.name_list[index] for index, name in enumerate(self.kata_list) if result in name]
            else:
                results = [name for name in self.name_list if result in name]
            return results

class Type:
    def __init__(self, path: str):
        self.dic = {
            "ノーマル": 0,
            "ほのお": 1,
            "みず": 2,
            "でんき": 3,
            "くさ": 4,
            "こおり": 5,
            "かくとう": 6,
            "どく": 7,
            "じめん": 8,
            "ひこう": 9,
            "エスパー": 10,
            "むし": 11,
            "いわ": 12,
            "ゴースト": 13,
            "ドラゴン": 14,
            "あく": 15,
            "はがね": 16,
            "フェアリー": 17
        }
        self.list = list(self.dic.keys())
        self.dic["Color"] = 18
        with open(path, encoding="utf-8") as f:
            reader = csv.reader(f)
            self.data = [row for row in reader]

    def index(self, key: str) -> int:
        return self.dic[key]

    def calc(self, attack: str, target: str) -> float:
        return float(self.data[self.index(attack)][self.index(target)])

    def typecolor(self, type: str) -> str:
        return self.data[self.index(type)][self.index("Color")]

POKEDATA = CSV(f"{FOLDER}/Data/PokeData.csv")
MOVEDATA = CSV(f"{FOLDER}/Data/MoveData.csv")
ITEMDATA = CSV(f"{FOLDER}/Data/ItemData.csv")
ITEM_POKE = Text(f"{FOLDER}/Data/AutoItem.txt").poke_item()
TYPEDATA = Type(f"{FOLDER}/Data/TypeData.csv")
LABEL = ["HP", "攻撃", "防御", "特攻", "特防", "素早"]
FIELD = ["", "エレキフィールド", "グラスフィールド", "サイコフィールド", "ミストフィールド"]
WEATHER = ["", "にほんばれ", "あめ", "すなあらし", "ゆき"]
BADSTAT = ["", "まひ", "やけど", "どく", "もうどく", "こおり", "ねむり", "ひんし", "じゅうでん"]
ABIILITY = ["", "わざわいのうつわ", "わざわいのつるぎ", "わざわいのおふだ", "わざわいのたま", "フレンドガード", "パワースポット", "バッテリー", "はがねのせいしん"]
