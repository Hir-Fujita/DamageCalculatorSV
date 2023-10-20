#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Union
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
    def __init__(self, parent, manager: Manager.Manager):
        self.manager = manager
        self.widget = Manager.StatusWidgetManager(Obj.Poke())
        self.widget.set_dic()
        self.widget.add_update_method(self.update)
        top_frame = tk.Frame(parent)
        top_frame.pack(pady=5)
        name_frame = tk.LabelFrame(top_frame, text="ポケモン名")
        name_frame.pack(side=tk.LEFT, padx=5)
        self.widget.name_widget.create(name_frame)
        # self.widget.name_widget.method = self.name_widget_func
        self.widget.name_widget.pack(padx=5, pady=5)

        level_frame = tk.LabelFrame(top_frame, text="Lv")
        level_frame.pack(side=tk.LEFT, padx=5)
        self.widget.level_widget.create(level_frame)
        # self.widget.level_widget.method = self.update
        self.widget.level_widget.pack(padx=5, pady=5)

        terastal_frame = tk.LabelFrame(top_frame, text="テラスタル")
        terastal_frame.pack(side=tk.LEFT, padx=5)
        self.widget.terastal_widget.create(terastal_frame)
        self.widget.terastal_widget.config(width=10)
        # self.widget.terastal_widget.method = self.update
        self.widget.terastal_widget.pack(padx=5, pady=5)

        ability_frame = tk.LabelFrame(top_frame, text="とくせい")
        ability_frame.pack(side=tk.LEFT, padx=5)
        self.widget.ability_widget.create(ability_frame)
        self.widget.ability_widget.pack(padx=5, pady=5)

        item_frame = tk.LabelFrame(top_frame, text="もちもの")
        item_frame.pack(side=tk.LEFT, padx=5)
        self.widget.item_widget.create(item_frame)
        # self.widget.item_widget.method = self.update
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
        [widget.create(status_frame) for widget in self.widget.status_widgets]
        [widget.status_label.config(font=("Helvetica", 20, "bold")) for widget in self.widget.status_widgets]

        labels = [tk.Label(status_frame, text=label) for label in ["", "実数値", "個体値", "努力値", "性格"]]
        self.effrot_label = tk.Label(status_frame, text=510, font=("Helvetica", 12, "bold"))
        labels.insert(4, self.effrot_label)
        [widget.grid(row=0, column=index) for index, widget in enumerate(labels)]

        labels = [tk.Label(status_frame, text=label) for label in ["HP", "攻撃", "防御", "特攻", "特防", "素早"]]
        [label.grid(row=index+1, column=0) for index, label in enumerate(labels)]
        for index, widget in enumerate(self.widget.status_widgets):
            widget.status_label.grid(row=index+1, column=1, padx=5)
            widget.individual.grid(row=index+1, column=2, padx=5)
            widget.effort.slider.grid(row=index+1, column=3, padx=5)
            widget.effort.grid(row=index+1, column=4, padx=5)
            if index:
                widget.nature.grid(row=index+1, column=5, padx=5)

        if self.manager.image_flag:
            img_frame = tk.Frame(middle_frame)
            img_frame.pack(side=tk.LEFT, padx=10)
            self.img_label = tk.Label(img_frame)
            self.generate_image()
            self.img_label.pack(side=tk.BOTTOM)

        bottom_frame = tk.Frame(parent)
        bottom_frame.pack()
        memo_frame = tk.LabelFrame(bottom_frame, text="メモ欄")
        memo_frame.pack()
        self.memo_widget = Wid.CustomTextBox(width=50, height=5, font=("Meiryo UI", 20, "bold"))
        self.memo_widget.create(memo_frame)
        self.memo_widget.pack()

    def generate_image(self):
        self.img = Pr.ImageGenerator.create_page1(self.widget.poke.name, self.widget.poke.item, self.widget.poke.terastal)
        self.img_label.config(image=self.img)

    def name_widget_func(self):
        self.widget.name_widget_func()
        self.generate_image()
        self.memo_widget.delete()
        self.update()

    def update(self):
        self.sum_effort()
        self.generate_image()

    def sum_effort(self):
        result = 510 - sum(status.effort for status in self.widget.poke.status_list)
        self.effrot_label.config(text=result)
        if result < 0:
            self.effrot_label.config(foreground="red")
        else:
            self.effrot_label.config(foreground="black")

    def save_poke(self):
        if self.save_check():
            path = Data.save_filedialogwindow(f"{self.poke.name}@{self.poke.item}", "ポケモン保存", "Pokemon", ("text_file", "txt"))
            if path:
                save_data = [self.poke.name, self.poke.level, self.poke.item, self.poke.ability, self.poke.terastal]
                save_data.append("/".join([move for move in self.poke.move_list]))
                for index, status in enumerate(self.poke.status_list):
                    if index == 0:
                        save_data.append(f"{str(status.individual)}/{str(status.effort)}")
                    else:
                        save_data.append(f"{str(status.individual)}/{str(status.effort)}/{str(status.nature)}")
                [save_data.append(m) for m in self.memo_widget.get().split("\n") if m != ""]
                with open(path, "w", encoding="UTF-8") as f:
                    [f.writelines(f"{data}\n") for data in save_data]

    def save_check(self):
        if self.poke.name == "":
            messagebox.showerror(title="error", message="ポケモンが選択されていません")
            return False
        if self.poke.ability == "":
            messagebox.showerror(title="error", message="とくせいが選択されていません")
            return False
        if self.poke.terastal == "":
            messagebox.showerror(title="error", message="テラスタルが選択されていません")
            return False
        if int(self.effrot_label["text"]) < 0:
            messagebox.showerror(title="error", message="努力値が不正です")
            return False
        return True

    def load_poke(self):
        path = Data.open_filedialogwindow("ポケモン読み込み", "Pokemon", ("text_file", "txt"))
        if path:
            data = Data.PokeData(path)
            self.poke.generate(data.name)
            self.name_widget.set(data.name)
            self.level_widget.set(data.level)
            self.item_widget.set(data.item)
            self.ability_widget.set(data.ability)
            self.terastal_widget.set(data.terastal)
            [self.move_widgets[i].set(data.move_list[i]) for i in range(4)]
            for index, widget in enumerate(self.status_widgets):
                widget.individual.set(data.status[index][0])
                widget.effort.set(data.status[index][1])
                if index != 0:
                    widget.nature.set(data.status[index][2])
                    widget.status_label.color_change(data.status[index][2])
            self.update()
            self.memo_widget.widget.delete()
            [self.memo_widget.widget.set(f"{m}\n") for m in data.memo]

