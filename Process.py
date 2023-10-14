#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pickle
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageOps, ImageFont, ImageFilter
import Data as D
import Object as Obj

def open_file(path):
    with open(path, "rb") as f:
        data = pickle.load(f)
    return data

def save_file(path, data):
    with open(path, "wb") as f:
        pickle.dump(data, f)

def save_filedialogwindow(save_name: str, title: str, parent_folder: str="") -> str:
    save_folder = f"./{D.FOLDER}/Data/{parent_folder}"
    filepath = filedialog.asksaveasfilename(
        title=title,
        initialfile=save_name,
        defaultextension=f".txt",
        filetypes=[("Text File", ".txt")],
        initialdir=save_folder
    )
    return filepath

def open_filedialogwindow(title: str, parent_folder: str="") -> str:
    load_folder = f"./{D.FOLDER}/Data/{parent_folder}"
    filepath = filedialog.askopenfilename(
        title=title,
        multiple=False,
        initialdir=load_folder,
        filetypes=[("Text File", ".txt")]
    )
    return filepath

def metronome(name: str, mirror: bool) -> Image.Image:
        name = name.replace("メトロノーム", "")
        image: Image.Image = open_file(f"{D.FOLDER}/Data/Image_data/item/メトロノーム")
        text_image = Image.new("RGBA", (image.size[0], image.size[1]), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_image)
        font = ImageFont.truetype(f"{D.FOLDER}/Data/Corporate-Logo-Rounded-Bold-ver3.otf", 40)
        draw.text((0, 0), name, fill="white", stroke_width=2, stroke_fill="black", font=font)
        text_image = text_image.crop(text_image.split()[-1].getbbox())
        if mirror:
            text_image = ImageOps.mirror(text_image)
            image.paste(text_image, (0, image.size[1]-text_image.size[1]), mask=text_image)
        else:
            image.paste(text_image, (image.size[0]-text_image.size[0], image.size[1]-text_image.size[1]), mask=text_image)
        return image

