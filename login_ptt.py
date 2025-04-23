import time
import PyPtt
import win32gui
import win32con
import win32console


from GET_AID import filename_to_aid

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
            Ptt_wd = input('請輸入密碼:')
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
        print('文章代碼(AID)與網址轉換 \nhttps://illya.tw/ptt-aid Ptt ')
        #看板名稱
        URL=input('請輸入網址:')
        filename=filename_to_aid(URL)
        board_name =filename[0]
        #文章ID
        aid = filename[1]
        with open('example.txt', 'w', encoding='utf-8') as file:
            file.write('')
        text_title=''
        text_content=''
        author_id=''
        while True:
            try:
                #取得文章內容
                post_info = ptt_bot.get_post(board_name, aid=aid)
                #post_info是json格式的資料
                if text_title =='':
                    text_title = post_info['title']
                    #取post_info['title']是文章標題
                    # print('文章標題:', post_info['title'])
                    #取post_info['content']是文章內容
                    # print('文章內容:', post_info['content'])
                #取post_info['comments']是推文內容
                line=0
                lines=0
                with open('example.txt', 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                for i in post_info['comments']:
                    # print(i)
                    
                    if i['type'] == 'PUSH':
                        text_html = "推  "
                    elif i['type'] == 'ARROW':
                        text_html = "->  "
                    else:
                        text_html =  "噓  "
                    
                    text_html += i['author']+'  ' + i['content']
                    
                    author_id = i['author']
                    text_html +="  " + i['time']+ '\n'
                    line += 1
                    if len(lines) < line:
                        with open('example.txt', 'a+', encoding='utf-8') as file2:
                            file2.write(f"{str(line) + text_html}")
                        #目前時間 格式用2024-01-01 00:00:00
                        print(text_html)
                    #目前時間 格式用2024-01-01 00:00:00
                # print('最新文章ID:', newest_index['aid'])
                
            except PyPtt.exceptions.ConnectionClosed:
                ptt_bot = None
                continue
            except Exception as e:
                print('其他錯誤:', e)
                break
            time.sleep(5)
    finally:
        ptt_bot.logout()