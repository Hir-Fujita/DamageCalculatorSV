#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Tuple, Union, Callable
import tkinter as tk
from tkinter import ttk
import time
import threading as th
import math

import Data
import Object as Obj
import Process as Pr
import Calculation as Calc

class TimeCounter:
    @classmethod
    def start(self):
        self.start_time = time.time()

    @classmethod
    def stop(self, text: str=""):
        result = time.time() - self.start_time
        print(f"{text}にかかった時間: {result} 秒")


class Method:
    def __init__(self, method: Callable=None):
        if method is None:
            self.method = []
        else:
            self.method = [method]

    def add_method(self, *methods: Callable):
        [self.method.append(met) for met in methods]

    def run_method(self):
        if self.method != []:
            [method() for method in self.method]


class CustomTextBox(tk.Text):
    def create(self, parent):
        self.widget = tk.Text(parent)
        scroll_x = tk.Scrollbar(parent, orient='horizontal', command=self.widget.xview)
        scroll_y = tk.Scrollbar(parent, orient='vertical', command=self.widget.yview)
        self.widget.config(xscrollcommand=scroll_x.set)
        self.widget.config(yscrollcommand=scroll_y.set)
        scroll_x.grid(row=1, column=0,sticky=tk.W + tk.E)
        scroll_y.grid(row=0, column=1,sticky=tk.N + tk.S)

    def pack(self):
        self.widget.grid(row=0, column=0)

    def get(self):
        return self.widget.get("1.0", tk.END)

    def set(self, value):
        print(type(value))
        self.widget.insert("end", value)

    def delete(self):
        self.widget.delete("1.0", tk.END)




class CustomCommboBox(ttk.Combobox, Method):
    def __init__(self, value: tk.Variable, values: Data.CSV=None, method: Callable=None, plus_delete: bool=False):
        Method.__init__(self, method)
        self.values = values
        self.plus_delete = plus_delete
        self.variable = value

    def create(self, parent, **kw):
        ttk.Combobox.__init__(self, parent, textvariable=self.variable, **kw, font=("Meiryo UI", 10))
        if isinstance(self.values, Data.CSV):
            self.config(values=self.values.name_list)
            self.bind("<KeyRelease-BackSpace>", lambda event:self.values_update(False))
            self.bind("<KeyRelease-Return>", lambda event:self.values_update(True))
        else:
            self.config(values=self.values)
        self.bind("<<ComboboxSelected>>", lambda event: self.selected())

    def set(self, value):
        self.variable.set(value)
        self.selected()

    def selected(self):
        self.run_method()

    def reset(self):
        self.set("")
        if isinstance(self.values, Data.CSV):
            self.config(values=self.values.name_list)
        else:
            self.config(values=self.values)

    def values_reset(self):
        self.config(values=self.values.name_list)

    def values_update(self, flag: bool):
        input = self.get()
        values = self.values.autocomplete(input, self.plus_delete)
        self.config(values=values)
        if len(values) == 1 and flag:
            self.set(values[0])
            self.run_method()
            if isinstance(self.values, Data.CSV):
                self.config(values=self.values.name_list)
            else:
                self.config(values=self.values)

    def values_config(self, values: "list[str]"):
        self.config(values=values)
        if len(values) == 1:
            self.set(values[0])