class Page2:
    def __init__(self, parent, manager: Manager.Manager):
        frame = tk.Frame(parent)
        frame.pack(pady=5)
        self.manager = manager
        self.widgets: "list[Wid.BannerWidget]" = [Wid.BannerWidget(frame, self.children_method, i) for i in range(6)]
        for index, widget in enumerate(self.widgets):
            if index < 3:
                widget.widget.grid(row=0, column=index)
            else:
                widget.widget.grid(row=1, column=index-3)

        right_frame = tk.Frame(parent)
        right_frame.pack(fill=tk.BOTH)
        self.default_text = "左クリックでポケモンを登録\n右クリックでポケモンを削除"
        self.text_variable = tk.StringVar(value=self.default_text)
        text_label = tk.Label(right_frame, textvariable=self.text_variable, font=("Meiryo UI", 20, "bold"),
                              anchor=tk.CENTER)
        text_label.pack(padx=5, fill=tk.BOTH)

    def children_method(self, event: str, index: int=None):
        if event == "Leave":
            self.text_variable.set(self.default_text)
        elif event == "Enter":
            text = "\n".join(self.widgets[index].data.memo)
            self.text_variable.set(text)
        elif event == "Button-1":
            self.manager.party[index].re_init(self.widgets[index].data)
        elif event == "Button-3":
            self.manager.party[index].reset()
            self.text_variable.set(self.default_text)

    def save_party(self):
        path = Data.save_filedialogwindow("", "パーティ登録", "Party", ("party_data", ".party"))
        if path:
            write_data = [widget.data.save() if widget.data is not None else [] for widget in self.widgets]
            Data.save_file(path, write_data)

    def load_party(self):
        path = Data.open_filedialogwindow("パーティ読み込み", "Party", ("party_data", ".party"))
        if path:
            data_list = Data.open_file(path)
            for index, widget in enumerate(self.widgets):
                data = Data.PokeData(data_list[index])
                widget.load(data)

