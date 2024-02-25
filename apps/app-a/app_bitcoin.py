import requests
from flask import Flask
from datetime import datetime

app = Flask(__name__)

TIME_BETWEEN_UPDATES = 60  # 1 minute
TIME_BETWEEN_AVG_CALC = 600  # 10 minutes


class BitcoinApp:
    def __init__(self):
        self.init_app()

    def init_app(self):
        self.bitcoin_values = []
        self.avg_value = None
        self.last_time_avg_updated = datetime.now()
        self.last_update_time = None

    def fetch_bitcoin_value(self):
        print("Fetching bitcoin value")
        try:
            response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
            data = response.json()
            bitcoin_value = round(float(data["bpi"]["USD"]["rate"].replace(",", "")), 2)
            self.last_update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.bitcoin_values.append(bitcoin_value)
            print(f"Bitcoin values: {self.bitcoin_values} USD")
        except Exception as e:
            print(f"Failed to fetch bitcoin value: {e}")

    def calc_avg(self):
        print("Calculating average")
        if not self.bitcoin_values:
            print("No values to calculate average")
            return
        if (datetime.now() - self.last_time_avg_updated).seconds < TIME_BETWEEN_AVG_CALC:
            print('returning - not enough time passed since last average calculation')
            return
        self.last_time_avg_updated = datetime.now()
        self.avg_value = sum(self.bitcoin_values) / len(self.bitcoin_values)
        self.avg_value = round(self.avg_value, 2)
        self.bitcoin_values = self.bitcoin_values[-1:]
        print(f"Average value: {self.avg_value} USD")

    def get_page(self):
        self.fetch_bitcoin_value()
        self.calc_avg()
        bitcoin_value_display = f"{self.bitcoin_values[-1]} USD ({self.last_update_time})" if self.bitcoin_values \
            else "No value fetched yet."
        avg_value_display = f"Average Bitcoin Value: {self.avg_value} USD ({self.last_time_avg_updated})" \
            if self.avg_value else "No average calculated yet."
        return f"""
                <html>
                    <head>
                        <title>Bitcoin Tracker</title>
                        <meta http-equiv="refresh" content="{TIME_BETWEEN_UPDATES}">
                        <style>
                        body {{
                            font-family: Arial, sans-serif;
                            background-color: #f5f5f5;
                            margin: 0;
                            padding: 0;
                        }}
                        .container {{
                            max-width: 800px;
                            margin: 20px auto;
                            padding: 20px;
                            background-color: #fff;
                            border-radius: 5px;
                            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        }}
                        h1 {{
                            text-align: center;
                        }}
                        p {{
                            margin: 10px 0;
                        }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <p>Bitcoin Value: {bitcoin_value_display}</p>
                            <p>{avg_value_display}</p>
                        </div>
                    </body>
                </html>
                """


my_app = BitcoinApp()


@app.route("/")
def home():
    return my_app.get_page()


if __name__ == "__main__":
    app.run(host="0.0.0.0")

