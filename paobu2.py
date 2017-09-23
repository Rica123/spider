import requests
from bs4 import BeautifulSoup
import pymysql.cursors
headers = {'content-type': 'application/x-www-form-urlencoded',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
session_requests = requests.session()



def login_website(username, password):
    # 登录信息
    payload = {'username': username, 'password': password}
    my_respone = session_requests.post('http://jhc.sunnysport.org.cn/login/',
                                       data=payload,
                                       allow_redirects=False,
                                       verify=False,
                                       headers=headers)
    # 获取sessionid值
    c = my_respone.headers.get('Set-Cookie')
    #print(c)
    index = c.index(';')
    #print(index)
    c = c[0:index]
    #print(c)
    index2 = c.index('=')
    #print(index2)
    cookeis = {'sessionid': c[index2 + 1:]}
    #print(cookeis)
    # 获取sessionid值
    r = session_requests.post('http://jhc.sunnysport.org.cn//runner/index.html', cookies=cookeis,
                              headers=headers)
    # 得到相应的数据信息
    get_user_info(r.text)
    return r.text


def get_user_info(r):
    soup = BeautifulSoup(r, "html.parser")
    body = soup.body
    #print(soup)
    # 这里要分离出用户的姓名和性别
    human = soup.select('div.thumbnail')
    r = human[0]
    name = r.find_all('label')[1].text  #获取姓名
    #print(name)
    sid = r.find_all('label')[2].text   #获取学号
    #print(sid)
    sex = r.find_all('label')[3].text  #获取性别
    #print(sex)
    # 这里分离出相应的用户详情信息
    details = soup.select('table')
    #print(details)
    table1 = details[0]
    sum_road = table1.find_all('td')[1].text
    print(sum_road)
    avg_speed = table1.find_all('td')[3].text
    print(avg_speed)
    valid = table1.find_all('td')[5].text
    print(valid)
    # 包含分组 最低速度 最低里程
    table2 = details[1]
    group = table2.find_all('td')[1].text.encode('utf-8')
    low_speed = table2.find_all('td')[3].text.encode('utf-8')[0:table2.find_all('td')[3].text.index('m/s')]
    low_road = table2.find_all('td')[5].text.encode('utf-8')[0:table2.find_all('td')[5].text.index('m')]
    a =[name,sid,sex,sum_road,avg_speed,valid]
    print(a[5])
    return a
def save(data1):
    connect = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='python',charset='utf8')
# Cursor 对象
    cursor = connect.cursor()
    # 插入数据
    sql = "INSERT INTO sunnyRun (id, name, sex,总米数,平均速度,次数) VALUES ( '%s', '%s', '%s', '%s', '%s', '%s' )"
    data = (data1[1], data1[0], data1[2],data1[3],data1[4],data1[5])
    cursor.execute(sql % data)
    connect.commit()
    print('成功插入', cursor.rowcount, '条数据')
    cursor.close()
    connect.close()


def manytime():
    x = 201600000000000
    while x < 201699999999999:
        try:
            a = login_website(x, x)
            b = get_user_info(a)
            #print(b)
            save(b)
            x= x+1
        except :
            print("已经改密码了")
            x= x+2
manytime()



'''
def main():
    login= login_website('201637011580039','201637011580039')
    data= get_user_info(login)
    #print(data)
    save(data)

main()
'''