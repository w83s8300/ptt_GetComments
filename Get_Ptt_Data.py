import time
import PyPtt

def get_web_scraper(ptt_bot,filename):
    board_name =filename[0]
    #文章ID
    aid = filename[1]
    with open('example.txt', 'w', encoding='utf-8') as file:
        file.write('')
    text_title=''
    while True:
        try:
            #取得文章內容
            post_info = ptt_bot.get_post(board_name, aid=aid)
            #post_info是json格式的資料
            if text_title =='':
                text_title = post_info['title']
                #取post_info['title']是文章標題
                print('文章標題:', post_info['title'])
                #取post_info['content']是文章內容
                print('文章內容:', post_info['content'])
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

if __name__ == "__main__":
    # 測試範例
    pass