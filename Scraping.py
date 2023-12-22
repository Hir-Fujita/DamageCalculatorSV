from PIL import Image
import cv2
import numpy as np

def pil_cv2(image: Image.Image) -> cv2.Mat:
    return np.array(image, dtype=np.uint8)

def template_matching(src, temp, size=None):
    if size:
        ratio = size / 100
        temp = cv2.resize(temp, None, fx=ratio, fy=ratio)
    res = cv2.matchTemplate(src, temp, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    threshold = 0.8
    if max_val >= threshold:
        return True, max_loc
    else:
        return False, max_val


src = Image.open("New_Pokemon\Image_Process/2023-07-05_21-34-33.png").crop((810, 150, 910, 560))
color = src.getpixel((10, 10))
src = src.convert("L")
print(src.size)
src = pil_cv2(src)

import os
list_a = os.listdir("New_Pokemon/Image_Process/A")
list_b = os.listdir("New_Pokemon/Image_Process/B")
list_c = os.listdir("New_Pokemon/Image_Process/C")
img_list = list_c + list_b + list_a

import Object
data = Object.POKEDATA

test_list = [
    "149.png",
    "448.png",
    "645_2.png",
    "970.png",
    "991.png",
    "994.png"
]

results = []
for i in img_list:
    if i in list_a:
        parent = "New_Pokemon/Image_Process/A"
    elif i in list_b:
        parent = "New_Pokemon/Image_Process/B"
    elif i in list_c:
        parent = "New_Pokemon/Image_Process/C"
    else:
        print(f"error_{i}")
        break
    img = Image.open(f"{parent}/{i}")

# for i in test_list:
#     img = Image.open(f"New_Pokemon/Image_Process/{i}")


    img = img.resize((100, 100))
    img = img.crop(img.split()[-1].getbbox())
    back = Image.new("RGB", img.size, color)
    back.paste(img, mask=img)
    img = back.convert("L")
    img = pil_cv2(img)

    ratio_list = [36, 37, 38, 46, 47, 48, 56, 57, 58, 59, 60, 61]
    for ratio in list(range(36, 101)):
        res, max = template_matching(src, img, ratio)
        num = i.replace(".png", "")
        name = data.find(num, "number")[data.key_index("name")]
        if res:
            print(f"サクセス！！{name}")
            results.append((name, max[1]))
            break
        # else:
        #     print(f"{name}:ratio_{ratio}:max_val_{res}")
    if len(results) == 6:
        break
results = sorted(results, key=lambda x: x[1])
print(results)