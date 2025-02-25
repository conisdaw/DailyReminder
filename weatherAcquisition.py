import requests
import copy
from weatherID import WEATHER_CITY

RUN_TIME_STORAGE = {}
config = {"SWITCH": {"weather": True}}

def get_weather_icon(weather):
    weather_icon = '🌈'
    weather_icon_list = ['☀️', '☁️', '⛅️', '☃️', '⛈️', '🏜️', '🏜️', '🌫️', '🌫️', '🌪️', '🌧️']
    weather_type = ['晴', '阴', '云', '雪', '雷', '沙', '尘', '雾', '霾', '风', '雨']

    for index, item in enumerate(weather_type):
        if item in weather:
            weather_icon = weather_icon_list[index]
    return weather_icon

def get_weather_city_info(city):
    for item in WEATHER_CITY:
        if item['city_name'] == city:
            return item['city_code']
    return None

def get_weather(city):
    if not config.get("SWITCH", {}).get("weather", True):
        return {}

    cache_key = f"{city}"
    if cache_key in RUN_TIME_STORAGE:
        print(f"获取缓存数据 >>> {cache_key}")
        return copy.deepcopy(RUN_TIME_STORAGE[cache_key])

    city_info = get_weather_city_info(city)
    if not city_info:
        print("配置中找不到对应城市信息")
        return {}

    url = f"http://t.weather.itboy.net/api/weather/city/{city_info}"
    try:
        response = requests.get(url, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 200:
                common_info = data.get("data", {})
                forecast = common_info.get("forecast", [])
                if not forecast:
                    return {}
                info = forecast[0]

                result = {
                    "shidu": common_info.get("shidu", ""),
                    "pm25": common_info.get("pm25", 0),
                    "pm10": common_info.get("pm10", 0),
                    "quality": common_info.get("quality", ""),
                    "ganmao": common_info.get("ganmao", ""),
                    "sunrise": info.get("sunrise", ""),
                    "sunset": info.get("sunset", ""),
                    "aqi": info.get("aqi", 0),
                    "weather": info.get("type", ""),
                    "maxTemperature": info.get("high", "").replace("高温", "").strip(),
                    "minTemperature": info.get("low", "").replace("低温", "").strip(),
                    "windDirection": info.get("fx", ""),
                    "windScale": info.get("fl", ""),
                    "notice": info.get("notice", "")
                }

                RUN_TIME_STORAGE[cache_key] = copy.deepcopy(result)
                return result
    except Exception as e:
        print(f"获取天气失败: {str(e)}")

    return {}


if __name__ == "__main__":
    # 示例调用
    city = "北京市"  # 示例城市
    weather = (str)(get_weather(city)) + "\n天气图标: " + get_weather_icon(get_weather(city).get("weather", "")) + "\n"
    print(weather)
