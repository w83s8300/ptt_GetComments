import time
import PyPtt
import requests
import asyncio
from bs4 import BeautifulSoup
from pynput import keyboard
from threading import Thread, Event
from GET_AID import filename_to_aid
import pyttsx3
def favourite_boards(ptt_bot):
    favourite_boards = ptt_bot.get_favourite_boards()
    board_list = []
    
    for board in  range(len(favourite_boards)):
        board_list.append(favourite_boards[board]['board'])
        print(f"{board}. {favourite_boards[board]['board']} {favourite_boards[board]['title']}")
    board_list_id=int(input('請輸入看板編號:'))
    # board_list_id=8
    URL=f'https://www.ptt.cc/bbs/{board_list[board_list_id]}/index.html'
    global board_URL
    board_URL = URL
    favourite_boards_list(ptt_bot,URL)
    
def favourite_boards_list(ptt_bot,URL):
    page_list = ['z','x','c','v']
    global board_URL
    while True:
        return_json=get_web_list(URL)
        boards_URL=URL
        file2 = open('Allexample.txt', 'w', encoding='utf-8')
        for i in return_json['title_list']:
            print(f"{i}. {return_json['title_list'][i]['title']}  {return_json['title_list'][i]['a']}")
            file2.write(f"{i}. {return_json['title_list'][i]['title']}\n")
        for i in range(len(return_json['page_list'])):
            print(f"{page_list[i]}. {return_json['page_list'][i]['page']}",end=' ')
        print(f"q或e 回看板",end=' ')
        file2.close()
        page_list_id=(input('請輸入頁碼:'))
        
        
        # #page_list_id是否是數字
        if page_list_id.isdigit():
            page_list_id=int(page_list_id)
            URL='https://www.ptt.cc/'+return_json['title_list'][page_list_id]['a']
            print(URL)
            filename=filename_to_aid(URL)
            get_web_scraper(ptt_bot,filename,boards_URL)
            
        else:
            if page_list_id==page_list[0]:
                URL='https://www.ptt.cc/'+return_json['page_list'][0]['a']
                board_URL = URL
            elif page_list_id==page_list[1]:
                URL='https://www.ptt.cc/'+return_json['page_list'][1]['a']
                board_URL = URL
            elif page_list_id==page_list[2]:
                URL='https://www.ptt.cc/'+return_json['page_list'][2]['a']
                board_URL = URL
            elif page_list_id==page_list[3]:
                URL='https://www.ptt.cc/'+return_json['page_list'][3]['a']
                board_URL = URL
            elif page_list_id=='e' or page_list_id=='q':
                favourite_boards(ptt_bot)

            
def get_web_list(URL):
    web = requests.get(URL, cookies={'over18':'1'})
    web.encoding='utf-8'       # 避免中文亂碼
    soup = BeautifulSoup(web.text, "html.parser")
    push = soup.find_all('div', class_='title')
    title_json={}
    page_json={}
    return_json={}
    for i in  range(len(push)):
        if push[i].find('a') != None:
            title_json[i] = {}  # Initialize as a dictionary
            title_json[i]['title'] = push[i].find('a').get_text()
            title_json[i]['a'] = push[i].find('a')['href']
            
            # title_list.append([push[i].find('a').get_text(), 'https://www.ptt.cc'+push[i].find('a')['href']])
    push = soup.find_all('a', class_='btn wide')
    for i in  range(len(push)):
        page_json[i] = {}  # Initialize as a dictionary
        page_json[i]['page'] = push[i].get_text()
        page_json[i]['a'] = push[i]['href']
    #title_list變json格式和page_list變json格式 
    return_json['title_list'] = title_json
    return_json['page_list'] = page_json
    
    return return_json

def get_web_scraper(ptt_bot, filename,boards_URL):
    stop_event = Event()  # 用於控制迴圈的旗標
    # 初始化
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # 語速控制
    rate = engine.getProperty('rate')
    print(rate)
    engine.setProperty('rate', rate-70)
    # 音量控制
    volume = engine.getProperty('volume')
    print(volume)
    engine.setProperty('volume', volume-0.25)
    try:
        def on_press(key):
            global last_key_pressed
            try:
                # 儲存最近按下的鍵
                last_key_pressed = key.char
                if key.char == 'e' :  # 偵測按下 'e' 鍵
                    print("按下了 'e' 鍵，停止迴圈並執行 回看板")
                    stop_event.set()  # 設定旗標，停止迴圈
                elif key.char == 'q':  # 偵測按下 'q' 鍵
                    print("按下了 'q' 鍵，停止迴圈並 回看板列表")
                    stop_event.set()  # 設定旗標，停止迴圈
            except AttributeError:
                pass

        # 啟動鍵盤監聽器
        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        board_name = filename[0]
        aid = filename[1]
        with open('example.txt', 'w', encoding='utf-8') as file:
            file.write('')
        with open('Allexample.txt', 'w', encoding='utf-8') as file:
            file.write('')
        text_title = ''
        while not stop_event.is_set():  # 當 stop_event 未被設定時，繼續執行迴圈
            try:
                with open('Allexample.txt', 'a+', encoding='utf-8') as file_All:
                    # 取得文章內容
                    post_info = ptt_bot.get_post(board_name, aid=aid)
                    if text_title == '':
                        text_title = post_info['title']
                        file_All.write(f"文章標題:{post_info['title']}\n")
                        file_All.write(f"文章內容:{post_info['content']}\n")
                        print('文章標題:', post_info['title'])
                        print('文章內容:', post_info['content'])
                        
                    line = 0
                    lines = 0
                    with open('example.txt', 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                    for i in post_info['comments']:
                        if i['type'] == 'PUSH':
                            text_html = "推  "
                        elif i['type'] == 'ARROW':
                            text_html = "->  "
                        else:
                            text_html = "噓  "

                        text_html += i['author'] + '  ' + i['content']
                        text_html += "  " + i['time'] + '\n'
                        line += 1
                        if len(lines) < line:
                            with open('example.txt', 'a+', encoding='utf-8') as file2:
                                file2.write(f"{str(line) + text_html}")
                                file_All.write(f"{str(line) + text_html}")
                            print(text_html)
                            # engine.say(text_html)
                            # engine.save_to_file(text, 'chinese.mp3')
                            # engine.runAndWait()

            except PyPtt.exceptions.ConnectionClosed:
                ptt_bot = None
                continue
            except Exception as e:
                print('其他錯誤:', e)
                break
            time.sleep(5)
    except KeyboardInterrupt:
        listener.stop()  # 停止鍵盤監聽器
        favourite_boards_list(ptt_bot,board_URL)
        

    # if last_key_pressed == 'e':
    #     favourite_boards(ptt_bot)
    # elif last_key_pressed == 'q':
    #     favourite_boards_list(ptt_bot,boards_URL)
    #     exit(0)
    
    

if __name__ == "__main__":
    # 測試範例
    pass