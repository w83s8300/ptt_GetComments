import time
import PyPtt
import win32gui
import win32con
import win32console
import requests
import asyncio
from bs4 import BeautifulSoup


from GET_AID import filename_to_aid
import Get_Ptt_Data
import getpass

# 取得當前的 CMD 視窗句柄
hwnd = win32console.GetConsoleWindow()

# 設定視窗為最上層顯示
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                      win32con.SWP_NOMOVE | win32con.SWP_NOSIZE) 

def login():
    max_retry = 5
    ptt_bot = None
    for retry_time in range(max_retry):
        try:
            ptt_bot = PyPtt.API()
            Ptt_id = input('請輸入帳號:')
            Ptt_wd = getpass.getpass('請輸入密碼:')
            ptt_bot.login(Ptt_id, Ptt_wd,
                          kick_other_session=False if retry_time == 0 else True)
            break
        except PyPtt.exceptions.LoginError:
            ptt_bot = None
            print('登入失敗')
            time.sleep(3)
        except PyPtt.exceptions.LoginTooOften:
            ptt_bot = None
            print('請稍後再試')
            time.sleep(60)
        except PyPtt.exceptions.WrongIDorPassword:
            print('帳號密碼錯誤')
            raise
        except Exception as e:
            print('其他錯誤:', e)
            break

    return ptt_bot

if __name__ == '__main__':
    ptt_bot = None
    last_newest_index = None
    try:
        if ptt_bot is None:
            ptt_bot = login()
        # https://illya.tw/ptt-aid Ptt 文章代碼(AID)與網址轉換
        line_type = input('請輸入網址類型(1)預覽(2)熱門(3)網址:')
        with open('Allexample.txt', 'w', encoding='utf-8') as file:
            file.write('')
        match line_type:
            case "1":
                Get_Ptt_Data.favourite_boards(ptt_bot,line_type)
            case "2":
                Get_Ptt_Data.favourite_hit_boards(ptt_bot,line_type)
            case "3":
                # 看板名稱
                URL=input('\n請輸入網址:')
                filename=filename_to_aid(URL)
                Get_Ptt_Data.get_web_scraper(ptt_bot,filename,'',line_type)
    except KeyboardInterrupt:
        match line_type:
            case "1":
                Get_Ptt_Data.favourite_boards(ptt_bot,line_type)
            case "2":
                Get_Ptt_Data.favourite_hit_boards(ptt_bot,line_type)
            case "3":
                # 看板名稱
                URL=input('\n請輸入網址:')
                filename=filename_to_aid(URL)
                Get_Ptt_Data.get_web_scraper(ptt_bot,filename,'',line_type)
    finally:
        ptt_bot.logout()