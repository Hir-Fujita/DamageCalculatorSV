#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Callable

import tkinter as tk
import Object as Obj
import Widget as Wid
import Process as Pr
import Data


class Manager:
    def __init__(self, master):
        self.master = master
        self.image_flag = True
        self.party = PartyManager("left")
        self.enemy = PartyManager("right")

class PartyManager:
    def __init__(self, side: str):
        self.list = [Obj.PokeDetail() for i in range(6)]
        self.back_up = [Obj.PokeDetail() for i in range(6)]
        self.menu = tk.Menu(None, tearoff=0)
        [self.menu.add_command(label=i) for i in range(6)]
        self.widget = Wid.ButtlePartyWidget(side, self.list, self.menu_update)

    def menu_update(self):
        for i in range(6):
            self.menu.entryconfig(i, label=self.list[i].name.get())

    def update(self, main_poke: Obj.PokeDetail=None):
        if main_poke is not None:
            for index, poke in enumerate(self.list):
                if poke.id == main_poke.id:
                    poke.paste(main_poke.copy())
                    self.widget.update(index)
                    break
        else:
            self.widget.update()

    def create_backup(self, index: int=None):
        if index is None:
            for i in range(6):
                self.back_up[i].paste(self.list[i].copy())
        else:
            self.back_up[index].paste(self.list[index].copy())
        self.update()

class PokeWidgetManager:
    def __init__(self, poke: Obj.Poke | Obj.PokeDetail):
        self.poke: Obj.Poke | Obj.PokeDetail = poke
        self.name_widget = Wid.CustomCommboBox(self.poke.name, Data.POKEDATA, self.name_widget_func)
        self.level_widget = Wid.CustomLevelBox(self.poke.level, self.status_update)
        self.ability_widget = Wid.CustomCommboBox(self.poke.ability)
        self.item_widget = Wid.CustomCommboBox(self.poke.item, Data.ITEMDATA)
        self.terastal_widget = Wid.CustomCommboBox(self.poke.terastal, Data.TYPEDATA.list)
        self.move_widgets = [Wid.CustomCommboBox(self.poke.move_list[i], Data.MOVEDATA) for i in range(4)]
        self.status_widget = Wid.StatusWidgets(self.poke)
        if isinstance(self.poke, Obj.PokeDetail):
            self.ability_flag_widget = Wid.CustomTuggleButton("特性発動", self.poke.ability_flag)
            self.terastal_flag_widget = Wid.CustomTuggleButton("テラスタル", self.poke.terastal_flag)
            self.rank_widgets = [Wid.CustomRankBox(self.poke.rank_list[i]) for i in range(5)]
            self.move_flag_widget = Wid.CustomTuggleButton("技効果", self.poke.move_flag)
            self.bad_stat_widget = Wid.CustomCommboBox(self.poke.bad_stat, Data.BADSTAT)

    def name_widget_func(self):
        raise NotImplementedError

    def status_update(self):
        self.status_widget.update()

    def auto_pokemon_item(self):
        name = self.name_widget.get()
        result = [data for data in Data.ITEM_POKE if data[0] == name]
        if len(result) > 0:
            self.item_widget.set(result[0][1])
            self.terastal_widget.set(result[0][2])

class PlayerFieldManager:
    def __init__(self):
        self.player = Obj.PlayerField()
        self.a_wall_widget = Wid.CustomTuggleButton("リフレクター", self.player.a_wall)
        self.c_wall_widget = Wid.CustomTuggleButton("ひかりのかべ", self.player.c_wall)
        self.wind_widget = Wid.CustomTuggleButton("おいかぜ", self.player.wind)
        self.help_widget = Wid.CustomTuggleButton("てだすけ", self.player.help)
        self.crit_widget = Wid.CustomTuggleButton("被急所", self.player.crit)

    def add_method(self, method: Callable):
        self.a_wall_widget.add_method(method)
        self.c_wall_widget.add_method(method)
        self.wind_widget.add_method(method)
        self.help_widget.add_method(method)
        self.crit_widget.add_method(method)

class FieldWidgetManager:
    def __init__(self):
        self.field_data = Obj.Field()
        self.double_widget = Wid.CustomTuggleButton("ダブルバトル", self.field_data.double)
        self.field_widget = Wid.CustomCommboBox(self.field_data.field, Data.FIELD)
        self.weather_widget = Wid.CustomCommboBox(self.field_data.weather, Data.WEATHER)
        self.field_ability_widget_1 = Wid.CustomCommboBox(self.field_data.ability_1, Data.ABIILITY)
        self.field_ability_widget_2 = Wid.CustomCommboBox(self.field_data.ability_2, Data.ABIILITY)
        self.gravity_widget = Wid.CustomTuggleButton("じゅうりょく", self.field_data.gravity)
        self.magic_room_widget = Wid.CustomTuggleButton("マジックルーム", self.field_data.magic_room)
        self.wonder_room_widget = Wid.CustomTuggleButton("ワンダールーム", self.field_data.wonder_room)
        self.image_label = Wid.CustomImageLabel(lambda: Pr.ImageGenerator.create_field(self.field_data))

    def update(self):
        self.image_label.update()

    def add_method(self, method: Callable):
        self.double_widget.add_method(method)
        self.field_widget.add_method(method)
        self.weather_widget.add_method(method)
        self.field_ability_widget_1.add_method(method)
        self.field_ability_widget_2.add_method(method)
        self.gravity_widget.add_method(method)
        self.magic_room_widget.add_method(method)
        self.wonder_room_widget.add_method(method)
