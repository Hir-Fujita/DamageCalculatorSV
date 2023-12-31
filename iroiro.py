#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import os
import re
import pickle
from PIL import Image
import numpy as np
import cv2
import Data

import tkinter as tk


def pil_cv2(image: Image.Image) -> cv2.Mat:
    return np.array(image, dtype=np.uint8)

def create_1():
    src = Image.open("DamageCalculatorSV/Image_Process/2023-07-05_21-34-33.png").crop((810, 150, 910, 560))
    color = src.getpixel((10, 10))
    img_list = os.listdir("DamageCalculatorSV/Data/Image_data/pokemon")
    for path in img_list:
        img: Image.Image = Data.open_file(f"DamageCalculatorSV/Data/Image_data/pokemon/{path}")
        img = img.resize((100, 100))
        img = img.crop(img.split()[-1].getbbox())
        back = Image.new("RGB", img.size, color)
        back.paste(img, mask=img)
        img = back.convert("L")
        img = pil_cv2(img)
        Data.save_file(f"DamageCalculatorSV\Data\Image_data\matching_data/{path}", img)

def create_poke_image():
    """
    ポケモンの画像データを生成
    """
    image_list = os.listdir("DamageCalculatorSV\Image")
    for path in image_list:
        img = Image.open(f"DamageCalculatorSV\Image/{path}")
        img = img.resize((200, 200))
        img = img.crop(img.split()[-1].getbbox())
        name = path.replace(".png", "")
        Data.save_file(f"DamageCalculatorSV/Data/Image_data/pokemon/{name}", img)

def csv_():
    def custom_sort_key(sublist):
        num_part = re.search(r'(\d+)_(\d+)', str(sublist[1]))
        if num_part:
            # 数字_数字の形式の場合、2つの数字を比較
            return (int(num_part.group(1)), int(num_part.group(2)))
        else:
            return (int(sublist[1]),)  # 数字_数字でない場合も整数に変換して比較
    with open("DamageCalculatorSV\Data\pokedata.csv", encoding="utf-8") as f:
        reader = csv.reader(f)
        data = [row for row in reader]
    index = data.pop(0)
    sorted_list = sorted(data, key=custom_sort_key)


    with open("DamageCalculatorSV/new_poke.csv", 'w', encoding='UTF-8') as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(index)
        for i, d in enumerate(sorted_list):
            d[0] = i+1
            writer.writerow(d)

    

csv_()

# data = data.split("<tr class=")
# data = [d.split("<td>") for d in data]
# data.pop(0)
# w_list = []
# for d in data:
#     num = re.findall(r'</td><td class="c1">(.*?)</td>', d[0])
#     num = int(num[0])
#     w = d[3].replace("</td>", "")
#     w_list.append((num, w))
# with open("New_Pokemon/Data/PokeData.csv", encoding="utf-8") as f:
#     reader = csv.reader(f)
#     pokedata = [row for row in reader]
# index = pokedata.pop(0)
# print(index)
# new = []
# for d in pokedata:
#     for num, w in w_list:
#         if str(num) == d[1]:
#             d[-3] = w
#     new.append(d)
# print(new)
# with open("New_Pokemon/new_poke.csv", 'w', encoding='UTF-8') as f:
#     writer = csv.writer(f, lineterminator="\n")
#     writer.writerow(index)
#     for d in new:
#         writer.writerow(d)
# print(pokedata)
# def pil_cv2(image: Image.Image) -> cv2.Mat:
#     return np.array(image, dtype=np.uint8)
# def template_matching(src, temp, size=None):
#     if size:
#         ratio = size / 100
#         # print(ratio)
#         temp = cv2.resize(temp, None, fx=ratio, fy=ratio)
#     res = cv2.matchTemplate(src, temp, cv2.TM_CCOEFF_NORMED)
#     _, max_val, _, max_loc = cv2.minMaxLoc(res)
#     # print(max_val)
#     threshold = 0.8
#     if max_val >= threshold:
#         return True, max_loc
#     else:
#         return False, max_val

# src = Image.open("New_Pokemon\Image_Process/ss/2023-07-05_21-34-33.png").crop((810, 150, 910, 560))
# color = src.getpixel((10, 10))
# src = src.convert("L")
# src = pil_cv2(src)

# files = os.listdir("New_Pokemon/Image_Process/poke")
# for path in files:
#     image = Image.open(f"New_Pokemon/Image_Process/poke/{path}")
#     image = image.resize((100, 100))
#     image = image.crop(image.split()[-1].getbbox())
#     back = Image.new("RGB", image.size, color)
#     back.paste(image, mask=image)

#     name = path.replace(".png", "")
#     back.save(f"New_Pokemon/Image_Process/test_poke/{name}.png")


