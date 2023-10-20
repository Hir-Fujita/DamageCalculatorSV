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

def save_filedialogwindow(save_name: str, title: str, parent_folder: str="") -> str:
    save_folder = f"./{Data.FOLDER}/Data/{parent_folder}"
    filepath = filedialog.asksaveasfilename(
        title=title,
        initialfile=save_name,
        defaultextension=f".txt",
        filetypes=[("Text File", ".txt")],
        initialdir=save_folder
    )
    return filepath

def open_filedialogwindow(title: str, parent_folder: str="") -> str:
    load_folder = f"./{Data.FOLDER}/Data/{parent_folder}"
    filepath = filedialog.askopenfilename(
        title=title,
        multiple=False,
        initialdir=load_folder,
        filetypes=[("Text File", ".txt")]
    )
    return filepath

def metronome(name: str, mirror: bool) -> Image.Image:
        name = name.replace("メトロノーム", "")
        image: Image.Image = open_file(f"{Data.FOLDER}/Data/Image_data/item/メトロノーム")
        text_image = Image.new("RGBA", (image.size[0], image.size[1]), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_image)
        font = ImageFont.truetype(f"{Data.FOLDER}/Data/Corporate-Logo-Rounded-Bold-ver3.otf", 40)
        draw.text((0, 0), name, fill="white", stroke_width=2, stroke_fill="black", font=font)
        text_image = text_image.crop(text_image.split()[-1].getbbox())
        if mirror:
            text_image = ImageOps.mirror(text_image)
            image.paste(text_image, (0, image.size[1]-text_image.size[1]), mask=text_image)
        else:
            image.paste(text_image, (image.size[0]-text_image.size[0], image.size[1]-text_image.size[1]), mask=text_image)
        return image

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
    def create_page1(cls, name: str="", item: str="", terastal: str=""):
        size = (200, 200)
        image = Image.new("RGBA", size, (0, 0, 0, 0))
        if name:
            number = Data.POKEDATA.find(name, "name", "number")
        else:
            number = "0"
        if terastal:
            terastal_image = cls.img_open(cls, terastal, "terastal", (100, 100))
            image.paste(terastal_image, (0, 0), terastal_image)
        poke_image: Image.Image = open_file(f"{Data.FOLDER}/Data/Image_data/pokemon/{number}")
        poke_image = cls.img_open(cls, name, "poke")
        image.paste(poke_image, (size[0]//2 - poke_image.size[0]//2, size[1]-poke_image.size[1]), mask=poke_image)
        if item:
            item_name = re.sub(r"[0-9+]", "", item)
            item_image = cls.img_open(cls, item_name, "item", (70, 70))
            if "+" in item:
                num = re.sub(r"[^0-9]", "", item)
                text: Image.Image = cls.create_text(cls, f"+{num}")
                text.thumbnail((200, item_image.size[1]/3))
                item_image.paste(text, (item_image.size[0]-text.size[0], item_image.size[1]-text.size[1]), mask=text)
            image.paste(item_image, (size[0]-item_image.size[0]-10, size[1]-item_image.size[1]), mask=item_image)
        return ImageTk.PhotoImage(image)

    @classmethod
    def create_banner(cls, data: Data.PokeData=None):
        size = (400, 200)
        image = Image.new("RGBA", size=size, color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        if data is None:
            draw.rounded_rectangle(
                [(0, 0), (size[0]-1, size[1]-1)],
                radius=10, fill="gray", outline="black", width=3)
        else:
            color = Data.TYPEDATA.typecolor(data.terastal)
            draw.rounded_rectangle(
                [(0, 0), (size[0]-1, size[1]-1)],
                radius=10, fill=color, outline="black", width=3)
            terastal_icon = cls.img_open(cls, data.terastal, "terastal", (size[1]-10, size[1]-10))
            image.paste(terastal_icon, (size[0]//2 - terastal_icon.size[0]//2, size[1]//2 - terastal_icon.size[1]//2), mask=terastal_icon)
            pokemon_icon = cls.img_open(cls, data.name, "poke", (size[1]-10, size[1]-10))
            pokemon_icon = ImageOps.mirror(pokemon_icon)
            image.paste(pokemon_icon, (10, size[1]-pokemon_icon.size[1]-4), mask=pokemon_icon)
            if data.item:
                item_name = re.sub(r"[0-9+]", "", data.item)
                item_image = cls.img_open(cls, item_name, "item", (60, 60))
                item_image = ImageOps.mirror(item_image)
                if "+" in data.item:
                    num = re.sub(r"[^0-9]", "", data.item)
                    text: Image.Image = cls.create_text(cls, f"+{num}")
                    text.thumbnail((200, item_image.size[1]/3))
                    item_image.paste(text, (item_image.size[0]-text.size[0], item_image.size[1]-text.size[1]), mask=text)
                image.paste(item_image, (4, size[1]-item_image.size[1]-4), mask=item_image)
            font = ImageFont.truetype(f"{Data.FOLDER}/Data/Corporate-Logo-Rounded-Bold-ver3.otf", 26)
            draw.text((10, 4), f"{data.name}:Lv{data.level}",fill="white", stroke_width=2, stroke_fill="black", font=font)
            font = ImageFont.truetype(f"{Data.FOLDER}/Data/Corporate-Logo-Rounded-Bold-ver3.otf", 20)
            draw.text((10, 35), f"{data.item}",fill="white", stroke_width=2, stroke_fill="black", font=font)
            draw.text((10, 60), f"{data.ability}",fill="white", stroke_width=2, stroke_fill="black", font=font)
            draw.text((160, 95), f"{data.move_list[0]}",fill="white", stroke_width=2, stroke_fill="black", font=font)
            draw.text((160, 120), f"{data.move_list[1]}",fill="white", stroke_width=2, stroke_fill="black", font=font)
            draw.text((160, 145), f"{data.move_list[2]}",fill="white", stroke_width=2, stroke_fill="black", font=font)
            draw.text((160, 170), f"{data.move_list[3]}",fill="white", stroke_width=2, stroke_fill="black", font=font)
            poke = Obj.Poke()
            poke.generate(data.name)
            stat = ["H", "A", "B", "C", "D", "S"]
            row = [45, 70, 95, 120, 145, 170]
            for i in range(6):
                if i == 0:
                    poke.status_list[i].status_update(data.status[i][1], data.status[i][0])
                    color = "white"
                else:
                    poke.status_list[i].status_update(data.status[i][1], data.status[i][0], data.status[i][2])
                    if data.status[i][2] == 1.0:
                        color = "white"
                    elif data.status[i][2] == 0.9:
                        color = "blue"
                    else:
                        color = "red"
                draw.text((320, row[i]), f"{stat[i]} {poke.status_list[i].value}", fill=color, stroke_width=2, stroke_fill="black", font=font)
        return ImageTk.PhotoImage(image)

    @classmethod
    def create_page3(cls, name:str="", item: str="", terastal: str="", mirror: bool=True):
        size = (180, 180)
        image = Image.new("RGBA", size, (0, 0, 0, 0))
        if terastal:
            terastal_image = cls.img_open(cls, terastal, "terastal", (150, 150))
            image.paste(terastal_image, (size[0]-terastal_image.size[0], 0), terastal_image)
        poke_image = cls.img_open(cls, name, "poke")
        image.paste(poke_image, (size[0]//2 - poke_image.size[0]//2, size[1]-poke_image.size[1]), mask=poke_image)
        if item:
            item_name = re.sub(r"[0-9+]", "", item)
            item_image = cls.img_open(cls, item_name, "item", (70, 70))
            if mirror:
                item_image = ImageOps.mirror(item_image)
            if "+" in item:
                num = re.sub(r"[^0-9]", "", item)
                text: Image.Image = cls.create_text(cls, f"+{num}")
                text.thumbnail((200, item_image.size[1]/3))
                item_image.paste(text, (item_image.size[0]-text.size[0], item_image.size[1]-text.size[1]), mask=text)
            if mirror:
                item_image = ImageOps.mirror(item_image)
            image.paste(item_image, (size[0]-item_image.size[0], size[1]-item_image.size[1]), mask=item_image)
        if mirror:
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
        color_max, _ = hp_color(max_dmg)
        min_dmg = round((hp - min) / hp * 100 *ratio, 1)
        _, color_min = hp_color(min_dmg)
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
    def create_field(self, weather: str="", field: str=""):
        dic = {
            "グラスフィールド": (0, 190, 0),
            "エレキフィールド": (255, 255, 0),
            "ミストフィールド": (255, 150, 210),
            "サイコフィールド": (180, 60, 255)
        }
        size = (100, 100)
        image = Image.new("RGBA", size, (0, 0, 0, 0))
        if field:
            color = dic[field]
            paste = Image.new("RGB", size, color)
            field_img = open_file(f"{Data.FOLDER}/Data/Image_data/misc/field")
            image.paste(paste, mask=field_img)
        if weather:
            weather_img = open_file(f"{Data.FOLDER}/Data/Image_data/misc/{weather}")
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
    def create_button(cls, name="", lock: bool=False, mirror: bool=False):
        image = Image.new("RGBA", (120, 50), (0, 0, 0, 0))
        poke_img = cls.img_open(cls, name, "poke")
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
    def create_battle_button(cls, poke: Obj.PokeDetail, mirror: bool):
        image = Image.new("RGBA", (160, 100), (0, 0, 0, 0))
        if poke.terastal_flag and poke.terastal != "":
            terastal_img = cls.img_open(cls, poke.terastal, "terastal" (100, 100))
            image.paste(terastal_img, (image.size[0]-terastal_img.size[0], 0))
        poke_img = cls.img_open(cls, poke.name, "poke")
        poke_img = poke_img.resize((int(poke_img.size[0]/3*2), int(poke_img.size[1]/3*2)))
        if poke_img.size[1] > image.size[1]:
            image.paste(poke_img, (image.size[0]-poke_img.size[0], 0))
        else:
            image.paste(poke_img, (image.size[0]-poke_img.size[0], image.size[1]-poke_img.size[1]))
        if poke.item != "":
            item_name = re.sub(r"[0-9+]", "", poke.item)
            item_image = cls.img_open(cls, item_name, "item", (40, 40))
            if mirror:
                item_image = ImageOps.mirror(item_image)
            if "+" in poke.item:
                num = re.sub(r"[^0-9]", "", poke.item)
                text: Image.Image = cls.create_text(cls, f"+{num}")
                text.thumbnail((200, item_image.size[1]/3))
                item_image.paste(text, (item_image.size[0]-text.size[0], item_image.size[1]-text.size[1]), mask=text)
            if mirror:
                item_image = ImageOps.mirror(item_image)
            image.paste(item_image, (image.size[0]-item_image.size[0], image.size[1]-item_image.size[1]), mask=item_image)
        move = cls.create_text(cls, "\n".join(poke.move_list), 4)
        move.thumbnail((140, 70))
        if mirror:
            move = ImageOps.mirror(move)
        image.paste(move, (0, image.size[1]-move.size[1]), move)
        if mirror:
            image = ImageOps.mirror(image)
        hp = poke.status_list[0].value
        dmg = hp - poke.hp_now + poke.hp_result
        hp_img = cls.create_hp_image((140, 10), hp, dmg, dmg, tk=False)
        image.paste(hp_img, (10, 5))

        return ImageTk.PhotoImage(image)

    @classmethod
    def create_double_banner(cls, poke_1: Obj.PokeDetail, poke_2: Obj.PokeDetail, mirror: bool=False):
        pass
