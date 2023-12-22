#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from typing import Union, Callable
import tkinter as tk
from tkinter import messagebox
import copy

import Manager
import Widget as Wid
import Data
import Process as Pr
import Object as Obj
import Calculation as Calc

class Page1:
    class WidgetManager(Manager.PokeWidgetManager):
        def __init__(self):
            super().__init__(Obj.Poke())
            [widget.effort.add_method(self.sum_update) for widget in self.status_widget.widgets]
            self.item_widget.add_method(self.image_update)
            self.terastal_widget.add_method(self.image_update)
            self.image_label = Wid.CustomImageLabel(lambda: Pr.ImageGenerator.create_page1(self.poke))
            self.memo = Wid.CustomTextBox()

        def create_sum_effor_widget(self, parent):
            self.sum_label = tk.Label(parent, text=510, font=("Helvetica", 12, "bold"), width=3)

        def create_memo_widget(self, parent):
            self.memo.create(parent)
            self.memo.widget.config(width=50, height=5, font=("Meiryo UI", 20, "bold"))

        def name_widget_func(self):
            if self.name_widget.get() in Data.POKEDATA.name_list:
                self.poke.generate()
                self.ability_widget.reset()
                self.ability_widget.values_config(self.poke.ability_list)
                self.item_widget.reset()
                self.terastal_widget.reset()
                [widget.reset() for widget in self.move_widgets]
                self.status_widget.reset()
                self.auto_pokemon_item()
                self.image_update()
                self.sum_update()

        def image_update(self):
            self.image_label.update()

        def sum_update(self):
            result = 510 - sum(widget.effort.get() for widget in self.status_widget.widgets)
            self.sum_label.config(text=result)
            if result < 0:
                self.sum_label.config(foreground="red")
            else:
                self.sum_label.config(foreground="black")

    def __init__(self, parent, manager: Manager.Manager):
        self.manager = manager
        self.widget = self.WidgetManager()
        top_frame = tk.Frame(parent)
        top_frame.pack(pady=5)
        name_frame = tk.LabelFrame(top_frame, text="ポケモン名")
        name_frame.pack(side=tk.LEFT, padx=5)
        self.widget.name_widget.create(name_frame)
        self.widget.name_widget.pack(padx=5, pady=5)

        level_frame = tk.LabelFrame(top_frame, text="Lv")
        level_frame.pack(side=tk.LEFT, padx=5)
        self.widget.level_widget.create(level_frame, width=3, font=("Helvetica", 10))
        self.widget.level_widget.pack(padx=5, pady=5)

        terastal_frame = tk.LabelFrame(top_frame, text="テラスタル")
        terastal_frame.pack(side=tk.LEFT, padx=5)
        self.widget.terastal_widget.create(terastal_frame, width=10)
        self.widget.terastal_widget.pack(padx=5, pady=5)

        ability_frame = tk.LabelFrame(top_frame, text="とくせい")
        ability_frame.pack(side=tk.LEFT, padx=5)
        self.widget.ability_widget.create(ability_frame)
        self.widget.ability_widget.pack(padx=5, pady=5)

        item_frame = tk.LabelFrame(top_frame, text="もちもの")
        item_frame.pack(side=tk.LEFT, padx=5)
        self.widget.item_widget.create(item_frame)
        self.widget.item_widget.pack(padx=5, pady=5)

        move_frame = tk.Frame(parent)
        move_frame.pack(pady=5)
        for i in range(4):
            frame = tk.LabelFrame(move_frame, text=f"わざ_{i+1}")
            frame.pack(side=tk.LEFT, padx=5)
            self.widget.move_widgets[i].create(frame)
            self.widget.move_widgets[i].pack(padx=5, pady=5)

        middle_frame = tk.Frame(parent)
        middle_frame.pack(pady=10)
        status_frame = tk.Frame(middle_frame)
        status_frame.pack(side=tk.LEFT)
        self.widget.status_widget.create(status_frame)
        for widget in self.widget.status_widget.widgets:
            widget.status_label.config(width=3, font=("Helvetica", 20, "bold"))
            widget.individual.config(width=3, font=("Helvetica", 10))
            widget.effort.config(width=3, font=("Helvetica", 10))

        labels = [tk.Label(status_frame, text=label) for label in ["", "実数値", "個体値", "努力値", "性格"]]
        self.widget.create_sum_effor_widget(status_frame)
        labels.insert(4, self.widget.sum_label)
        [widget.grid(row=0, column=index) for index, widget in enumerate(labels)]

        labels = [tk.Label(status_frame, text=label) for label in ["HP", "攻撃", "防御", "特攻", "特防", "素早"]]
        [label.grid(row=index+1, column=0) for index, label in enumerate(labels)]
        for index, widget in enumerate(self.widget.status_widget.widgets):
            widget.status_label.grid(row=index+1, column=1, padx=5)
            widget.individual.grid(row=index+1, column=2, padx=5)
            widget.effort.slider.grid(row=index+1, column=3, padx=5)
            widget.effort.grid(row=index+1, column=4, padx=5)
            if index:
                widget.nature.grid(row=index+1, column=5, padx=5)

        if self.manager.image_flag:
            img_frame = tk.Frame(middle_frame)
            img_frame.pack(side=tk.LEFT, padx=10)
            self.widget.image_label.create(img_frame)
            self.widget.image_label.pack(side=tk.BOTTOM)

        bottom_frame = tk.Frame(parent)
        bottom_frame.pack()
        memo_frame = tk.LabelFrame(bottom_frame, text="メモ欄")
        memo_frame.pack()
        self.widget.create_memo_widget(memo_frame)
        self.widget.memo.pack()

    def save_poke(self):
        if self.save_check():
            poke = self.widget.poke
            path = Data.save_filedialogwindow(f"{poke.name}@{poke.item}", "ポケモン保存", "Pokemon", ("text_file", "txt"))
            if path:
                save_data = poke.save()
                [save_data.append(m) for m in self.widget.memo.get().split("\n") if m != ""]
                with open(path, "w", encoding="UTF-8") as f:
                    [f.writelines(f"{data}\n") for data in save_data]

    def save_check(self):
        if self.widget.poke.name == "":
            messagebox.showerror(title="error", message="ポケモンが選択されていません")
            return False
        if self.widget.poke.ability == "":
            messagebox.showerror(title="error", message="とくせいが選択されていません")
            return False
        if self.widget.poke.terastal == "":
            messagebox.showerror(title="error", message="テラスタルが選択されていません")
            return False
        if int(self.widget.sum_label["text"]) < 0:
            messagebox.showerror(title="error", message="努力値が不正です")
            return False
        return True

    def load_poke(self):
        path = Data.open_filedialogwindow("ポケモン読み込み", "Pokemon", ("text_file", "txt"))
        if path:
            data = Data.PokeData.load(path)
            self.widget.name_widget.set(data.name)
            self.widget.poke.generate()
            self.widget.level_widget.set(data.level)
            self.widget.item_widget.set(data.item)
            self.widget.ability_widget.set(data.ability)
            self.widget.terastal_widget.set(data.terastal)
            [self.widget.move_widgets[i].set(data.move_list[i]) for i in range(4)]
            for index, widget in enumerate(self.widget.status_widget.widgets):
                widget.individual.set(data.status[index][0])
                widget.effort.set(data.status[index][1])
                if index != 0:
                    widget.nature.set(data.status[index][2])
                    widget.status_label.color_change(data.status[index][2])
            self.widget.memo.delete()
            [self.widget.memo.set(f"{m}\n") for m in data.memo]
            self.widget.sum_update()

