from datetime import datetime
import calendar
from zhdate import ZhDate
import pytz
from config import accounts

def get_next_solar_birthday(month, day):
    tz = pytz.timezone('Asia/Shanghai')
    today = datetime.now(tz).replace(tzinfo=None)

    current_year = today.year
    try:
        birthday_this_year = datetime(current_year, month, day)
    except ValueError:
        if month == 2 and day == 29:
            birthday_this_year = datetime(current_year, 2, 28)
        else:
            raise ValueError("Invalid birthday date")

    if birthday_this_year > today:
        return birthday_this_year
    else:
        next_year = current_year + 1
        try:
            birthday_next_year = datetime(next_year, month, day)
        except ValueError:
            if month == 2 and day == 29:
                if calendar.isleap(next_year):
                    birthday_next_year = datetime(next_year, 2, 29)
                else:
                    birthday_next_year = datetime(next_year, 2, 28)
            else:
                raise ValueError("Invalid birthday date for next year")
        return birthday_next_year

def get_next_lunar_birthday(lunar_month, lunar_day, leap_month=False):
    tz = pytz.timezone('Asia/Shanghai')
    today = datetime.now(tz).replace(tzinfo=None)

    lunar_today = ZhDate.from_datetime(today)
    current_lunar_year = lunar_today.lunar_year

    try:
        lunar_birthday_current = ZhDate(current_lunar_year, lunar_month, lunar_day, leap_month)
        solar_birthday_current = lunar_birthday_current.to_datetime()
    except:
        raise ValueError("Invalid lunar date")

    if solar_birthday_current > today:
        return solar_birthday_current
    else:
        next_lunar_year = current_lunar_year + 1
        try:
            lunar_birthday_next = ZhDate(next_lunar_year, lunar_month, lunar_day, leap_month)
            solar_birthday_next = lunar_birthday_next.to_datetime()
        except:
            raise ValueError("Invalid lunar date for next year")
        return solar_birthday_next

def days_until_birthday(birthday_type, month, day, leap_month=False):
    try:
        if birthday_type == 'solar':
            next_birthday = get_next_solar_birthday(month, day)
        elif birthday_type == 'lunar':
            next_birthday = get_next_lunar_birthday(month, day, leap_month)
        else:
            return "Invalid birthday type. Use 'solar' or 'lunar'."

        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        next_birthday = next_birthday.replace(hour=0, minute=0, second=0, microsecond=0)
        delta = (next_birthday - today).days

        return f"距离下一次生日还有 {delta} 天"
    except Exception as e:
        return f"错误: {str(e)}"


if __name__ == "__main__":
    for account in accounts:
        solar_brithday_day = "距离阳历生日还有" + days_until_birthday('solar', account["solar_month"], account["solar_day"]) + "天\n"
        lunar_brithday_day = "距离阴历生日还有" + days_until_birthday('lunar', account["lunar_month"], account["lunar_day"]) + "天\n"
        print(solar_brithday_day)
        print(lunar_brithday_day)
        # 闰月示例（需要时）
        # print(days_until_birthday('lunar', 4, 30, True))  # 闰四月三十
        # 特殊日期如2月29日
        # print(days_until_birthday('solar', 2, 29))
