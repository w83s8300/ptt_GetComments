def to_base64(num, length):
    """將數字轉換為指定長度的 64 進位字串"""
    table = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    result = []
    while num > 0:
        result.append(table[num % 64])
        num //= 64
    while len(result) < length:
        result.append('0')
    return ''.join(reversed(result))

def filename_to_aid(URL):
    """
    將 PTT 的檔案名稱轉換為 AID
    filename 格式: M.timestamp.A.random
    """
    try:
        filename=URL.split('/')[-1]
        filename=filename.split('.html')[0]
        board=URL.split('/')[-2]
        parts = filename.split('.')
        if len(parts) != 4 or parts[0] != 'M':
            raise ValueError("檔案名稱格式錯誤")
        
        timestamp = int(parts[1])  # 10 進位的 timestamp
        random_value = int(parts[3], 16)  # 16 進位的 random 值

        # 將 timestamp 和 random 值轉換為 64 進位
        timestamp_base64 = to_base64(timestamp, 6)
        random_base64 = to_base64(random_value, 2)

        # 組合成 AID
        aid = timestamp_base64 + random_base64
        return board,aid
    except Exception as e:
        return f"轉換失敗: {e}"

if __name__ == "__main__":
    # 測試範例
    URL='https://www.ptt.cc/bbs/C_Chat/M.1745310650.A.AC0.html'
    
    aid = filename_to_aid(URL)
    print(f"AID: {aid[0]}")