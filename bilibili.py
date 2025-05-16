import re
import requests

def parse_cookies_from_curl(curl_file):

    with open(curl_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    line4 = lines[3].strip()

    if line4.startswith("-b $'"):
        line4 = line4[len("-b $'"):]

    line4 = re.sub(r"'\s*\\?$", '', line4)
    items = [item.strip() for item in line4.split(';') if item.strip()]

    cookies = {}
    for kv in items:
        if '=' in kv:
            key, value = kv.split('=', 1)
            cookies[key] = value

    return cookies


def send_request_with_cookies(cookies, vmid):
    url = 'https://api.bilibili.com/x/space/bangumi/follow/list'

    params = {
        'vmid': vmid,
        'type': 1,
        'pn': 1,
        'ps': 24,
        'playform': 'web',
        'follow_status': 0,
        'web_location': '333.1387'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': f'https://space.bilibili.com/{vmid}/bangumi',
        'Origin': 'https://space.bilibili.com',
    }

    response = requests.get(url, headers=headers, params=params, cookies=cookies)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    return response.json()

if __name__ == '__main__':
    curl_file = './curl.txt'
    cookies = parse_cookies_from_curl(curl_file)

    vmid = 4552522
    result = send_request_with_cookies(cookies, vmid)

    if result:
        for i in result["data"]["list"]:
            print(i["title"],i["progress"])
