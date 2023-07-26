from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

oddsdf = pd.read_csv('nbaodds.csv')

@app.route('/filter_data')
def filter_data():
    var_dict = {"bet_type": "type",
                "season": "season",
                "team":  "team",
                "regular_or_playoffs": "reg_or_playoff",
                "home_or_away": "team_home_away",
                "opponent": "opponent",
                "favorite": "favorite",
                "bookmaker": "bookmaker",
                "line": "line",
                "odds": "odds",
                "over_or_under": "over_under",
                "hit": "hit"
                }
    try:
        print('balls')
        json_bet_data = request.get_json()
        # json_bet_data = [
        #     {
        #         "bet": 1,
        #         "bet_amount": "300",
        #         "filters": {
        #             "season": "2021-2022",
        #             "bet_type": "spread",
        #             "team": "76ers"
        #             }
        #     },
        #     {
        #         "bet": 2,
        #         "bet_amount": "100",
        #         "filters": {
        #             "team": "76ers"
        #             }
        #     }
        # ]
        print(json_bet_data)
        for bet in json_bet_data:
            idx = bet["bet"]
            amount = float(bet["bet_amount"])
            filters = bet["filters"]
            print(idx, amount, filters)

            df = oddsdf
            for key, value in filters.items():
                df = df[df[var_dict[key]] == value]

            payout = round(sum(df['payout_multiplier'] * amount), 2)
            print(payout)

        return 'hello'
    except Exception as e:
        return jsonify({'error': str(e)})
    return 'data!'


if __name__ == '__main__':
    app.run()