class Page2:
    def __init__(self, parent, manager: Manager.Manager):
        frame = tk.Frame(parent)
        frame.pack(pady=5)
        self.manager = manager
        self.default_text = "左クリックでポケモンを登録\n右クリックでポケモンを削除"
        self.text_variable = tk.StringVar(value=self.default_text)
        self.widgets: "list[Wid.BannerWidget]" = [Wid.BannerWidget(frame, self.manager.party.list[i], self.text_variable, lambda i=i: self.manager.party.create_backup(i)) for i in range(6)]
        for index, widget in enumerate(self.widgets):
            if index < 3:
                widget.widget.grid(row=0, column=index)
            else:
                widget.widget.grid(row=1, column=index-3)

        right_frame = tk.Frame(parent)
        right_frame.pack(fill=tk.BOTH)
        text_label = tk.Label(right_frame, textvariable=self.text_variable, font=("Meiryo UI", 20, "bold"), anchor=tk.CENTER)
        text_label.pack(padx=5, fill=tk.BOTH)

    def save_party(self):
        path = Data.save_filedialogwindow("", "パーティ登録", "Party", ("party_data", ".party"))
        if path:
            write_data = [widget.poke.save() if widget.poke.name else [] for widget in self.widgets]
            Data.save_file(path, write_data)

    def load_party(self):
        path = Data.open_filedialogwindow("パーティ読み込み", "Party", ("party_data", ".party"))
        if path:
            data_list = Data.open_file(path)
            for index, widget in enumerate(self.widgets):
                widget.load(Data.PokeData.generate(data_list[index]))
        self.manager.party.create_backup()

