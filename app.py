from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return 'Hello, World!'


oddsdf = pd.read_csv('nbaodds.csv')


@app.route('/filter_data', methods=['POST'])
def filter_data():
    key_dict = {"bet_type": "type",
                "regular_or_playoffs": "reg_or_playoff",
                "home_or_away": "team_home_away",
                "over_or_under": "over_under",
                "line": "line_float"
                }
    val_dict = {"favorite": 1,
                "underdog": 0,
                "regular season": "reg",
                "playoffs": "playoff",
                "hit": 1,
                "miss": 0
                }
    try:
        json_bet_data = request.get_json()
        output_array = []
        for bet in json_bet_data:
            idx = bet["bet"]
            amount = float(bet["bet_amount"])
            filters = bet["filters"]

            df = oddsdf.copy()
            for key, value in filters.items():
                # if key in ["line", "odds", "over_or_under"]:
                if key in ["line", "odds"]:
                    limiters = [float(i) for i in value]
                    smaller = min(limiters)
                    larger = max(limiters)
                    df = df[df[key_dict.get(key, key)].between(
                        smaller, larger)]
                elif key == "over_or_under":
                    over_or_under = value[0]
                    limiters = [float(i) for i in value[1:3]]
                    smaller = min(limiters)
                    larger = max(limiters)
                    df = df[df[key_dict.get(key, key)] == over_or_under]
                    df = df[df['line_float'].between(smaller, larger)]
                else:
                    df = df[df[key_dict.get(key, key)]
                            == val_dict.get(value, value)]

            num_games = len(df)
            total_bet_amount = num_games * amount
            payout = round(sum(df['payout_multiplier'] * amount), 2)
            profit = payout - total_bet_amount
            bets_won = int(sum(df['hit']))

            output_array.append([idx] + [f"{i:,}" for i in [num_games, bets_won]
                                         ] + [str(round(bets_won/num_games * 100, 2)) + '%'] + [f"{i:,.2f}" for i in [amount,
                                total_bet_amount, payout, round(profit, 2), round(profit/num_games, 2), round(profit/total_bet_amount, 2)]])
        return output_array
    except Exception as e:
        return jsonify({'error': str(e)})
    return 'data!'


if __name__ == '__main__':
    app.run()
