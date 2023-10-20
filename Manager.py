#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Callable

import tkinter as tk
import Object as Obj
import Widget as Wid
import Data

class Manager:
    def __init__(self, master):
        self.master = master
        self.image_flag = False
        self.party = [Obj.PokeDetail() for i in range(6)]
        self.enemy = [Obj.PokeDetail() for i in range(6)]

    def poke_generate(self, index: int, data):
        self.party[index].re_init(data)

class StatusWidgetManager:
    def __init__(self):
        self.poke = Obj.Poke()
        self.method = None
        self.name_widget = Wid.CustomCommboBox(Data.POKEDATA, method=self.name_widget_func)
        self.level_widget = Wid.CustomLevelBox(method=self.update)
        self.ability_widget = Wid.CustomCommboBox(method=self.update)
        self.item_widget = Wid.CustomCommboBox(Data.ITEMDATA, method=self.update)
        self.terastal_widget = Wid.CustomCommboBox(Data.TYPEDATA.list, method=self.update)
        self.move_widgets = [Wid.CustomCommboBox(Data.MOVEDATA, method=self.update) for i in range(4)]
        self.status_widgets = [Wid.StatusWidget(status, self.children_method) for status in self.poke.status_list]

    def set_dic(self):
        self.poke.set_dic("item", self.item_widget)
        self.poke.set_dic("terastal", self.terastal_widget)
        self.poke.set_dic("ability", self.ability_widget)
        self.poke.set_dic("level", self.level_widget)
        self.poke.set_dic("individual", [widget.individual.variable for widget in self.status_widgets])
        self.poke.set_dic("effort", [widget.effort.variable for widget in self.status_widgets])
        self.poke.set_dic("nature", [widget.nature.variable for index, widget in enumerate(self.status_widgets) if index != 0])
        self.poke.set_dic("move", [widget for widget in self.move_widgets])

    def update(self):
        self.poke.update()
        [widget.set_label() for widget in self.status_widgets]
        if self.method is not None:
            self.method()

    def name_widget_func(self):
        if self.name_widget.get() in Data.POKEDATA.name_list:
            self.poke.generate(self.name_widget.get())
            self.ability_widget.reset()
            self.ability_widget.values_config(self.poke.ability_list)
            self.item_widget.reset()
            self.terastal_widget.reset()
            [widget.reset() for widget in self.move_widgets]
            [widget.reset() for widget in self.status_widgets]
            self.auto_pokemon_item()
            self.update()

    def auto_pokemon_item(self):
        name = self.name_widget.get()
        result = [data for data in Data.ITEM_POKE if data[0] == name]
        if len(result) > 0:
            self.item_widget.set(result[0][1])
            self.terastal_widget.set(result[0][2])

    def children_method(self, flag: bool | float=False):
        if flag == 1.1:
            [widget.nature.set(1) for widget in self.status_widgets[1:] if widget.nature.get() == 1.1]
        elif flag == 0.9:
            [widget.nature.set(1) for widget in self.status_widgets[1:] if widget.nature.get() == 0.9]
        [widget.status_label.color_change(widget.nature.get()) for widget in self.status_widgets[1:]]
        self.update()

    def add_update_method(self, method: Callable):
        self.method = method

