from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trades.db'  # nebo použijte PostgreSQL
db = SQLAlchemy(app)

class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pair = db.Column(db.String(10), nullable=False)
    side = db.Column(db.String(4), nullable=False)
    trade_time = db.Column(db.String(8), nullable=False)
    trend_1d = db.Column(db.String(10), nullable=False)
    trend_1h = db.Column(db.String(10), nullable=False)
    trend_15m = db.Column(db.String(10), nullable=False)
    criteria = db.Column(db.String(200), nullable=False)
    result = db.Column(db.Float, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    notes = db.Column(db.String(200), nullable=True)

# Vytvoření tabulky musí být uvnitř kontextu aplikace
with app.app_context():
    db.create_all()

@app.route('/trade', methods=['POST'])
def add_trade():
    data = request.get_json()
    new_trade = Trade(
        pair=data['Pair'],
        side=data['Side'],
        trade_time=data['Trade Time'],
        trend_1d=data['1D Trend'],
        trend_1h=data['1H Trend'],
        trend_15m=data['15m Trend'],
        criteria=','.join([key for key, value in data.items() if value is True]),
        result=data['Result'],
        balance=data['Balance'],
        notes=data['Notes']
    )
    db.session.add(new_trade)
    db.session.commit()
    return jsonify({'message': 'Trade has been added!'})

@app.route('/trades', methods=['GET'])
def get_trades():
    trades = Trade.query.all()
    return jsonify([{
        'Pair': trade.pair,
        'Side': trade.side,
        'Trade Time': trade.trade_time,
        '1D Trend': trade.trend_1d,
        '1H Trend': trade.trend_1h,
        '15m Trend': trade.trend_15m,
        'Criteria': trade.criteria,
        'Result': trade.result,
        'Balance': trade.balance,
        'Notes': trade.notes
    } for trade in trades])

if __name__ == '__main__':
    app.run(debug=True)
