import requests
from bs4 import BeautifulSoup
import re
import pymongo

# 连接到MongoDB
MONGO_URL = 'localhost'
MONGO_DB = 'spider_house'
MONGO_COLLECTION = 'wuxi_house_price'
client = pymongo.MongoClient(MONGO_URL, port=27017)
db = client[MONGO_DB]


def get_page(page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/65.0.3325.162 Safari/537.36 '
    }
    url = "https://wx.fang.anjuke.com/loupan/all/p" + str(page) + "/"
    response = requests.get(url, headers=headers)
    return response.text


def parse(html):
    soup = BeautifulSoup(html, 'lxml')
    data = soup.find(class_='key-list')
    items = data.find_all(class_='item-mod')
    for item in items:
        title = item.find(class_='items-name')
        location = item.find(class_='list-map')
        raw_price = item.find(class_='price')
        price = re.sub("\D", "", str(raw_price))
        print(title.string)
        print(location.string)
        print('均价:', price)
        print("=="*50)
        detail = {
            '名称': title.string,
            '位置': location.string,
            '均价': price
        }
        save_to_mongo(detail)


def save_to_mongo(data):
    # 保存到MongoDB中
    try:
        if db[MONGO_COLLECTION].insert(data):
            print('存储到 MongoDB 成功')
    except Exception:
        print('存储到 MongoDB 失败')


if __name__ == '__main__':
    # ------------ 获取数据 ---------------
    # get_page()
    for i in range(1, 30):
        print("正在爬取第", i, "页")
        html = get_page(i)

    # ------------ 解析数据 ---------------
        parse(html)
