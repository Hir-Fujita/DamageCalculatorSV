#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pickle
from tkinter import filedialog
import re
from PIL import Image, ImageTk, ImageDraw, ImageOps, ImageFont, ImageFilter
import Data
import Object as Obj

GREEN = (0, 196, 0)
GREEN_2 = (164, 255, 164)
YELLOW = (229, 176, 0)
YELLOW_2 = (255, 255, 148)
RED = (255, 0, 0)
RED_2 = (226, 139, 139)
BLACK = (0, 0, 0)
WHITE = (0, 0, 0, 0)

def open_file(path):
    with open(path, "rb") as f:
        data = pickle.load(f)
    return data

def save_file(path, data):
    with open(path, "wb") as f:
        pickle.dump(data, f)

class ImageGenerator:
    def img_open(self, name: str, category: str, size: "tuple[int]"=None):
        if category == "poke":
            name = Data.POKEDATA.find(name, "name", "number")
            parent = "pokemon"
        elif category == "item":
            parent = "item"
        elif category == "terastal":
            parent = "type"
        image: Image.Image = open_file(f"{Data.FOLDER}/Data/Image_data/{parent}/{name}")
        if size is not None:
            if image.size[0] > size[0] or image.size[1] > size[1]:
                image = image.resize((image.size[0]*2, image.size[1]*2))
            image.thumbnail(size)
        return image

    def product(self, name: str) -> Image.Image:
        num = re.sub(r"[^0-9]", "", name)
        text_image = self.create_text(f"+{num}")
        return text_image

    def create_text(self, text: str, width=2) -> Image.Image:
        text_image = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_image)
        font = ImageFont.truetype(f"{Data.FOLDER}/Data/Corporate-Logo-Rounded-Bold-ver3.otf", 40)
        draw.text((0, 0), text, fill="white", stroke_width=width, stroke_fill="black", font=font)
        text_image = text_image.crop(text_image.split()[-1].getbbox())
        return text_image

    @classmethod
    def create_page1(cls, poke: Obj.Poke):
        size = (200, 200)
        image = Image.new("RGBA", size, (0, 0, 0, 0))
        if poke.name.get():
            number = Data.POKEDATA.find(poke.name.get(), "name", "number")
        else:
            number = "0"
        if poke.terastal.get():
            terastal_image = cls.img_open(cls, poke.terastal.get(), "terastal", (100, 100))
            image.paste(terastal_image, (0, 0), terastal_image)
        poke_image: Image.Image = open_file(f"{Data.FOLDER}/Data/Image_data/pokemon/{number}")
        poke_image = cls.img_open(cls, poke.name.get(), "poke")
        image.paste(poke_image, (size[0]//2 - poke_image.size[0]//2, size[1]-poke_image.size[1]), mask=poke_image)
        if poke.item.get():
            item_name = re.sub(r"[0-9+]", "", poke.item.get())
            item_image = cls.img_open(cls, item_name, "item", (70, 70))
            if "+" in poke.item.get():
                num = re.sub(r"[^0-9]", "", poke.item.get())
                text: Image.Image = cls.create_text(cls, f"+{num}")
                text.thumbnail((200, item_image.size[1]/3))
                item_image.paste(text, (item_image.size[0]-text.size[0], item_image.size[1]-text.size[1]), mask=text)
            image.paste(item_image, (size[0]-item_image.size[0]-10, size[1]-item_image.size[1]), mask=item_image)
        return ImageTk.PhotoImage(image)

    @classmethod
    def create_banner(cls, poke: Obj.PokeDetail=None):
        size = (400, 200)
        image = Image.new("RGBA", size=size, color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        if poke is None:
            draw.rounded_rectangle(
                [(0, 0), (size[0]-1, size[1]-1)],
                radius=10, fill="gray", outline="black", width=3)
        else:
            color = Data.TYPEDATA.typecolor(poke.terastal.get())
            draw.rounded_rectangle(
                [(0, 0), (size[0]-1, size[1]-1)],
                radius=10, fill=color, outline="black", width=3)
            terastal_icon = cls.img_open(cls, poke.terastal.get(), "terastal", (size[1]-10, size[1]-10))
            image.paste(terastal_icon, (size[0]//2 - terastal_icon.size[0]//2, size[1]//2 - terastal_icon.size[1]//2), mask=terastal_icon)
            pokemon_icon = cls.img_open(cls, poke.name.get(), "poke", (size[1]-10, size[1]-10))
            pokemon_icon = ImageOps.mirror(pokemon_icon)
            image.paste(pokemon_icon, (10, size[1]-pokemon_icon.size[1]-4), mask=pokemon_icon)
            if poke.item.get():
                item_name = re.sub(r"[0-9+]", "", poke.item.get())
                item_image = cls.img_open(cls, item_name, "item", (60, 60))
                item_image = ImageOps.mirror(item_image)
                if "+" in poke.item.get():
                    num = re.sub(r"[^0-9]", "", poke.item.get())
                    text: Image.Image = cls.create_text(cls, f"+{num}")
                    text.thumbnail((200, item_image.size[1]/3))
                    item_image.paste(text, (item_image.size[0]-text.size[0], item_image.size[1]-text.size[1]), mask=text)
                image.paste(item_image, (4, size[1]-item_image.size[1]-4), mask=item_image)
            font = ImageFont.truetype(f"{Data.FOLDER}/Data/Corporate-Logo-Rounded-Bold-ver3.otf", 26)
            draw.text((10, 4), f"{poke.name.get()}:Lv{poke.level.get()}",fill="white", stroke_width=2, stroke_fill="black", font=font)
            font = ImageFont.truetype(f"{Data.FOLDER}/Data/Corporate-Logo-Rounded-Bold-ver3.otf", 20)
            draw.text((10, 35), f"{poke.item.get()}",fill="white", stroke_width=2, stroke_fill="black", font=font)
            draw.text((10, 60), f"{poke.ability.get()}",fill="white", stroke_width=2, stroke_fill="black", font=font)
            draw.text((160, 95), f"{poke.move_list[0].get()}",fill="white", stroke_width=2, stroke_fill="black", font=font)
            draw.text((160, 120), f"{poke.move_list[1].get()}",fill="white", stroke_width=2, stroke_fill="black", font=font)
            draw.text((160, 145), f"{poke.move_list[2].get()}",fill="white", stroke_width=2, stroke_fill="black", font=font)
            draw.text((160, 170), f"{poke.move_list[3].get()}",fill="white", stroke_width=2, stroke_fill="black", font=font)
            stat_label = ["H", "A", "B", "C", "D", "S"]
            row = [45, 70, 95, 120, 145, 170]
            for index, stat in enumerate(poke.status_list):
                color = "white"
                if isinstance(stat, Obj.Status):
                    if stat.nature == 1.1:
                        color = "red"
                    elif stat.nature == 0.9:
                        color = "blue"
                draw.text((320, row[index]), f"{stat_label[index]} {stat.value.get()}", fill=color, stroke_width=2, stroke_fill="black", font=font)
        return ImageTk.PhotoImage(image)

    @classmethod
    def create_page3(cls, poke: Obj.PokeDetail, side: str):
        size = (180, 180)
        image = Image.new("RGBA", size, (0, 0, 0, 0))
        if poke.terastal.get() and poke.terastal_flag.get():
            terastal_image = cls.img_open(cls, poke.terastal.get(), "terastal", (150, 150))
            image.paste(terastal_image, (size[0]-terastal_image.size[0], 0), terastal_image)
        poke_image = cls.img_open(cls, poke.name.get(), "poke")
        image.paste(poke_image, (size[0]//2 - poke_image.size[0]//2, size[1]-poke_image.size[1]), mask=poke_image)
        if poke.item.get():
            item_name = re.sub(r"[0-9+]", "", poke.item.get())
            item_image = cls.img_open(cls, item_name, "item", (70, 70))
            if side == "left":
                item_image = ImageOps.mirror(item_image)
            if "+" in poke.item.get():
                num = re.sub(r"[^0-9]", "", poke.item.get())
                text: Image.Image = cls.create_text(cls, f"+{num}")
                text.thumbnail((200, item_image.size[1]/3))
                item_image.paste(text, (item_image.size[0]-text.size[0], item_image.size[1]-text.size[1]), mask=text)
            if side == "left":
                item_image = ImageOps.mirror(item_image)
            image.paste(item_image, (size[0]-item_image.size[0], size[1]-item_image.size[1]), mask=item_image)
        if side == "left":
            image = ImageOps.mirror(image)
        return ImageTk.PhotoImage(image)

    @classmethod
    def create_hp_image(self, size: "tuple[int]", hp: int, max: int, min: int, width: int=2, tk: bool=True):
        def hp_color(ratio: int):
            if ratio > 50:
                return GREEN, GREEN_2
            elif ratio <= 20:
                return RED, RED_2
            elif ratio >= 100:
                return BLACK, BLACK
            else:
                return YELLOW, YELLOW_2

        image = Image.new("RGB", (size[0]+width*2, size[1]+width*2), (0, 0, 0))
        paste_image = Image.new("RGB", (size[0], size[1]), (0, 0, 0))
        draw = ImageDraw.Draw(paste_image)
        ratio = size[0] / 100
        max_dmg = round((hp - max) / hp * 100 *ratio, 1)
        color_max, _ = hp_color(max_dmg / ratio)
        min_dmg = round((hp - min) / hp * 100 *ratio, 1)
        _, color_min = hp_color(min_dmg / ratio)
        if min_dmg > 0:
            draw.rectangle((0, 0, min_dmg, size[1]), fill=color_min)
        if max_dmg > 0:
            draw.rectangle((0, 0, max_dmg, size[1]), fill=color_max)
        for i in range(9):
            num = i+1
            draw.line(((int(num* paste_image.size[0]/10), 0), (int(num* paste_image.size[0]/10), paste_image.size[1])), (255, 255, 255), 1)
        image.paste(paste_image, (width, width))
        if tk:
            return ImageTk.PhotoImage(image)
        else:
            return image

    @classmethod
    def create_field(self, data: Obj.Field):
        dic = {
            "グラスフィールド": (0, 190, 0),
            "エレキフィールド": (255, 255, 0),
            "ミストフィールド": (255, 150, 210),
            "サイコフィールド": (180, 60, 255)
        }
        size = (100, 100)
        image = Image.new("RGBA", size, (0, 0, 0, 0))
        if data.field.get():
            color = dic[data.field.get()]
            paste = Image.new("RGB", size, color)
            field_img = open_file(f"{Data.FOLDER}/Data/Image_data/misc/field")
            image.paste(paste, mask=field_img)
        if data.weather.get():
            weather_img = open_file(f"{Data.FOLDER}/Data/Image_data/misc/{data.weather.get()}")
            image.paste(weather_img, mask=weather_img)
        return ImageTk.PhotoImage(image)

    @classmethod
    def create_time(cls, minit: str, second: str):
        image = Image.new("RGBA", (200, 50), (0, 0 ,0, 0))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(f"{Data.FOLDER}/Data/Corporate-Logo-Rounded-Bold-ver3.otf", 50)
        if int(minit) < 5:
            color = "red"
        else:
            color = "white"
        draw.text((image.size[0]/2, image.size[1]/2-2), f"{minit}:{second}", fill=color, stroke_width=4, stroke_fill="black", font=font, anchor='mm')
        return ImageTk.PhotoImage(image)


    @classmethod
    def create_button(cls, poke: Obj.PokeDetail, lock: bool=False, mirror: bool=False):
        image = Image.new("RGBA", (120, 50), (0, 0, 0, 0))
        poke_img = cls.img_open(cls, poke.name.get(), "poke")
        poke_img = ImageOps.mirror(poke_img)
        poke_img = poke_img.resize((int(poke_img.size[0]/2), int(poke_img.size[1]/2)))
        if poke_img.size[1] > image.size[1]:
            image.paste(poke_img, (0, int(image.size[1]/2-poke_img.size[1]/2)))
        else:
            image.paste(poke_img, (0, image.size[1]-poke_img.size[1]))
        if not mirror:
            image = ImageOps.mirror(image)
        if lock:
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype(f"{Data.FOLDER}/Data/Corporate-Logo-Rounded-Bold-ver3.otf", 20)
            draw.text((62, 29), "LOCK", fill="white", stroke_width=2, stroke_fill="black", font=font)
        return ImageTk.PhotoImage(image)

    @classmethod
    def create_battle_button(cls, poke: Obj.PokeDetail, mirror: bool, gray: bool=False):
        image = Image.new("RGBA", (170, 80), (0, 0, 0, 0))
        if poke.terastal_flag.get() and poke.terastal.get() != "":
            terastal_img = cls.img_open(cls, poke.terastal.get(), "terastal", (100, 100))
            terastal_img.thumbnail((80, 80))
            image.paste(terastal_img, (0, 0), terastal_img)
        poke_img = cls.img_open(cls, poke.name.get(), "poke")
        poke_img = poke_img.resize((int(poke_img.size[0]/3*2), int(poke_img.size[1]/3*2)))
        if poke_img.size[1] > image.size[1]:
            image.paste(poke_img, (image.size[0]-poke_img.size[0], 5), poke_img)
        else:
            image.paste(poke_img, (image.size[0]-poke_img.size[0], image.size[1]-poke_img.size[1]+5), poke_img)
        if poke.item.get() != "":
            item_name = re.sub(r"[0-9+]", "", poke.item.get())
            item_image = cls.img_open(cls, item_name, "item", (40, 40))
            if mirror:
                item_image = ImageOps.mirror(item_image)
            if "+" in poke.item.get():
                num = re.sub(r"[^0-9]", "", poke.item.get())
                text: Image.Image = cls.create_text(cls, f"+{num}")
                text.thumbnail((200, item_image.size[1]/3))
                item_image.paste(text, (item_image.size[0]-text.size[0], item_image.size[1]-text.size[1]), mask=text)
            if mirror:
                item_image = ImageOps.mirror(item_image)
            image.paste(item_image, (image.size[0]-item_image.size[0], image.size[1]-item_image.size[1]), mask=item_image)
        move = cls.create_text(cls, "\n".join([move.get() if move.get() else "." for move in poke.move_list]), 4)
        move.thumbnail((200, 60))
        if mirror:
            move = ImageOps.mirror(move)
        image.paste(move, (0, image.size[1]-move.size[1]), move)
        if mirror:
            image = ImageOps.mirror(image)
        hp = poke.status_list[0].value.get()
        dmg = hp - poke.hp_now.get() + poke.hp_result.get()
        hp_img = cls.create_hp_image((160, 10), hp, dmg, dmg, tk=False)
        image.paste(hp_img, (5, 0))
        if gray:
            image = image.convert("L")
        return ImageTk.PhotoImage(image)

    @classmethod
    def create_battle_banner(cls, poke: Obj.PokeDetail, mirror: bool=False):
        image = Image.new("RGBA", (140, 70), (0, 0, 0, 0))
        poke_img = cls.img_open(cls, poke.name.get(), "poke")
        poke_img = ImageOps.mirror(poke_img)
        poke_img = poke_img.resize((int(poke_img.size[0]/2), int(poke_img.size[1]/2)))
        if poke_img.size[1] > image.size[1]:
            image.paste(poke_img, (0, int(image.size[1]/2-poke_img.size[1]/2)))
        else:
            image.paste(poke_img, (0, image.size[1]-poke_img.size[1]))
        if mirror:
            image = ImageOps.mirror(image)
        return ImageTk.PhotoImage(image)


