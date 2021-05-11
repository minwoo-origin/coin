import requests
import threading
import pymysql
from bs4 import BeautifulSoup

#전역 변수
loopcnt=0
cnt = 0
coin_name = []
#mariadb 셋팅
coindb = pymysql.connect(
    user='root',
    passwd='root',
    host="192.168.178.160",
    port=3306,
    db='coindb',
    charset='utf8'
)
cursor = coindb.cursor(pymysql.cursors.DictCursor)
# 코인리스트 크롤링
COIN_URL = "https://api.upbit.com/v1/market/all"
response = requests.get(COIN_URL)
datas = response.json()
for item in datas:
    coin_name.append(item["korean_name"])
coin_name.append("비골")
coin_name.append("비토")
coin_name.append("이클")
coin_name.append("던프")
coin_name.append("비캐")


# print(coin_name)
def Todo():
    global cnt, loopcnt
    if loopcnt == 40:
        sql = '''DELETE FROM coin'''
        cursor.execute(sql)
        loopcnt = 0
        cnt = 0
    #file = open("result.txt", 'a')
    # 코인갤 1page 크롤링
    BASE_URL = "https://gall.dcinside.com/board/lists"
    headers = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'},
    ]
    params = {'id': 'bitcoins', 'page': 1}
    response = requests.get(BASE_URL, params=params, headers=headers[0])
    soup = BeautifulSoup(response.content, 'html.parser')
    article_list = soup.find('tbody').find_all('tr')
    del article_list[0:3]
    for tr_item in article_list:
        title_tag = tr_item.find('a', href=True)
        title = title_tag.text
        #    print(title)
        for i in coin_name:
            if title.find(i) != -1:
                # print(i)
                # print(title)
                text = "%d, %s, %s \n" %(cnt,i,title)
                print(text)
                #file.write(text)
                #db 인서트 쿼리 ID, COIN NAME, TITLE
                sql = '''INSERT INTO `coin` (ID, CoinName, Title) VALUES (%s, %s, %s)'''
                val = (cnt, i, title)
                cursor.execute(sql,val)
                coindb.commit()
                cnt = cnt + 1
                break

    #file.close()
    loopcnt = loopcnt + 1
    threading.Timer(15, Todo).start()


if __name__ == '__main__':
    Todo()
