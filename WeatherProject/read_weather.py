import json

# باز کردن فایل داده‌های آب‌وهوا
with open("weather_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# بررسی کل پیش‌بینی‌ها
forecasts = data['list']

# تعریف تابع پیشنهادات
def suggest_activity(weather_description, temperature):
    if "rain" in weather_description or "shower" in weather_description:
        return "هوا بارونیه! بیا یه چای داغ بخوریم بعدش بشینیم!"
    elif "clear" in weather_description or "sunny" in weather_description:
        if temperature > 25:
            return "هوا آفتابیه و گرمه! یه بستنی بگیر و بریم پارک قدم بزنیم!"
        else:
            return "هوا آفتابیه و خنکه! بیا بریم کوه‌نوردی یا دوچرخه‌سواری!"
    elif "cloud" in weather_description:
        return "هوا ابریه! زیاد چیزی دود نکن به ریت استراحت بده!"
    else:
        return "هوا کمی نامشخصه، ولی می‌تونی هر کاری که دوست داری انجام بدی!"

# پردازش داده‌های پیش‌بینی
for forecast in forecasts:
    # گرفتن تاریخ و زمان پیش‌بینی
    date_time = forecast['dt_txt']
    # گرفتن توضیحات آب‌وهوا و دما
    weather_description = forecast['weather'][0]['description']
    temperature = forecast['main']['temp']

    # دریافت پیشنهاد
    suggestion = suggest_activity(weather_description, temperature)

    # نمایش اطلاعات روز و پیشنهاد
    print(f"تاریخ و زمان: {date_time}")
    print(f"توضیحات: {weather_description}")
    print(f"دما: {temperature} درجه سانتی‌گراد")
    print(f"پیشنهاد: {suggestion}")
    print("-" * 40)
