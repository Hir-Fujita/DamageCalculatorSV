#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Tuple, Union, Callable
import tkinter as tk
from tkinter import ttk

import Data as D
import Object as Obj
import Process as Pr
import Calculation as Calc


class CustomLabel(tk.Label):
    def __init__(self, parent=None, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.variable = tk.StringVar(value=0)
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
    def __init__(self, values: D.CSV=None, parent=None, method: Callable=None,
                 *args, **kwargs):
        self.values = values
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.variable = tk.StringVar()
        if parent is not None:
            self.create(parent)

    def create(self, parent):
        ttk.Combobox.__init__(self, parent, textvariable=self.variable, *self.args, **self.kwargs, font=("Meiryo UI", 10))
        if isinstance(self.values, D.CSV):
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
        if isinstance(self.values, D.CSV):
            self.config(values=self.values.name_list)
        else:
            self.config(values=self.values)

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
    def __init__(self, method: Callable=None,
                 *args, **kwargs):
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
        self.max = 1
        self.now_variable = tk.IntVar(value=1)
        if parent is not None:
            self.create(parent)

    def create(self, parent):
        tk.Spinbox.__init__(self, parent, *self.args, **self.kwargs)
        self.config(textvariable=self.now_variable, font=("Meiryo UI", 16), width=3,
                    command=self.run_method, from_=1, to=1)
        self.bind("<MouseWheel>", lambda event: self.mousewheel(event))
        self.bind("<Button-3>", lambda event: self.rightclick())
        self.bind("<KeyRelease>", lambda event: self.key_input())
        self.label = tk.Label(parent, text="/", font=("Meiryo UI", 16))
        self.max_label = tk.Label(parent, textvariable=self.max_variable, font=("Meiryo UI", 16), width=3)

    def max_set(self, value: int):
        self.max = value
        self.max_variable.set(value)
        self.config(to=value)
        if self.now_variable.get() > value:
            self.now_variable.set(value)

    def set(self, now: int, max: int=None):
        self.now_variable.set(self.value_check(now))
        if max is not None:
            self.max_set(max)

    def get(self) -> int:
        return self.now_variable.get()

    def mousewheel(self, event: tk.Event):
        if event.delta > 0:
            self.now_variable.set(self.value_check(self.now_variable.get() + 1))
        else:
            self.now_variable.set(self.value_check(self.now_variable.get() - 1))
        self.run_method()

    def value_check(self, value: int) -> int:
        if value > self.max:
            return self.max
        elif value < 1:
            return 1
        else:
            return value

    def rightclick(self):
        if self.now_variable.get() != self.max:
            self.now_variable.set(self.max)
        self.run_method()

    def key_input(self):
        self.now_variable.set(self.value_check(self.now_variable.get()))
        self.run_method()


class CustomCommboButtonBox(CustomCommboBox):
    def __init__(self, values: D.CSV=None, parent=None, method: Callable=None,
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
        self.method()


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


CUSTOM_WIDGET = Union[
    CustomCommboBox,
    CustomEffortBox,
    CustomIndividualBox,
    CustomLevelBox,
    CustomLabel,
    CustomTextBox,
    CustomRankBox,
    CustomCommboButtonBox,
    CustomButton,
    CustomTuggleButton,
    CustomHPNowBox,
    CustomImageLabel,
    CustomImageLabelPage3
]


class CustomFrame(tk.LabelFrame):
    def __init__(self, widget: CUSTOM_WIDGET, parent=None, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.widget = widget
        if parent is not None:
            self.create(self)

    def create(self, parent, label: bool=True):
        if label:
            tk.LabelFrame.__init__(self, parent, *self.args, **self.kwargs)
        else:
            tk.Frame.__init__(self, parent, *self.args, **self.kwargs)
        self.widget.create(self)

    def get(self):
        return self.widget.get()

    def set(self, value: Union[int, str]):
        self.widget.set(value)

    def config(self, **kw):
        self.widget.config(kw)

    def pack_widget(self, anchor=tk.TOP, padx=0, pady=0, inner_pad=5):
        self.widget.pack(pady=inner_pad, padx=inner_pad, side=tk.LEFT)
        self.pack(side=anchor, padx=padx, pady=pady)


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

    def grid(self, anchor: str, start_index: int, freeze_index: int, padx: int=0, pady: int=0):
        if anchor == "x":
            self.status_label.grid(row=freeze_index, column=start_index, padx=padx, pady=pady)
            self.individual.grid(row=freeze_index, column=start_index+1, padx=padx, pady=pady)
            self.effort.slider.grid(row=freeze_index, column=start_index+2, padx=padx, pady=pady)
            self.effort.grid(row=freeze_index, column=start_index+3, padx=padx, pady=pady)
            if isinstance(self.status, Obj.Status):
                self.nature.grid(row=freeze_index, column=start_index+4, padx=padx, pady=pady)


class StatusWidgetManager:
    def __init__(self, poke: Obj.Poke):
        self.poke = poke
        self.name_widget = CustomFrame(CustomCommboBox(D.POKEDATA, method=self.name_widget_func), text="ポケモン名")
        self.level_widget = CustomFrame(CustomLevelBox(method=self.update), text="Lv")
        self.ability_widget = CustomFrame(CustomCommboBox(method=self.update), text="とくせい")
        self.item_widget = CustomFrame(CustomCommboBox(D.ITEMDATA, method=self.update), text="もちもの")
        self.terastal_widget = CustomFrame(CustomCommboBox(D.TYPEDATA.list, method=self.update), text="テラスタル")
        self.move_widgets = [CustomFrame(CustomCommboBox(D.MOVEDATA, method=self.update), text=f"技_{i+1}") for i in range(4)]
        self.status_widgets = [StatusWidget(status, self.children_method) for status in self.poke.status_list]

    def config(self):
        self.poke.config(
            self.name_widget.widget.variable,
            self.item_widget.widget.variable,
            self.terastal_widget.widget.variable,
            self.ability_widget.widget.variable,
            self.level_widget.widget.variable,
            [widget.individual.variable for widget in self.status_widgets],
            [widget.effort.variable for widget in self.status_widgets],
            [widget.nature.variable for index, widget in enumerate(self.status_widgets) if index != 0],
            [widget.widget.variable for widget in self.move_widgets]
        )

    def update(self):
        self.poke.update()
        [widget.set_label() for widget in self.status_widgets]

    def name_widget_func(self):
        if self.name_widget.get() in D.POKEDATA.name_list:
            self.poke.generate(self.name_widget.get())
            self.ability_widget.widget.reset()
            self.ability_widget.widget.values_config(self.poke.ability_list)
            self.item_widget.widget.reset()
            self.terastal_widget.widget.reset()
            [widget.widget.reset() for widget in self.move_widgets]
            [widget.reset() for widget in self.status_widgets]
            self.auto_pokemon_item()
            self.update()

    def auto_pokemon_item(self):
        name = self.name_widget.get()
        result = [data for data in D.ITEM_POKE if data[0] == name]
        if len(result) > 0:
            self.item_widget.set(result[0][1])
            self.terastal_widget.set(result[0][2])

    def children_method(self, flag: Union[bool, float]=False):
        if flag == 1.1:
            [widget.nature.set(1) for widget in self.status_widgets[1:] if widget.nature.get() == 1.1]
        elif flag == 0.9:
            [widget.nature.set(1) for widget in self.status_widgets[1:] if widget.nature.get() == 0.9]
        [widget.status_label.color_change(widget.nature.get()) for widget in self.status_widgets[1:]]
        self.update()

class StatusWidgetManagerPlus(StatusWidgetManager):
    def __init__(self, poke: Obj.PokeDetail):
        super().__init__(poke)
        self.poke = poke
        self.ability_widget = CustomFrame(CustomCommboButtonBox(method=self.update), text="とくせい")
        self.terastal_widget = CustomFrame(CustomCommboButtonBox(D.TYPEDATA.list, method=self.update), text="テラスタル")
        self.move_widgets = [CustomCommboButtonBox(D.MOVEDATA, method=self.update) for i in range(4)]
        self.rank_widgets = [CustomRankBox(method=self.update) for i in range(5)]
        self.move_flag_widget = CustomTuggleButton("技効果", method=self.update, width=10)
        self.bad_stat_widget = CustomFrame(CustomCommboBox(D.BADSTAT, method=self.update, width=6), text="状態異常")
        self.a_wall_widget = CustomTuggleButton("リフレクター", method=self.update, width=10)
        self.c_wall_widget = CustomTuggleButton("ひかりのかべ", method=self.update, width=10)
        self.wind_widget = CustomTuggleButton("おいかぜ", method=self.update, width=10)
        self.help_widget = CustomTuggleButton("てだすけ", method=self.update, width=10)
        self.crit_widget = CustomTuggleButton("被急所", method=self.update, width=10)
        self.image_label = CustomImageLabelPage3()
        self.hp_now_widget = CustomFrame(CustomHPNowBox(method=self.hp_now_update), text="現在HP")
        self.result_widget = ResultWidget()
        self.button_widget = ChangeButtonWidget(7)

    def name_widget_func(self):
        if self.name_widget.get() in D.POKEDATA.name_list:
            self.poke.generate(self.name_widget.get())
            self.ability_widget.widget.reset()
            self.ability_widget.widget.values_config(self.poke.ability_list)
            self.item_widget.widget.reset()
            self.terastal_widget.widget.reset()
            [widget.reset() for widget in self.move_widgets]
            [widget.reset() for widget in self.status_widgets]
            [widget.reset() for widget in self.rank_widgets]
            self.ability_widget.widget.t_button.reset()
            self.terastal_widget.widget.t_button.reset()
            self.bad_stat_widget.widget.reset()
            self.move_flag_widget.reset()
            self.a_wall_widget.reset()
            self.c_wall_widget.reset()
            self.wind_widget.reset()
            self.help_widget.reset()
            self.crit_widget.reset()
            self.auto_pokemon_item()
            self.hp_now_widget.widget.set(self.poke.status_list[0].value, self.poke.status_list[0].value)
            self.update()
            self.image_update()

    def config(self):
        self.poke.config(
            self.name_widget.widget,
            self.item_widget.widget,
            self.terastal_widget.widget,
            self.ability_widget.widget,
            self.level_widget.widget,
            [widget.individual for widget in self.status_widgets],
            [widget.effort for widget in self.status_widgets],
            [widget.nature for index, widget in enumerate(self.status_widgets) if index != 0],
            [widget for widget in self.move_widgets],
            [widget for widget in self.rank_widgets],
            self.terastal_widget.widget.t_button,
            self.move_flag_widget,
            self.ability_widget.widget.t_button,
            self.bad_stat_widget.widget,
            self.a_wall_widget,
            self.c_wall_widget,
            self.wind_widget,
            self.help_widget,
            self.crit_widget,
            self.hp_now_widget.widget
        )

    def update(self):
        self.poke.update()
        [widget.set_label() for widget in self.status_widgets]
        self.image_update()
        self.hp_now_widget.widget.set(self.poke.status_list[0].value_now, self.poke.status_list[0].value)
        self.result_widget.image_update(self.status_widgets[0].status.value, 0, 0)

    def widget_update(self):
        self.name_widget.set(self.poke.name)
        self.item_widget.set(self.poke.item)
        self.terastal_widget.set(self.poke.terastal)
        self.ability_widget.set(self.poke.ability)
        self.ability_widget.widget.config(values=self.poke.ability_list)
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
        self.terastal_widget.widget.t_button.set(self.poke.terastal_flag)
        self.bad_stat_widget.set(self.poke.bad_stat)
        self.image_update()
        for index, status in enumerate(self.status_widgets):
            status.set_label()
        self.hp_now_widget.widget.set(self.poke.status_list[0].value_now, self.poke.status_list[0].value)
        hp = self.poke.status_list[0].value
        now = self.poke.status_list[0].value_now
        self.result_widget.image_update(hp, hp-now, hp-now)

    def hp_now_update(self):
        self.poke.status_list[0].set_now(self.hp_now_widget.widget.now_variable.get())
        hp = self.poke.status_list[0].value
        now = self.poke.status_list[0].value_now
        self.result_widget.image_update(hp, hp-now, hp-now)

    def image_update(self):
        terastal = ""
        if self.terastal_widget.widget.get_variable():
            terastal = self.terastal_widget.get()
        self.image_label.update(self.name_widget.get(), self.item_widget.get(), terastal)


class FieldWidgetManager:
    def __init__(self, field_data: Obj.Field):
        self.field_data = field_data
        self.double_widget = CustomTuggleButton("ダブルバトル", method=self.update, width=12)
        self.field_widget = CustomFrame(CustomCommboBox(D.FIELD, method=self.update, width=12), text="フィールド")
        self.weather_widget = CustomFrame(CustomCommboBox(D.WEATHER, method=self.update, width=12), text="天候")
        self.field_ability_widget_1 = CustomFrame(CustomCommboBox(D.ABIILITY, method=self.update, width=12), text="特性")
        self.field_ability_widget_2 = CustomFrame(CustomCommboBox(D.ABIILITY, method=self.update, width=12), text="特性_2")
        self.image_label = CustomFrame(CustomImageLabel())

    def config(self):
        self.field_data.config(
            self.double_widget.variable,
            self.field_widget.widget.variable,
            self.weather_widget.widget.variable,
            self.field_ability_widget_1.widget.variable,
            self.field_ability_widget_2.widget.variable,
        )

    def update(self):
        self.field_data.update()
        self.image_label.widget.image_update(self.weather_widget.get(), self.field_widget.get())


class BannerWidget:
    def __init__(self, parent, method: Callable, index_number: int):
        self.method = method
        self.index = index_number
        self.generator = Pr.ImageGenerator()
        self.data: D.PokeData = None
        self.image = self.generator.create_banner()
        self.widget = tk.Label(parent, image=self.image)
        self.widget.bind("<Button-1>", lambda event: self.click())
        self.widget.bind("<Button-3>", lambda event: self.reset())
        self.widget.bind("<Enter>", lambda event: self.on_mouse())
        self.widget.bind("<Leave>", lambda event: self.off_mouse())

    def click(self):
        path = Pr.open_filedialogwindow("ポケモン選択", "Pokemon")
        if path:
            self.data = D.PokeData(path)
            self.load()

    def load(self, data: D.PokeData=None):
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
        self.image = Pr.ImageGenerator.create_hp_image(self.size, 10, 0, 0)
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