class CustomSpinBox(tk.Spinbox, Method):
    def __init__(self, method: Callable=None):
        Method.__init__(self, method)
        self.increment: int
        self.variable: tk.IntVar
        self.max: int
        self.min: int

    def create(self, parent, **kw):
        tk.Spinbox.__init__(self, parent, **kw)
        self.config(from_=self.min, to=self.max, increment=self.increment, textvariable=self.variable, command=self.key_input)
        self.bind("<MouseWheel>", lambda event: self.mousewheel(event))
        self.bind("<Button-3>", lambda event: self.rightclick())
        self.bind("<KeyRelease>", lambda event: self.key_input())

    def get(self) -> int:
        return self.variable.get()

    def set(self, value: int):
        self.variable.set(int(value))

    def mousewheel(self, event: tk.Event):
        if event.delta > 0:
            self.set(self.value_check(self.variable.get() + self.increment))
        else:
            self.set(self.value_check(self.variable.get() - self.increment))
        self.run_method()

    def value_check(self, value: int) -> int:
        if value > self.max:
            return self.max
        elif value < self.min:
            return self.min
        else:
            return value

    def rightclick(self):
        if self.get() != self.max:
            self.set(self.max)
        else:
            self.set(self.min)
        self.run_method()

    def key_input(self):
        self.set(self.value_check(self.variable.get()))
        self.run_method()

    def disabled(self):
        self.bind("<MouseWheel>", lambda event: self.dummy_function())
        self.bind("<Button-3>", lambda event: self.dummy_function())
        self.bind("<KeyRelease>", lambda event: self.dummy_function())
        self.config(state=tk.DISABLED)

    def dummy_function(self):
        pass


class CustomLevelBox(CustomSpinBox):
    def __init__(self, value: tk.Variable, method: Callable=None):
        CustomSpinBox.__init__(self, method)
        self.variable = value
        self.max = 100
        self.min = 1
        self.increment = 1

    def rightclick(self):
        self.variable.set(50)
        self.run_method()

    def get(self) -> int:
        return self.variable.get()

    def set(self, value: int):
        self.variable.set(int(value))

    def key_input(self):
        self.set(self.value_check(self.variable.get()))
        self.run_method()

class CustomRankBox(CustomSpinBox):
    def __init__(self, value: tk.Variable, method: Callable=None):
        CustomSpinBox.__init__(self, method)
        self.variable = value
        self.values = ["-6", "-5", "-4", "-3", "-2", "-1", "", "+1", "+2", "+3", "+4", "+5", "+6"]

    def create(self, parent, **kw):
        tk.Spinbox.__init__(self, parent, **kw)
        self.config(textvariable=self.variable, font=("Helvetica", 10), values=self.values, width=3)
        self.variable.set("")
        self.bind("<MouseWheel>", lambda event: self.mousewheel(event))
        self.bind("<Button-3>", lambda event: self.rightclick())

    def set(self, value):
        self.variable.set(value)

    def rightclick(self):
        self.set("")
        self.run_method()

    def mousewheel(self, event: tk.Event):
        index = self.values.index(self.variable.get())
        if event.delta > 0:
            if index < len(self.values)-1:
                self.set(self.values[index+1])
        else:
            if index > 0:
                self.set(self.values[index-1])
        self.run_method()

    def reset(self):
        self.set("")


class CustomHPNowBox(tk.Spinbox, Method):
    def __init__(self, value: tk.Variable, max_value: tk.Variable, method: Callable=None):
        Method.__init__(self, method)
        self.max_variable = max_value
        self.now_variable = value

    def create(self, parent, font=None):
        tk.Spinbox.__init__(self, parent)
        self.config(textvariable=self.now_variable, width=3, command=self.run_method, from_=1, to=1, increment=1)
        self.bind("<MouseWheel>", lambda event: self.mousewheel(event))
        self.bind("<Button-3>", lambda event: self.rightclick())
        self.bind("<KeyRelease>", lambda event: self.key_input())
        self.label = tk.Label(parent, text="/")
        self.max_label = tk.Label(parent, textvariable=self.max_variable, width=3)
        if font is not None:
            self.config(font=font)
            self.label.config(font=font)
            self.max_label.config(font=font)

    def pack_widget(self):
        self.pack(side=tk.LEFT)
        self.label.pack(side=tk.LEFT)
        self.max_label.pack(side=tk.LEFT)

    def create_slider(self, parent):
        self.slider = ttk.Scale(parent, orient="horizontal", variable=self.now_variable, from_=0, to=self.max_variable.get(), length=210, command=lambda event: self.scale())

    def slider_update(self):
        self.slider.config(to=self.max_variable.get())
        self.slider.set(self.now_variable.get())

    def mousewheel(self, event: tk.Event):
        if event.delta > 0:
            self.now_variable.set(self.value_check(self.now_variable.get() + 1))
        else:
            self.now_variable.set(self.value_check(self.now_variable.get() - 1))
        self.run_method()

    def value_check(self, value: int) -> int:
        if value > self.max_variable.get():
            return self.max_variable.get()
        elif value < 1:
            return 1
        else:
            return value

    def rightclick(self):
        if self.now_variable.get() != self.max_variable.get():
            self.now_variable.set(self.max_variable.get())
        self.run_method()

    def key_input(self):
        self.now_variable.set(self.value_check(self.now_variable.get()))
        self.run_method()

    def scale(self):
        self.now_variable.set(int(self.slider.get()))
        self.run_method()


