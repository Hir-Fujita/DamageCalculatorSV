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
import Manager

class CustomLabel(tk.Label):
    def __init__(self, parent=None, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.variable = tk.StringVar(value=1)
        if parent is not None:
            self.create(parent)

    def create(self, parent):
        tk.Label.__init__(self, parent, *self.args, **self.kwargs, textvariable=self.variable)

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


class CustomTextBox(tk.Text):
    def __init__(self, parent=None, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        if parent is not None:
            self.create(parent)

    def create(self, parent):
        self.widget = tk.Text(parent, *self.args, **self.kwargs)
        scroll_x = tk.Scrollbar(parent, orient='horizontal', command=self.widget.xview)
        scroll_y = tk.Scrollbar(parent, orient='vertical', command=self.widget.yview)
        self.widget.config(xscrollcommand=scroll_x.set)
        self.widget.config(yscrollcommand=scroll_y.set)
        scroll_x.grid(row=1, column=0,sticky=tk.W + tk.E)
        scroll_y.grid(row=0, column=1,sticky=tk.N + tk.S)

    def pack(self, **kwrgs):
        self.widget.grid(row=0, column=0)

    def get(self):
        return self.widget.get("1.0", tk.END)

    def set(self, value):
        self.widget.insert("end", value)

    def delete(self):
        self.widget.delete("1.0", tk.END)


class CustomNatureBox(tk.Button):
    def __init__(self, parent=None, method: Callable=None, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.variable = tk.DoubleVar(value=1)
        self.method = method
        if parent is not None:
            self.create(parent)

    def create(self, parent):
        tk.Button.__init__(self, parent, *self.args, **self.kwargs, width=2, text=" ")
        self.config(command=lambda: self.click(1.1))
        self.bind("<Button-3>", lambda event: self.click(0.9))

    def get(self):
        return self.variable.get()

    def set(self, value: float):
        self.variable.set(value)
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
        self.method(value)
        variable = self.get()
        if variable != value:
            self.set(value)
        else:
            self.set(1)
        self.method()


class CustomCommboBox(ttk.Combobox):
    def __init__(self, values: Data.CSV=None, parent=None, method: Callable=None, *args, **kwargs):
        self.values = values
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.variable = tk.StringVar()
        if parent is not None:
            self.create(parent)

    def create(self, parent):
        ttk.Combobox.__init__(self, parent, textvariable=self.variable, *self.args, **self.kwargs, font=("Meiryo UI", 10))
        if isinstance(self.values, Data.CSV):
            self.config(values=self.values.name_list)
            self.bind("<KeyRelease-BackSpace>", lambda event:self.values_update(False))
            self.bind("<KeyRelease-Return>", lambda event:self.values_update(True))
        else:
            self.config(values=self.values)
        if self.method is not None:
            self.bind("<<ComboboxSelected>>", lambda event: self.run_method())

    def set(self, value):
        self.variable.set(value)

    def run_method(self):
        if self.method is not None:
            self.method()

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
        values = self.values.autocomplete(input)
        self.config(values=values)
        if len(values) == 1 and flag:
            self.set(values[0])
            self.run_method()

    def values_config(self, values: "list[str]"):
        self.config(values=values)
        if len(values) == 1:
            self.set(values[0])

class CustomSpinBox(tk.Spinbox):
    def __init__(self, method: Callable=None, *args, **kwargs):
        self.method = method
        self.increment: int
        self.variable: tk.IntVar
        self.max: int
        self.min: int
        self.args = args
        self.kwargs = kwargs

    def create(self, parent):
        tk.Spinbox.__init__(self, parent, *self.args, **self.kwargs)
        self.config(from_=self.min, to=self.max, increment=self.increment, width=4, textvariable=self.variable,
                    font=("Helvetica", 10), command=self.key_input)
        self.bind("<MouseWheel>", lambda event: self.mousewheel(event))
        self.bind("<Button-3>", lambda event: self.rightclick())
        self.bind("<KeyRelease>", lambda event: self.key_input())

    def get(self) -> int:
        return self.variable.get()

    def set(self, value: int):
        self.variable.set(int(value))

    def run_method(self):
        if self.method is not None:
            self.method()

    def mousewheel(self, event: tk.Event):
        if event.delta > 0:
            self.variable.set(self.value_check(self.variable.get() + self.increment))
        else:
            self.variable.set(self.value_check(self.variable.get() - self.increment))
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
    def __init__(self, parent=None, method: Callable=None,
                 *args, **kwargs):
        CustomSpinBox.__init__(self, method, *args, **kwargs)
        self.variable = tk.IntVar(value=50)
        self.max = 100
        self.min = 1
        self.increment = 1
        if parent is not None:
            self.create(parent)

    def rightclick(self):
        self.variable.set(50)
        self.run_method()


class CustomIndividualBox(CustomSpinBox):
    def __init__(self, parent=None, method: Callable=None,
                 *args, **kwargs):
        CustomSpinBox.__init__(self, method, *args, **kwargs)
        self.variable = tk.IntVar(value=31)
        self.max = 31
        self.min = 0
        self.increment = 1
        if parent is not None:
            self.create(parent)
            self.config(width=3)


class CustomEffortBox(CustomSpinBox):
    def __init__(self, parent=None, method: Callable=None,
                 *args, **kwargs):
        CustomSpinBox.__init__(self, method, *args, **kwargs)
        self.variable = tk.IntVar(value=0)
        self.max = 252
        self.min = 0
        self.increment = 4
        if parent is not None:
            self.create(parent)

    def create(self, parent):
        super().create(parent)
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


class CustomRankBox(CustomSpinBox):
    def __init__(self, parent=None, method: Callable=None,
                 *args, **kwargs):
        CustomSpinBox.__init__(self, method, *args, **kwargs)
        self.variable = tk.StringVar(value="")
        self.values = ["-6", "-5", "-4", "-3", "-2", "-1", "", "+1", "+2", "+3", "+4", "+5", "+6"]
        if parent is not None:
            self.create(parent)

    def create(self, parent):
        tk.Spinbox.__init__(self, parent, *self.args, **self.kwargs)
        self.config(textvariable=self.variable, font=("Helvetica", 10), values=self.values, width=3,
                    command=self.run_method)
        self.variable.set("")
        self.bind("<MouseWheel>", lambda event: self.mousewheel(event))
        self.bind("<Button-3>", lambda event: self.rightclick())

    def set(self, value):
        self.variable.set(value)

    def rightclick(self):
        self.variable.set("")
        self.run_method()

    def mousewheel(self, event: tk.Event):
        index = self.values.index(self.variable.get())
        if event.delta > 0:
            if index < len(self.values)-1:
                self.variable.set(self.values[index+1])
        else:
            if index > 0:
                self.variable.set(self.values[index-1])
        self.run_method()

    def reset(self):
        self.variable.set("")


class CustomHPNowBox(CustomSpinBox):
    def __init__(self, parent=None, method: Callable=None,
                 *args, **kwargs):
        CustomSpinBox.__init__(self, method, *args, **kwargs)
        self.max_variable = tk.IntVar(value=1)
        self.now_variable = tk.IntVar(value=1)
        if parent is not None:
            self.create(parent)

    def create(self, parent, font=None):
        tk.Spinbox.__init__(self, parent, *self.args, **self.kwargs)
        self.config(textvariable=self.now_variable, width=3, command=self.run_method, from_=1, to=1)
        self.bind("<MouseWheel>", lambda event: self.mousewheel(event))
        self.bind("<Button-3>", lambda event: self.rightclick())
        self.bind("<KeyRelease>", lambda event: self.key_input())
        self.label = tk.Label(parent, text="/")
        self.max_label = tk.Label(parent, textvariable=self.max_variable, width=3)
        self.slider = None
        if font is not None:
            self.config(font=font)
            self.label.config(font=font)
            self.max_label.config(font=font)

    def create_slider(self, parent):
        self.slider = ttk.Scale(parent, orient="horizontal", variable=self.now_variable, from_=0, to=1,
                                length=210, command=lambda event: self.scale())

    def max_set(self, value: int):
        self.max_variable.set(value)
        self.config(to=value)
        self.now_variable.set(value)
        if self.slider is not None:
            self.slider.config(to=value)

    def set(self, now: int, max: int=None):
        if max is not None:
            self.max_set(max)
        self.now_variable.set(self.value_check(now))

    def get(self) -> int:
        return self.now_variable.get()

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
        print(self.now_variable.get())


class CustomCountBox(CustomSpinBox):
    def __init__(self, parent=None, method: Callable=None, max: int=1,
                 *args, **kwargs):
        CustomSpinBox.__init__(self, method, *args, **kwargs)
        self.variable = tk.IntVar(value=1)
        self.max = max
        self.min = 0
        self.increment = 1
        if parent is not None:
            self.create(parent)

    def create(self, parent):
        super().create(parent)
        self.config(width=3)
        self.variable.set(self.max)

    def set(self, value: int, max_value: int=None):
        self.variable.set(value)
        if max_value is not None:
            self.max = max_value
            self.config(to=max_value)

class CustomCommboButtonBox(CustomCommboBox):
    def __init__(self, values: Data.CSV=None, parent=None, method: Callable=None,
                 *args, **kwargs):
        super().__init__(values, parent, method, *args, **kwargs)

    def add_button(self, parent, text: str, method: Callable):
        self.button = CustomButton(text, parent, method=method)

    def add_tuggle_button(self, parent, text: str, method: Callable):
        self.t_button = CustomTuggleButton(text, parent, method=method)

    def get_variable(self) -> bool:
        return self.t_button.get()


class CustomButton(tk.Button):
    def __init__(self, text: str, parent=None, method: Callable=None,
                 *args, **kwargs):
        self.variable = tk.StringVar(value=text)
        self.method = method
        self.args = args
        self.kwargs = kwargs
        if parent is not None:
            self.create(parent, method)

    def create(self, parent, method: Callable=None):
        if method is not None:
            self.method = method
        tk.Button.__init__(self, parent, textvariable=self.variable, *self.args, **self.kwargs)
        self.config(command=self.click)

    def click(self):
        self.method()

    def set(self, value: str):
        self.variable.set(value)


class CustomTuggleButton(tk.Button):
    def __init__(self, text: str, parent=None, method: Callable=None,
                 *args, **kwargs):
        self.text = text
        self.variable = tk.BooleanVar(value=False)
        self.method = method
        self.args = args
        self.kwargs = kwargs
        if parent is not None:
            self.create(parent, method)

    def create(self, parent, method: Callable=None):
        if method is not None:
            self.method = method
        tk.Button.__init__(self, parent, text=self.text, *self.args, **self.kwargs)
        self.config(command=self.click)

    def click(self):
        self.variable.set(not self.variable.get())
        if self.variable.get():
            self.config(relief=tk.SUNKEN)
        else:
            self.config(relief=tk.RAISED)
        self.method()

    def reset(self):
        self.variable.set(False)
        self.config(relief=tk.RAISED)

    def get(self) -> bool:
        return self.variable.get()

    def set(self, value: bool):
        self.variable.set(value)
        if value:
            self.config(relief=tk.SUNKEN)
        else:
            self.config(relief=tk.RAISED)

class CustomImageLabel(tk.Label):
    def __init__(self, parent=None, method: Callable=None, *args, **kwargs):
        self.size = (150, 150)
        self.args = args
        self.kwargs = kwargs
        self.method = method
        if parent is not None:
            self.create(parent, method)

    def create(self, parent, method: Callable=None):
        if method is not None:
            self.method = method
        tk.Label.__init__(self, parent, *self.args, **self.kwargs)
        self.image = Pr.ImageGenerator.create_field()
        self.config(image=self.image)
        self.pack()

    def image_update(self, weather: str, field: str):
        self.image = Pr.ImageGenerator.create_field(weather, field)
        self.config(image=self.image)

class CustomImageLabelPage3(tk.Label):
    def __init__(self, parent=None, method: Callable=None, *args, **kwargs):
        self.size = (200, 200)
        self.args = args
        self.kwargs = kwargs
        self.method = method
        if parent is not None:
            self.create(parent, method)

    def create(self, parent, method: Callable=None, mirror=False):
        self.mirror = mirror
        if method is not None:
            self.method = method
        tk.Label.__init__(self, parent, *self.args, **self.kwargs)
        self.image = Pr.ImageGenerator.create_page3()
        self.config(image=self.image)

    def update(self, name: str, item: str, terastal: str):
        self.image = Pr.ImageGenerator.create_page3(name, item, terastal, self.mirror)
        self.config(image=self.image)


class StatusWidget:
    def __init__(self, status: Union[Obj.StatusHP, Obj.Status], method: Callable):
        self.status = status
        self.method = method
        self.status_label = CustomLabel(font=("Helvetica", 10, "bold"), width=3)
        self.individual = CustomIndividualBox(method=self.method)
        self.effort = CustomEffortBox(method=self.method)
        if isinstance(self.status, Obj.Status):
            self.nature = CustomNatureBox(method=self.method)

    def create(self, parent):
        self.status_label.create(parent)
        self.individual.create(parent)
        self.effort.create(parent)
        if isinstance(self.status, Obj.Status):
            self.nature.create(parent)

    def reset(self):
        self.individual.set(31)
        self.effort.set(0)
        if isinstance(self.status, Obj.Status):
            self.nature.set(1.0)
            self.status_label.color_change(1.0)

    def set_label(self):
        self.status_label.set(self.status.value)
        if isinstance(self.status, Obj.Status):
            self.status_label.color_change(self.nature.variable.get())

class BannerWidget:
    def __init__(self, parent, method: Callable, index_number: int):
        self.method = method
        self.index = index_number
        self.generator = Pr.ImageGenerator()
        self.data: Data.PokeData = None
        self.image = self.generator.create_banner()
        self.widget = tk.Label(parent, image=self.image)
        self.widget.bind("<Button-1>", lambda event: self.click())
        self.widget.bind("<Button-3>", lambda event: self.reset())
        self.widget.bind("<Enter>", lambda event: self.on_mouse())
        self.widget.bind("<Leave>", lambda event: self.off_mouse())

    def click(self):
        path = Data.open_filedialogwindow("ポケモン選択", "Pokemon", ("text_file", "txt"))
        if path:
            self.data = Data.PokeData(path)
            self.load()

    def load(self, data: Data.PokeData=None):
        if data is not None:
            self.data = data
        self.image = self.generator.create_banner(self.data)
        self.widget.config(image=self.image)
        self.method("Button-1", self.index)

    def reset(self):
        self.image = self.generator.create_banner()
        self.widget.config(image=self.image)
        self.method("Button-3", self.index)
        self.data = None

    def on_mouse(self):
        if self.data is not None:
            self.method("Enter", self.index)

    def off_mouse(self):
        if self.data is not None:
            self.method("Leave")

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
        self.random_number_label = tk.Label(self, font=("Meiryo UI", 10), text="")
        self.random_number_label.pack()
        left_frame = tk.Frame(self)
        left_frame.pack(side=tk.LEFT)
        scroll = tk.Scrollbar(left_frame)
        scroll.grid(row=0,column=1,sticky=tk.N + tk.S, pady=3)
        self.result_list_variable = tk.StringVar()
        result_list_box = tk.Listbox(left_frame, selectmode="single", height=6, width=50, yscrollcommand=scroll.set, listvariable=self.result_list_variable)
        result_list_box.grid(row=0, column=0, sticky=tk.N + tk.S, pady=3)

    def update(self, calculator: Calc.DamageCalculator):
        random_number = [0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.00]
        results = [calculator.final_calc(num) for num in random_number]
        hp = calculator.target_status[0]
        minus = hp[1] - hp[0]
        self.image_update(hp[1], results[-1]+minus, results[0]+minus)
        result_text = "["+",".join([str(res) for res in results])+"]"
        self.random_number_label.config(text=result_text)

        max_per = round(100 -((hp[1] -results[-1]) /hp[1] * 100), 1)
        min_per = round(100 -((hp[1] -results[0]) /hp[1] * 100), 1)
        num, per, confirm = Calc.fixed_num(hp[0], results)
        log = calculator.calc_log + calculator.log
        log.insert(0, f"{confirm} {num}発: {per}%")
        self.result_list_variable.set(log)

    def reset(self):
        self.image_update(10, 0, 0)
        self.random_number_label.config(text="")
        self.result_list_variable.set("error!!")

    def image_update(self, hp: int, max: int, min: int):
        if hp:
            self.image = Pr.ImageGenerator.create_hp_image(self.size, hp, max, min)
            self.label.config(image=self.image)


class ChangeButton(tk.Button):
    def __init__(self, index: int):
        self.index = index

    def create(self, parent, side: str, method: Callable):
        self.side = side
        if side == tk.LEFT:
            self.mirror = True
        else:
            self.mirror = False
        self.method = method
        self.image = Pr.ImageGenerator.create_button(mirror=self.mirror)
        tk.Button.__init__(self, parent, image=self.image, command=self.click)
        self.pack(pady=2, padx=5)

    def click(self):
        self.method(self.side, self.index)

    def image_update(self, poke: dict="", lock: bool=False):
        if poke:
            self.image = Pr.ImageGenerator.create_button(poke["name"], lock, self.mirror)
            self.config(image=self.image)
        else:
            self.image = Pr.ImageGenerator.create_button(mirror=self.mirror)
            self.config(image=self.image)

class ChangeButtonWidget(tk.Frame):
    def __init__(self, length: int):
        self.poke_list: "list[Obj.PokeDetail]" = [Obj.PokeDetail() for i in range(length)]
        self.buttons: "list[ChangeButton]" = [ChangeButton(i) for i in range(length)]

    def create(self, parent, side: str, method: Callable):
        self.side = side
        tk.Frame.__init__(self, parent)
        [btn.create(parent, side, method) for btn in self.buttons]
        [btn.bind("<Button-3>", lambda event, index=index: self.btn_reset(index)) for index, btn in enumerate(self.buttons)]

    def copy(self, index: int) -> dict:
        return self.poke_list[index].copy()

    def paste(self, index: int, poke: dict, lock: bool):
        self.poke_list[index].paste(poke)
        self.buttons[index].image_update(poke, lock)

    def btn_reset(self, index: int):
        self.poke_list[index].reset()
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


class ButtlePokeButton(tk.Button):
    def __init__(self, index: int, mirror: bool):
        self.index = index
        self.mirror = mirror

    def create(self, parent, poke: Obj.PokeDetail):
        self.poke = poke
        tk.Button.__init__(self, parent, command=self.func)
        self.update()

    def update(self):
        self.image = Pr.ImageGenerator.create_battle_button(self.poke, self.mirror)
        self.config(image=self.image)

    def func(self):
        print(self.poke.name, self.poke.id, self.index)

class ChangePokeWidget:
    def __init__(self, side: str, poke_list: list[Obj.PokeDetail]):
        self.poke_list = poke_list
        if side == tk.LEFT:
            self.buttons = [ButtlePokeButton(i, True) for i in range(6)]
        else:
            self.buttons = [ButtlePokeButton(i, False) for i in range(6)]

    def create(self, parent):
        [btn.create(parent, self.poke_list[index]) for index, btn in enumerate(self.buttons)]
        [btn.pack(pady=2) for btn in self.buttons]

    def update(self):
        [btn.update() for btn in self.buttons]


class BattleHPWidget(tk.Label):
    def __init__(self, width: float, text: str):
        self.width = width
        self.text = text
        self.image = Pr.ImageGenerator.create_hp_image((int(400*self.width), 15), 1, 0, 0)

    def create(self, parent):
        frame = tk.LabelFrame(parent, text=self.text)
        frame.pack()
        tk.Label.__init__(self, frame, image=self.image)
        self.pack()



class BattleHPWidgets:
    def __init__(self, side: str, width: float):
        self.side = side
        self.width = width
        self.max_result = BattleHPWidget(width, "特化")
        self.min_result = BattleHPWidget(width, "無振")
        self.calc_result = BattleHPWidget(width, "入力")


    def create(self, parent):
        self.max_result.create(parent)
        self.max_result.pack()
        self.min_result.create(parent)
        self.min_result.pack()
        self.calc_result.create(parent)
        self.calc_result.pack()

class BattleWidget:
    def __init__(self, side: str, battle_type: int):
        self.side = side
        self.battle_type = battle_type
        self.width = 1 / battle_type
        self.hp_widget = BattleHPWidgets(side, self.width)
        self.widget = Manager.StatusWidgetManagerBattle(self.side)

    def create(self, parent):
        top_frame = tk.Frame(parent)
        top_frame.pack()
        self.hp_widget.create(top_frame)

        middle_2_frame = tk.Frame(parent)
        middle_2_frame.pack()
        terastal_frame = tk.LabelFrame(middle_2_frame, text="テラスタル")
        terastal_frame.grid(row=0, column=0)
        self.widget.terastal_widget.create(terastal_frame)
        self.widget.terastal_widget.config(width=6)
        self.widget.terastal_widget.pack(side=tk.LEFT, padx=5)
        self.widget.terastal_widget.add_tuggle_button(terastal_frame, "テラスタル", self.widget.update)
        self.widget.terastal_widget.t_button.pack(side=tk.LEFT, padx=5)
        hp_now_frame = tk.LabelFrame(middle_2_frame, text="現在HP")
        hp_now_frame.grid(row=0, column=1)
        self.widget.hp_now_widget.create(hp_now_frame)
        self.widget.hp_now_widget.create_slider(top_frame)
        self.widget.hp_now_widget.slider.pack()
        self.widget.hp_now_widget.pack(side=tk.LEFT)
        self.widget.hp_now_widget.label.pack(side=tk.LEFT)
        self.widget.hp_now_widget.max_label.pack(side=tk.LEFT)
        ability_frame = tk.LabelFrame(middle_2_frame, text="とくせい")
        ability_frame.grid(row=1, column=0)
        self.widget.ability_widget.create(ability_frame)
        self.widget.ability_widget.config(width=12)
        self.widget.ability_widget.pack(side=tk.LEFT)
        self.widget.ability_widget.add_tuggle_button(ability_frame, "発動", self.widget.update)
        self.widget.ability_widget.t_button.pack(side=tk.LEFT)
        bad_stat_frame = tk.LabelFrame(middle_2_frame, text="状態異常")
        bad_stat_frame.grid(row=1, column=1)
        self.widget.bad_stat_widget.create(bad_stat_frame)
        self.widget.bad_stat_widget.pack()
        item_frame = tk.LabelFrame(middle_2_frame, text="もちもの")
        item_frame.grid(row=2, column=0)
        self.widget.item_widget.create(item_frame)
        self.widget.item_widget.config(width=14)
        self.widget.item_widget.pack(side=tk.LEFT, padx=5)
        self.widget.move_flag_widget.create(middle_2_frame)
        self.widget.move_flag_widget.config(width=8)
        self.widget.move_flag_widget.grid(row=2, column=1)
        if self.side == tk.LEFT:
            self.widget.terastal_widget.config(state="disable")

        middle_frame = tk.Frame(parent)
        middle_frame.pack()
        font = ("MeiryoUI", 10)
        for i in range(6):
            self.widget.status_widgets[i].status_label.create(middle_frame)
            self.widget.status_widgets[i].status_label.config(width=3, font=("MeiryoUI", 12, "bold"))
            self.widget.status_widgets[i].status_label.grid(row=0, column=i)
            self.widget.status_widgets[i].individual.create(middle_frame)
            self.widget.status_widgets[i].individual.config(width=3, font=font)
            self.widget.status_widgets[i].effort.create(middle_frame)
            self.widget.status_widgets[i].effort.config(width=3, font=font)
            self.widget.status_widgets[i].individual.grid(row=1, column=i, padx=2, pady=1)
            self.widget.status_widgets[i].effort.grid(row=2, column=i)
            if self.side == tk.LEFT:
                self.widget.status_widgets[i].individual.disabled()
                self.widget.status_widgets[i].effort.disabled()
            if i != 0:
                self.widget.rank_widgets[i-1].create(middle_frame)
                self.widget.rank_widgets[i-1].config(width=3, font=font)
                self.widget.rank_widgets[i-1].grid(row=3, column=i, padx=2, pady=1)

        bottom_frame = tk.LabelFrame(parent, text="わざ")
        bottom_frame.pack()
        for index, wid in enumerate(self.widget.move_widgets):
            wid.create(bottom_frame)
            self.widget.move_counter_widgets[index].create(bottom_frame)
            wid.config(width=14)
            wid.add_button(bottom_frame, "計算", lambda index=index: print(index))
            wid.grid(row=index, column=0)
            self.widget.move_counter_widgets[index].grid(row=index, column=1, padx=5, pady=2)
            wid.button.grid(row=index, column=2)
        self.widget.set_dic()

    def poke_select(self, poke: Obj.PokeDetail):
        data = poke.copy()
        self.widget.poke.paste(data)
        self.widget.widget_update()


class BannerWidgetPage3(tk.Button):
    def __init__(self, side: str, menu: tk.Menu):
        self.menu = menu
        self.mirror = False if side == tk.LEFT else True
        self.image = Pr.ImageGenerator.create_battle_banner(Obj.PokeDetail(), self.mirror)

    def create(self, parent):
        tk.Button.__init__(self, parent, image=self.image)
        self.bind("<Button-3>", lambda event: self.show_menu(event))

    def update(self, poke: Obj.PokeDetail):
        self.image = Pr.ImageGenerator.create_battle_banner(poke, self.mirror)
        self.config(image=self.image)

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