class StatusWidgetManagerPage3(StatusWidgetManager):
    def __init__(self):
        super().__init__()
        self.poke = Obj.PokeDetail()
        self.ability_widget = Wid.CustomCommboButtonBox(method=self.update)
        self.terastal_widget = Wid.CustomCommboButtonBox(Data.TYPEDATA.list, method=self.update)
        self.move_widgets = [Wid.CustomCommboButtonBox(Data.MOVEDATA, method=self.update) for i in range(4)]
        self.rank_widgets = [Wid.CustomRankBox(method=self.update) for i in range(5)]
        self.move_flag_widget = Wid.CustomTuggleButton("技効果", method=self.update, width=10)
        self.bad_stat_widget = Wid.CustomCommboBox(Data.BADSTAT, method=self.update, width=6)
        self.image_label = Wid.CustomImageLabelPage3()
        self.hp_now_widget = Wid.CustomHPNowBox(method=self.hp_now_update)
        self.result_widget = Wid.ResultWidget()
        self.button_widget = Wid.ChangeButtonWidget(7)

    def name_widget_func(self):
        if self.name_widget.get() in Data.POKEDATA.name_list:
            self.poke.generate(self.name_widget.get())
            self.ability_widget.reset()
            self.ability_widget.values_config(self.poke.ability_list)
            self.item_widget.reset()
            self.terastal_widget.reset()
            [widget.reset() for widget in self.move_widgets]
            [widget.reset() for widget in self.status_widgets]
            [widget.reset() for widget in self.rank_widgets]
            self.ability_widget.t_button.reset()
            self.terastal_widget.t_button.reset()
            self.bad_stat_widget.reset()
            self.move_flag_widget.reset()
            self.auto_pokemon_item()
            self.update()
            self.image_update()

    def set_dic(self):
        super().set_dic()
        self.poke.set_dic("rank", [widget for widget in self.rank_widgets])
        self.poke.set_dic("terastal_flag", self.terastal_widget.t_button)
        self.poke.set_dic("move_flag", self.move_flag_widget)
        self.poke.set_dic("ability_flag", self.ability_widget.t_button)
        self.poke.set_dic("bad_stat", self.bad_stat_widget)

    def update(self):
        self.poke.update()
        [widget.set_label() for widget in self.status_widgets]
        self.image_update()
        self.hp_now_widget.set(self.poke.hp_now, self.poke.status_list[0].value)
        self.result_widget.image_update(self.status_widgets[0].status.value, 0, 0)

    def widget_update(self):
        self.name_widget.set(self.poke.name)
        self.item_widget.set(self.poke.item)
        self.terastal_widget.set(self.poke.terastal)
        self.ability_widget.set(self.poke.ability)
        self.ability_widget.config(values=self.poke.ability_list)
        self.level_widget.set(self.poke.level)
        for index, status in enumerate(self.status_widgets):
            status.individual.set(self.poke.status_list[index].individual)
            status.effort.set(self.poke.status_list[index].effort)
            if index != 0:
                status.nature.set(self.poke.status_list[index].nature)
        for index, widget in enumerate(self.move_widgets):
            widget.set(self.poke.move_list[index])
        for index, widget in enumerate(self.rank_widgets):
            widget.set(self.poke.rank_list[index])
        self.ability_widget.t_button.set(self.poke.ability_flag)
        self.terastal_widget.t_button.set(self.poke.terastal_flag)
        self.move_flag_widget.set(self.poke.move_flag)
        self.bad_stat_widget.set(self.poke.bad_stat)
        self.image_update()
        for index, status in enumerate(self.status_widgets):
            status.set_label()
        self.hp_now_widget.set(self.poke.hp_now, self.poke.status_list[0].value)
        hp = self.poke.status_list[0].value
        self.result_widget.image_update(hp, hp-self.poke.hp_now, hp-self.poke.hp_now)

    def hp_now_update(self):
        self.poke.hp_now = self.hp_now_widget.now_variable.get()
        hp = self.poke.status_list[0].value
        self.result_widget.image_update(hp, hp-self.poke.hp_now, hp-self.poke.hp_now)

    def image_update(self):
        terastal = ""
        if self.terastal_widget.get_variable():
            terastal = self.terastal_widget.get()
        self.image_label.update(self.name_widget.get(), self.item_widget.get(), terastal)


class StatusWidgetManagerBattle(StatusWidgetManagerPage3):
    def __init__(self, side: str):
        super().__init__()
        del self.result_widget
        del self.button_widget
        self.move_counter_widgets = [Wid.CustomCountBox() for i in range(4)]

    def image_update(self):
        pass


