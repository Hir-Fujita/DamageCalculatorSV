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
        self.image_flag = True
        self.party = [Obj.PokeDetail() for i in range(6)]

    def poke_generate(self, index: int, data):
        self.party[index].re_init(data)

class StatusWidgetManager:
    def __init__(self, poke: Obj.Poke):
        self.poke = poke
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

class StatusWidgetManagerPlus(StatusWidgetManager):
    def __init__(self, poke: Obj.PokeDetail):
        super().__init__(poke)
        self.poke = poke
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

    def config(self):
        super().config()
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
        self.terastal_widget.t_button.set(self.poke.terastal_flag)
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

class PlayerFieldManager:
    def __init__(self, player_data: Obj.PlayerField):
        self.player = player_data
        self.a_wall_widget = Wid.CustomTuggleButton("リフレクター", method=self.update, width=10)
        self.c_wall_widget = Wid.CustomTuggleButton("ひかりのかべ", method=self.update, width=10)
        self.wind_widget = Wid.CustomTuggleButton("おいかぜ", method=self.update, width=10)
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
    def __init__(self, field_data: Obj.Field):
        self.field_data = field_data
        self.double_widget = Wid.CustomTuggleButton("ダブルバトル", method=self.update, width=12)
        self.field_widget = Wid.CustomCommboBox(Data.FIELD, method=self.update, width=12)
        self.weather_widget = Wid.CustomCommboBox(Data.WEATHER, method=self.update, width=12)
        self.field_ability_widget_1 = Wid.CustomCommboBox(Data.ABIILITY, method=self.update, width=12)
        self.field_ability_widget_2 = Wid.CustomCommboBox(Data.ABIILITY, method=self.update, width=12)
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
        self.party_widget = Wid.ChangePokeWidget(self.side)
        self.pokemons = [Obj.PokeDetail() for i in range(battle_type)]
        self.battle_widgets = [Wid.BattleWidget(self.pokemons[i], side, 1 / battle_type) for i in range(battle_type)]
        self.status_widgets = [StatusWidgetManagerPlus(self.pokemons[i]) for i in range(battle_type)]

    def create(self, parents: "list[tk.Tk]"):
        for index, parent in enumerate(parents):
            top_frame = tk.Frame(parent)
            top_frame.pack()
            self.battle_widgets[index].create(top_frame)

            middle_frame = tk.Frame(parent)
            middle_frame.pack()
            font = ("MeiryoUI", 10)
            for i in range(6):
                self.status_widgets[index].status_widgets[i].status_label.create(middle_frame)
                self.status_widgets[index].status_widgets[i].status_label.config(width=3, font=("MeiryoUI", 12, "bold"))
                self.status_widgets[index].status_widgets[i].status_label.grid(row=0, column=i)
                self.status_widgets[index].status_widgets[i].individual.create(middle_frame)
                self.status_widgets[index].status_widgets[i].individual.config(width=3, font=font)
                self.status_widgets[index].status_widgets[i].effort.create(middle_frame)
                self.status_widgets[index].status_widgets[i].effort.config(width=3, font=font)
                self.status_widgets[index].status_widgets[i].individual.grid(row=1, column=i, padx=2, pady=1)
                self.status_widgets[index].status_widgets[i].effort.grid(row=2, column=i)
                if self.side == tk.LEFT:
                    self.status_widgets[index].status_widgets[i].individual.disabled()
                    self.status_widgets[index].status_widgets[i].effort.disabled()
                if i != 0:
                    self.status_widgets[index].rank_widgets[i-1].create(middle_frame)
                    self.status_widgets[index].rank_widgets[i-1].config(width=3, font=font)
                    self.status_widgets[index].rank_widgets[i-1].grid(row=3, column=i, padx=2, pady=1)
            

            middle_2_frame = tk.Frame(parent)
            middle_2_frame.pack()
            self.status_widgets[index].terastal_widget.create(middle_2_frame)
            self.status_widgets[index].terastal_widget.widget.config(width=12)
            self.status_widgets[index].terastal_widget.widget.pack(side=tk.LEFT, padx=5)
            self.status_widgets[index].terastal_widget.widget.add_tuggle_button(self.status_widgets[index].terastal_widget, "テラスタル", self.status_widgets[index].update)
            self.status_widgets[index].terastal_widget.widget.t_button.pack(side=tk.LEFT)
            self.status_widgets[index].terastal_widget.grid(row=0, column=0, columnspan=2)
            self.status_widgets[index].ability_widget.create(middle_2_frame)
            self.status_widgets[index].ability_widget.config(width=12)
            self.status_widgets[index].ability_widget.widget.pack(side=tk.LEFT)
            self.status_widgets[index].ability_widget.widget.add_tuggle_button(self.status_widgets[index].ability_widget, "発動", self.status_widgets[index].update)
            self.status_widgets[index].ability_widget.widget.t_button.pack(side=tk.LEFT)
            self.status_widgets[index].ability_widget.grid(row=1, column=0)
            self.status_widgets[index].bad_stat_widget.create(middle_2_frame)
            self.status_widgets[index].bad_stat_widget.widget.pack()
            self.status_widgets[index].bad_stat_widget.grid(row=1, column=1)
            self.status_widgets[index].item_widget.create(middle_2_frame)
            self.status_widgets[index].item_widget.config(width=16)
            self.status_widgets[index].item_widget.widget.pack(side=tk.LEFT)
            self.status_widgets[index].item_widget.grid(row=2, column=0)
            self.status_widgets[index].move_flag_widget.create(middle_2_frame)
            self.status_widgets[index].move_flag_widget.config(width=8)
            self.status_widgets[index].move_flag_widget.grid(row=2, column=1)
            if self.side == tk.LEFT:
                pass
            self.status_widgets[index].config()




class DoubleBattleManager:
    def __init__(self):
        self.left = BattleManager(tk.LEFT, 2)
        self.right = BattleManager(tk.RIGHT, 2)
        self.timer_widget = Wid.Timer_widget()

    def team_update(self):
        self.left.party_widget.update()