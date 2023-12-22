#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import itertools
import Object as Obj
import Data as D

MOVE = "move"
ATK = "attack"
DEF = "defence"
DMG = "damage"

def my_round(val) -> int:
    """
    四捨五入
    """
    return int((val * 2 + 1) // 2)

def my_round5(val) ->int:
    """
    五捨五超入
    """
    return int(math.ceil(val-0.5))

def rank_int(value):
    if value:
        return int(value)
    else:
        return 0

def fixed_num(hp: int, result: tuple[int]) -> (int, int, str):
    min_dmg, max_dmg = result[0], result[-1]
    num, temp, count = 1, [], 0
    while min_dmg != 0:
        if hp <= min_dmg * num:
            return num, 100, "確定"
        elif hp <= max_dmg * num:
            if num < 4:
                temp = list(itertools.product(result, repeat=num))
                count = sum(1 for i in temp if hp <= sum(i))
                per = round(count / len(temp) * 100, 2)
            else:
                per = "計算中止"
            return num, per, "乱数"
        else:
            num += 1
    return 0, 0, "確定"

class DamageCalculator:
    def __init__(
            self,
            attacker: Obj.SendData,
            attacker_field: Obj.SendData,
            target: Obj.SendData,
            target_field: Obj.SendData,
            field: Obj.SendData
        ):
        self.attacker: Obj.SendData = attacker
        self.attacker_field: Obj.SendData = attacker_field
        self.target: Obj.SendData = target
        self.target_field: Obj.SendData = target_field
        self.field: Obj.SendData = field

        self.log = []
        self.calc_log = []
        self.move_damage_list: "list[int]" = [] #威力補正
        self.attack_list: "list[int]" = [] #攻撃補正
        self.defence_list: "list[int]" = [] #防御補正
        self.damage_list: "list[int]" = [] #ダメージ補正

        self.attacker_type = [D.POKEDATA.find(self.attacker.name, "name", "type1"), D.POKEDATA.find(self.attacker.name, "name", "type2")]
        self.target_type = [D.POKEDATA.find(self.target.name, "name", "type1"), D.POKEDATA.find(self.target.name, "name", "type2")]
        self.attacker_status = self.status_calculation(self.attacker, self.attacker_field, self.target, self.field)
        self.target_status = self.status_calculation(self.target, self.target_field, self.attacker, self.field)

        self.attack = 0
        self.defence = 0

        self.result = 0
        self.drain = []
        self.recoil = []

    def calculation(self, move_name: str):
        self.move = D.MOVEDATA.find(move_name, "name")
        self.move_name = self.move[D.MOVEDATA.key_index("name")]
        self.move_type = self.move[D.MOVEDATA.key_index("type")]
        self.move_power = int(self.move[D.MOVEDATA.key_index("power")])
        self.move_category = self.move[D.MOVEDATA.key_index("category")]
        if self.move_category in ["物理", "特殊"]:
            self.move_category_change()
            self.poke_type_change()
            self.move_type_change()
            self.move_power_check()

            self.item_calculation()
            self.field_calculation()
            self.active_calculation()
            self.ability_calculation()
            self.weather_calculation()
            self.move_calculation()

    def type_effective(self, attack_type: str, defence_types: "list[str]") -> float:
        result = 1
        for deff in defence_types:
            if deff != "":
                if deff == "ゴースト" and self.attacker.ability in ["きもったま, しんがん"]:
                    if not self.gas_check():
                        self.log.append(f"{self.attacker.ability}: *1.0")
                elif deff == "みず" and self.move_name == "フリーズドライ":
                    result = result * 2
                else:
                    result = result * float(D.TYPEDATA.calc(attack_type, deff))
        return result

    def add(self, list_name: str, name: str, num: int):
        if list_name == MOVE:
            add_list = self.move_damage_list
        elif list_name == ATK:
            add_list = self.attack_list
        elif list_name == DEF:
            add_list = self.defence_list
        elif list_name == DMG:
            add_list = self.damage_list
        add_list.append(num)
        ratio = round(num / 4096, 1)
        self.log.append(f"{name}: *{ratio}")

    def status_calculation(self, poke: Obj.SendData, player: Obj.SendData, opponent_poke: Obj.SendData, field: Obj.SendData):
        def paradox_check(poke: Obj.SendData, field: Obj.SendData) -> bool:
            """
            パラドックスの特性が発動するならTrue,しないならFalseを返す
            """
            if poke.ability == "こだいかっせい" and field.weather == "にほんばれ":
                if self.weather_check():
                    return True
                else:
                    return False
            elif poke.ability == "こだいかっせい" and poke.ability_flag:
                return True
            elif poke.ability == "クォークチャージ" and field.field == "エレキフィールド":
                return True
            elif poke.ability == "クォークチャージ" and poke.ability_flag:
                return True
            else:
                return False

        status: "list[list[int]]" = []
        for index, stat in enumerate(poke.status):
            if index == 0:
                status.append([poke.hp_now, stat])
            else:
                if rank_int(poke.rank[index-1]) > 0:
                    rank = (rank_int(poke.rank[index-1]) +2) /2
                    if opponent_poke.ability == "てんねん" and not self.gas_check():
                        if poke.ability != "かたやぶり":
                            rank = 1
                else:
                    rank = 2 /(2 - rank_int(poke.rank[index-1]))
                num = math.floor(stat * rank)
                status.append([stat, num])
        if paradox_check(poke, field):
            max_stat = 0
            max_index = 0
            for index, stat in enumerate(status):
                if index != 0:
                    if stat[1] > max_stat:
                        max_stat = stat[1]
                        max_index = index
                    if max_index == 5:
                        status[max_index].append(my_round(max_stat * 6144 / 4096))
                    else:
                        status[max_index].append(my_round(max_stat * 5325 / 4096))
                    label = D.LABEL[max_index]
            self.log.append(f"{poke.ability}発動: {label}上昇")
        status[5][1] = self.speed_calc(poke, player, field, status[5][-1])
        return status

    def speed_calc(self, poke: Obj.SendData, player_field: Obj.SendData, field: Obj.SendData, spd: int):
        speed = 4096
        if not self.gas_check():
            if poke.ability == "ようりょくそ" and field.weather == "にほんばれ":
                speed = my_round5(speed * 8192 / 4096)
                self.log.append(f"{poke.ability}: 素早*2.0")
            if poke.ability == "すいすい" and field.weather == "あめ":
                speed = my_round5(speed * 8192 / 4096)
                self.log.append(f"{poke.ability}: 素早*2.0")
            if poke.ability == "すなかき" and field.weather == "すなあらし":
                speed = my_round5(speed * 8192 / 4096)
                self.log.append(f"{poke.ability}: 素早*2.0")
            if poke.ability == "ゆきかき" and field.weather == "ゆき":
                speed = my_round5(speed * 8192 / 4096)
                self.log.append(f"{poke.ability}: 素早*2.0")
            if poke.ability == "サーフテール" and field.field == "エレキフィールド":
                speed = my_round5(speed * 8192 / 4096)
                self.log.append(f"{poke.ability}: 素早*2.0")
            if poke.ability == "かるわざ" and poke.ability_flag:
                speed = my_round5(speed * 8192 / 4096)
                self.log.append(f"{poke.ability}: 素早*2.0")
            if poke.ability == "はやあし" and poke.bad_stat in ["まひ", "やけど", "どく", "もうどく", "こおり", "ねむり"]:
                speed = my_round5(speed * 8192 / 4096)
                self.log.append(f"{poke.ability}: 素早*1.5")
        if poke.item == 'こだわりスカーフ' and poke.ability != "ぶきよう":
            speed = my_round5(speed * 6144 / 4096)
            self.log.append(f"{poke.item}: 素早*1.5")
        if poke.item == "くろいてっきゅう" and poke.ability != "ぶきよう":
            speed = my_round5(speed * 2048 / 4096)
            self.log.append(f"{poke.item}: 素早*0.5")
        if player_field.wind:
            speed = my_round5(speed * 8192 / 4096)
            self.log.append("おいかぜ: 素早*2.0")
        speed = my_round5(spd * speed / 4096)
        if poke.bad_stat == "まひ":
            if poke.ability == "はやあし":
                if self.gas_check():
                    speed = math.floor(speed / 2)
                    self.log.append("まひ: 素早*0.5")
            else:
                speed = math.floor(speed / 2)
                self.log.append("まひ: 素早*0.5")
        return speed

    def poke_type_change(self):
        """
        ポケモンのタイプを変更する
        """
        if self.attacker.name == "アルセウス":
            name = D.ITEMDATA.find(self.attacker.item, "name", "type")
            if not "_" in name and name != "":
                self.attacker_type = [D.ITEMDATA.find(self.attacker.item, "name", "type")]
                self.log.append(f"攻撃側: {self.attacker.name}: タイプ変更:{self.attacker_type}")
        if self.target.name == "アルセウス":
            name = D.ITEMDATA.find(self.target.item, "name", "type")
            if not "_" in name and name != "":
                self.target_type = [D.ITEMDATA.find(self.target.item, "name", "type")]
                self.log.append(f"防御側: {self.target.name}: タイプ変更:{self.target_type}")
        if self.attacker.terastal_flag:
            self.attacker_type.append(self.attacker.terastal)
            self.log.append(f"攻撃側: {self.attacker.name}: テラスタル{self.attacker.terastal}")
        if self.target.terastal_flag:
            self.target_type = [self.target.terastal]
            self.log.append(f"防御側: {self.target.name}: テラスタル{self.target.terastal}")

    def move_type_change(self):
        """
        わざのタイプを変更する
        """
        if self.attacker.name == "ケンタロス(パルデア炎)" and self.move_name == "レイジングブル":
            self.move_type = "ほのお"
            self.log.append(f"タイプ変更: {self.move_name} {self.move_type}")
        if self.attacker.name == "ケンタロス(パルデア水)" and self.move_name == "レイジングブル":
            self.move_type = "みず"
            self.log.append(f"タイプ変更: {self.move_name} {self.move_type}")
        if self.move_name == "ウェザーボール":
            if self.field.weather == "にほんばれ":
                self.move_power = 100
                self.move_type = "ほのお"
                self.log.append(f"タイプ変更: {self.move_name} {self.move_type}")
            elif self.field.weather == "あめ":
                self.move_power = 100
                self.move_type = "みず"
                self.log.append(f"タイプ変更: {self.move_name} {self.move_type}")
            elif self.field.weather == "すなあらし":
                self.move_power = 100
                self.move_type = "いわ"
                self.log.append(f"タイプ変更: {self.move_name} {self.move_type}")
            elif self.field.weather == "ゆき":
                self.move_power = 100
                self.move_type = "こおり"
                self.log.append(f"タイプ変更: {self.move_name} {self.move_type}")
        if self.move_name == "さばきのつぶて":
            name = D.ITEMDATA.find(self.attacker.item, "name", "type")
            if not "_" in name and name != "":
                self.move_type = D.ITEMDATA.find(self.attacker.item, "name", "type")
                self.log.append(f"タイプ変更: {self.move_name} {self.move_type}")
        if self.move_name == "だいちのはどう":
            if self.field.field == "エレキフィールド":
                self.move_power = 100
                self.move_type = "でんき"
                self.log.append(f"タイプ変更: {self.move_name} {self.move_type}")
            elif self.field.field == "グラスフィールド":
                self.move_power = 100
                self.move_type = "くさ"
                self.log.append(f"タイプ変更: {self.move_name} {self.move_type}")
            elif self.field.field == "ミストフィールド":
                self.move_power = 100
                self.move_type = "フェアリー"
                self.log.append(f"タイプ変更: {self.move_name} {self.move_type}")
            elif self.field.field == "サイコフィールド":
                self.move_power = 100
                self.move_type = "エスパー"
                self.log.append(f"タイプ変更: {self.move_name} {self.move_type}")
        if self.move_name == "ツタこんぼう" and "オーガポン" in self.attacker.name:
            if self.attacker.item == "いどのめん":
                self.move_type = "みず"
                self.log.append(f"タイプ変更: {self.move_name} {self.move_type}")
            elif self.attacker.item == "かまどのめん":
                self.move_type = "ほのお"
                self.log.append(f"タイプ変更: {self.move_name} {self.move_type}")
            elif self.attacker.item == "いしずえのめん":
                self.move_type = "いわ"
                self.log.append(f"タイプ変更: {self.move_name} {self.move_type}")
        if self.move_name == "テラバースト" and self.attacker.terastal_flag:
            self.move_type = self.attacker.terastal
            self.log.append(f"タイプ変更: {self.move_name} {self.move_type}")
        if self.move_name == "めざめるダンス" and "オドリドリ" in self.attacker.name:
            self.move_type = D.POKEDATA.find(self.attacker.name, "name", "type1")
            self.log.append(f"タイプ変更: {self.move_name} {self.move_type}")

    def move_category_change(self):
        """
        テラバーストの処理,物理特殊の処理
        """
        if self.move_name == "テラバースト":
            if self.attacker.terastal_flag:
                self.move_type = self.attacker.terastal
                if self.attacker_status[1][-1] > self.attacker_status[3][-1]:
                    self.move_category = "物理"
                    self.log.append(f"テラバースト物理")
        if self.move_name == "シェルアームズ":
            a = ((self.attacker.level *2 /5 +2) *90 *self.attacker_status[1][-1] /self.target_status[2][-1]) / 50
            c = ((self.attacker.level *2 /5 +2) *90 *self.attacker_status[3][-1] /self.target_status[4][-1]) / 50
            if a > c:
                self.move_category == "物理"
        if self.move_category == "物理":
            self.defence = self.target_status[2]
            if self.move_name == "ボディプレス":
                self.attack = self.attacker_status[2]
                if len(self.attacker_status[1]) == 3:
                    self.attack = my_round(self.attacker_status[2][-1] * 6144 / 4096)
            else:
                if self.move_name == "イカサマ":
                    self.attack = self.target_status[1][-1]
                else:
                    self.attack = self.attacker_status[1][-1]
        elif self.move_category == "特殊":
            self.attack = self.attacker_status[3][-1]
            if self.move_name == "サイコショック" or self.move_name == "サイコブレイク":
                self.defence = self.target_status[2]
            else:
                self.defence = self.target_status[4]
        if self.move_name == "せいなるつるぎ":
            self.defence = self.defence[0]
        else:
            self.defence = self.defence[-1]

    def gas_check(self) -> bool:
        """
        かがくへんかガスならTrue,違うならFalseを返す
        """
        if self.attacker.ability == "かがくへんかガス":
            return True
        elif self.target.ability == "かがくへんかガス":
            return True
        else:
            return False

    def weather_check(self) -> bool:
        """
        天候が影響するならTrue,しないならFalseを返す
        """
        if self.attacker.ability == "エアロック" or self.attacker.ability == "ノーてんき":
            if self.gas_check():
                return True
            return False
        else:
            return True

    def move_power_check(self):
        if self.move_name in ["アシストパワー", "つけあがる"]:
            power = 20
            for rank in self.attacker.rank:
                if rank_int(rank) > 0:
                    power = power +(20 *rank_int(rank))
            self.move_power = power
            self.log.append(f"{self.move_name}: 威力{self.move_power}")

        if self.move_name in ["けたぐり", "くさむすび"]:
            kg = float(D.POKEDATA.find(self.target.name, "name", "weight"))
            if kg < 10:
                self.move_power = 20
            elif kg < 25:
                self.move_power = 40
            elif kg < 50:
                self.move_power = 60
            elif kg < 100:
                self.move_power = 80
            elif kg < 200:
                self.move_power = 100
            elif 200 < kg:
                self.move_power = 120
            self.log.append(f"{self.move_name}: 威力{self.move_power}")

        if self.move_name in ["しおふき", "ふんか", "ドラゴンエナジー"]:
            self.move_power = math.floor(150 * self.attacker_status[0][0] / self.attacker_status[0][1])
            self.log.append(f"{self.move_name}: 威力{self.move_power}")

        if self.move_name in ["きしかいせい", "じたばた"]:
            x = math.floor(48 *self.attacker_status[0][0] /self.attacker_status[0][1])
            if 33 <= x:
                self.move_power = 20
            elif 17 <= x <= 32:
                self.move_power = 40
            elif 10 <= x <= 16:
                self.move_power = 80
            elif 5 <= x <= 9:
                self.move_power = 100
            elif 2 <= x <= 4:
                self.move_power = 150
            elif 0 <= x <= 1:
                self.move_power = 200
            self.log.append(f"{self.move_name}: 威力{self.move_power}")

        if self.move_name in ["ヒートスタンプ", "ヘビーボンバー"]:
            atk = float(D.POKEDATA.find(self.attacker.name, "name", "weight"))
            deff = float(D.POKEDATA.find(self.target.name, "name", "weight"))
            if self.target.item == "かるいし":
                deff = deff /2
            if deff <= atk /5:
                self.move_power = 120
            elif deff <= atk /4:
                self.move_power = 100
            elif deff <= atk /3:
                self.move_power = 80
            elif deff <= atk /2:
                self.move_power = 60
            else:
                self.move_power = 40
            self.log.append(f"{self.move_name}: 威力{self.move_power}")

        if self.move_name == "たたりめ" and self.target.bad_stat != "":
            self.move_power = 130
            self.log.append(f"{self.move_name}: 威力{self.move_power}")

        if self.move_name == "なげつける" and self.attacker.item != "":
            self.move_power = int(D.ITEMDATA.find(self.attacker.item, "name", "なげつける"))
            self.log.append(f"{self.move_name}: 威力{self.move_power}")

        if self.move_name == "エレキボール":
            atk_spd = self.attacker_status[5][-1]
            def_spd = self.target_status[5][-1]
            if atk_spd >= def_spd *4:
                self.move_power = 150
            elif atk_spd >= def_spd *3:
                self.move_power = 120
            elif atk_spd >= def_spd *2:
                self.move_power = 80
            elif atk_spd >= def_spd:
                self.move_power = 60
            elif atk_spd < def_spd:
                self.move_power = 40
            self.log.append(f"{self.move_name}: 威力{self.move_power}")

        if self.move_name == "ジャイロボール":
            atk_spd = self.attacker_status[5][-1]
            def_spd = self.target_status[5][-1]
            self.move_power = math.floor((25 * def_spd / atk_spd) +1)
            if self.move_power > 150:
                self.move_power = 150
            self.log.append(f"{self.move_name}: 威力{self.move_power}")

    def item_calculation(self):
        """
        ダメージ計算に影響するアイテムの計算
        """
        if D.ITEMDATA.find(self.attacker.item, "name", "type") == self.move_type:
            self.add(MOVE, self.attacker.item, 4915)
        if self.attacker.item == "こんごうだま" and self.attacker.name == "ディアルガ(通常)":
            if self.move_type == "ドラゴン" or self.move_type == "はがね":
                self.add(MOVE, self.attacker.item, 4915)
        if self.attacker.item == "だいこんごうだま" and self.attacker.name == "ディアルガ(オリジン)":
            if self.move_type == "ドラゴン" or self.move_type == "はがね":
                self.add(MOVE, self.attacker.item, 4915)
        if self.attacker.item == "しらたま" and self.attacker.name == "パルキア(通常)":
            if self.move_type == "ドラゴン" or self.move_type == "みず":
                self.add(MOVE, self.attacker.item, 4915)
        if self.attacker.item == "だいしらたま" and self.attacker.name == "パルキア(オリジン)":
            if self.move_type == "ドラゴン" or self.move_type == "みず":
                self.add(MOVE, self.attacker.item, 4915)
        if self.attacker.item == "はっきんだま" and self.attacker.name == "ギラティナ(アナザー)":
            if self.move_type == "ドラゴン" or self.move_type == "ゴースト":
                self.add(MOVE, self.attacker.item, 4915)
        if self.attacker.item == "だいはっきんだま" and self.attacker.name == "ギラティナ(オリジン)":
            if self.move_type == "ドラゴン" or self.move_type == "ゴースト":
                self.add(MOVE, self.attacker.item, 4915)
        if self.attacker.item == "ノーマルジュエル" and self.move_type == "ノーマル":
            self.add(MOVE, self.attacker.item, 5325)
        if self.attacker.item == "ちからのハチマキ" and self.move_category == "物理":
            self.add(MOVE, self.attacker.item, 4505)
        if self.attacker.item == "ものしりメガネ" and self.move_category == "特殊":
            self.add(MOVE, self.attacker.item, 4505)
        if self.attacker.item == "パンチグローブ" and self.move[D.MOVEDATA.key_index("パンチわざ")] != "":
            self.add(MOVE, self.attacker.item, 4506)
        if self.attacker.item == "こだわりハチマキ" and self.move_category == "物理":
            self.add(ATK, self.attacker.item, 6144)
        if self.attacker.item == "こだわりメガネ" and self.move_category == "特殊":
            self.add(ATK, self.attacker.item, 6144)
        if self.attacker.item == "でんきだま" and self.attacker.name == "ピカチュウ":
            self.add(ATK, self.attacker.item, 8192)
        if self.attacker.item in ["かまどのめん", "いどのめん", "いしずえのめん"] and "オーガポン" in self.attacker.name:
            self.add(MOVE, self.attacker.item, 4915)
        if self.target.item == "しんかのきせき":
            self.add(DEF, self.target.item, 6144)
        if self.target.item == "とつげきチョッキ" and self.move_category == "特殊":
            self.add(DEF, self.target.item, 6144)
        if self.attacker.item == "いのちのたま":
            self.add(DMG, self.attacker.item, 5324)
        if self.attacker.item == "たつじんのおび" and self.type_effective(self.move_type, self.target_type) >= 2:
            self.add(DMG, self.attacker.item, 4915)
        if self.attacker.item == "メトロノーム+2":
            self.add(DMG, self.attacker.item, 4915)
        if self.attacker.item == "メトロノーム+3":
            self.add(DMG, self.attacker.item, 5734)
        if self.attacker.item == "メトロノーム+4":
            self.add(DMG, self.attacker.item, 6553)
        if self.attacker.item == "メトロノーム+5":
            self.add(DMG, self.attacker.item, 7372)
        if self.attacker.item == "メトロノーム+6":
            self.add(DMG, self.attacker.item, 8192)
        if self.type_effective(self.move_type, self.target_type) >= 2:
            if D.ITEMDATA.find(self.target.item, "name", "type") == f"_{self.move_type}":
                self.add(DMG, self.target.item, 2048)
        if self.target.item == "ホズのみ" and self.move_type == "ノーマル":
            self.add(DMG, self.target.item, 2048)

    def field_calculation(self):
        """
        ダメージ計算に影響するフィールドの計算
        """
        if self.field.field == "エレキフィールド":
            if self.move_name == "サイコブレイド":
                    self.add(MOVE, self.move_name, 6144)
            if not "ひこう" in self.attacker_type and self.attacker.ability != "ふゆう":
                if self.move_type == "でんき":
                    self.add(MOVE, f"{self.field.field}強化", 5325)
                if self.move_name == "ライジングボルト":
                    self.add(MOVE, f"{self.move_name}+{self.field.field}", 6144)
        if self.field.field == "サイコフィールド":
            if not "ひこう" in self.attacker_type and self.attacker.ability != "ふゆう":
                if self.move_type == "エスパー":
                    self.add(MOVE, f"{self.field.field}強化", 5325)
                if self.move_name == "ワイドフォース":
                    self.add(MOVE, f"{self.move_name}+{self.field.field}", 6144)
        if self.field.field == "ミストフィールド":
            if not "ひこう" in self.target_type and self.target.ability != "ふゆう":
                if self.move_type == "ドラゴン":
                    self.add(MOVE, f"{self.field.field}弱化", 2048)
        if self.field.field == "グラスフィールド":
            if not "ひこう" in self.attacker_type and self.attacker.ability != "ふゆう":
                if self.move_type == "くさ":
                    self.add(MOVE, f"{self.field.field}強化", 5325)
            if not "ひこう" in self.target_type and self.target.ability != "ふゆう":
                if self.move_name in ["じしん", "じならし"]:
                    self.add(MOVE, f"{self.field.field}弱化", 2048)

    def active_calculation(self):
        """
        ダメージ計算に影響するとくせいの計算
        オンオフがあるもの
        """
        if not self.gas_check():
            if self.attacker.ability_flag:
                if self.attacker.ability == "アナライズ":
                    self.add(MOVE, self.attacker.ability, 5325)
                if self.attacker.ability == "スロースタート":
                    self.add(ATK, self.attacker.ability, 2048)
                if self.attacker.ability == "はりこみ":
                    self.add(ATK, self.attacker.ability, 8192)
            if self.attacker.ability == "スナイパー" and self.target_field.crit:
                self.add(DMG, self.attacker.ability, 6144)

        if self.attacker.bad_stat == "じゅうでん" and self.move_type == "でんき":
            self.add(MOVE, "じゅうでん強化", 8192)

        if self.attacker.move_flag:
            if self.move_name in ["じだんだ", "しっぺがえし", "ダメおし", "ゆきなだれ", "アクロバット", "うっぷんばらし"]:
                self.move_power = self.move_power *2
                self.log.append(f"{self.move_name}: 効果発動")
            if self.move_name == "はたきおとす":
                if not self.target.item in ["かまどのめん", "いどのめん", "いしずえのめん"] and not "オーガポン" in self.target.name:
                    self.add(MOVE, self.move_name, 6144)
            if self.move_name == "かたきうち":
                self.add(MOVE, self.move_name, 8192)

        if self.attacker_field.help:
            self.add(MOVE, "てだすけ", 6144)
        if (self.move_name != "かわらわり" or self.move_name != "サイコファング" or self.attacker.ability != "すりぬけ"
            or self.target_field.crit or self.move_name != "レイジングブル"):
            if self.target_field.a_wall and self.move_category == "物理":
                if self.field.double:
                    self.add(DMG, "ダブルバトルリフレクター", 2732)
                else:
                    self.add(DMG, "リフレクター", 2048)
            if self.target_field.c_wall and self.move_category == "特殊":
                if self.field.double:
                    self.add(DMG, "ダブルバトルひかりのかべ", 2732)
                else:
                    self.add(DMG, "ひかりのかべ", 2048)

    def ability_calculation(self):
        """
        ダメージ計算に影響するとくせいの計算
        """
        if not self.gas_check():
            if self.attacker_status[0][0] <= self.attacker_status[0][1] /3:
                if self.attacker.ability == "しんりょく" and self.move_type == "くさ":
                    self.add(ATK, self.attacker.ability, 6144)
                if self.attacker.ability == "もうか" and self.move_type == "ほのお":
                    self.add(ATK, self.attacker.ability, 6144)
                if self.attacker.ability == "げきりゅう" and self.move_type == "みず":
                    self.add(ATK, self.attacker.ability, 6144)
                if self.attacker.ability == "むしのしらせ" and self.move_type == "むし":
                    self.add(ATK, self.attacker.ability, 6144)

            if self.attacker.ability == "ねつぼうそう" and self.attacker.bad_stat == "やけど":
                if self.move_category == "特殊":
                    self.add(MOVE, self.attacker.ability, 6144)
            if self.attacker.ability == "どくぼうそう" and self.attacker.bad_stat in ["どく", "もうどく"]:
                if self.move_category == "物理":
                    self.add(MOVE, self.attacker.ability, 6144)
            if self.attacker.ability == "フェアリースキン" and self.move_type == "ノーマル":
                self.move_type = "フェアリー"
                self.add(MOVE, self.attacker.ability, 4915)
            if self.attacker.ability == "エレキスキン" and self.move_type == "ノーマル":
                self.move_type = "でんき"
                self.add(MOVE, self.attacker.ability, 4915)
            if self.attacker.ability == "てつのこぶし" and D.MOVEDATA.find(self.move_name, "name", "パンチわざ") != "":
                self.add(MOVE, self.attacker.ability, 4915)
            if self.attacker.ability == "すてみ" and D.MOVEDATA.find(self.move_name, "name", "すてみ") != "":
                self.add(MOVE, self.attacker.ability, 4915)
            if self.attacker.ability == "ちからずく" and D.MOVEDATA.find(self.move_name, "name", "ちからずく") != "":
                self.add(MOVE, self.attacker.ability, 5325)
            if self.attacker.ability == "すなのちから" and self.field.weather == "すなあらし":
                if self.move_type in ["いわ", "じめん", "はがね"]:
                    self.add(MOVE, self.attacker.ability, 5325)
            if self.attacker.ability == "かたいツメ" and D.MOVEDATA.find(self.move_name, "name", "direct") != "":
                self.add(MOVE, self.attacker.ability, 5325)
            if self.attacker.ability == "パンクロック" and D.MOVEDATA.find(self.move_name, "name", "音技") != "":
                self.add(MOVE, self.attacker.ability, 5325)
            if self.attacker.ability == "きれあじ" and D.MOVEDATA.find(self.move_name, "name", "きれあじ") != "":
                self.add(MOVE, self.attacker.ability, 6144)
            if self.attacker.ability == "テクニシャン" and self.move_power >= 60:
                self.add(MOVE, self.attacker.ability, 6144)
            if self.attacker.ability == "がんじょうあご" and D.MOVEDATA.find(self.move_name, "name", "がんじょうあご") != "":
                self.add(MOVE, self.attacker.ability, 6144)
            if self.attacker.ability == "メガランチャー" and D.MOVEDATA.find(self.move_name, "name", "メガランチャー") != "":
                self.add(MOVE, self.attacker.ability, 6144)

            if self.attacker.ability == "トランジスタ" and self.move_type == "でんき":
                self.add(ATK, self.attacker.ability, 5325)
            if self.attacker.ability == "りゅうのあぎと" and self.move_type == "ドラゴン":
                self.add(ATK, self.attacker.ability, 6144)
            if self.attacker.ability == "ちからもち" and self.move_category == "物理":
                self.add(ATK, self.attacker.ability, 8192)
            if self.attacker.ability == "ヨガパワー" and self.move_category == "物理":
                self.add(ATK, self.attacker.ability, 8192)
            if self.attacker.ability == "もらいび" and self.move_type == "ほのお":
                if self.attacker.ability_flag:
                    self.add(ATK, self.attacker.ability)
            if self.attacker.ability == "ハドロンエンジン" and self.move_category == "特殊" and self.field.field == "エレキフィールド":
                self.add(ATK, self.attacker.ability, 5461)
            if self.attacker.ability == "ひひいろのこどう" and self.move_category == "物理" and self.field.weather == "にほんばれ":
                self.add(ATK, self.attacker.ability, 5461)
            if self.attacker.ability == "こんじょう" and self.attacker.bad_stat in ["まひ", "やけど", "どく", "もうどく", "こおり", "ねむり"]:
                self.add(ATK, self.attacker.ability, 6144)
            if self.attacker.ability == "いわはこび" and self.move_type == "いわ":
                self.add(ATK, self.attacker.ability, 6144)
            if self.attacker.ability == "そうだいしょう+1":
                self.add(ATK, self.attacker.ability, 4506)
            if self.attacker.ability == "そうだいしょう+2":
                self.add(ATK, self.attacker.ability, 4915)
            if self.attacker.ability == "そうだいしょう+3":
                self.add(ATK, self.attacker.ability, 5325)
            if self.attacker.ability == "そうだいしょう+4":
                self.add(ATK, self.attacker.ability, 5734)
            if self.attacker.ability == "そうだいしょう+5":
                self.add(ATK, self.attacker.ability, 6144)

            if self.attacker.ability != "かたやぶり":
                if self.target.ability == "かんそうはだ":
                    if self.move_type == "ほのお":
                        self.add(MOVE, self.target.ability, 5120)
                if self.target.ability == "あついしぼう":
                    if self.move_type == "ほのお" or self.move_type == "こおり":
                        self.add(ATK, self.target.ability, 2048)
                if self.target.ability == "きよめのしお" and self.move_type == "ゴースト":
                    self.add(ATK, self.target.ability, 2048)
                if self.target.ability == "たいねつ" and self.move_type == "ほのお":
                    self.add(ATK, self.target.ability, 2048)

                if self.target.ability == "ふしぎなうろこ" and self.target.bad_stat in ["まひ", "やけど", "どく", "もうどく", "こおり", "ねむり"]:
                    if self.move_category == "物理":
                        self.add(DEF, self.target.ability, 6144)
                if self.target.ability == "くさのけがわ" and self.field.field == "グラスフィールド":
                    if self.move_category == "物理":
                        self.add(DEF, self.target.ability, 6144)
                if self.target.ability == "ファーコート" and self.move_category == "物理":
                    self.add(DEF, self.target.ability, 8192)

            if self.attacker.ability == "はがねのせいしん" and self.move_type == "はがね":
                self.add(MOVE, self.attacker.ability, 6144)
            if self.target.ability == "はがねのせいしん" and self.move_type == "はがね":
                self.add(MOVE, self.target.ability, 6144)
            if self.field.ability_1 == "はがねのせいしん" and self.move_type == "はがね":
                self.add(MOVE, self.field.ability_1, 6144)
            if self.field.ability_2 == "はがねのせいしん" and self.move_type == "はがね":
                self.add(MOVE, self.field.ability_2, 6144)
            if self.field.ability_1 == "パワースポット" or self.field.ability_2 == "パワースポット":
                self.add(MOVE, "パワースポット", 5325)
            if (self.attacker.ability == "わざわいのおふだ" or self.target.ability == "わざわいのおふだ"
                or self.field.ability_1 == "わざわいのおふだ" or self.field.ability_2 == "わざわいのおふだ"):
                if self.move_category == "物理":
                    self.add(ATK, "わざわいのおふだ", 3072)
            if (self.attacker.ability == "わざわいのうつわ" or self.target.ability == "わざわいのうつわ"
                or self.field.ability_1 == "わざわいのうつわ" or self.field.ability_2 == "わざわいのうつわ"):
                if self.move_category == "特殊":
                    self.add(ATK, "わざわいのうつわ", 3072)
            if (self.attacker.ability == "わざわいのつるぎ" or self.target.ability == "わざわいのつるぎ"
                or self.field.ability_1 == "わざわいのつるぎ" or self.field.ability_2 == "わざわいのつるぎ"):
                if self.move_category == "物理":
                    self.add(DEF, "わざわいのつるぎ", 3072)
            if (self.attacker.ability == "わざわいのたま" or self.target.ability == "わざわいのたま"
                or self.field.ability_1 == "わざわいのたま" or self.field.ability_2 == "わざわいのたま"):
                if self.move_category == "特殊":
                    self.add(DEF, "わざわいのたま", 3072)

            if self.attacker.ability == "いろめがね" and self.type_effective(self.move_type, self.target_type) < 1:
                self.add(DMG, self.attacker.ability, 8192)
            if self.attacker.ability != "かたやぶり":
                if self.target.ability == "もふもふ" and self.move_type == "ほのお":
                    self.add(DMG, self.target.ability, 8192)
                if self.target.ability == "マルチスケイル" and self.target_status[0][0] == self.target_status[0][1]:
                    self.add(DMG, self.target.ability, 2048)
                if self.target.ability == "もふもふ" and D.MOVEDATA.find(self.move_name, "name", "direct") != "":
                    self.add(DMG, self.target.ability, 2048)
                if self.target.ability == "パンクロック" and D.MOVEDATA.find(self.move_name, "name", "パンクロック") != "":
                    self.add(DMG, self.target.ability, 2048)
                if self.target.ability == "こおりのりんぷん" and self.move_category == "特殊":
                    self.add(DMG, self.target.ability, 2048)
                if self.field.ability_1 == "フレンドガード" or self.field.ability_2 == "フレンドガード":
                    self.add(DMG, "フレンドガード", 3072)
                if self.target.ability == "ハードロック" and self.type_effective(self.move_type, self.target_type) >= 2:
                    self.add(DMG, self.target.ability, 3072)
                if self.target.ability == "フィルター" and self.type_effective(self.move_type, self.target_type) >= 2:
                    self.add(DMG, self.target.ability, 3072)

    def move_calculation(self):
        """
        ダメージ計算に影響するわざの特殊効果
        """
        if self.move_name == "からげんき" and self.attacker.bad_stat in ["まひ", "やけど", "どく", "もうどく", "こおり", "ねむり"]:
            self.add(MOVE, self.move_name, 8192)
        if self.move_name == "ヴェノムショック" and self.target.bad_stat in ["どく", "もうどく"]:
            self.add(MOVE, self.move_name, 8192)
        if self.move_name == "しおみず" and self.target_status[0][0] <= self.target_status[0][1] /2:
            self.add(MOVE, self.move_name, 8192)
        if self.move_name == "アクセルブレイク" and self.type_effective(self.move_type, self.target_type) >= 2:
            self.add(DMG, self.move_name, 5461)
        if self.move_name == "イナズマドライブ" and self.type_effective(self.move_type, self.target_type) >= 2:
            self.add(DMG, self.move_name, 5461)

    def weather_calculation(self):
        """
        ダメージ計算に影響する天候の計算
        補正値
        """
        if self.weather_check():
            if self.move_name == "ソーラービーム" and self.field.weather in ["あめ", "すなあらし", "ゆき"]:
                self.add(MOVE, "天候弱化", 2048)
            if self.move_name == "ソーラーブレード" and self.field.weather in ["あめ", "すなあらし", "ゆき"]:
                self.add(MOVE, "天候弱化", 2048)
            if self.attacker.ability == "サンパワー" and self.field.weather == "にほんばれ" and self.move_category == "特殊":
                self.add(ATK, self.attacker.ability, 6144)

    def drain_calculation(self, result: int):
        if result > self.target_status[0][0]:
            result = self.target_status[0][0]
        if D.MOVEDATA.find(self.move_name, "name", "吸収") != "":
            if self.move_name == "ドレインキッス":
                dmg = my_round(result /4 *3)
            elif self.move_name == "ちからをすいとる":
                dmg = self.target_status[1][-1]
            else:
                dmg = my_round(result /2)
            if self.attacker.item == "おおきなねっこ":
                dmg = my_round5(dmg *5324 /4096)
                self.calc_log.append("おおきなねっこ: *1.3")
            self.drain.append(dmg)
            self.calc_log.append(f"{self.move_name}: 回復量: {min(self.drain)} ~ {max(self.drain)}")

    def recoil_calculation(self, result: int):
        dmg = 0
        if result > self.target_status[0][0]:
            result = self.target_status[0][0]
        if D.MOVEDATA.find(self.move_name, "name", "すてみ") != "":
            if self.move_name == "もろはのずつき":
                dmg = my_round(result *(50 /100))
            elif self.move_name in ["ウェーブタックル", "ウッドハンマー", "すてみタックル", "フレアドライブ", "ブレイブバード", "ボルテッカー"]:
                dmg = my_round(result *(33 /100))
            elif self.move_name in ["とっしん", "ワイルドボルト"]:
                dmg = my_round(result *(25 /100))
        if self.move_name == "わるあがき":
            dmg = my_round(self.attacker_status[0][0] /2)
        if self.move_name in ["とびひさげり", "かかとおとし"]:
            dmg = math.floor(self.attacker_status[0][0] /2)
        if self.move_name == "てっていこうせん":
            dmg = math.ceil(self.attacker_status[0][0] /2)
        if dmg != 0:
            self.recoil.append(dmg)
            self.calc_log.append(f"{self.move_name}: 反動ダメージ: {min(self.recoil)} ~ {max(self.recoil)}")

    def final_calc(self, random_number: float) -> int:
        """最終計算"""
        def power() -> int:
            """威力計算"""
            dmg = self.move_power
            if dmg == 0:
                return 0
            for num in self.move_damage_list:
                dmg = my_round5(dmg * num / 4096)
            dmg = max(dmg, 1)
            if self.attacker.terastal_flag and self.attacker.terastal == self.move_type:
                dmg = max(dmg, 60)
            return dmg

        def attack() -> int:
            """攻撃力計算"""
            atk = self.attack
            if self.attacker.ability == "はりきり":
                atk = math.floor(atk * 6144 / 4096)
            for num in self.attack_list:
                atk = my_round5(atk * num / 4096)
            atk = max(atk, 1)
            return atk

        def deffence() -> int:
            """防御計算"""
            deff = self.defence
            if self.weather_check():
                if self.field.weather == "すなあらし" and "いわ" in self.target_type:
                    if self.move_category == "特殊":
                        deff = math.floor(deff * 6144 / 4096)
                        self.calc_log.append(f"{self.field.weather} 特防*1.5")
                if self.field.weather == "ゆき" and "こおり" in self.target_type:
                    if self.move_category == "物理":
                        deff = math.floor(deff * 6144 / 4096)
                        self.calc_log.append(f"{self.field.weather} 防御*1.5")
            for num in self.defence_list:
                deff = my_round5(deff * num / 4096)
            deff = max(deff, 1)
            return deff

        def type_effective(num):
            if self.attacker.ability == "てきおうりょく" and not self.gas_check():
                if self.attacker.terastal_flag and self.attacker.terastal == self.move_type:
                    num = my_round5(num * 9216 / 4096)
                    self.calc_log.insert(0, f"攻撃側: {self.attacker.ability}: テラスタル")
                elif self.move_type in self.attacker_type:
                    num = my_round5(num * 8192 / 4096)
                    self.calc_log.insert(0, f"攻撃側: {self.attacker.ability}")
            else:
                if self.attacker.terastal_flag and self.attacker.terastal == self.move_type and self.move_type in self.attacker_type[:2]:
                    num = my_round5(num * 8192 / 4096)
                    self.calc_log.insert(0, "攻撃側: タイプ一致テラスタル: *2.0")
                elif self.move_type in self.attacker_type:
                    num = my_round5(num * 6144 / 4096)
                    self.calc_log.insert(0, "攻撃側: タイプ一致: *1.5")
            effective = self.type_effective(self.move_type, self.target_type)
            if not self.gas_check():
                if self.target.ability == "かぜのり" and D.MOVEDATA.find(self.move_name, "name", "かぜ") != "":
                    effective = 0
                    self.calc_log.insert(0, f"{self.target.ability}: *{effective}")
                if self.target.ability == "かんそうはだ" and self.move_type == "みず":
                    effective = 0
                    self.calc_log.insert(0, f"{self.target.ability}: *{effective}")
                if self.target.ability == "こんがりボディ" and self.move_type == "ほのお":
                    effective = 0
                    self.calc_log.insert(0, f"{self.target.ability}: *{effective}")
                if self.target.ability == "そうしょく" and self.move_type == "くさ":
                    effective = 0
                    self.calc_log.insert(0, f"{self.target.ability}: *{effective}")
                if self.target.ability == "ちくでん" and self.move_type == "でんき":
                    effective = 0
                    self.calc_log.insert(0, f"{self.target.ability}: *{effective}")
                if self.target.ability == "ちょすい" and self.move_type == "みず":
                    effective = 0
                    self.calc_log.insert(0, f"{self.target.ability}: *{effective}")
                if self.target.ability == "どしょく" and self.move_type == "じめん":
                    effective = 0
                    self.calc_log.insert(0, f"{self.target.ability}: *{effective}")
                if self.target.ability == "ひらいしん" and self.move_type == "でんき":
                    effective = 0
                    self.calc_log.insert(0, f"{self.target.ability}: *{effective}")
                if self.target.ability == "でんきエンジン" and self.move_type == "でんき":
                    effective = 0
                    self.calc_log.insert(0, f"{self.target.ability}: *{effective}")
                if self.target.ability == "ふゆう" and self.move_type == "じめん":
                    effective = 0
                    self.calc_log.insert(0, f"{self.target.ability}: *{effective}")
                if self.target.ability == "ぼうおん" and D.MOVEDATA.find(self.move_name, "name", "音技") != "":
                    effective = 0
                    self.calc_log.insert(0, f"{self.target.ability}: *{effective}")
                if self.target.ability == "ぼうだん" and D.MOVEDATA.find(self.move_name, "name", "ぼうだん") != "":
                    effective = 0
                    self.calc_log.insert(0, f"{self.target.ability}: *{effective}")
                if self.target.ability == "もらいび" and self.move_type == "ほのお":
                    effective = 0
                    self.calc_log.insert(0, f"{self.target.ability}: *{effective}")
                if self.target.ability == "よびみず" and self.move_type == "みず":
                    effective = 0
                    self.calc_log.insert(0, f"{self.target.ability}: *{effective}")

            if effective >= 2:
                self.calc_log.insert(0, f"こうかはばつぐんだ: *{effective}")
            elif effective == 0:
                self.calc_log.insert(0, f"こうかがないみたいだ: *{effective}")
            elif effective < 1:
                self.calc_log.insert(0, f"こうかはいまひとつのようだ: *{effective}")
            result = math.floor(num * effective)
            return result

        def damage(dmg) -> int:
            """ダメージ計算"""
            result = dmg
            for num in self.damage_list:
                result = my_round5(result * num / 4096)
            return result

        if power() == 0:
            return 0
        self.calc_log = []
        result = math.floor(self.attacker.level * 2 / 5 + 2)
        result = math.floor(result * power() * attack() / deffence())
        result = math.floor(result / 50 + 2)
        if self.field.double and D.MOVEDATA.find(self.move_name, "name", "target") != "":
            result = my_round5(result * 3072 / 4096)
        if self.weather_check():
            if self.field.weather == "にほんばれ" and self.move_type == "みず":
                result = my_round5(result * 2048 / 4096)
                self.calc_log.append(f"{self.field.weather}弱化: *0.5")
            if self.field.weather == "あめ" and self.move_type == "ほのお":
                result = my_round5(result * 2048 / 4096)
                self.calc_log.append(f"{self.field.weather}弱化: *0.5")
            if self.field.weather == "にほんばれ" and self.move_type == "ほのお":
                result = my_round5(result * 6144 / 4096)
                self.calc_log.append(f"{self.field.weather}強化: *1.5")
            if self.field.weather == "あめ" and self.move_type == "みず":
                result = my_round5(result * 6144 / 4096)
                self.calc_log.append(f"{self.field.weather}強化: *1.5")
        if self.move_name == "きょけんとつげき" and self.attacker.move_flag:
            result = my_round5(result * 8192 / 4096)
            self.calc_log.append(f"{self.move_name}: *2.0")
        if self.target_field.crit:
            result = my_round5(result * 6144 / 4096)
            self.calc_log.append(f"急所: *2.0")
        result = math.floor(result * random_number)
        result = type_effective(result)
        if self.move_category == "物理" and self.attacker.bad_stat == "やけど":
                if self.attacker.ability != "こんじょう":
                    result = my_round5(result * 2048 / 4096)
                    self.calc_log.append("やけど: 攻撃*0.5")
        result = damage(result)
        if self.move_name == "いかりのまえば" or self.move_name == "カタストロフィ":
            result = math.floor(self.target_status[0][0] /2)
        if self.move_name == "いのちがけ":
            if not "ゴースト" in self.target_type:
                result = self.attacker_status[0][0]
        if self.move_name == "ステルスロック":
            ratio = self.type_effective("いわ", self.target_type)
            if ratio == 4:
                result = math.floor(self.target_status[0][1] / 2)
            elif ratio == 2:
                result = math.floor(self.target_status[0][1] / 4)
            elif ratio == 1:
                result = math.floor(self.target_status[0][1] / 8)
            elif ratio == 0.5:
                result = math.floor(self.target_status[0][1] / 16)
            elif ratio == 0.25:
                result = math.floor(self.target_status[0][1] / 32)
        self.drain_calculation(result)
        self.recoil_calculation(result)
        return result