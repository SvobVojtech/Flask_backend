from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

data_file = 'trades.csv'

@app.route('/trade', methods=['POST'])
def add_trade():
    trade_data = request.json
    data = pd.read_csv(data_file)
    new_trade = pd.DataFrame([trade_data])
    data = pd.concat([data, new_trade], ignore_index=True)
    data.to_csv(data_file, index=False)
    return jsonify({'status': 'success'}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

