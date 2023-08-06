import requests
from bs4 import BeautifulSoup
from lxml import etree
import time
import os
from turtle import*
from getpass import getpass
import win32gui
import win32con
import win32api
import random

a = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
}
'''
版权归tjsh所有
请先安装requests,bs4,lxml库
'''
# twine upload -u tjsh -p windowsasdftjsh dist/*
class html:
  def get_bs4(url, select):
      a1 = requests.get(url, headers=a)  # get
      soup = BeautifulSoup(a1.content.decode('utf-8'), 'html.parser')
      price = soup.select(select)
      return price
  def post_bs4(url, data, select):
      a1 = requests.post(url, headers=a, data=data)
      soup = BeautifulSoup(a1.content.decode('utf-8'), 'html.parser')
      price = soup.select(select)
      return price
  def get_lxml(url, xpath):
      a1 = requests.get(url, headers=a)  # get
      s = etree.HTML(a1.content.decode('utf-8'))
      id = s.xpath(xpath)
      return id
  def post_lxml(url, data, xpath):
    a1 = requests.post(url, headers=a, data=data)
    s = etree.HTML(a1.content.decode('utf-8'))
    id = s.xpath(xpath)
    return id
  def html(url):
      a1 = requests.get(url, headers=a)
      return [a1, a1.content.decode('utf-8')]  # 返回列表
class key1:
    def key_1(text):
        for p in text:
             if ord('a') <= ord(p) <= ord('z'):
                print(chr(ord('a') + (ord(p) - ord('a') + 3) % 26))
             else:
                 return p
    def key_2(text):
        for p in text:
              if ord('a') <= ord(p) <= ord('z'):
                  print(chr(ord('a') + (ord(p) - ord('a') - 3) % 26))
              else:
                return p
class ti:
    def data(self=0):
        return [time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour, time.localtime().tm_min]
    def cmd(self):
        return os.popen(self)
h = Turtle()
m = Turtle()
s = Turtle()
def 禁止使用2():
    tracer(False)
    h.reset()
    m.reset()
    s.reset()
    mi = time.localtime().tm_hour
    hi = time.localtime().tm_hour
    hd = -360/(12*60)*(60*hi+mi)+90
    h.width(8)
    h.color("white")
    h.seth(hd)
    h.fd(60)
    h.hideturtle()
    md = -6*mi+90
    m.width(8)
    m.color('white')
    m.seth(md)
    m.fd(110)
    si = time.localtime().tm_sec
    sd = 6*si+90
    s.width(2)
    s.color('white')
    s.seth(sd)
    s.fd(140)
    tracer(True)
    time.sleep(0.5)
    ontimer(a, 500)
    h.clear()
    m.clear()
    s.clear()
def draw1():
    hp = Turtle()
    mp = Turtle()
    sp = Turtle()
    color('#ffa500', '#ffbb00')
    goto(0, -150)
    begin_fill()
    width(30)
    circle(150)
    end_fill()
    color('#FFF')
    pu()
    for hour in [12, 3, 6, 9]:
        home()
        goto(0, -9)
        seth(-hour*30+90)
        fd(148)
        write(str(hour), False, 'center', ('Arial', 18, 'normal'))
    hideturtle()
    禁止使用2()
    done()
def echo(text):
    print(text)
def hide_input(text):
    a = getpass(text)
    return a
def min():
    a = time.localtime().tm_min
    return a
def hor():
    a = time.localtime().tm_hour
    return a
def n1():
    return 'ok'
from turtle import*
def 禁止使用1():
    penup()
    fd(5)
def 禁止使用3(d):
    禁止使用1()
    pendown() if d else penup()
    fd(140)
    禁止使用1()
    right(90)
def 禁止使用4(d):
    禁止使用3(True) if d in [2, 3, 4, 5, 6, 8, 9] else 禁止使用3(False)
    禁止使用3(True) if d in [0, 1, 3, 4, 5, 6, 7, 8, 9] else 禁止使用3(False)
    禁止使用3(True) if d in [0, 2, 3, 4, 5, 6, 8, 9] else 禁止使用3(False)
    禁止使用3(True) if d in [0, 2, 6, 8] else 禁止使用3(False)
    left(90)
    禁止使用3(True) if d in [0, 4, 5, 6, 8, 9] else 禁止使用3(False)
    禁止使用3(True) if d in [0, 2, 3, 5, 6, 7, 8, 9] else 禁止使用3(False)
    禁止使用3(True) if d in [0, 1, 2, 3, 4, 7, 8, 9] else 禁止使用3(False)
    left(180)
    penup()
    fd(20)
def 禁止使用5(data):
    pencolor("red")
    for i in data:
        if i == '-':
            write('年', font=('Arial', 18, 'normal'))
            pencolor('green')
            fd(40)
        elif i == '=':
            write('月', font=('Arial', 18, 'normal'))
            pencolor('blue')
            fd(40)
        elif i == '+':
            write('日', font=('Arial', 18, 'normal'))
        else:
            禁止使用4(eval(i))
def draw_time():
    import datetime
    while True:
        speed(5)
        goto(-300, 0)
        setup(800, 350, 200, 200)
        penup()
        fd(-350)
        pensize(5)
        禁止使用5(datetime.datetime.now().strftime('%Y-%m=%d+'))
        time.sleep(5)
        clear()
class img:
    def ok(imagepath):
        k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2")
        win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, imagepath, 1 + 2)
class list:
    def random(self):
        random.choice(self)
    def end(self, text):
        self.append(text)
class file:
    def write(self, jams=0, text=0):
        if jams == 0:
            with open(self, 'w') as f:
                f.write(text)
        else:
            with open(self, 'w+') as f:
                f.write(text)
    def read(self):
        with open(self) as f:
            a = f.read()
            return a