class Page3:
    def __init__(self, parent):
        frame = tk.Frame(parent)
        frame.pack()
        self.id_dic = Obj.PokeDict()

        left_frame = tk.Frame(frame)
        left_frame.pack(side=tk.LEFT, anchor=tk.W)
        self.left = Manager.StatusWidgetManagerPlus(Obj.PokeDetail())
        self.left_field = Manager.PlayerFieldManager(Obj.PlayerField())
        self.create(left_frame, self.left, self.left_field, tk.LEFT)

        right_frame = tk.Frame(frame)
        right_frame.pack(side=tk.RIGHT, anchor=tk.E)
        self.right = Manager.StatusWidgetManagerPlus(Obj.PokeDetail())
        self.right_field = Manager.PlayerFieldManager(Obj.PlayerField())
        self.create(right_frame, self.right, self.right_field, tk.RIGHT)

        self.manager = {
            tk.LEFT: self.left,
            tk.RIGHT: self.right
        }

        self.field_manager = Manager.FieldWidgetManager(Obj.Field())
        center_frame = tk.LabelFrame(frame, text="状況")
        center_frame.pack(side=tk.BOTTOM, anchor=tk.S)
        self.field_manager.image_label.create(center_frame, False)
        self.field_manager.image_label.pack(padx=10, pady=2)
        self.field_manager.double_widget.create(center_frame)
        self.field_manager.double_widget.pack(padx=5, pady=2)
        self.field_manager.weather_widget.create(center_frame)
        self.field_manager.weather_widget.pack_widget(padx=5, pady=2)
        self.field_manager.field_widget.create(center_frame)
        self.field_manager.field_widget.pack_widget(padx=5, pady=2)
        self.field_manager.field_ability_widget_1.create(center_frame)
        self.field_manager.field_ability_widget_1.pack_widget(padx=5, pady=2)
        self.field_manager.field_ability_widget_2.create(center_frame)
        self.field_manager.field_ability_widget_2.pack_widget(padx=5, pady=2)
        self.field_manager.config()

        result_frame = tk.Frame(parent)
        result_frame.pack()
        self.left.result_widget.create(result_frame)
        self.left.result_widget.pack(side=tk.LEFT, padx=2)
        self.right.result_widget.create(result_frame)
        self.right.result_widget.pack(side=tk.LEFT, padx=2)

    def create(self, frame, manager: Manager.StatusWidgetManagerPlus, field: Manager.PlayerFieldManager, side):
        out_frame = tk.Frame(frame)
        out_frame.pack(side=side, padx=5)
        manager.button_widget.create(out_frame, side, self.change)
        manager.button_widget.pack()
        in_frame = tk.Frame(frame)
        in_frame.pack(side=side, padx=5)
        top_frame = tk.Frame(in_frame)
        top_frame.pack()
        manager.name_widget.create(top_frame)
        manager.name_widget.pack_widget(tk.LEFT)
        manager.level_widget.create(top_frame)
        manager.level_widget.pack_widget(tk.LEFT)
        manager.item_widget.create(top_frame)
        manager.item_widget.config(width=14)
        manager.item_widget.pack_widget(tk.LEFT)

        frame_2 = tk.Frame(in_frame)
        frame_2.pack()
        manager.ability_widget.create(frame_2)
        manager.ability_widget.config(width=12)
        manager.ability_widget.pack_widget(tk.LEFT)
        manager.ability_widget.widget.add_tuggle_button(manager.ability_widget, "特性発動", manager.update)
        manager.ability_widget.widget.t_button.pack(side=tk.LEFT, padx=5)
        manager.terastal_widget.create(frame_2)
        manager.terastal_widget.config(width=12)
        manager.terastal_widget.pack_widget(tk.LEFT, padx=5)
        manager.terastal_widget.widget.add_tuggle_button(manager.terastal_widget, "テラスタル", manager.update)
        manager.terastal_widget.widget.t_button.pack(side=tk.LEFT, padx=5)

        frame_3 = tk.Frame(in_frame)
        frame_3.pack()
        status_frame = tk.LabelFrame(frame_3, text="ステータス")
        status_frame.pack(side=side)
        labels = [tk.Label(status_frame, text=l, font=("Meiryo UI", 10)) for l in ["", "HP", "攻撃", "防御", "特攻", "特防", "素早"]]
        rows = [tk.Label(status_frame, text=l, font=("Meiryo UI", 10)) for l in ["実数値", "個体値", "努力値", "性格", "ランク"]]
        [label.grid(row=0, column=index) for index, label in enumerate(labels)]
        [row.grid(row=index+1, column=0) for index, row in enumerate(rows)]
        for index, widget in enumerate(manager.status_widgets):
            widget.create(status_frame)
            widget.status_label.config(font=("Meiryo UI", 12, "bold"))
            widget.status_label.grid(row=1, column=index+1, padx=1, pady=2)
            widget.individual.grid(row=2, column=index+1, padx=1, pady=2)
            widget.individual.config(width=3)
            widget.effort.config(width=3)
            widget.effort.grid(row=3, column=index+1, padx=1, pady=2)
            if index != 0:
                widget.nature.grid(row=4, column=index+1, padx=1, pady=2)
                manager.rank_widgets[index-1].create(status_frame)
                manager.rank_widgets[index-1].grid(row=5, column=index+1, padx=1, pady=2)
        situation_frame = tk.Frame(frame_3)
        situation_frame.pack(side=side)
        field.a_wall_widget.create(situation_frame)
        field.a_wall_widget.pack(padx=10, pady=1)
        field.c_wall_widget.create(situation_frame)
        field.c_wall_widget.pack(padx=10, pady=1)
        field.wind_widget.create(situation_frame)
        field.wind_widget.pack(padx=10, pady=1)
        field.help_widget.create(situation_frame)
        field.help_widget.pack(padx=10, pady=1)
        field.crit_widget.create(situation_frame)
        field.crit_widget.pack(padx=10, pady=1)
        manager.move_flag_widget.create(situation_frame)
        manager.move_flag_widget.pack(padx=10, pady=1)

        frame_4 = tk.Frame(in_frame)
        frame_4.pack()
        if side == tk.LEFT:
            manager.image_label.create(frame_4, mirror=True)
        else:
            manager.image_label.create(frame_4, mirror=False)
        manager.image_label.pack(side=side)
        frame_4_1 = tk.Frame(frame_4)
        frame_4_1.pack(side=side)
        frame4_1_top = tk.Frame(frame_4_1)
        frame4_1_top.pack()
        manager.hp_now_widget.create(frame4_1_top)
        manager.hp_now_widget.pack(side=side)
        manager.hp_now_widget.widget.pack(side=tk.LEFT)
        manager.hp_now_widget.widget.label.pack(side=tk.LEFT)
        manager.hp_now_widget.widget.max_label.pack(side=tk.LEFT)
        manager.bad_stat_widget.create(frame4_1_top)
        manager.bad_stat_widget.pack_widget(side)
        move_frame = tk.LabelFrame(frame_4_1, text="わざ")
        move_frame.pack()
        for index, widget in enumerate(manager.move_widgets):
            widget.create(move_frame)
            widget.config(width=12)
            widget.grid(row=index, column=0, padx=5, pady=2)
            widget.add_button(move_frame, "計算", lambda index=index:self.damage_calc(side, index))
            widget.button.grid(row=index, column=1, padx=3, pady=2)
            widget.add_tuggle_button(move_frame, "ロック", lambda index=index:self.damage_calc(side, index, True))
            widget.t_button.grid(row=index, column=2, padx=3, pady=2)
        manager.config()
        field.config()

    def damage_calc(self, side: str, move_index: int, lock: bool=False):
        result = self.lock_calc(side)
        if side == tk.LEFT:
            attacker = self.left.poke
            attacker_field = self.left_field
            target = self.right.poke
            target_field = self.right_field
            widget = self.right.result_widget
            not_side = tk.RIGHT
        else:
            attacker = self.right.poke
            attacker_field = self.right_field
            target = self.left.poke
            target_field = self.left_field
            widget = self.left.result_widget
            not_side = tk.LEFT
        if attacker.name and target.name and attacker.move_list[move_index]:
            if lock:
                data = attacker.copy()
                res = self.id_dic.access(side, move_index, data)
                self.manager[side].move_widgets[move_index].t_button.set(res)
            else:
                before_hp = target.hp_now
                target.hp_now = before_hp - result
                calculator = Calc.DamageCalculator(attacker, attacker_field.player, target, target_field.player, self.field_manager.field_data, move_index)
                calculator.calculation()
                widget.update(calculator)
                target.hp_now = before_hp
                self.manager[not_side].hp_now_widget.widget.set(before_hp)
        else:
            self.manager[side].move_widgets[move_index].t_button.set(False)
            widget.reset()

    def change(self, side: str, index: int):
        self.manager[side].name_widget.widget.values_reset()
        main_poke = self.manager[side].poke.copy()
        button_poke = self.manager[side].button_widget.copy(index)
        self.manager[side].poke.paste(button_poke)
        self.manager[side].widget_update()
        lock = self.id_dic.key_check(side, main_poke["id"])
        self.manager[side].button_widget.paste(index, main_poke, lock)
        result = self.id_dic.move_index_check(side, button_poke["id"])
        [widget.t_button.set(False) for widget in self.manager[side].move_widgets]
        [self.manager[side].move_widgets[index].t_button.set(True) for index in result]

    def lock_calc(self, side: str):
        if side == tk.LEFT:
            attacker = self.left.poke
            target = self.right.poke
        else:
            attacker = self.right.poke
            target = self.left.poke
        result = []
        save = attacker.copy()
        for _, values in self.id_dic.dic[side].items():
            attacker.paste(values[0])
            for index in values[1:]:
                calc = Calc.DamageCalculator(attacker, target, self.field_manager.field_data, index)
                calc.calculation()
                result.append(calc.final_calc(0.85))
        attacker.paste(save)
        return sum(result)

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
    """
    ダブルバトル
    """
    def __init__(self, parent, manager: Manager.Manager):
        self.manager = manager
        self.battle_manager = Manager.DoubleBattleManager()
        left_frame = tk.Frame(parent)
        left_frame.pack(side=tk.LEFT)
        self.battle_manager.left.party_widget.create(left_frame, self.manager.party)

        right_frame = tk.Frame(parent)
        right_frame.pack(side=tk.RIGHT)
        self.battle_manager.right.party_widget.create(right_frame, self.manager.party)

        top_frame = tk.Frame(parent)
        top_frame.pack()
        self.battle_manager.timer_widget.create(top_frame, self.manager.master)

        middle_frame = tk.Frame(parent)
        middle_frame.pack()
        middle_left_frames = [tk.LabelFrame(middle_frame, relief=tk.SOLID, bd=2, text=i) for i in range(2)]
        [frame.pack(side=tk.LEFT, fill="both", expand=True, padx=5) for frame in middle_left_frames]
        self.battle_manager.left.create(middle_left_frames)

        middle_right_frames = [tk.LabelFrame(middle_frame, relief=tk.SOLID, bd=2, text=i) for i in range(2)]
        [frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=5) for frame in middle_right_frames]
        self.battle_manager.right.create(middle_right_frames)


class Page6:
    def __init__(self, parent):
        a = tk.Label(parent, text="a")
        a.pack()


class Page7:
    def __init__(self, parent):
        a = tk.Label(parent, text="a")
        a.pack()


class Page8:
    def __init__(self, parent):
        a = tk.Label(parent, text="a")
        a.pack()
