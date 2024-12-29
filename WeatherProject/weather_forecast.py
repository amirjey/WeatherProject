import requests
from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta
from khayyam import JalaliDate
import random

# API Keys
WEATHER_API_KEY = "837522b492dafd553b9f22fc0f7d604e"

# Base URLs
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

# پیشنهادها برای هر وضعیت آب و هوا
suggestions = {
    "rain": [
        "بارونه! چتر یادت نره و یه نوشیدنی گرم بخور!",
        "هوا بارونی هست، مراقب باش زمین خیسه!",
        "چتر و کفش مناسب یادت نره، بارون منتظرته!"
    ],
    "clear": [
        "هوا صافه! برو یه گردش بزن و از آفتاب لذت ببر!",
        "آسمون صافه، پیاده‌روی عالیه!",
        "هوا خوبه، می‌تونی برنامه‌ای بیرون از خونه داشته باشی!"
    ],
    "cloud": [
        "هوا ابریه، شاید بارون بیاد، آماده باش!",
        "آسمون خاکستریه، شاید وقتشه یه کتاب بخونی!",
        "ابریه، ولی خوبه برای یه چای گرم کنار پنجره!"
    ],
    "snow": [
        "برفیه! لباس گرم بپوش و از مناظر سفید لذت ببر!",
        "هوا برفی هست، مراقب سر خوردن باش!",
        "برفیه، وقتشه یه آدم‌برفی بسازی!"
    ],
    "default": [
        "هوا عجیبه! آماده هر اتفاقی باش!",
        "شرایط غیرمنتظره‌ای هست، ولی نگران نباش!",
        "هر اتفاقی ممکنه بیفته، ولی همیشه خوش‌بین باش!"
    ]
}

# دریافت پیشنهاد طنز
def get_funny_suggestion(weather_description):
    for key in suggestions:
        if key in weather_description:
            return random.choice(suggestions[key])
    return random.choice(suggestions["default"])

# دریافت اطلاعات آب و هوا
def fetch_weather_and_time():
    city = city_entry.get().strip()
    country = country_entry.get().strip()
    selected_date_shamsi = date_combobox.get()

    if not city or not country:
        display_message("لطفاً نام شهر و کشور را وارد کنید.", "error")
        return

    # تبدیل تاریخ شمسی به میلادی
    try:
        selected_date_miladi = str(JalaliDate(*map(int, selected_date_shamsi.split("-"))).todate())
    except ValueError:
        display_message("تاریخ انتخاب‌شده نامعتبر است.", "error")
        return

    try:
        # درخواست به API
        weather_url = f"{WEATHER_BASE_URL}?q={city},{country}&appid={WEATHER_API_KEY}&units=metric&lang=fa"
        weather_response = requests.get(weather_url)

        if weather_response.status_code == 200:
            weather_data = weather_response.json()
            city_name = weather_data["city"]["name"]
            country_name = weather_data["city"]["country"]
            local_time = JalaliDate(datetime.now()).strftime("%H:%M:%S %d-%m-%Y")
            show_results(weather_data, local_time, city_name, country_name, selected_date_miladi, selected_date_shamsi)
        else:
            display_message("اطلاعات برای این شهر یافت نشد.", "error")
    except Exception as e:
        display_message(f"خطا در اتصال: {e}", "error")

# نمایش پیام در نتایج
def display_message(message, tag):
    results_box.delete(1.0, END)
    results_box.insert(END, message, tag)

