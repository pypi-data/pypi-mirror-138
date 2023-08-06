from random import *
from time import *
import pygame,sys
def p(a):#Python基础代码优化，print语句
    print(a)
def sjs(b,c):#随机数
    d = randint(b,c)
    return d
def shuimian(e):#暂停程序
    sleep(e)
def shijian():#时间
    f = strftime("%H:%M")#时，分
    return f
def shijian2():
    g = strftime("%H:%M:%S")#时，分，秒
    return g
def shijian3():
    h = strftime("%Y,%m,%d,%H:%M:%S")#年，月，日，时，分，秒
    return h
def pykj(k):#pygame的框架，k=窗口名称,必须和screen = pygame.display.set_mode((700,500))代码配合使用！！！
    pygame.init()
    pygame.display.set_caption(k)
def pysx():#pygame的刷新
    pygame.display.update()
def pytpjz(l):#pygame的图片加载
    jz=pygame.image.load(l)
    return jz
def pytpsf(tp,k,g):#pygame的图片缩放
    sf=pygame.transform.scale(tp,(k,g))
    return sf
def tpzs(dx,mc,tp,x,y):#pygame的图片展示，dx=窗口的大小mc=窗口名称tp=图片名称x=缩放的x坐标y=缩放的y坐标
    import pygame,sys
    pygame.init()
    screen = pygame.display.set_mode(dx)
    pygame.display.set_caption(mc)
    myImg = pygame.image.load(tp)
    myImg1 = pytpsf(myImg,x,y)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((255,255,255))
        screen.blit(myImg1,(0,0))
        pygame.display.update()
def wzzs(dx,mc,bjys,ztmc,ztdx,zsnr,ztys,zb):#pygame的文字展示
    import pygame, sys
    pygame.init()
    screen = pygame.display.set_mode(dx)
    pygame.display.set_caption(mc)
    pangwa = pygame.font.Font(ztmc,ztdx)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(bjys)
        text_code1 = pangwa.render(zsnr, True, ztys)
        screen.blit(text_code1, zb)
        pygame.display.update()
def xtwzzs(dx,mc,bjys,ztdx,zsnr,ztys,zb):#pygame的系统字体文字展示
    import pygame, sys
    pygame.init()
    screen = pygame.display.set_mode(dx)
    pygame.display.set_caption(mc)
    pangwa = pygame.font.SysFont("kaiti",ztdx)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(bjys)
        text_code1 = pangwa.render(zsnr, True, ztys)
        screen.blit(text_code1, zb)
        pygame.display.update()
#图片绘制必须使用：screen.blit(myImg,(0,0))
#内容填充必须使用：screen.fill((255,255,255))
def dkwy(wz):#打卡网址，wz=网址
    import webbrowser as w
    w.open(wz)
def zzsc(text,sj):#逐字输出，text=内容，sj=时间
    import sys, time
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(sj)
def xyx():  # 小游戏，你的外卖到底经历了什么？
    p("小游戏《你的外卖到底经历了什么？》")
    while True:
        p("是否查看外卖情况？是回T，不是回F")
        pd = input("T或F：")
        if pd == "T":
            p("正在查看。。。")
            shuimian(1)
            sj = sjs(1, 7)
            if sj == 1:
                p("骑手正在穿越宇宙，距离你30光年")
            if sj == 2:
                p("骑手正在买电动车，距离你5km")
            if sj == 3:
                p("骑手父母正在领证，距离你10km")
            if sj == 4:
                p("骑手受到了大军的阻击，距离你100km")
            if sj == 5:
                p("骑手正在战斗，距离你5km")
            if sj == 6:
                p("骑手正在吃你的外卖，距离你1km")
            if sj == 7:
                p("骑手正在回血，距离你3km")

        if pd == "F":
            p("你TM吃屎去吧！！！")

def cssc(text, t):  # 随机彩色逐字输出text=内容 t = 等待时间
    col = randint(1, 2)
    if col == 1:
        co = str(randint(1, 6))
        for a in text:
            sleep(t)
            print("\033[3" + co + "m" + a + "\033[0m", end="", flush=True)

        print("", end="\n")

    if col == 2:
        co = str(randint(1, 6))
        for a in text:
            sleep(t)
            print("\033[9" + co + "m" + a + "\033[0m", end="", flush=True)

        print("", end="\n")


