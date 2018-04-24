import redis
import subprocess
from flask import Flask, Blueprint, jsonify, render_template, request, redirect

from data import DataAccess
from crawler.crawler import get_crawler

app = Flask(__name__)


# bp = Blueprint("error", __name__)


# @bp.app_errorhandler(404)
# def not_found_error(error):
#     pass


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/product', methods=['POST'])
def get_products():
    condition = request.get_json()
    # print(condition)
    try:
        min = condition['min']
        max = condition['max']
        order = condition['order']
        stock = condition['stock']
        price = condition['price']
    except KeyError:
        return jsonify(error="Invalid request")

    if not max:
        max = min
    if not min.isdigit() or not max.isdigit():
        return jsonify(error="Invalid range")
    min = int(min) - 1
    max = int(max)
    if min < 0 or max < 0 or min > max:
        return jsonify(error="Invalid range")

    condition = {
        'min': min,
        'max': max,
        'order': order == '1',
        'unknown_price': False,
        'in_stock': False,
        'out_of_stock': False,
        'discontinued': False,
        'unknown_stock': False,
    }

    for s in stock:
        condition[s] = True
    for p in price:
        condition[p] = True

    # print(condition)
    result = db.load_data(**condition)
    # print(result)
    return jsonify(result)


if __name__ == '__main__':
    # Initialize redis database (only for init, can be commented)
    # r = redis.Redis()
    # r.flushdb()

    # Initialize or update database first (only for init, can be commented)
    # crawler = get_crawler(init=True)

    crawler = get_crawler(init=False)
    crawler.start()
    del crawler

    # print("Init done!")
    db = DataAccess()

    # Spawn a subprocess to run the crawler periodically
    subprocess.Popen("python scrape.py", shell=True)
    # print("Server is starting...")
    app.run(debug=True)
