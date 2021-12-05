import sys
sys.path.append("./")
from service.model import insert, get, update
import datetime
from wisdoms.utils import o2d
import requests
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import io
import time
import pandas as pd
from retrying import retry

s = requests.Session()


def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today-oneday
    return str(yesterday).split(" ")[0]

@retry
def loop_url_for_data(url, page_count=1, project_id=None, token=""):
    header = {
        "gzfauthentication": token
    }
    for page_index in range(page_count):
        print("获取数据中....")
        body = {
            "pageIndex": page_index,
            "pageSize": 10,
            "where": {"keywords": "", "projectId": project_id}
        }
        res = requests.post(url=url, json=body, headers=header)
        if res.status_code == 200:
            try:
                yield res.json()
            except Exception as e:
                print("获取数据失败,重新获取中...:", res.status_code, "错误信息:", res.text)


def update_by_query(data):
    if get({"id": data['id']}):
        update(data=data)
    else:
        insert(data)
def style_negative(v):
    if v == "未出租":
        return "background-color:green"
    elif v == "已出租":
        return "background-color:red"
def export():
    data = o2d(get())
    res = pd.DataFrame.from_dict(data)
    today = str(datetime.datetime.now()).split(".")[0]
    today_date = today.split(" ")[0]
    H = datetime.datetime.now().hour
    M = datetime.datetime.now().minute
    S = datetime.datetime.now().second
    columns = {"propertyName":"小区名称","id":"序号","address":"地址","rent":"租金","area":"面积","floorName":"楼层","createTime":"录入日期","status":"状态","region":"区域位置","metroDistance":"地铁距离",
               "houseType":"户型","leaseTime":"租出日期","lastingDays":"持续时间","lesseePerson":"承租人资格编号","lesseeTime":"承租人资格通过日期",
               "queueNumber":"排队人数"}
    res.rename(columns=columns, inplace=True)
    res = res.loc[:,["小区名称","序号","区域位置","地址","地铁距离","租金","户型","面积","楼层","排队人数","状态","录入日期","租出日期","持续时间","承租人资格编号","承租人资格通过日期"
]]
    res = res.style.applymap(style_negative)
    file_name = f"./export/公租房信息{today_date}T{H}.{M}.{S}.xlsx"
    res.to_excel(file_name,index=False)
def get_captcha():
    while True:
        code_res = s.get(
            url="https://select.pdgzf.com/api/v1.0/gzf/captcha/image/captcha.png?height=47&width=135&date=1638589964620")
        print("获取验证码...")
        if code_res.status_code == 200:
            fp = io.BytesIO(code_res.content)
            with fp:
                img = mpimg.imread(fp, format='png')
            plt.imshow(img)
            plt.show()
            break
        else:
            print("获取失败等待重新获取...")
            time.sleep(2)


def login(account="13730884364", password="WAEa2cVg3Rw6AejheflzOA=="):
    token = ""
    get_captcha()
    while True:
        captcha = input("请输入验证码：")
        body = {
            "account": account,
            "password": password,
            "captcha": str(captcha)
        }
        user_res = s.post(
            url="https://select.pdgzf.com/api/v1.0/app/gzf/user/login", json=body)
        if user_res.status_code == 200 and user_res.json()['success']:
            print("登录成功...")
            token = user_res.json()['data']['accessToken']
            break
        else:
            print("登录失败,等待重新登录", user_res.status_code, "错误信息:", user_res.text)
            get_captcha()
    return token

def execute(token):
    housing_estates = []
    houses = []
    estates_page = page_count = next(loop_url_for_data(
        "https://select.pdgzf.com/api/v1.0/app/gzf/project/list"))['data']['pageCount']
    for estate in loop_url_for_data("https://select.pdgzf.com/api/v1.0/app/gzf/project/list", estates_page):
        for e in estate['data']['data']:
            e['metroDistance'] = "无"
            latitude = e['latitude']
            longitude = e['longitude']
            nearby_res = requests.get(f"https://api.map.baidu.com/place/v2/search?query=地铁&location={latitude},{longitude}&radius=2000&output=json&ak=ANwXDC5L7Af2InEayr5p1gi6tHmunrv3")
            nearby = nearby_res.json()['results'][0]
            print(nearby)
            metro_latitude = nearby['location']['lat']
            metro_longitude = nearby['location']['lng']
            distance_res = requests.get(f"https://api.map.baidu.com/routematrix/v2/walking?ak=ANwXDC5L7Af2InEayr5p1gi6tHmunrv3&origins={latitude},{longitude}&destinations={metro_latitude},{metro_longitude}")
            distance = distance_res.json()['result'][0]['distance']['text']
            print(distance)
            e['metroDistance'] = distance
        housing_estates += estate['data']['data']
    for estate in housing_estates:
        page_count = 1
        page_count = next(loop_url_for_data("https://select.pdgzf.com/api/v1.0/app/gzf/house/list",
                          page_count=page_count, project_id=estate['id']))['data']['pageCount']
        for house in loop_url_for_data("https://select.pdgzf.com/api/v1.0/app/gzf/house/list", page_count, project_id=estate['id'], token=token):
            for h in house['data']['data']:
                h['metroDistance'] = estate['metroDistance']
            houses += house['data']['data']
    for h in houses:
        h['updateTime'] = h['updateTime'].split(' ')[0]
        h['createTime'] = h['createTime'].split(' ')[0]
        h['status'] = "未出租"
        if h['project']['area']:
            h['region'] = h.get('project', {}).get('area', {}).get('areaName')
        h["houseType"] = "一居室"
        if float(h['area']) > 60:
            h['houseType'] = "俩居室"
        if float(h['area']) > 100:
            h['houseType'] = "三居室"
        if h['queue']:
            h['lesseePerson'] = str(h['queue'][0]['qualification']['code'])
            h['lesseeTime'] = h['queue'][0]['qualification']['startDate']
            h['queueNumber'] = len(h['queue'])
            h['lesseeQueue'] = [i['qualification'] for i in h['queue']]
        update_by_query(h)
    old_houses = o2d(get({"updateTime": getYesterday()}))
    old_houses = [i['id'] for i in old_houses]
    new_houses = [i['id'] for i in houses]
    has_lease = [i for i in old_houses if i not in new_houses]
    for did in has_lease:
        old_time = o2d(get({"id": did}))[0]
        interval = datetime.datetime.now(
        ) - datetime.datetime.strptime(old_time['updateTime'], "%Y-%m-%d")
        lastingDays = interval.days
        update(data={"id": did, "status": "已出租", "leaseTime": str(
            datetime.datetime.now()).split(' ')[0], "lastingDays": lastingDays})