def rgzzjqr():#人工智障机器人
    p("你好，我是奥利给硬件科技工作室研发的人工智障")
    p("你可以和我聊天，我还有许多实用的功能等待你的发现！不过也不要忘了关注一下奥利给硬件科技工作室哦！！！")
    import json
    import requests
    api_url = "http://openapi.tuling123.com/openapi/api/v2"
    running = True
    while running:
        text_input = input('我：')
        if text_input == "再见":
            running = False
        data = {
            "reqType": 0,
            "perception":
            {
                "inputText":
                {
                    "text": text_input
                },
            },
            "userInfo":
            {
                "apiKey": "57e8a35bf9f349a1bb49f2da6d48d518",
                "userId": "586065"
            }
        }
        data = json.dumps(data).encode('utf8')
        response_str = requests.post(api_url, data=data, headers={'content-type': 'application/json'})
        response_dic = response_str.json()
        results_text = response_dic['results'][0]['values']['text']
        print('人工智障：' + results_text)
    print('人工智障：再见')

def zxbyq():#在线编译器，命令行模式
    import code
    console = code.InteractiveConsole()
    console.interact()

def jsq():#计算器程序
    while True:
        print("欢迎来到奥利给计算器！")
        wen = input("请输入:a.加法   b.减法  c.乘法  d.除法")
        if wen == "a":
            #加法
            a = input("请输入加数1：")
            b = input("请输入加数2:")
            a1 = int(a)
            b1 = int(b)
            h = a1 + b1
            print("等于:",h)
        if wen == "b":
            q = input("请输入被减数：")
            w = input("请输入减数:")
            q1 = int(q)
            w1 = int(w)
            e = q1 - w1
            print("等于:",e)
        if wen == "c":
            r = input("请输入乘数：")
            t = input("请输入乘数：")
            r1 = int(r)
            t1 = int(t)
            y = r1*t1
            print("等于:",y)
        if wen == "d":
            a = input("请输入被除数：")
            s = input("请输入除数：")
            a1 = int(a)
            s1 = int(s)
            d = a1/s1
            print("等于:",d)

def ktwz():#是一个很好用的抠图网站！
    dkwy("https://www.remove.bg/")
def pythonbb():#可以获取你的Python版本
    import sys
    print("Python",sys.version[:5])

import requests
import json
import hashlib


def ycd():  # python的云存档系统

    class up(object):
        def _getUploadParams(self, filename, md5):
            url = 'https://code.xueersi.com/api/assets/get_oss_upload_params'
            params = {"scene": "offline_python_assets", "md5": md5, "filename": filename}
            response = requests.get(url=url, params=params)
            data = json.loads(response.text)['data']
            return data

        def uploadAbsolutePath(self, filepath):
            md5 = None
            contents = None
            fp = open(filepath, 'rb')
            contents = fp.read()
            fp.close()
            md5 = hashlib.md5(contents).hexdigest()

            if md5 is None or contents is None:
                raise Exception("文件不存在")

            uploadParams = self._getUploadParams(filepath, md5)
            requests.request(method="PUT", url=uploadParams['host'], data=contents, headers=uploadParams['headers'])
            return uploadParams['url']

    def selectfile(filenm):
        if filenm:
            file = open(filenm)
            myuploader = up()
            url = myuploader.uploadAbsolutePath(filenm)
        return url

    print("1、读取 2、上传")
    fy = input("")
    if fy == "2":
        password = input("设置密码：")
        nr = input("输入要上传的内容：")
        with open("user.txt", "w") as az:
            az.write(f"password:{password}\nnr:{nr}")
        users = selectfile("user.txt")
        usernm = users.replace("https://livefile.xesimg.com/programme/python_assets/", "").replace(".txt", "")
        print(f"你的存档码是：{usernm}")
    elif fy == "1":
        head1 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
        }
        zh = input("输入存档码：")
        response = requests.get("https://livefile.xesimg.com/programme/python_assets/" + zh + ".txt",
                                headers=head1).content

        with open("x.txt", "wb") as h:
            h.write(response)
        with open("x.txt", "r") as h:
            ss = h.read()
        pw = ss.split("\n")[0].replace("password:", "")
        nrs = ss.split("\n")[1].replace("nr:", "")
        u = input("输入密码：")
        if u == pw:
            print("密码正确！")
            print("存档内容为:")
            print(nrs)
        else:
            print("密码错误！")


