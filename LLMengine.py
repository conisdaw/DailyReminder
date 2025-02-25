import dashscope
from config import api_key, chat_model, template_text, accounts
from weatherAcquisition import get_weather, get_weather_icon
from birthday import days_until_birthday

dashscope.api_key = api_key

def call_qwen(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = dashscope.Generation.call(
                model=chat_model,
                prompt=prompt,
                temperature=0.8,
                top_p=0.9,
                timeout=20
            )
            if response.status_code == 200:
                return response.output.choices[0].message.content
            else:
                if "RequestTimeOut" in response.message and attempt < max_retries - 1:
                    continue
                return f"Error: {response.code} - {response.message}"
        except Exception as e:
            if "timed out" in str(e) and attempt < max_retries - 1:
                continue
            return str(e)
    return "Error: Max retries exceeded"


def generate_message(account):
    weather_data = get_weather(account["city"])
    weather_icon = "天气图标:" + get_weather_icon(weather_data.get("weather", ""))
    weather_info = (
        f"    天气: {weather_data.get('weather', '')} | "
        f"    温度: {weather_data.get('maxTemperature', '')}°C/{weather_data.get('minTemperature', '')}°C\n"
        f"    湿度: {weather_data.get('shidu', '')} | "
        f"    风向: {weather_data.get('windDirection', '')} {weather_data.get('windScale', '')}\n"
        f"    空气质量: {weather_data.get('quality', '')} | "
        f"    PM2.5: {weather_data.get('pm25', 0)}μg/m³ | "
        f"    PM10: {weather_data.get('pm10', 0)}μg/m³\n"
        f"    生活建议: {weather_data.get('ganmao', '')}\n"
        f"    {weather_icon}"
    )
    solar_brithday_day = "    阳历:" + days_until_birthday('solar', account["solar_month"], account["solar_day"])
    lunar_brithday_day = "    阴历:" + days_until_birthday('lunar', account["lunar_month"], account["lunar_day"])
    input_text = template_text + weather_info + "\n" + solar_brithday_day + "\n" + lunar_brithday_day + "\n"
    return call_qwen(input_text)

LLM_out_tpm = []
for account in accounts:
    result = generate_message(account)
    if not result.startswith("Error: RequestTimeOut"):
        LLM_out_tpm.append(result)
LLM_out_texts = LLM_out_tpm


if __name__ == "__main__":
    print(LLM_out_texts)