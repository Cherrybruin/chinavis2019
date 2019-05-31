# coding=utf-8
import json
import csv

from datetime import time
import pandas

import pickle

def second2time(aim_time:int):
    second = aim_time % 60
    minute = aim_time // 60 % 60
    hour = aim_time // 60 // 60
    return time(hour, minute, second)

def gen_walk():
    day1 = pandas.read_csv("传感器日志数据\day1.csv")

    position = pandas.read_csv("传感器布置表.csv")

    final_day1 = pandas.merge(day1, position, how="left")

    groupbyuser = final_day1.groupby("id")

    users = groupbyuser.size().keys()

    user_walk = {}

    for user in users:
        user_data = groupbyuser.get_group(user)
        
        user_walk[user] = user_data

    file_path = r"C:\Users\cherry\Documents\GitHub\chinavis2019\\"

    with open(file_path + "user_walk.pkl", 'wb') as fp: 
        pickle.dump(user_walk, fp)

def read_walk():
    file_path = r"C:\Users\cherry\Documents\GitHub\chinavis2019\\"

    with open(file_path + "user_walk.pkl", 'rb') as fp: 
        return pickle.load(fp)

def show_walk():
    user_walk = read_walk()
    for single_user, single_walk in user_walk.items():
        print(single_user, single_walk)

def gen_map():
    first_floor = [
        "##############################",
        "##########FF.................#",
        "#AAAAA......###SSSSMMMMMMMMMM#",
        "#AAAAA.PP...###SSSSMMMMMMMMMM#",
        "#BBBBB.PP.TT###SSSSMMMMMMMMMM#",
        "#BBBBB.PP.TT###SSSSMMMMMMMMMM#",
        "#CCCCC.PP.11###SSSSMMMMMMMMMM#",
        "#CCCCC.PP.11###SSSSMMMMMMMMMM#",
        "#DDDDD.PP.11###SSSSMMMMMMMMMM#",
        "#DDDDD.PP.11###SSSSMMMMMMMMMM#",
        "######....22###SSSSMMMMMMMMMM#",
        "######....22###SSSSMMMMMMMMMM#",
        "#.CCCC.......................#",
        "I.CCCC.......................#",
        "#.........ff.......HH333344tt#",
        "##I#IO#I#######O#O#HH333344tt#"
    ]
    second_floor = [
        "##############################",
        "##########FF##################",
        "#RRRRR......##################",
        "#RRRRR......##################",
        "#RRRRR....TT##################",
        "#RRRRR....TT##################",
        "#RRRRR....66##################",
        "#RRRRR....66##################",
        "#RRRRR....####################",
        "#RRRRR....####################",
        "#55555....####################",
        "#55555....####################",
        "######......##################",
        "EEEEEE......##################",
        "EEEEEE....ff##################",
        "EEEEEE########################"
    ]
    return first_floor, second_floor


if __name__ == "__main__":
    # show_walk()
    # a,b = gen_map()
    # for linea, lineb in zip(a,b):
    #     print(linea , lineb)

    user_walk = read_walk( )

    for single_user, single_walk in user_walk.items():
        print(single_walk)
        for x,y, pre_x, pre_y in zip(single_walk.x, single_walk.y, single_walk.x[1:], single_walk.y[1:]):
            if abs(x-pre_x) >1 or 1 or abs(y-pre_y) > 1:
                # print(single_walk)
                for line in single_walk.:
                    print(line)

                input()
                break
        