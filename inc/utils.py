import requests

def get_api_time():
    url = "https://timeapi.io/api/time/current/zone?timeZone=Asia/Ho_Chi_Minh"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Không lấy được dữ liệu từ API.")