class Page3:
    class WidgetManager(Manager.PokeWidgetManager):
        def __init__(self, side: str, dmg_update_method: Callable):
            self.side = side
            self.dmg_update_method = dmg_update_method
            super().__init__(Obj.PokeDetail())
            self.level_widget.add_method(self.dmg_update_method)
            self.ability_widget.add_method(self.dmg_update_method)
            self.ability_flag_widget.add_method(self.dmg_update_method)
            [rank.add_method(self.dmg_update_method) for rank in self.rank_widgets]
            [move.add_method(self.dmg_update_method) for move in self.move_widgets]
            self.move_flag_widget.add_method(self.dmg_update_method)
            self.bad_stat_widget.add_method(self.dmg_update_method)
            self.item_widget.add_method(self.image_update, self.dmg_update_method)
            self.terastal_widget.add_method(self.image_update, self.dmg_update_method)
            self.terastal_flag_widget.add_method(self.image_update, self.dmg_update_method)
            self.status_widget.widgets[0].effort.add_method(self.hp_set)
            self.status_widget.widgets[0].individual.add_method(self.hp_set)
            for index, widget in enumerate(self.status_widget.widgets):
                widget.individual.add_method(self.dmg_update_method)
                widget.effort.add_method(self.dmg_update_method)
                if index != 0:
                    widget.nature.add_method(self.dmg_update_method)
            self.image_label = Wid.CustomImageLabel(lambda: Pr.ImageGenerator.create_page3(self.poke, self.side))
            self.calc_buttons = [Wid.CustomTuggleButton("計算", self.poke.calc_list[i]) for i in range(4)]
            [self.calc_buttons[i].add_method(lambda i=i: self.calc_check(i), self.dmg_update_method) for i in range(4)]
            self.hp_now_widget = Wid.CustomHPNowBox(self.poke.hp_now, self.poke.status_list[0].value, method=self.dmg_update_method)
            self.result_widget = Wid.ResultWidget()
            self.button_widget = Wid.ChangeButtonWidget(self.poke, 7, self.image_update)
            self.button_widget.add_method(self.change_button_update, self.dmg_update_method)

        def name_widget_func(self):
            if self.name_widget.get() in Data.POKEDATA.name_list:
                self.poke.generate()
                self.ability_widget.reset()
                self.ability_widget.values_config(self.poke.ability_list)
                self.item_widget.reset()
                self.terastal_widget.reset()
                self.status_widget.reset()
                [widget.reset() for widget in self.move_widgets]
                [widget.reset() for widget in self.rank_widgets]
                [widget.reset() for widget in self.calc_buttons]
                self.ability_flag_widget.reset()
                self.terastal_flag_widget.reset()
                self.bad_stat_widget.reset()
                self.move_flag_widget.reset()
                self.auto_pokemon_item()
                self.image_update()
                self.dmg_update_method()

        def hp_set(self):
            self.poke.hp_now.set(self.poke.status_list[0].value.get())
            self.dmg_update_method()

        def change_button_update(self):
            [btn.update() for btn in self.calc_buttons]
            self.status_widget.update()

        def calc_check(self, index: int):
            if self.move_widgets[index].get() == "":
                self.calc_buttons[index].variable.set(False)
                self.calc_buttons[index].config(relief=tk.RAISED)

        def image_update(self):
            self.image_label.update()

    def __init__(self, parent):
        frame = tk.Frame(parent)
        frame.pack()
        self.id_dic = Obj.PokeDict()

        left_frame = tk.Frame(frame)
        left_frame.pack(side=tk.LEFT, anchor=tk.W)
        self.left = self.WidgetManager(tk.LEFT, self.dmg_update)
        self.left_field = Manager.PlayerFieldManager()
        self.left_field.add_method(self.dmg_update)
        self.create(left_frame, self.left, self.left_field, tk.LEFT)

        right_frame = tk.Frame(frame)
        right_frame.pack(side=tk.RIGHT, anchor=tk.E)
        self.right = self.WidgetManager(tk.RIGHT, self.dmg_update)
        self.right_field = Manager.PlayerFieldManager()
        self.right_field.add_method(self.dmg_update)
        self.create(right_frame, self.right, self.right_field, tk.RIGHT)

        self.manager = {
            tk.LEFT: self.left,
            tk.RIGHT: self.right
        }

        self.field_manager = Manager.FieldWidgetManager()
        self.field_manager.field_widget.add_method(self.field_manager.update)
        self.field_manager.weather_widget.add_method(self.field_manager.update)
        self.field_manager.add_method(self.dmg_update)
        center_frame = tk.LabelFrame(frame, text="状況")
        center_frame.pack(side=tk.BOTTOM, anchor=tk.S)
        image_frame = tk.Frame(center_frame)
        image_frame.pack(padx=5, pady=2)
        self.field_manager.image_label.create(image_frame)
        self.field_manager.image_label.pack(padx=10, pady=2)
        self.field_manager.double_widget.create(center_frame, width=12)
        self.field_manager.double_widget.pack(padx=5, pady=2)
        weather_frame = tk.LabelFrame(center_frame, text="天候")
        weather_frame.pack(padx=5, pady=2)
        self.field_manager.weather_widget.create(weather_frame, width=12)
        self.field_manager.weather_widget.pack(padx=5, pady=2)
        field_frame = tk.LabelFrame(center_frame, text="フィールド")
        field_frame.pack(padx=5, pady=2)
        self.field_manager.field_widget.create(field_frame, width=12)
        self.field_manager.field_widget.pack(padx=5, pady=2)
        ability_1_frame = tk.LabelFrame(center_frame, text="とくせい_1")
        ability_1_frame.pack(padx=5, pady=2)
        self.field_manager.field_ability_widget_1.create(ability_1_frame, width=12)
        self.field_manager.field_ability_widget_1.pack(padx=5, pady=2)
        ability_2_frame = tk.LabelFrame(center_frame, text="とくせい_2")
        ability_2_frame.pack(padx=5, pady=2)
        self.field_manager.field_ability_widget_2.create(ability_2_frame, width=12)
        self.field_manager.field_ability_widget_2.pack(padx=5, pady=2)
        self.field_manager.gravity_widget.create(center_frame, width=12)
        self.field_manager.gravity_widget.pack(padx=5, pady=2)
        self.field_manager.wonder_room_widget.create(center_frame, width=12)
        self.field_manager.wonder_room_widget.pack(padx=5, pady=2)
        self.field_manager.magic_room_widget.create(center_frame, width=12)
        self.field_manager.magic_room_widget.pack(padx=5, pady=2)

        result_frame = tk.Frame(parent)
        result_frame.pack()
        self.left.result_widget.create(result_frame)
        self.left.result_widget.pack(side=tk.LEFT, padx=2)
        self.right.result_widget.create(result_frame)
        self.right.result_widget.pack(side=tk.LEFT, padx=2)

    def create(self, frame, manager: WidgetManager, field: Manager.PlayerFieldManager, side):
        out_frame = tk.Frame(frame)
        out_frame.pack(side=side, padx=5)
        manager.button_widget.create(out_frame, side)
        manager.button_widget.pack()

        in_frame = tk.Frame(frame)
        in_frame.pack(side=side, padx=5)
        top_frame = tk.Frame(in_frame)
        top_frame.pack()
        name_frame = tk.LabelFrame(top_frame, text="ポケモン名")
        name_frame.pack(side=tk.LEFT)
        manager.name_widget.create(name_frame)
        manager.name_widget.pack(padx=5, pady=5)
        level_frame = tk.LabelFrame(top_frame, text="Lv")
        level_frame.pack(side=tk.LEFT)
        manager.level_widget.create(level_frame, width=3, font=("Helvetica", 10))
        manager.level_widget.pack(padx=5, pady=5)
        item_frame = tk.LabelFrame(top_frame, text="もちもの")
        item_frame.pack(side=tk.LEFT)
        manager.item_widget.create(item_frame, width=14)
        manager.item_widget.pack(padx=5, pady=5)

        frame_2 = tk.Frame(in_frame)
        frame_2.pack()
        ability_frame = tk.LabelFrame(frame_2, text="とくせい")
        ability_frame.pack(side=tk.LEFT)
        manager.ability_widget.create(ability_frame, width=12)
        manager.ability_widget.pack(side=tk.LEFT, padx=5, pady=5)
        manager.ability_flag_widget.create(ability_frame)
        manager.ability_flag_widget.pack(side=tk.LEFT, padx=5)
        terastal_frame = tk.LabelFrame(frame_2, text="テラスタル")
        terastal_frame.pack(side=tk.LEFT)
        manager.terastal_widget.create(terastal_frame, width=12)
        manager.terastal_widget.pack(side=tk.LEFT, padx=5, pady=5)
        manager.terastal_flag_widget.create(terastal_frame)
        manager.terastal_flag_widget.pack(side=tk.LEFT, padx=5)

        frame_3 = tk.Frame(in_frame)
        frame_3.pack()
        status_frame = tk.LabelFrame(frame_3, text="ステータス")
        status_frame.pack(side=side)
        labels = [tk.Label(status_frame, text=l, font=("Meiryo UI", 10)) for l in ["", "HP", "攻撃", "防御", "特攻", "特防", "素早"]]
        rows = [tk.Label(status_frame, text=l, font=("Meiryo UI", 10)) for l in ["実数値", "個体値", "努力値", "性格", "ランク"]]
        [label.grid(row=0, column=index) for index, label in enumerate(labels)]
        [row.grid(row=index+1, column=0) for index, row in enumerate(rows)]
        for index, widget in enumerate(manager.status_widget.widgets):
            widget.create(status_frame)
            widget.status_label.config(font=("Meiryo UI", 12, "bold"), width=3)
            widget.status_label.grid(row=1, column=index+1, padx=1, pady=2)
            widget.individual.grid(row=2, column=index+1, padx=1, pady=2)
            widget.individual.config(width=3, font=("Helvetica", 10))
            widget.effort.config(width=3, font=("Helvetica", 10))
            widget.effort.grid(row=3, column=index+1, padx=1, pady=2)
            if index != 0:
                widget.nature.grid(row=4, column=index+1, padx=1, pady=2)
                manager.rank_widgets[index-1].create(status_frame, font=("Helvetica", 10))
                manager.rank_widgets[index-1].grid(row=5, column=index+1, padx=1, pady=2)
        situation_frame = tk.Frame(frame_3)
        situation_frame.pack(side=side)
        field.a_wall_widget.create(situation_frame, width=12)
        field.a_wall_widget.pack(padx=10, pady=1)
        field.c_wall_widget.create(situation_frame, width=12)
        field.c_wall_widget.pack(padx=10, pady=1)
        field.wind_widget.create(situation_frame, width=12)
        field.wind_widget.pack(padx=10, pady=1)
        field.help_widget.create(situation_frame, width=12)
        field.help_widget.pack(padx=10, pady=1)
        field.crit_widget.create(situation_frame, width=12)
        field.crit_widget.pack(padx=10, pady=1)
        manager.move_flag_widget.create(situation_frame, width=12)
        manager.move_flag_widget.pack(padx=10, pady=1)

        frame_4 = tk.Frame(in_frame)
        frame_4.pack()
        manager.image_label.create(frame_4)
        manager.image_label.pack(side=side)
        frame_4_1 = tk.Frame(frame_4)
        frame_4_1.pack(side=side)
        frame4_1_top = tk.Frame(frame_4_1)
        frame4_1_top.pack()
        hp_now_frame = tk.LabelFrame(frame4_1_top, text="現在HP")
        hp_now_frame.pack(side=side)
        manager.hp_now_widget.create(hp_now_frame, ("Meiryo UI", 14, "bold"))
        manager.hp_now_widget.pack_widget()
        bad_stat_frame = tk.LabelFrame(frame4_1_top, text="状態異常")
        bad_stat_frame.pack(side=tk.LEFT, padx=5)
        manager.bad_stat_widget.create(bad_stat_frame, width=8)
        manager.bad_stat_widget.pack(padx=5, pady=5)
        move_frame = tk.LabelFrame(frame_4_1, text="わざ")
        move_frame.pack()
        for index, widget in enumerate(manager.move_widgets):
            widget.create(move_frame, width=16)
            widget.grid(row=index, column=0, padx=5, pady=2)
            manager.calc_buttons[index].create(move_frame)
            manager.calc_buttons[index].grid(row=index, column=2, padx=3, pady=2)

    def dmg_update(self):
        self.dmg_calc(tk.LEFT)
        self.dmg_calc(tk.RIGHT)

    def dmg_calc(self, side: str):
        if side == tk.LEFT:
            attacker = self.left.poke
            attacker_list = self.left.button_widget.buttons
            attacker_field = self.left_field.player.get()
            target = self.right.poke.get()
            target_field = self.right_field.player.get()
            widget = self.right.result_widget
        else:
            attacker = self.right.poke
            attacker_list = self.right.button_widget.buttons
            attacker_field = self.right_field.player.get()
            target = self.left.poke.get()
            target_field = self.left_field.player.get()
            widget = self.left.result_widget
        result_text: list[str] = []
        result_dmg: list[list[int]] = [[] for i in range(16)]
        if attacker.name.get() and target.name:
            calc = Calc.DamageCalculator(attacker.get(), attacker_field, target, target_field, self.field_manager.field_data.get())
            for index, calc_flag in enumerate(attacker.calc_list):
                move_name = attacker.move_list[index].get()
                if calc_flag.get() and move_name:
                    calc.calculation(move_name)
                    result_text.append(f"{attacker.name.get()}: {move_name}")
                    dmg = [calc.final_calc(0.85+ i*0.01) for i in range(16)]
                    logs = calc.calc_log + calc.log
                    [dmg_list.append(dmg[index]) for index, dmg_list in enumerate(result_dmg)]
                    result_text.append(["最低乱数"]+dmg+["最高乱数"])
                    [result_text.append(log) for log in logs]
                    result_text.append("------------------------------------------------------------")
        for atk in attacker_list:
            poke = atk.poke
            if poke.name.get():
                calc = Calc.DamageCalculator(poke.get(), attacker_field, target, target_field, self.field_manager.field_data.get())
                for index, calc_flag in enumerate(poke.calc_list):
                    move_name = poke.move_list[index].get()
                    if calc_flag.get() and move_name:
                        calc.calculation(move_name)
                        result_text.append(f"{poke.name.get()}: {move_name}")
                        dmg = [calc.final_calc(0.85+ i*0.01) for i in range(16)]
                        logs = calc.calc_log + calc.log
                        [dmg_list.append(dmg[index]) for index, dmg_list in enumerate(result_dmg)]
                        result_text.append(["最低乱数"]+dmg+["最高乱数"])
                        [result_text.append(log) for log in logs]
                        result_text.append("------------------------------------------------------------")
        dmg_list = [sum(dmg) for dmg in result_dmg]
        widget.update(target, result_text, dmg_list)