# نمایش نتایج
def show_results(weather_data, local_time, city_name, country_name, selected_date_miladi, selected_date_shamsi):
    results_box.delete(1.0, END)

    # اطلاعات کلی
    results_box.insert(END, f"\ud83c\udf0d شهر: {city_name}, کشور: {country_name}\n", "header")
    results_box.insert(END, f"\ud83d\udd52 زمان محلی: {local_time}\n\n", "header")

    selected_date_data = [
        entry
        for entry in weather_data["list"]
        if entry["dt_txt"].startswith(selected_date_miladi)
    ]

    if not selected_date_data:
        results_box.insert(END, f"\u26d4 اطلاعاتی برای تاریخ {selected_date_shamsi} موجود نیست.\n", "error")
        return

    # پیش‌بینی
    for entry in selected_date_data:
        date = entry["dt_txt"].split(" ")[0]
        time = entry["dt_txt"].split(" ")[1]
        temp = entry["main"]["temp"]
        weather_description = entry["weather"][0]["description"]

        suggestion = get_funny_suggestion(weather_description)

        results_box.insert(END, f"\ud83d\udcc5 تاریخ: {JalaliDate(datetime.strptime(date, '%Y-%m-%d'))}\n", "date")
        results_box.insert(END, f"\u23f0 زمان: {time}\n", "time")
        results_box.insert(END, f"\ud83c\udf21 دما: {temp}°C\n", "temperature")
        results_box.insert(END, f"\ud83c\udf26 وضعیت: {weather_description}\n", "description")
        results_box.insert(END, f"\ud83d\udca1 پیشنهاد: {suggestion}\n", "suggestion")
        results_box.insert(END, "-" * 50 + "\n", "separator")

# ایجاد لیست تاریخ‌های شمسی
def generate_date_list():
    today = JalaliDate(datetime.now())
    return [
        (today + timedelta(days=i - 7)).strftime("%Y-%m-%d")
        for i in range(37)
    ]

# رابط کاربری
root = Tk()
root.title("پیش‌بینی آب و هوا")
root.geometry("800x800")
root.configure(bg="#001833")

# پنل اطلاعات ورودی
input_frame = Frame(root, bg="#ffffff", bd=5)
input_frame.place(relx=0.5, rely=0.1, relwidth=0.8, relheight=0.3, anchor="n")

city_label = Label(input_frame, text="شهر:", font=("B Nazanin", 14), bg="#ffffff", anchor="e")
city_label.grid(row=0, column=0, padx=10, sticky=E)
city_entry = Entry(input_frame, font=("B Nazanin", 14), justify="right")
city_entry.grid(row=0, column=1, padx=10)

country_label = Label(input_frame, text="کشور:", font=("B Nazanin", 14), bg="#ffffff", anchor="e")
country_label.grid(row=1, column=0, padx=10, sticky=E)
country_entry = Entry(input_frame, font=("B Nazanin", 14), justify="right")
country_entry.grid(row=1, column=1, padx=10)

date_label = Label(input_frame, text="انتخاب تاریخ:", font=("B Nazanin", 14), bg="#ffffff", anchor="e")
date_label.grid(row=2, column=0, padx=10, sticky=E)
date_combobox = ttk.Combobox(input_frame, values=generate_date_list(), font=("B Nazanin", 12), justify="right")
date_combobox.grid(row=2, column=1, padx=10)
date_combobox.set(generate_date_list()[7])

fetch_button = Button(input_frame, text="دریافت اطلاعات", command=fetch_weather_and_time, font=("B Nazanin", 14), bg="#66b3ff", fg="white")
fetch_button.grid(row=3, column=0, columnspan=2, pady=10)

# پنل نمایش نتایج
results_frame = Frame(root, bg="#ffffff", bd=5)
results_frame.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.4, anchor="n")

results_box = Text(results_frame, font=("B Nazanin", 14), wrap=WORD, bg="#e0f7fa", borderwidth=2, relief="solid")
results_box.pack(side=LEFT, fill=BOTH, expand=True)

# استایل‌دهی
results_box.tag_configure("header", font=("B Nazanin", 16, "bold"), foreground="#003333", justify="right")
results_box.tag_configure("date", font=("B Nazanin", 14, "bold"), foreground="#006666", justify="right")
results_box.tag_configure("time", font=("B Nazanin", 14), foreground="#009999", justify="right")
results_box.tag_configure("temperature", font=("B Nazanin", 13, "italic"), foreground="#cc6600", justify="right")
results_box.tag_configure("description", font=("B Nazanin", 13), foreground="#6666cc", justify="right")
results_box.tag_configure("suggestion", font=("B Nazanin", 12, "italic"), foreground="#cc0066", justify="right")
results_box.tag_configure("separator", font=("B Nazanin", 10), justify="center", foreground="#999999")
results_box.tag_configure("error", font=("B Nazanin", 12, "bold"), justify="center", foreground="red")

root.mainloop()