# with open("New_Pokemon/Data/PokeData.csv", encoding="utf-8") as f:
#     reader = csv.reader(f)
#     data = [row for row in reader]
#     num_list = [row[1] for row in data]
#     index_data = data.pop(0)
#     num_list.pop(0)

# print(num_list)
# for index, number in enumerate(num_list):
#     flag = False
#     l = os.listdir("New_Pokemon/Image_Process/4")
#     for i in l:
#         i = i.replace(".png", "")
#         if i == number:
#             data[index][-1] = 4
#             flag = True
#             break
#     l = os.listdir("New_Pokemon/Image_Process/3")
#     if not flag:
#         for i in l:
#             i = i.replace(".png", "")
#             if i == number:
#                 data[index][-1] = 3
#                 flag = True
#                 break
#     l = os.listdir("New_Pokemon/Image_Process/2")
#     if not flag:
#         for i in l:
#             i = i.replace(".png", "")
#             if i == number:
#                 data[index][-1] = 2
#                 flag = True
#                 break
#     l = os.listdir("New_Pokemon/Image_Process/1")
#     if not flag:
#         for i in l:
#             i = i.replace(".png", "")
#             if i == number:
#                 data[index][-1] = 1
#                 flag = True
#                 break
#     l = os.listdir("New_Pokemon/Image_Process/0")
#     if not flag:
#         for i in l:
#             i = i.replace(".png", "")
#             if i == number:
#                 data[index][-1] = 0
#                 flag = True
#                 break

# with open("New_Pokemon/new_poke.csv", 'w', encoding='UTF-8') as f:
#     writer = csv.writer(f, lineterminator="\n")
#     writer.writerow(index_data)
#     for d in data:
#         writer.writerow(d)


    # with open(f"New_Pokemon/Data/Image_data/type/{name}", "wb") as f:
    #     pickle.dump(image, f)

# files = os.listdir("New_Pokemon/item/icon/")
# for path in files:
# img = Image.open(f"New_Pokemon/Image_Process/item_0581.png")
# img = img.resize((100, 100))

# with open(f"New_Pokemon/Data/Image_data/item/でかいきんのたま", "wb") as f:
#     pickle.dump(img, f)

# kana = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもらりるれろやゆよわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽゔぁぃぅぇぉゃゅょっｎー"
# kata = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモラリルレロヤユヨワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポヴァィゥェォャュョッンー"
# files = os.listdir("New_Pokemon/item icons/icon")
# data = []
# data.append(["","name", "kata"])
# for index, path in enumerate(files):
#     name = path.replace(".png", "")
#     kata_names = []
#     for n in name:
#         if n in kata:
#             kata_names.append(n)
#         else:
#             index = kana.index(n)
#             kata_names.append(kata[index])
#     kata_name = "".join(kata_names)
#     data.append([index, name, kata_name])
# with open("New_Pokemon/new_item.csv", 'w', encoding='UTF-8') as f:
#     writer = csv.writer(f, lineterminator="\n")
#     for d in data:
#         writer.writerow(d)

# with open("New_Pokemon\Data\move.csv", encoding="utf-8") as f:
#     reader = csv.reader(f)
#     data = [row for row in reader]

# data = [row[0].split(";") for row in data]
# print(data)
# array = []
# for dd in data:
#     new_list = []
#     for d in dd:
#         if "×" in d:
#             d = ""
#         if "○" in d:
#             d = "○"
#         if "1体選択" == d:
#             d = ""
#         if "自分" == d:
#             d = ""
#         if "ランダム1体" == d:
#             d = ""
#         new_list.append(d)
#     array.append(new_list)

# print(array)
# with open("New_Pokemon/new_move.csv", 'w', encoding='UTF-8') as f:
#     writer = csv.writer(f, lineterminator="\n")
#     for d in array:
#         writer.writerow(d)


# a = [str(num) for num in range(20)]

# print(a[6: 12])

# with open("New_Pokemon\Data\poke_data.csv", encoding="utf-8") as f:
#     reader = csv.reader(f)
#     data = [row for row in reader]
# index = data.pop(0)



# def custom_sort_key(sublist):
#     num_part = re.search(r'(\d+)_(\d+)', str(sublist[1]))
#     if num_part:
#         # 数字_数字の形式の場合、2つの数字を比較
#         return (int(num_part.group(1)), int(num_part.group(2)))
#     else:
#         return (int(sublist[1]),)  # 数字_数字でない場合も整数に変換して比較
# sorted_list = sorted(data, key=custom_sort_key)


# with open("New_Pokemon/new_poke.csv", 'w', encoding='UTF-8') as f:
#     writer = csv.writer(f, lineterminator="\n")
#     writer.writerow(index)
#     for i, d in enumerate(sorted_list):
#         d[0] = i+1
#         writer.writerow(d)