def wxxxhz():
    import itchat
    import time

    print('扫一下弹出来的二维码')
    itchat.auto_login(hotReload=True)
    boom_remark_name = input('输入你要轰炸的人的微信备注，按回车键继续：')
    message = input('输入你要轰炸的内容，按回车键开始轰炸：')
    boom_obj = itchat.search_friends(remarkName=boom_remark_name)[0]['UserName']
    while True:
        time.sleep(0.5)
        print('消息已经发送')
        itchat.send_msg(msg=message, toUserName=boom_obj)

def pqwydm(wz):#爬取网页源代码，wz=网址
    import requests
    import bs4
    url = wz
    res = requests.get(url)
    res.encoding = "UTF-8"
    print(res.text)
    return res.text


def pqwybqnr(wz, bq):  # 爬取网页标签内容，wz=网址，bq=标签
    import requests
    import bs4
    # 请求网页
    # 作答区域1：修改下一行的网址，改为自己要请求的网页地址
    url = wz
    # 作答区域2：补充下一行代码，使用requests库中的get()函数，请求网页url
    res = requests.get(url)
    res.encoding = "UTF-8"
    # 选取数据
    soup = bs4.BeautifulSoup(res.text,"lxml")
    # 作答区域3：查找soup中所有的a标签
    data = soup.find_all(bq)
    # 展示结果
    for n in data:
        print(n.text)


def pqwybqsxnr(wz, bq, sx):  # 爬取网页属性标签内容，wz=网址，bq=标签，sx=属性值
    import requests
    import bs4
    # 请求网页
    # 作答区域1：修改下一行的网址，改为自己要请求的网页地址
    url = wz
    # 作答区域2：补充下一行代码，使用requests库中的get()函数，请求网页url
    res = requests.get(url)
    res.encoding = "UTF-8"
    # 选取数据
    soup = bs4.BeautifulSoup(res.text, "lxml")
    # 作答区域3：查找soup中所有的a标签
    data = soup.find_all(bq, class_=sx)
    # 展示结果
    for n in data:
        print(n.text)


def pqbcwybqsxnr(wz, bq, sx, wjm):  # 爬取保存网页标签属性内容，wz=网址，bq=标签，sx=属性，wjm=文件名
    import requests
    import bs4

    # 作答区域1：打开起点中文网，选取喜欢的书籍，点击“免费试读”后，修改下一行代码为试读页的网址
    url = wz
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, "lxml")
    # 作答区域2：补充下一行代码，查找标签名为div，class属性为"main-text-wrap"的内容
    data = soup.find_all(bq, class_=sx)
    # 展示结果chr()
    for n in data:
        print(n.text)
        # 作答区域3：1.补充文件的名称 2.设置文件的打开方式为追加模式"a"
        with open(wjm, "a", encoding="UTF-8") as file:
            # 作答区域4：补充下一行代码，写入存储在变量n的标签文字
            file.write(n.text)


def pqbcwybqnr(wz, bq, wjm):  # 爬取保存网页标签属性内容，wz=网址，bq=标签，wjm=文件名
    import requests
    import bs4

    # 作答区域1：打开起点中文网，选取喜欢的书籍，点击“免费试读”后，修改下一行代码为试读页的网址
    url = wz
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, "lxml")
    # 作答区域2：补充下一行代码，查找标签名为div，class属性为"main-text-wrap"的内容
    data = soup.find_all(bq)
    # 展示结果chr()
    for n in data:
        print(n.text)
        # 作答区域3：1.补充文件的名称 2.设置文件的打开方式为追加模式"a"
        with open(wjm, "a", encoding="UTF-8") as file:
            # 作答区域4：补充下一行代码，写入存储在变量n的标签文字
            file.write(n.text)