class CustomCountBox(CustomSpinBox):
    def __init__(self, value: tk.IntVar, method: Callable=None):
        CustomSpinBox.__init__(self, method)
        self.variable = value
        self.increment = 1
        self.min = 0
        self.max = 99

    def rightclick(self):
        raise NotImplementedError

    def key_input(self):
        raise NotImplementedError


class CustomButton(tk.Button, Method):
    def __init__(self, text: str, method: Callable=None):
        self.variable = tk.StringVar(value=text)
        Method.__init__(self, method)

    def create(self, parent):
        tk.Button.__init__(self, parent, textvariable=self.variable)
        self.config(command=self.click)

    def click(self):
        self.run_method()

    def set(self, value: str):
        self.variable.set(value)


class CustomTuggleButton(tk.Button, Method):
    def __init__(self, text: str, value: tk.Variable, method: Callable=None,):
        self.text = text
        self.variable = value
        Method.__init__(self, method)

    def create(self, parent, **kw):
        tk.Button.__init__(self, parent, text=self.text, **kw)
        self.config(command=self.click)

    def set(self, value: bool):
        self.variable.set(value)
        self.update()
        self.run_method()

    def click(self):
        self.set(not self.get())

    def reset(self):
        self.variable.set(False)
        self.update()

    def update(self):
        if self.get():
            self.config(relief=tk.SUNKEN)
        else:
            self.config(relief=tk.RAISED)

    def get(self) -> bool:
        return self.variable.get()


class CustomImageLabel(tk.Label):
    def __init__(self, create_method: Callable, method: Callable=None):
        self.create_method = create_method
        self.method = method

    def create(self, parent):
        tk.Label.__init__(self, parent)
        self.image = self.create_method()
        self.config(image=self.image)
        self.pack()

    def update(self):
        self.image = self.create_method()
        self.config(image=self.image)

