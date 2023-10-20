#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, filedialog
from typing import Callable

import Manager
import Note

NAME = "ポケモンSV ダメージ計算+αツール"
VERSION = "開発版"

class Application(tk.Frame):
    """
    アプリケーション
    """
    def __init__(self, master: tk.Tk=None):
        super().__init__(master)

        self.window_width = 1350
        self.window_height = 700
        master.geometry(f"{self.window_width}x{self.window_height}+100+100")
        master.title(f"{NAME}_{VERSION}")
        master.resizable(height=False, width=False)
        style = ttk.Style()
        style.configure("example.TNotebook", tabmargins=[2, 5, 2, 0])
        style.configure("example.TNotebook.Tab", padding=[40, 6])
        style.configure("normal.TButton", font=("Helvetica", 20, "bold"))
        style.map("example.TNotebook.Tab", foreground=[
            ('active', 'white'),
            ('disabled', 'gray'),
            ('selected', 'blue')
            ])
        self.pack()

        self.menu_widget = tk.Menu(master)
        master.config(menu=self.menu_widget)

        self.manager = Manager.Manager(master)

        note = ttk.Notebook(self, width=self.window_width, height=self.window_height-40, style="example.TNotebook")
        note.pack()

        self.page_1 = PokeRegisterNote(note, self.menu_widget, self.manager)
        self.page_2 = PartyRegisterNote(note, self.menu_widget, self.manager)
        self.page_3 = DamageCalculatorNote(note, self.menu_widget, self.manager)
        self.page_4 = SingleDamageCalculatorNote(note, self.menu_widget, self.manager)
        self.page_5 = DoubleDamageCalculatorNote(note, self.menu_widget, self.manager)
        self.page_6 = StatusCalculatorNote(note, self.menu_widget, self.manager)
        self.page_7 = TestNote(note, self.menu_widget, self.manager)

class ParentFrame:
    """
    各タブの親フレーム
    """
    def __init__(self, note: ttk.Notebook, menu: tk.Menu, manager: Manager.Manager):
        self.menu = menu
        self.manager = manager
        self.frame = tk.Frame()
        self.frame.pack()
        self.frame.bind("<Visibility>", lambda e:self.active_page())
        note.add(self.frame, text=self.get_tab_name())

    def get_tab_name(self) -> str:
        raise NotImplementedError

    def active_page(self):
        self.menu.delete(0, "end")

class PokeRegisterNote(ParentFrame):
    """
    ポケモン登録のためのタブ
    """
    def __init__(self, note: ttk.Notebook, menu: tk.Menu, manager: Manager.Manager):
        super().__init__(note, menu, manager)
        self.widget_manager = Note.Page1(self.frame, manager)

    def get_tab_name(self) -> str:
        return "ポケモン登録"

    def active_page(self):
        super().active_page()
        self.menu.add_command(label="  ポケモンを保存    ", command=self.widget_manager.save_poke)
        self.menu.add_command(label=" ポケモンを読み込み ", command=self.widget_manager.load_poke)
        self.menu.add_command(label="    設定    ")
        self.menu.add_command(label=" あいことば ")

class PartyRegisterNote(ParentFrame):
    """
    パーティ登録のためのタブ
    """
    def __init__(self, note: ttk.Notebook, menu: tk.Menu, manager: Manager):
        super().__init__(note, menu, manager)
        self.widget_manager = Note.Page2(self.frame, manager)

    def get_tab_name(self) -> str:
        return "パーティ登録"

    def active_page(self):
        super().active_page()
        self.menu.add_command(label="    パーティを保存    ", command=self.widget_manager.save_party)
        self.menu.add_command(label="  パーティを読み込み  ", command=self.widget_manager.load_party)
        self.menu.add_command(label="    設定    ")
        self.menu.add_command(label=" あいことば ")

class DamageCalculatorNote(ParentFrame):
    def __init__(self, note: ttk.Notebook, menu: tk.Menu, manager: Manager):
        super().__init__(note, menu, manager)
        self.widget_manager = Note.Page3(self.frame)

    def get_tab_name(self) -> str:
        return "ダメージ計算"

    def active_page(self):
        super().active_page()
        self.menu.add_command(label="    設定    ")
        self.menu.add_command(label=" あいことば ")

class SingleDamageCalculatorNote(ParentFrame):
    def __init__(self, note: ttk.Notebook, menu: tk.Menu, manager: Manager):
        super().__init__(note, menu, manager)
        self.widget_manager = Note.Page4(self.frame, manager)

    def get_tab_name(self) -> str:
        return "シングルバトル"

    def active_page(self):
        super().active_page()
        self.menu.add_command(label="    設定    ")
        self.menu.add_command(label=" あいことば ")

class DoubleDamageCalculatorNote(ParentFrame):
    def __init__(self, note: ttk.Notebook, menu: tk.Menu, manager: Manager):
        super().__init__(note, menu, manager)
        self.widget_manager = Note.Page5(self.frame, manager)

    def get_tab_name(self) -> str:
        return "ダブルバトル"

    def active_page(self):
        super().active_page()
        self.menu.add_command(label="    設定    ")
        self.menu.add_command(label=" あいことば ")
        self.widget_manager.battle_manager.team_update()

class StatusCalculatorNote(ParentFrame):
    def __init__(self, note: ttk.Notebook, menu: tk.Menu, manager: Manager):
        super().__init__(note, menu, manager)
        self.widget_manager = Note.Page6(self.frame)

    def get_tab_name(self) -> str:
        return "個体値計算"

    def active_page(self):
        super().active_page()
        self.menu.add_command(label="    設定    ")
        self.menu.add_command(label=" あいことば ")

class TestNote(ParentFrame):
    def __init__(self, note: ttk.Notebook, menu: tk.Menu, manager: Manager):
        super().__init__(note, menu, manager)
        self.widget_manager = Note.Page6(self.frame)

    def get_tab_name(self) -> str:
        return "ポケモンなんじゃろな"

    def active_page(self):
        super().active_page()
        self.menu.add_command(label="    設定    ")
        self.menu.add_command(label=" あいことば ")

def main():
    win = tk.Tk()
    app = Application(master=win)
    app.mainloop()

if __name__ == "__main__":
    main()
