import time
import requests
import qrcode
from urllib.parse import urlparse, parse_qs

def extract_cookies_from_url(url):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    cookies = {
        "DedeUserID": query.get("DedeUserID", [""])[0],
        "SESSDATA": query.get("SESSDATA", [""])[0],
        "bili_jct": query.get("bili_jct", [""])[0],
    }

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

def get_qr_login_url():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.bilibili.com/",
        "Origin": "https://www.bilibili.com",
    }
    resp = requests.get("https://passport.bilibili.com/qrcode/getLoginUrl", headers=headers)

    resp.raise_for_status()  # 报错时能更清楚原因
    data = resp.json()['data']
    return data['url'], data['oauthKey']

def show_qr_code(url):
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.make()
    qr.print_ascii(invert=True)

def wait_for_login(oauthKey):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://www.bilibili.com/",
        "User-Agent": "Mozilla/5.0"
    }

    print("⌛ 等待扫码并确认登录（120秒内）...")

    for _ in range(60):  # 等待总时长 120 秒，每次 sleep 2 秒
        time.sleep(2)
        poll_url = f"https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={oauthKey}&source=main-fe-header&web_location=333.1007"
        resp = requests.get(poll_url, headers=headers)
        result = resp.json().get("data")
        code = result.get("code")

        if code == 0:
            print("✅ 登录成功！")
            return result.get("url")
        elif code == 86101:
            print("📷 尚未扫码...")
        elif code == 86090:
            print("⚠️ 已扫码，等待确认...")
        elif code == 86038:
            print("⌛ 二维码已过期，请重新获取。")
            break
        else:
            print(f"⚠️ 状态码 {code}：{result.get('message')}")

    return None


if __name__ == "__main__":
    print("📡 获取二维码...")
    login_url, oauth_key = get_qr_login_url()
    print("📱 请使用 Bilibili App 扫码登录：")
    show_qr_code(login_url)
    redirect_url = wait_for_login(oauth_key)
    if redirect_url:
        cookies = extract_cookies_from_url(redirect_url)
        vmid = 4552522
        result = send_request_with_cookies(cookies, vmid)
        if result:
            for i in result["data"]["list"]:
                print(i["title"],i["progress"])