class StatusWidgets:
    class StatusWidget:
        class CustomLabel(tk.Label):
            def __init__(self):
                self.variable = tk.StringVar(value=1)

            def create(self, parent):
                tk.Label.__init__(self, parent, textvariable=self.variable)

            def get(self):
                return self.variable.get()

            def set(self, value):
                self.variable.set(value)

            def color_change(self, color: Union[float, str]):
                if isinstance(color, float):
                    color = self.float_color(color)
                self.config(foreground=color)

            def float_color(self, value):
                if value == 1:
                    return "black"
                elif value == 0.9:
                    return "blue"
                elif value == 1.1:
                    return "red"

        class CustomIndividualBox(CustomSpinBox):
            def __init__(self, value: tk.IntVar,  method: Callable=None):
                CustomSpinBox.__init__(self, method)
                self.variable = value
                self.max = 31
                self.min = 0
                self.increment = 1

        class CustomEffortBox(CustomSpinBox):
            def __init__(self, value: tk.IntVar, method: Callable=None):
                CustomSpinBox.__init__(self, method)
                self.variable = value
                self.max = 252
                self.min = 0
                self.increment = 4

            def create(self, parent, **kw):
                super().create(parent, **kw)
                self.slider_variable = tk.IntVar(value=0)
                self.slider = ttk.Scale(parent, orient="horizontal", from_=0, to=63, length=150, variable=self.slider_variable,
                                        command=lambda event: self.slider_adjust())

            def slider_adjust(self):
                self.variable.set(self.slider_variable.get() *4)
                self.run_method()

            def set(self, value: int):
                super().set(value)
                self.slider_variable.set(value //4)

            def mousewheel(self, event: tk.Event):
                super().mousewheel(event)
                self.slider_variable.set(self.variable.get() //4)

        class CustomNatureBox(tk.Button, Method):
            def __init__(self, value: tk.DoubleVar, method: Callable=None):
                self.variable = value
                Method.__init__(self, method)

            def create(self, parent):
                tk.Button.__init__(self, parent, width=2, text=" ")
                self.config(command=lambda: self.click(1.1))
                self.bind("<Button-3>", lambda event: self.click(0.9))

            def get(self):
                return self.variable.get()

            def set(self, value: float):
                self.variable.set(value)
                if hasattr(self, "tk"):
                    color, text = self.float_color(value)
                    self.config(text=text, bg=color)

            def float_color(self, value):
                if value == 1:
                    return "SystemButtonFace", " "
                elif value == 1.1:
                    return "#fc6c98", "+"
                elif value == 0.9:
                    return "#4ac9fe", "-"

            def click(self, value: float):
                variable = self.get()
                if variable != value:
                    self.set(value)
                else:
                    self.set(1)
                self.run_method()

        def __init__(self, status: Union[Obj.StatusHP, Obj.Status], level: tk.Variable):
            self.status = status
            self.level = level
            self.status_label = self.CustomLabel()
            self.individual = self.CustomIndividualBox(status.individual, method=self.update)
            self.effort = self.CustomEffortBox(status.effort, method=self.update)
            if isinstance(self.status, Obj.Status):
                self.nature = self.CustomNatureBox(status.nature, method=self.update)

        def create(self, parent):
            self.status_label.create(parent)
            self.individual.create(parent)
            self.effort.create(parent)
            if isinstance(self.status, Obj.Status):
                self.nature.create(parent)

        def update(self):
            self.status.status_update(self.level.get())
            self.set_label()

        def reset(self):
            self.individual.set(31)
            self.effort.set(0)
            if isinstance(self.status, Obj.Status):
                self.nature.set(1.0)

        def set_label(self):
            self.status_label.set(self.status.value.get())
            if isinstance(self.status, Obj.Status):
                self.status_label.color_change(self.nature.variable.get())

        def set_click(self):
            if isinstance(self.status, Obj.Status):
                self.status_label.bind("<Button-1>", lambda event: self._click(1.1))
                self.status_label.bind("<Button-3>", lambda event: self._click(0.9))

        def _click(self, value: float):
            if value != self.nature.get():
                self.nature.variable.set(value)
            else:
                self.nature.variable.set(1)
            self.update()

    def __init__(self, poke: Obj.Poke | Obj.PokeDetail):
        self.level = poke.level
        self.widgets = [self.StatusWidget(stat, self.level) for stat in poke.status_list]

    def create(self, parent):
        [widget.create(parent) for widget in self.widgets]

    def update(self):
        [widget.update() for widget in self.widgets]

    def reset(self):
        [widget.reset() for widget in self.widgets]
        self.update()


class BannerWidget:
    def __init__(self, parent, poke: Obj.PokeDetail, text_variable: tk.StringVar, create_backup: Callable):
        self.poke = poke
        self.text_variable = text_variable
        self.create_backup = create_backup
        self.image = Pr.ImageGenerator.create_banner()
        self.widget = tk.Label(parent, image=self.image)
        self.widget.bind("<Button-1>", lambda event: self.click())
        self.widget.bind("<Button-3>", lambda event: self.reset())
        self.widget.bind("<Enter>", lambda event: self.on_mouse())
        self.widget.bind("<Leave>", lambda event: self.off_mouse())

    def click(self):
        path = Data.open_filedialogwindow("ポケモン選択", "Pokemon", ("text_file", "txt"))
        if path:
            self.poke.load(Data.PokeData.load(path))
            self.load()

    def load(self, data: Data.PokeData=None):
        if data is not None:
            self.poke.load(data)
        self.image = Pr.ImageGenerator.create_banner(self.poke)
        self.widget.config(image=self.image)
        self.create_backup()

    def reset(self):
        self.poke.reset()
        self.image = Pr.ImageGenerator.create_banner()
        self.widget.config(image=self.image)
        self.create_backup()

    def on_mouse(self):
        if self.poke.name:
            self.text_variable.set(self.poke.memo)

    def off_mouse(self):
        if self.poke.name:
            self.text_variable.set("左クリックでポケモンを登録\n右クリックでポケモンを削除")


class ResultWidget(tk.LabelFrame):
    def __init__(self, parent=None):
        tk.LabelFrame.__init__(self, parent, text="計算結果")
        self.size = (400, 25)
        self.image = Pr.ImageGenerator.create_hp_image(self.size, 1, 0, 0)
        if parent is not None:
            self.create(parent)

    def create(self, parent):
        tk.LabelFrame.__init__(self, parent, text="計算結果")
        self.label = tk.Label(self, image=self.image, width=500)
        self.label.pack(padx=5)
        left_frame = tk.Frame(self)
        left_frame.pack(side=tk.LEFT)
        scroll = tk.Scrollbar(left_frame)
        scroll.grid(row=0,column=1,sticky=tk.N + tk.S, pady=3)
        self.result_list_variable = tk.StringVar()
        result_list_box = tk.Listbox(left_frame, selectmode="single", height=9, width=60, yscrollcommand=scroll.set, listvariable=self.result_list_variable)
        result_list_box.grid(row=0, column=0, sticky=tk.N + tk.S, pady=3)

    def update(self, target: Obj.SendData, result: list[str], dmg_list: list[int]):
        hp_now = target.hp_now
        hp = target.status[0]
        minus = hp - hp_now
        self.image_update(hp, dmg_list[-1]+minus, dmg_list[0]+minus)
        num, per, confirm = Calc.fixed_num(hp_now, dmg_list)
        result.insert(0, "------------------------------------------------------------")
        result.insert(0, f"対象HP: {hp_now} 最低ダメージ: {dmg_list[0]} ~ 最高ダメージ: {dmg_list[-1]}")
        result.insert(0, f"{confirm} {num}発: {per}%")
        self.result_list_variable.set(result)

    def image_update(self, hp: int, max: int, min: int):
        if hp:
            self.image = Pr.ImageGenerator.create_hp_image(self.size, hp, max, min)
            self.label.config(image=self.image)


class ChangeButtonWidget(tk.Frame, Method):
    class ChangeButton(tk.Button, Method):
        def __init__(self, master_poke: Obj.PokeDetail):
            self.master_poke = master_poke
            self.poke = Obj.PokeDetail()

        def create(self, parent, side: str, method: Callable=None):
            self.side = side
            self.mirror = False
            Method.__init__(self, method)
            if side == tk.LEFT:
                self.mirror = True
            tk.Button.__init__(self, parent, command=self.click)
            self.bind("<Button-3>", lambda event: self.right_click())
            self.image_update()
            self.pack(pady=2, padx=5)

        def click(self):
            master = self.master_poke.copy()
            poke = self.poke.copy()
            self.master_poke.paste(poke)
            self.poke.paste(master)
            self.image_update()
            self.run_method()

        def right_click(self):
            self.poke.reset()

        def image_update(self):
            if True in [lock.get() for lock in self.poke.calc_list]:
                lock = True
            else:
                lock = False
            self.image = Pr.ImageGenerator.create_button(self.poke, lock=lock, mirror=self.mirror)
            self.config(image=self.image)


    def __init__(self, poke: Obj.PokeDetail, length: int, method: Callable):
        self.poke = poke
        Method.__init__(self, method)
        self.buttons = [self.ChangeButton(self.poke) for i in range(length)]

    def create(self, parent, side: str):
        tk.Frame.__init__(self, parent)
        [btn.create(parent, side) for btn in self.buttons]
        [[btn.add_method(method) for btn in self.buttons] for method in self.method]
        [btn.bind("<Button-3>", lambda event, index=index: self.btn_reset(index)) for index, btn in enumerate(self.buttons)]

    def btn_reset(self, index: int):
        self.buttons[index].poke.reset()
        self.buttons[index].image_update()


class Timer_widget(tk.Button):
    def __init__(self):
        self.playing = False
        self.timer_thread = None
        self.image = Pr.ImageGenerator.create_time("20", "00")

    def create(self, parent, master: tk.Tk):
        self.master = master
        tk.Button.__init__(self, parent, image=self.image, command=self.click, font=("Mairyo UI", 20, "bold"))

    def set(self, minit: str, second: str):
        self.image = Pr.ImageGenerator.create_time(minit, second)
        self.config(image=self.image)

    def click(self):
        self.playing = not self.playing
        if self.playing:
            self.time_start = time.time()
            self.timer_thread = th.Thread(target=self.battle_timer())
            self.timer_thread.setDaemon(True)
            self.timer_thread.start()
        else:
            self.timer_thread = None
            self.set("20", "00")

    def update(self):
        now = time.time()
        times = math.floor(now - self.time_start)
        minit = math.floor(times / 60)
        second = times % 60
        second = 60 - second
        if second == 60:
            second = "00"
            minit = 20 - minit
        elif second < 10:
            second = f"0{second}"
            minit = 20 - minit -1
        else:
            minit = 20 - minit -1
        if minit < 0 and second < 0:
            self.set("--", "--")
        else:
            self.set(minit, second)

    def battle_timer(self):
        if self.playing:
            self.update()
            self.master.after(1000, self.battle_timer)



class ButtlePartyWidget:
    class ButtlePokeButton(tk.Button):
        def __init__(self, poke: Obj.PokeDetail, side: str, method: Callable):
            self.poke = poke
            self.method = method
            self.mirror = True if side == tk.LEFT else False
            self.entry = CustomCommboBox(self.poke.name, Data.POKEDATA, self.re_generate)

        def create(self, parent):
            tk.Button.__init__(self, parent)
            self.update()

        def update(self, dmg: tuple[int]=(0, 0)):
            self.image = Pr.ImageGenerator.create_battle_button(self.poke, self.mirror, dmg)
            self.config(image=self.image)
            self.method()

        def re_generate(self):
            self.poke.re_generate()
            self.update()

    def __init__(self, side: str, poke_list: list[Obj.PokeDetail], method: Callable):
        self.buttons = [self.ButtlePokeButton(poke, side, method) for poke in poke_list]

    def create(self, parent):
        for btn in self.buttons:
            btn.entry.create(parent, width=18)
            btn.entry.pack()
            btn.create(parent)
            btn.pack(pady=2)

    def update(self, index: int=None):
        if index is not None:
            self.buttons[index].update()
        else:
            [btn.update() for btn in self.buttons]


class BattleHPWidgets:
    class BattleHPWidget(tk.Label):
        def __init__(self, width: int, text: str):
            self.width = width
            self.text = text
            self.image = Pr.ImageGenerator.create_hp_image((width, 15), 1, 0, 0)
            self.variable = tk.StringVar()
            self.pop = CustomPopupWindow(self.variable)

        def create(self, parent):
            frame = tk.LabelFrame(parent, text=self.text)
            frame.pack()
            tk.Label.__init__(self, frame, image=self.image)
            self.bind("<Enter>", lambda event: self.mouse_enter(event))
            self.bind("<Leave>", lambda event: self.mouse_leave())
            self.pack()

        def update(self, poke: Obj.PokeDetail, min_dmg: int=0, max_dmg: int=0, result_text: list[str]=[""]):
            self.variable.set("\n".join(result_text))
            hp = poke.status_list[0].value.get()
            min_dmg = hp - poke.hp_now.get() + min_dmg
            max_dmg = hp - poke.hp_now.get() + max_dmg
            self.image = Pr.ImageGenerator.create_hp_image((self.width, 15), hp, max_dmg, min_dmg)
            self.config(image=self.image)

        def mouse_enter(self, event: tk.Event):
            self.pop.create(event)

        def mouse_leave(self):
            self.pop.destroy_window()

    def __init__(self, poke: Obj.PokeDetail, side: str, width: int):
        self.poke = poke
        self.side = side
        # self.max_result = self.BattleHPWidget(width, "特化")
        # self.min_result = self.BattleHPWidget(width, "無振")
        # self.calc_result = self.BattleHPWidget(width, "入力")
        self.result = self.BattleHPWidget(width, "HP")
        self.hp_now_widget = CustomHPNowBox(self.poke.hp_now, self.poke.status_list[0].value, self.update)

    def create(self, parent):
        self.result.create(parent)
        # self.max_result.create(parent)
        # self.max_result.pack()
        # self.min_result.create(parent)
        # self.min_result.pack()
        # self.calc_result.create(parent)
        # self.calc_result.pack()

    def update(self, min: int=0, max: int=0, text: list[str]=[""]):
        self.result.update(self.poke, min, max, text)
        # self.max_result.update(self.poke, dmg[0][0], dmg[0][1], dmg[0][2])
        # self.min_result.update(self.poke, dmg[1][0], dmg[1][1], dmg[1][2])
        # self.calc_result.update(self.poke, dmg[2][0], dmg[2][1], dmg[2][2])


class ImageWidget(tk.Label):
    def __init__(self, poke: Obj.PokeDetail, side: str, menu: tk.Menu, menu_method: Callable, wheel_method: Callable):
        self.method = menu_method
        self.wheel_method = wheel_method
        self.poke = poke
        self.menu = menu
        self.mirror = False if side == tk.LEFT else True
        self.image = Pr.ImageGenerator.create_battle_banner(self.poke, self.mirror)

    def create(self, parent):
        tk.Label.__init__(self, parent, image=self.image, relief="solid", borderwidth=2)
        self.bind("<Button-1>", lambda event: self.show_menu(event))
        self.bind("<Button-3>", lambda event: self.show_menu(event))
        self.bind("<MouseWheel>", lambda event: self.mouse_wheel(event))

    def update(self):
        self.image = Pr.ImageGenerator.create_battle_banner(self.poke, self.mirror)
        self.config(image=self.image)

    def show_menu(self, event: tk.Event=None):
        self.method()
        if event is not None:
            self.menu.post(event.x_root, event.y_root)
        else:
            self.menu.post()

    def mouse_wheel(self, event: tk.Event):
        if event.delta > 0:
            self.wheel_method(-1)
        else:
            self.wheel_method(1)


class CustomPopupWindow:
    def __init__(self, variable: tk.Variable):
        self.variable = variable
        self.window = None

    def create(self, event: tk.Event):
        if self.variable.get():
            self.window = tk.Toplevel()
            self.window.overrideredirect(True)
            self.window.configure(bg="white")
            label = tk.Label(self.window, textvariable=self.variable, bg="white")
            label.pack(pady=5, padx=5)
            width = label.winfo_reqwidth()
            height = label.winfo_reqheight()
            self.window.geometry(f"{width+10}x{height+10}+{event.x_root+10}+{event.y_root+10}")

    def destroy_window(self):
        if self.window is not None:
            self.window.destroy()