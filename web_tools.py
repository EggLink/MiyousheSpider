import requests
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 "
                  "Safari/537.36 Edg/127.0.0.0",
    "Referer": "https://www.miyoushe.com/"
}


def get_web_page(url, try_count=0):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text.encode(response.encoding).decode('utf-8')  # Convert to utf-8
    except requests.RequestException as e:
        print(e)
        if try_count <= 3:
            print('发生错误！3秒后重试')
            time.sleep(3)
            return get_web_page(url, try_count + 1)
        return None
