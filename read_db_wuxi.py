import pymongo
import pandas as pd


def to_csv_wuxi():
    client = pymongo.MongoClient('localhost')
    cur = client["spider_house"]["wuxi_house_price"]
    data = pd.DataFrame(list(cur.find()))
    # 存储的时候可以做一些数据清洗的工作,清洗脏数据
    data.to_csv("wuxi_house_price.csv")


if __name__ == '__main__':
    to_csv_wuxi()