class Page4:
    """
    シングルバトル
    """
    def __init__(self, parent, manager: Manager.Manager):
        self.manager = manager
        left_frame = tk.Frame(parent)
        left_frame.pack(side=tk.LEFT)

        right_frame = tk.Frame(parent)
        right_frame.pack(side=tk.RIGHT)

class Page5:
    class PokeManager(Manager.PokeWidgetManager):
        def __init__(self, side: str, party_manager: Manager.PartyManager, dmg_update_method: Callable):
            self.dmg_update_method = dmg_update_method
            super().__init__(Obj.PokeDetail())
            self.item_widget.add_method(self.update, self.dmg_update_method)
            self.terastal_widget.add_method(self.update, self.dmg_update_method)
            self.terastal_flag_widget.add_method(self.update, self.dmg_update_method)
            self.status_widget.widgets[0].effort.add_method(self.hp_set, self.dmg_update_method)
            self.status_widget.widgets[0].individual.add_method(self.hp_set, self.dmg_update_method)
            [widget.effort.add_method(self.update, self.dmg_update_method) for widget in self.status_widget.widgets]
            [widget.individual.add_method(self.update, self.dmg_update_method) for widget in self.status_widget.widgets]
            [widget.nature.add_method(self.update, self.dmg_update_method) for widget in self.status_widget.widgets[1:]]
            [rank.add_method(self.update, self.dmg_update_method) for rank in self.rank_widgets]
            self.ability_widget.add_method(self.update, self.dmg_update_method)
            self.ability_flag_widget.add_method(self.update, self.dmg_update_method)
            self.move_flag_widget.add_method(self.update, self.dmg_update_method)
            self.bad_stat_widget.add_method(self.update, self.dmg_update_method)
            self.side = side
            self.party_manager: Manager.PartyManager = party_manager
            self.banner = Wid.ImageWidget(self.poke, self.side, self.party_manager.menu, self.menu_method_config, self.poke_select_index)
            self.hp_widget = Wid.BattleHPWidgets(self.poke, self.side, 200)
            self.hp_widget.hp_now_widget.add_method(self.update, self.dmg_update_method)
            [widget.add_method(self.update, self.poke.pp_set, self.dmg_update_method) for widget in self.move_widgets]
            self.add_buttons = [Wid.CustomTuggleButton("計算", self.poke.calc_list[i], self.update) for i in range(4)]
            self.move_counters = [Wid.CustomCountBox(self.poke.pp_list[i], self.update) for i in range(4)]
            [btn.add_method(self.dmg_update_method) for btn in self.add_buttons]

        def poke_select(self, index: int):
            self.poke.paste(self.party_manager.list[index].copy())
            self.ability_widget.config(value=self.poke.ability_list)
            self.status_update()
            self.hp_widget.hp_now_widget.slider_update()
            self.banner.update()

        def poke_select_index(self, index_count: int):
            index = self.party_manager.get_index(self.poke.id)
            if index is not None:
                index = index + index_count
                index = 0 if index < 0 else index
                index = 5 if index > 5 else index
                self.poke_select(index)

        def hp_set(self):
            self.poke.hp_now.set(self.poke.status_list[0].value.get())
            self.hp_widget.hp_now_widget.slider_update()

        def menu_method_config(self):
            for i in range(6):
                self.party_manager.menu.entryconfig(i, command=lambda index=i: self.poke_select(index))

        def update(self):
            self.party_manager.update(self.poke)


    class BattleManager:
        def __init__(self, side: str, party_manager, dmg_update_method: Callable):
            self.side = side
            self.dmg_update_method = dmg_update_method
            self.party_manager: Manager.PartyManager = party_manager
            self.player = Manager.PlayerFieldManager()
            self.pokemons = [Page5.PokeManager(self.side, self.party_manager, self.dmg_update_method) for i in range(2)]

    def __init__(self, parent, manager: Manager.Manager):
        self.manager = manager

        self.left = self.BattleManager(tk.LEFT, self.manager.party, self.update)
        left_frame = tk.Frame(parent)
        left_frame.pack(side=tk.LEFT)
        self.manager.party.widget.create(left_frame)

        self.right = self.BattleManager(tk.RIGHT, self.manager.enemy, self.update)
        right_frame = tk.Frame(parent)
        right_frame.pack(side=tk.RIGHT)
        self.manager.enemy.widget.create(right_frame)

        top_frame = tk.Frame(parent)
        top_frame.pack()
        [poke.banner.create(top_frame) for poke in self.left.pokemons]
        [poke.banner.pack(side=tk.LEFT, padx=5) for poke in self.left.pokemons]
        [poke.banner.create(top_frame) for poke in self.right.pokemons]
        [poke.banner.pack(side=tk.RIGHT, padx=5) for poke in self.right.pokemons]
        self.timer_button = Wid.Timer_widget()
        self.timer_button.create(top_frame, self.manager.master)
        self.timer_button.pack(side=tk.TOP, padx=5)

        middle_frame = tk.Frame(parent)
        middle_frame.pack()
        middle_left_frames = [tk.LabelFrame(middle_frame, text=i) for i in range(2)]
        [frame.pack(side=tk.LEFT, padx=2) for frame in middle_left_frames]
        for i in range(2):
            self.create_poke(middle_left_frames[i], self.left.pokemons[i], tk.LEFT)

        middle_right_frame = [tk.LabelFrame(middle_frame, text=i) for i in range(2)]
        [frame.pack(side=tk.RIGHT, padx=2) for frame in middle_right_frame]
        for i in range(2):
            self.create_poke(middle_right_frame[i], self.right.pokemons[i], tk.RIGHT)

        bottom_frame = tk.Frame(parent)
        bottom_frame.pack()
        bottom_left_frame = tk.Frame(bottom_frame)
        bottom_left_frame.pack(side=tk.LEFT, fill="both", expand=True)
        self.create_player(bottom_left_frame, self.left, tk.LEFT)

        bottom_right_frame = tk.Frame(bottom_frame)
        bottom_right_frame.pack(side=tk.RIGHT, fill="both", expand=True)
        self.create_player(bottom_right_frame, self.right, tk.RIGHT)

        self.field = Manager.FieldWidgetManager()
        bottom_center_frame = tk.LabelFrame(bottom_frame, text="状況")
        bottom_center_frame.pack()
        b_frame_1 = tk.Frame(bottom_center_frame)
        b_frame_1.pack()
        self.field.double_widget.variable.set(True)
        weather_frame = tk.LabelFrame(b_frame_1, text="天候")
        weather_frame.pack(side=tk.LEFT, padx=5)
        self.field.weather_widget.create(weather_frame, width=12)
        self.field.weather_widget.pack(side=tk.LEFT, padx=2, pady=2)
        field_frame = tk.LabelFrame(b_frame_1, text="フィールド")
        field_frame.pack(side=tk.LEFT, padx=5)
        self.field.field_widget.create(field_frame, width=12)
        self.field.field_widget.pack(side=tk.LEFT, padx=2, pady=2)
        b_frame_2 = tk.Frame(bottom_center_frame)
        b_frame_2.pack()
        self.field.gravity_widget.create(b_frame_2, width=12)
        self.field.gravity_widget.pack(side=tk.LEFT, padx=5, pady=2)
        self.field.wonder_room_widget.create(b_frame_2, width=12)
        self.field.wonder_room_widget.pack(side=tk.LEFT, padx=5, pady=2)
        self.field.magic_room_widget.create(b_frame_2, width=12)
        self.field.magic_room_widget.pack(side=tk.LEFT, padx=5, pady=2)

    def create_poke(self, parent, widget: PokeManager, side):
        top_frame = tk.Frame(parent)
        top_frame.pack()
        widget.hp_widget.create(top_frame)
        widget.hp_widget.hp_now_widget.create_slider(top_frame)
        widget.hp_widget.hp_now_widget.slider.pack()

        middle_2_frame = tk.Frame(parent)
        middle_2_frame.pack()
        terastal_frame = tk.LabelFrame(middle_2_frame, text="テラスタル")
        terastal_frame.grid(row=0, column=0)
        widget.terastal_widget.create(terastal_frame, width=6)
        widget.terastal_widget.pack(side=tk.LEFT, padx=5)
        widget.terastal_flag_widget.create(terastal_frame)
        widget.terastal_flag_widget.pack(side=tk.LEFT, padx=5)
        hp_now_frame = tk.LabelFrame(middle_2_frame, text="現在HP")
        hp_now_frame.grid(row=0, column=1)
        widget.hp_widget.hp_now_widget.create(hp_now_frame, ("Helvetica", 10, "bold"))
        widget.hp_widget.hp_now_widget.pack_widget()
        item_frame = tk.LabelFrame(middle_2_frame, text="もちもの")
        item_frame.grid(row=1, column=0)
        widget.item_widget.create(item_frame)
        widget.item_widget.config(width=14)
        widget.item_widget.pack(side=tk.LEFT, padx=5)
        bad_stat_frame = tk.LabelFrame(middle_2_frame, text="状態異常")
        bad_stat_frame.grid(row=1, column=1)
        widget.bad_stat_widget.create(bad_stat_frame, width=6)
        widget.bad_stat_widget.pack()
        ability_frame = tk.LabelFrame(middle_2_frame, text="とくせい")
        ability_frame.grid(row=2, column=0)
        widget.ability_widget.create(ability_frame, width=12)
        widget.ability_widget.pack(side=tk.LEFT)
        widget.ability_flag_widget.create(ability_frame)
        widget.ability_flag_widget.config(text="発動")
        widget.ability_flag_widget.pack(side=tk.LEFT)
        move_flag_frame = tk.LabelFrame(middle_2_frame, text="技効果")
        move_flag_frame.grid(row=2, column=1)
        widget.move_flag_widget.create(move_flag_frame, width=6)
        widget.move_flag_widget.config(text="発動")
        widget.move_flag_widget.pack()
        if side == tk.LEFT:
            widget.terastal_widget.config(state="disable")

        middle_frame = tk.Frame(parent)
        middle_frame.pack()
        font = ("MeiryoUI", 10)
        for i in range(6):
            widget.status_widget.widgets[i].status_label.create(middle_frame)
            widget.status_widget.widgets[i].status_label.config(width=3, font=("MeiryoUI", 12, "bold"))
            widget.status_widget.widgets[i].status_label.grid(row=0, column=i)
            widget.status_widget.widgets[i].individual.create(middle_frame)
            widget.status_widget.widgets[i].individual.config(width=3, font=font)
            widget.status_widget.widgets[i].effort.create(middle_frame)
            widget.status_widget.widgets[i].effort.config(width=3, font=font)
            widget.status_widget.widgets[i].individual.grid(row=1, column=i, padx=2, pady=1)
            widget.status_widget.widgets[i].effort.grid(row=2, column=i)
            if i == 0:
                rank = tk.Label(middle_frame, text="Rank")
                rank.grid(row=3, column=i)
            else:
                widget.rank_widgets[i-1].create(middle_frame)
                widget.rank_widgets[i-1].grid(row=3, column=i)
            if side == tk.LEFT:
                widget.status_widget.widgets[i].individual.disabled()
                widget.status_widget.widgets[i].effort.disabled()
            else:
                widget.status_widget.widgets[i].set_click()

        bottom_frame = tk.LabelFrame(parent, text="わざ")
        bottom_frame.pack()
        for i in range(4):
            widget.move_widgets[i].create(bottom_frame, width=14)
            widget.move_widgets[i].grid(row=i, column=0, padx=2)
            widget.move_counters[i].create(bottom_frame, width=2, font=("MeiryoUI", 12))
            widget.move_counters[i].grid(row=i, column=1, padx=2)
            widget.add_buttons[i].create(bottom_frame)
            widget.add_buttons[i].grid(row=i, column=2, padx=2)

    def create_player(self, parent, player: BattleManager, side):
        widget = player.player
        widget.a_wall_widget.create(parent, width=10)
        widget.c_wall_widget.create(parent, width=10)
        widget.wind_widget.create(parent, width=10)
        widget.help_widget.create(parent, width=10)
        widget.crit_widget.create(parent, width=10)
        col = 0 if side == tk.LEFT else 1
        widget.a_wall_widget.grid(row=0, column=col, padx=2, pady=2)
        widget.c_wall_widget.grid(row=1, column=col, padx=2, pady=2)
        widget.wind_widget.grid(row=2, column=col, padx=2, pady=2)
        col = 2 if side == tk.LEFT else 0
        widget.help_widget.grid(row=0, column=col, padx=2, pady=2)
        widget.crit_widget.grid(row=1, column=col, padx=2, pady=2)

    def update(self):
        self.damage_calc(tk.LEFT)
        self.damage_calc(tk.RIGHT)

    def field_check(self, side: str, attacker_index: int, target_index: int) -> Obj.SendData:
        def check_index(index: int) -> int:
            if index == 0:
                return 1
            else:
                return 0

        attacker = self.left.pokemons[check_index(attacker_index)] if side == tk.LEFT else self.right.pokemons[check_index(attacker_index)]
        target = self.right.pokemons[check_index(target_index)] if side == tk.LEFT else self.left.pokemons[check_index(target_index)]
        field = self.field.field_data.get()
        field.ability_1 = attacker.poke.ability.get()
        field.ability_2 = target.poke.ability.get()
        return field

    def damage_calc(self, side: str):
        attackers = self.left.pokemons if side == tk.LEFT else self.right.pokemons
        attacker_field = self.left.player.player if side == tk.LEFT else self.right.player.player
        targets = self.right.pokemons if side == tk.LEFT else self.left.pokemons
        target_party = self.right.party_manager if side == tk.LEFT else self.left.party_manager
        target_field = self.right.player.player if side == tk.LEFT else self.left.player.player

        for target_index, target in enumerate(targets):
            if target.poke.name.get():
                target_result_text: list[list[str]] = [
                    [f"無振:{target.poke.name.get()}: 現在HP{target.poke.hp_now.get()}"],
                    [f"特化:{target.poke.name.get()}: 現在HP{target.poke.hp_now.get()}"],
                    [f"入力:{target.poke.name.get()}: 現在HP{target.poke.hp_now.get()}"]
                    ]
                target_result_dmg: list[list[list[int]]] = [[[] for _ in range(16)] for _ in range(3)]
                for attacker_index, poke in enumerate(attackers):
                    if poke.poke.name.get():
                        field = self.field_check(side, attacker_index, target_index)
                        calc = Calc.DamageCalculator(poke.poke.get(), attacker_field.get(), target.poke.get(), target_field.get(), field)
                        calc_max = Calc.DamageCalculator(poke.poke.get(), attacker_field.get(), target.poke.craete_any_stat(True), target_field.get(), field)
                        calc_min = Calc.DamageCalculator(poke.poke.get(), attacker_field.get(), target.poke.craete_any_stat(), target_field.get(), field)
                        for index, calc_flag in enumerate(poke.poke.calc_list):
                            if calc_flag.get() and poke.poke.move_list[index].get():
                                move_name = poke.poke.move_list[index].get()
                                for index, _calc in enumerate([calc_max, calc_min, calc]):
                                    _calc.calculation(move_name)
                                    dmg_list = [_calc.final_calc(0.85 + i * 0.01) for i in range(16)]
                                    target_result_text[index].append(f"{poke.poke.name.get()}: {move_name}")
                                    [target_result_dmg[index][dmg_index].append(dmg) for dmg_index, dmg in enumerate(dmg_list)]
                                    target_result_text[index].append(f"最低乱数 {' '.join(map(str, dmg_list))} 最高乱数")
                                    [target_result_text[index].append(log) for log in _calc.log + _calc.calc_log]
                                    target_result_text[index].append("------------------------------------------------------------")
                target_result_dmg = [
                    [sum(dmg_list) for dmg_list in target_result_dmg[0]],
                    [sum(dmg_list) for dmg_list in target_result_dmg[1]],
                    [sum(dmg_list) for dmg_list in target_result_dmg[2]]
                ]
                target.hp_widget.update(
                    [(target_result_dmg[0][0], target_result_dmg[0][-1], target_result_text[0]),
                    (target_result_dmg[1][0], target_result_dmg[1][-1], target_result_text[1]),
                    (target_result_dmg[2][0], target_result_dmg[2][-1], target_result_text[2])]
                )
        field = self.field.field_data.get()
        for widget_index, enemy in enumerate(target_party.list):
            if enemy.name.get():
                max_dmg, min_dmg = [], []
                for poke in attackers:
                    if poke.poke.name.get():
                        if [status.effort.get() for status in enemy.status_list] == [0, 0, 0, 0, 0, 0]:
                            max_calc = Calc.DamageCalculator(poke.poke.get(), attacker_field, enemy.craete_any_stat(), target_field, field)
                            min_calc = Calc.DamageCalculator(poke.poke.get(), attacker_field, enemy.craete_any_stat(True), target_field, field)
                        else:
                            max_calc = Calc.DamageCalculator(poke.poke.get(), attacker_field, enemy.get(), target_field, field)
                            min_calc = Calc.DamageCalculator(poke.poke.get(), attacker_field, enemy.get(), target_field, field)
                        for index, calc_flag in enumerate(poke.poke.calc_list):
                            if calc_flag.get() and poke.poke.move_list[index].get():
                                move_name = poke.poke.move_list[index].get()
                                max_calc.calculation(move_name)
                                min_calc.calculation(move_name)
                                max_dmg.append(max_calc.final_calc(1.00))
                                min_dmg.append(min_calc.final_calc(0.85))
                target_party.widget.buttons[widget_index].update((sum(min_dmg), sum(max_dmg)))



