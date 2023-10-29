
def auto_input(input: str):
    V_list = ["a", "i", "u", "e", "o"]
    C_list = ["k", "s", "t", "n", "h", "m", "y", "r", "w", "g", "z", "d", "b", "p", "f", "v", "j", "l", "x", "c", "q"]
    S_lsit = ["ky",  "sy",  "ty",  "ny",  "hy",  "my"]
    res = [
        ["あ", "い", "う", "え", "お"],
        ["か", "き", "く", "け", "こ"],
        ["さ", "し", "す", "せ", "そ"],
        ["た", "ち", "つ", "て", "と"],
        ["な", "に", "ぬ", "ね", "の"],
        ["は", "ひ", "ふ", "へ", "ほ"],
        ["ま", "み", "む", "め", "も"],
        ["や", "い", "ゆ", "え", "よ"],
        ["ら", "り", "る", "れ", "ろ"],
        ["わ", "うぃ", "う", "うぇ", "を"],
        ["が", "ぎ", "ぐ", "げ", "ご"],
        ["ざ", "じ", "ず", "ぜ", "ぞ"],
        ["だ", "ぢ", "づ", "で", "ど"],
        ["ば", "び", "ぶ", "べ", "ぼ"],
        ["ぱ", "ぴ", "ぷ", "ぺ", "ぽ"],
        ["ふぁ", "ふぃ", "ふ", "ふぇ", "ふぉ"],
        ["ゔぁ", "ゔぃ", "ゔ", "ゔぇ", "ゔぉ"],
        ["じゃ", "じ", "じゅ", "じぇ", "じょ"],
        ["ぁ", "ぃ", "ぅ", "ぇ", "ぉ"],
        ["ぁ", "ぃ", "ぅ", "ぇ", "ぉ"],
        ["か", "し", "く", "せ", "こ"],
        ["くぁ", "くぃ", "く", "くぇ", "くぉ"]
    ]

    result = []
    temp = []
    for t in input:
        if temp:
            if temp == ["n", "n"]:
                result.append("ん")
                temp = []
            elif t in V_list:
                result.append(res[C_list.index(temp[0])+1][V_list.index(t)])
                temp = []
            else:
                temp.append(t)

        else:
            if t in V_list:
                result.append(res[0][V_list.index(t)])
            else:
                temp.append(t)


    return "".join(result)


print(auto_input("metagurosunohakaikousei"))



import tkinter as tk

class App(tk.Frame):
    def __init__(self, master: tk.Tk=None):
        super().__init__(master)
        self.window_width = 600
        self.window_height = 300
        master.geometry(f"{self.window_width}x{self.window_height}+100+100")
        master.title(f"test")
        self.pack()

        self.text_variable = tk.StringVar()
        text_box = tk.Entry(self, width=30, textvariable=self.text_variable)
        text_box.pack()
        text_box.bind("<KeyRelease>", lambda event: self.auto_input())

    def auto_input(self):
        import re
        input = self.text_variable.get()
        self.text_variable.set("")
        pattern = r"^[a-zA-Z0-9]+$"
        r = []
        for t in input:
            if re.match(pattern, t):
                r.append(t)
        input = "".join(r)

        V_list = ["a", "i", "u", "e", "o"]
        C_list = ["k", "s", "t", "n", "h", "m", "y", "r", "w", "g", "z", "d", "b", "p", "f", "v", "j", "l", "x", "c", "q"]
        S_lsit = ["ky",  "sy",  "ty",  "ny",  "hy",  "my"]
        res = [
            ["あ", "い", "う", "え", "お"],
            ["か", "き", "く", "け", "こ"],
            ["さ", "し", "す", "せ", "そ"],
            ["た", "ち", "つ", "て", "と"],
            ["な", "に", "ぬ", "ね", "の"],
            ["は", "ひ", "ふ", "へ", "ほ"],
            ["ま", "み", "む", "め", "も"],
            ["や", "い", "ゆ", "え", "よ"],
            ["ら", "り", "る", "れ", "ろ"],
            ["わ", "うぃ", "う", "うぇ", "を"],
            ["が", "ぎ", "ぐ", "げ", "ご"],
            ["ざ", "じ", "ず", "ぜ", "ぞ"],
            ["だ", "ぢ", "づ", "で", "ど"],
            ["ば", "び", "ぶ", "べ", "ぼ"],
            ["ぱ", "ぴ", "ぷ", "ぺ", "ぽ"],
            ["ふぁ", "ふぃ", "ふ", "ふぇ", "ふぉ"],
            ["ゔぁ", "ゔぃ", "ゔ", "ゔぇ", "ゔぉ"],
            ["じゃ", "じ", "じゅ", "じぇ", "じょ"],
            ["ぁ", "ぃ", "ぅ", "ぇ", "ぉ"],
            ["ぁ", "ぃ", "ぅ", "ぇ", "ぉ"],
            ["か", "し", "く", "せ", "こ"],
            ["くぁ", "くぃ", "く", "くぇ", "くぉ"]
        ]

        result = []
        temp = []
        for t in input:
            if temp:
                if temp == ["n", "n"]:
                    result.append("ん")
                    temp = []
                elif t in V_list:
                    result.append(res[C_list.index(temp[0])+1][V_list.index(t)])
                    temp = []
                else:
                    temp.append(t)

            else:
                if t in V_list:
                    result.append(res[0][V_list.index(t)])
                else:
                    temp.append(t)

        value = self.text_variable.get()
        res = "".join(result)
        self.text_variable.set(value +res)




def main():
    win = tk.Tk()
    app = App(master=win)
    app.mainloop()

if __name__ == "__main__":
    main()
