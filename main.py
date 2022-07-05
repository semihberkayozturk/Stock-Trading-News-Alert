import requests
STOCK_NAME = input("Company's Stock Name: ")
COMPANY_NAME = input("Company Name: ")

STOCK_API = ""
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API = "News API"
BOT_KEY =  "Your Telegram Bot Key"
BOT_ID =  "Telegram Bot ID"
BOT_ENDPOINT = f"https://api.telegram.org/bot"+BOT_KEY+"/sendMessage"

#yesterday's closing stock price. 
stock_params = {
    "function":"TIME_SERIES_DAILY", 
    "symbol":STOCK_NAME,
    "apikey":STOCK_API,
}
yesterday_prices = requests.get(STOCK_ENDPOINT,stock_params)
response = yesterday_prices
data = response.json()["Time Series (Daily)"]
data_list = [value for (key,value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

#day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

#positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = abs(float(day_before_yesterday_closing_price) - float(yesterday_closing_price))
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

#the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percent_diff = round((difference/float(yesterday_closing_price))*100)

def get_articles(output_func):
    parameters_news = {
        "apiKey":NEWS_API,
        "qInTitle":COMPANY_NAME,
        "pageSize":3,
    }
    response1 = requests.get(NEWS_ENDPOINT,params=parameters_news)
    response1.raise_for_status()
    news_data = response1.json()["articles"]
    formatted_articles = [f"{COMPANY_NAME}: {up_down}%{percent_diff} \n\n{article['url']}" for article in news_data]

    for article in formatted_articles:
        output_func(article)

def bot_message(text):
    parameters_bot = {
        "chat_id":BOT_ID,
        "text":text,
    }

    response = requests.post(BOT_ENDPOINT,params=parameters_bot)
    response.raise_for_status
if percent_diff > 0:
    get_articles(bot_message)

print("The information has been sent successfully.")
