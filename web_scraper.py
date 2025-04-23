import requests
import asyncio
from bs4 import BeautifulSoup
import time
import win32gui
import win32con
import win32console


# while True:
    #每5秒跑一次
def get_html(URL):
    while True:
        web = requests.get(URL, cookies={'over18':'1'})
        web.encoding='utf-8'       # 避免中文亂碼
        soup = BeautifulSoup(web.text, "html.parser")
        # titles = soup.find_all('div', class_='title')
        push = soup.find_all('div', class_='push')
        text_html=''
        line=0
        lines=0
        for i in push:
            # print(i)
            if  i.find('span', class_='f1 hl push-tag') != None:
                text_html=i.find('span', class_='f1 hl push-tag').get_text() + i.find('span', class_='f3 hl push-userid').get_text()
            elif  i.find('span', class_='hl push-tag') != None:
                text_html=i.find('span', class_='hl push-tag').get_text() + i.find('span', class_='f3 hl push-userid').get_text() 
            else:
                text_html=i.find('span', class_='f3 hl push-userid').get_text()
            text_html+= i.find('span', class_='f3 push-content').get_text() 
            text_html+= i.find('span', class_='push-ipdatetime').get_text() + '\n'
            line+=1
            with open('example.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()
            if len(lines) <= line:
                with open('example.txt', 'a+', encoding='utf-8') as file2:
                    file2.write(f"{str(line) + text_html}")
                #目前時間 格式用2024-01-01 00:00:00
                print(str(line) + text_html+'__'+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        time.sleep(5)
              
# 取得當前的 CMD 視窗句柄
hwnd = win32console.GetConsoleWindow()

# 設定視窗為最上層顯示
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                      win32con.SWP_NOMOVE | win32con.SWP_NOSIZE) 
URL=input('請輸入網址:')
#清除檔案內容
with open('example.txt', 'w', encoding='utf-8') as file:
    file.write('')
get_html(URL)
    