class Page6:
    class WidgetManager(Manager.PokeWidgetManager):
        def __init__(self):
            super().__init__(Obj.PokeDetail())

    def __init__(self, parent):
        self.widget = self.WidgetManager()
        top_frame = tk.Frame(parent)
        top_frame.pack(pady=5)
        name_frame = tk.LabelFrame(top_frame, text="ポケモン名")
        name_frame.pack(side=tk.LEFT, padx=5)
        self.widget.name_widget.create(name_frame)
        self.widget.name_widget.pack(padx=5, pady=5)

        level_frame = tk.LabelFrame(top_frame, text="Lv")
        level_frame.pack(side=tk.LEFT, padx=5)
        self.widget.level_widget.create(level_frame)
        self.widget.level_widget.pack(padx=5, pady=5)

        terastal_frame = tk.LabelFrame(top_frame, text="テラスタル")
        terastal_frame.pack(side=tk.LEFT, padx=5)
        self.widget.terastal_widget.create(terastal_frame)
        self.widget.terastal_widget.config(width=10)
        self.widget.terastal_widget.pack(padx=5, pady=5)

        ability_frame = tk.LabelFrame(top_frame, text="とくせい")
        ability_frame.pack(side=tk.LEFT, padx=5)
        self.widget.ability_widget.create(ability_frame)
        self.widget.ability_widget.pack(padx=5, pady=5)

        item_frame = tk.LabelFrame(top_frame, text="もちもの")
        item_frame.pack(side=tk.LEFT, padx=5)
        self.widget.item_widget.create(item_frame)
        self.widget.item_widget.pack(padx=5, pady=5)

        move_frame = tk.Frame(parent)
        move_frame.pack(pady=5)
        for i in range(4):
            frame = tk.LabelFrame(move_frame, text=f"わざ_{i+1}")
            frame.pack(side=tk.LEFT, padx=5)
            self.widget.move_widgets[i].create(frame)
            self.widget.move_widgets[i].pack(padx=5, pady=5)

        middle_frame = tk.Frame(parent)
        middle_frame.pack(pady=10)
        status_frame = tk.Frame(middle_frame)
        status_frame.pack(side=tk.LEFT)
        self.widget.status_widget.create(status_frame)

        labels = [tk.Label(status_frame, text=label) for label in ["", "実数値", "個体値", "努力値", "性格"]]
        self.effrot_label = tk.Label(status_frame, text=510, font=("Helvetica", 12, "bold"))
        labels.insert(4, self.effrot_label)
        [widget.grid(row=0, column=index) for index, widget in enumerate(labels)]

        labels = [tk.Label(status_frame, text=label) for label in ["HP", "攻撃", "防御", "特攻", "特防", "素早"]]
        [label.grid(row=index+1, column=0) for index, label in enumerate(labels)]
        for index, widget in enumerate(self.widget.status_widget.widgets):
            widget.status_label.grid(row=index+1, column=1, padx=5)
            widget.individual.grid(row=index+1, column=2, padx=5)
            widget.effort.slider.grid(row=index+1, column=3, padx=5)
            widget.effort.grid(row=index+1, column=4, padx=5)
            if index:
                widget.nature.grid(row=index+1, column=5, padx=5)

