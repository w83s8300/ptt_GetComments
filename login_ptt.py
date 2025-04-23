import time
import PyPtt
import win32gui
import win32con
import win32console


from GET_AID import filename_to_aid
from Get_Ptt_Data import get_web_scraper

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
            # Ptt_id = input('請輸入帳號:')
            # Ptt_wd = input('請輸入密碼:')
            Ptt_id = 'w83s8300'
            Ptt_wd = 'q83a8300'
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
        favourite_boards = ptt_bot.get_favourite_boards()
        board_list = []
        
        for board in  range(len(favourite_boards)):
            board_list.append(favourite_boards[board]['board'])
            print(f"{board}. {favourite_boards[board]['board']} {favourite_boards[board]['title']}")
        # board_list_id=int(input('請輸入看板編號:'))
        # newest_index = ptt_bot.get_newest_index(PyPtt.NewIndex.BOARD,board_list[board_list_id])
        # print(newest_index)
        # for i in range(int(newest_index)-10,newest_index):
        #     post_info = ptt_bot.get_post(board_list[10], index=i)
            # print('ID={i} 標題={title} 作者={author}'.format(
            #     i=post_info['aid'], title=post_info['title'],
            #     author=post_info['author']))
            # get_web_scraper(ptt_bot,(board_list[10],'1e26Ao9M'))
            
        #看板名稱
        URL=input('請輸入網址:')
        filename=filename_to_aid(URL)
        get_web_scraper(ptt_bot,filename)
        
    finally:
        ptt_bot.logout()