class ImageGenerator:
    @classmethod
    def create_page1(self, name: str="", item: str="", terastal: str=""):
        size = (200, 200)
        image = Image.new("RGBA", size, (0, 0, 0, 0))
        if name:
            number = D.POKEDATA.find(name, "name", "number")
        else:
            number = "0"
        if terastal:
            terastal_image: Image.Image = open_file(f"{D.FOLDER}/Data/Image_data/type/{terastal}")
            terastal_image.thumbnail((100, 100))
            image.paste(terastal_image, (0, 0), terastal_image)
        poke_image: Image.Image = open_file(f"{D.FOLDER}/Data/Image_data/pokemon/{number}")
        image.paste(poke_image, (size[0]//2 - poke_image.size[0]//2, size[1]-poke_image.size[1]), mask=poke_image)
        if item:
            if "メトロノーム" in item:
                item_image = metronome(item, False)
            else:
                item_image: Image.Image = open_file(f"{D.FOLDER}/Data/Image_data/item/{item}")
            item_image = item_image.resize((70, 70))
            image.paste(item_image, (size[0]-item_image.size[0]-10, size[1]-item_image.size[1]), mask=item_image)
        return ImageTk.PhotoImage(image)

    @classmethod
    def create_banner(self, data: D.PokeData=None):
        size = (400, 200)
        image = Image.new("RGBA", size=size, color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        if data is None:
            draw.rounded_rectangle(
                [(0, 0), (size[0]-1, size[1]-1)],
                radius=10, fill="gray", outline="black", width=3)
        else:
            color = D.TYPEDATA.typecolor(data.terastal)
            draw.rounded_rectangle(
                [(0, 0), (size[0]-1, size[1]-1)],
                radius=10, fill=color, outline="black", width=3)
            terastal_icon: Image.Image = open_file(f"{D.FOLDER}/Data/Image_data/type/{data.terastal}")
            terastal_icon.thumbnail((size[1]-10, size[1]-10))
            image.paste(terastal_icon, (size[0]//2 - terastal_icon.size[0]//2, size[1]//2 - terastal_icon.size[1]//2), mask=terastal_icon)
            number = D.POKEDATA.find(data.name, "name", "number")
            pokemon_icon: Image.Image = open_file(f"{D.FOLDER}/Data/Image_data/pokemon/{number}")
            pokemon_icon.thumbnail((size[1]-10, size[1]-10))
            pokemon_icon = ImageOps.mirror(pokemon_icon)
            image.paste(pokemon_icon, (10, size[1]-pokemon_icon.size[1]-4), mask=pokemon_icon)
            if data.item:
                if "メトロノーム" in data.item:
                    item_icon = metronome(data.item, True)
                else:
                    item_icon: Image.Image = open_file(f"{D.FOLDER}/Data/Image_data/item/{data.item}")
                item_icon.thumbnail((60, 60))
                item_icon = ImageOps.mirror(item_icon)
                image.paste(item_icon, (4, size[1]-item_icon.size[1]-4), mask=item_icon)
            font = ImageFont.truetype(f"{D.FOLDER}/Data/Corporate-Logo-Rounded-Bold-ver3.otf", 26)
            draw.text((10, 4), f"{data.name}:Lv{data.level}",fill="white", stroke_width=2, stroke_fill="black", font=font)
            font = ImageFont.truetype(f"{D.FOLDER}/Data/Corporate-Logo-Rounded-Bold-ver3.otf", 20)
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
    def create_page3(self, name:str="", item: str="", terastal: str="", mirror: bool=True):
        size = (180, 180)
        image = Image.new("RGBA", size, (0, 0, 0, 0))
        if name:
            number = D.POKEDATA.find(name, "name", "number")
        else:
            number = "0"
        if terastal:
            terastal_image: Image.Image = open_file(f"{D.FOLDER}/Data/Image_data/type/{terastal}")
            terastal_image.thumbnail((150, 150))
            image.paste(terastal_image, (size[0]-terastal_image.size[0], 0), terastal_image)
        poke_image: Image.Image = open_file(f"{D.FOLDER}/Data/Image_data/pokemon/{number}")
        image.paste(poke_image, (size[0]//2 - poke_image.size[0]//2, size[1]-poke_image.size[1]), mask=poke_image)
        if item:
            if "メトロノーム" in item:
                item_image = metronome(item, mirror)
            else:
                item_image: Image.Image = open_file(f"{D.FOLDER}/Data/Image_data/item/{item}")
            item_image = item_image.resize((70, 70))
            image.paste(item_image, (size[0]-item_image.size[0], size[1]-item_image.size[1]), mask=item_image)
        if mirror:
            image = ImageOps.mirror(image)
        return ImageTk.PhotoImage(image)

    @classmethod
    def create_hp_image(self, size: "tuple[int]", hp: int, max: int, min: int, width: int=2):
        def hp_color(ratio: int):
            GREEN = (0, 196, 0)
            GREEN_2 = (164, 255, 164)
            YELLOW = (229, 176, 0)
            YELLOW_2 = (255, 255, 148)
            RED = (255, 0, 0)
            RED_2 = (226, 139, 139)
            BLACK = (0, 0, 0)
            if ratio > 50:
                return GREEN, GREEN_2
            elif ratio <= 20:
                return RED, RED_2
            elif ratio >= 100:
                return BLACK, BLACK
            else:
                return YELLOW, YELLOW_2
        image = Image.new("RGB", (size[0]+width, size[1]+width*2), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        ratio = size[0] // 100
        max_dmg = round((hp - max) / hp * 100, ratio)
        color_max, _ = hp_color(max_dmg)
        min_dmg = round((hp - min) / hp * 100, ratio)
        _, color_min = hp_color(min_dmg)
        # if now:
        #     max_dmg = round((now - max) / now * 100, ratio)
        #     min_dmg = round((now - min) / now * 100, ratio)
        #     color_max, _ = hp_color(max_dmg)
        #     _, color_min = hp_color(min_dmg)
        if min_dmg > 0:
            draw.rectangle((width, width, min_dmg *ratio-1, size[1]+width-1), fill=color_min)
        if max_dmg > 0:
            draw.rectangle((width, width, max_dmg *ratio-1, size[1]+width-1), fill=color_max)
        for i in range(9):
            num = i+1
            draw.line(((num*10*ratio, width), (num*10*ratio, size[1]+width-1)), (255, 255, 255), 1)
        return ImageTk.PhotoImage(image)

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
            field_img = open_file(f"{D.FOLDER}/Data/Image_data/misc/field")
            image.paste(paste, mask=field_img)
        if weather:
            weather_img = open_file(f"{D.FOLDER}/Data/Image_data/misc/{weather}")
            image.paste(weather_img, mask=weather_img)
        return ImageTk.PhotoImage(image)

    @classmethod
    def create_button(self, name="", lock: bool=False, mirror: bool=False):
        image = Image.new("RGBA", (120, 50), (0, 0, 0, 0))
        if name == "":
            poke: Image.Image = open_file(f"{D.FOLDER}/Data/Image_data/pokemon/0")
        else:
            num = D.POKEDATA.find(name, "name", "number")
            poke: Image.Image = open_file(f"{D.FOLDER}/Data/Image_data/pokemon/{num}")
        poke = poke.resize((poke.size[0]*2, poke.size[1]*2))
        poke = poke.crop((0, 0, poke.size[0], poke.size[1]/3*2))
        poke = poke.crop(poke.split()[-1].getbbox())
        poke.thumbnail((120, 50))
        poke = ImageOps.mirror(poke)
        image.paste(poke, (0, 0))
        if not mirror:
            image = ImageOps.mirror(image)
        if lock:
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype(f"{D.FOLDER}/Data/Corporate-Logo-Rounded-Bold-ver3.otf", 20)
            draw.text((62, 29), "LOCK",fill="white", stroke_width=2, stroke_fill="black", font=font)
        return ImageTk.PhotoImage(image)

