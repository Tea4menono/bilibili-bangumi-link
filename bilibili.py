import requests

url = 'https://api.bilibili.com/x/space/bangumi/follow/list'
params = {
    'vmid': 4552522,
    'type': 1
}
headers = {
    'User-Agent': 'Mozilla/5.0'
}

response = requests.get(url, params=params, headers=headers)

# 结果是 JSON
data = response.json()