class PlayerFieldManager:
    def __init__(self):
        self.player = Obj.PlayerField()
        self.a_wall_widget = Wid.CustomTuggleButton("リフレクター", method=self.update, width=10)
        self.a_wall_counter = Wid.CustomCountBox(max=5)
        self.c_wall_widget = Wid.CustomTuggleButton("ひかりのかべ", method=self.update, width=10)
        self.c_wall_counter = Wid.CustomCountBox(max=5)
        self.wind_widget = Wid.CustomTuggleButton("おいかぜ", method=self.update, width=10)
        self.wind_counter = Wid.CustomCountBox(max=5)
        self.help_widget = Wid.CustomTuggleButton("てだすけ", method=self.update, width=10)
        self.crit_widget = Wid.CustomTuggleButton("被急所", method=self.update, width=10)

    def config(self):
        self.player.config(
            self.a_wall_widget,
            self.c_wall_widget,
            self.wind_widget,
            self.help_widget,
            self.crit_widget,
        )

    def update(self):
        self.player.update()

class FieldWidgetManager:
    def __init__(self):
        self.field_data = Obj.Field()
        self.double_widget = Wid.CustomTuggleButton("ダブルバトル", method=self.update, width=12)
        self.field_widget = Wid.CustomCommboBox(Data.FIELD, method=self.update, width=12)
        self.weather_widget = Wid.CustomCommboBox(Data.WEATHER, method=self.update, width=12)
        self.field_ability_widget_1 = Wid.CustomCommboBox(Data.ABIILITY, method=self.update, width=12)
        self.field_ability_widget_2 = Wid.CustomCommboBox(Data.ABIILITY, method=self.update, width=12)
        self.gravity_widget = Wid.CustomTuggleButton("じゅうりょく", method=self.update, width=12)
        self.magic_room_widget = Wid.CustomTuggleButton("マジックルーム", method=self.update, width=12)
        self.wonder_room_widget = Wid.CustomTuggleButton("ワンダールーム", method=self.update, width=12)
        self.image_label = Wid.CustomImageLabel()

    def config(self):
        self.field_data.config(
            self.double_widget.variable,
            self.field_widget.variable,
            self.weather_widget.variable,
            self.field_ability_widget_1.variable,
            self.field_ability_widget_2.variable,
        )

    def update(self):
        self.field_data.update()
        self.image_label.image_update(self.weather_widget.get(), self.field_widget.get())

class BattleManager:
    def __init__(self, side: str, battle_type: int):
        self.side = side
        self.battle_type = battle_type
        self.banners = [Wid.BannerWidgetPage3(side) for i in range(battle_type)]
        self.party_widget = Wid.ChangePokeWidget(self.side)
        self.battle_widgets = [Wid.BattleWidget(side, battle_type) for i in range(battle_type)]
        self.player_widget = PlayerFieldManager()

    def create(self, parent: "list[tk.Tk]"):
        for index in range(self.battle_type):
            frame = tk.LabelFrame(parent, text=index)
            frame.pack(side=self.side, fill="both", expand=True, padx=2)
            self.battle_widgets[index].create(frame)

    def player_create(self, parent):
        self.player_widget.a_wall_widget.create(parent)
        self.player_widget.c_wall_widget.create(parent)
        self.player_widget.wind_widget.create(parent)
        self.player_widget.help_widget.create(parent)
        self.player_widget.crit_widget.create(parent)
        col = 0 if self.side == tk.LEFT else 1
        self.player_widget.a_wall_widget.grid(row=0, column=col, padx=2, pady=2)
        self.player_widget.c_wall_widget.grid(row=1, column=col, padx=2, pady=2)
        self.player_widget.wind_widget.grid(row=2, column=col, padx=2, pady=2)
        col = 2 if self.side == tk.LEFT else 0
        self.player_widget.help_widget.grid(row=0, column=col, padx=2, pady=2)
        self.player_widget.crit_widget.grid(row=1, column=col, padx=2, pady=2)




class DoubleBattleManager:
    def __init__(self):
        self.left = BattleManager(tk.LEFT, 2)
        self.right = BattleManager(tk.RIGHT, 2)
        self.field = FieldWidgetManager()
        self.timer_widget = Wid.Timer_widget()

    def team_update(self):
        self.left.party_widget.update()