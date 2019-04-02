#!/usr/bin/env python
# coding=UTF-8


import json
import time


TABLE_PATH = "../../../MBServer/Active_Value.txt"
DATE_PATH = "./data/date.json"

SCHEDULES = {
    "schedules": [],
    "options": {
        "time": True,
        "timeFormat": "yyyyMMdd-HH:mm"
        # "timeFormat": "yyyyMMdd-HH:mm"
    }
}

SCHEDULE = {
    "end": "2019/05/10 3:00",
    "start": "2019/05/10 1:40",
    "title": "Schedule 1"
}

TODAY = time.strftime("%Y/%m/%d", time.localtime())


COL_LINE_NUM = 0
COL_ID = 1
COL_DESC = 3
COL_TIME = 14


def make_schedules():
    rows = []
    with open(TABLE_PATH, "r") as f:
        lines = f.readlines()
    lines = ["%d\t%s" % (i, lines[i]) for i in xrange(len(lines))]
    lines = [line.split("\t") for line in lines]
    for i in xrange(len(lines)):
        if i > 4:
            line = lines[i]
            try:
                rows.append([line[COL_LINE_NUM], line[COL_ID], line[COL_DESC], line[COL_TIME]])
            except Exception as e:
                print(i, line, e)
    rows = [row for row in rows if len(row[3]) > 0 and row[3] != '-1']
    return rows


def make_one_schedules(row_num, title, schedules_string):
    schedueles = schedules_string.split("&")
    schedueles = [s.split("*") for s in schedueles]
    scheduele = {}
    ret = []
    for ss in schedueles:
        scheduele["lnum"] = row_num
        scheduele["start"] = "%s %s" % (TODAY, ss[0])
        scheduele["end"] = "%s %s" % (TODAY, ss[1])
        scheduele["title"] = "%s(%s,%s)" % (title.decode("GBK").encode("UTF8"), ss[0], ss[1])
        ret.append(scheduele)
    return ret


rows = make_schedules()
for row in rows:
    try:
        if len(row) != 4:
            raise(r"warning")
        for item in make_one_schedules(row[0], row[2], row[3]):
            SCHEDULES["schedules"].append(item)
    except Exception as e:
        print(row, e)

print(json.dumps(SCHEDULES))

with open(DATE_PATH, "w") as f:
    f.write("var dataMap = %s;" % json.dumps(SCHEDULES))
