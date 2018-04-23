import re
from flask import Flask, Blueprint, jsonify, render_template, request, redirect

from data import DataAccess

app = Flask(__name__)
bp = Blueprint("error", __name__)
db = DataAccess()


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/<range>', methods=['GET'])
def get_products(range):
    min = 0
    max = 100
    if re.match("^[0-9]+$", range):
        max = int(range)
    elif re.match("^[0-9]+-[0-9]+$", range):
        range_new = range.split("-")
        min = int(range_new[0]) - 1
        max = int(range_new[1])
        if min > max or min < 0 or max < 0:
            return jsonify(error="Range error")
    else:
        return jsonify(error="Not found")
    condition = {
        'min': min,
        'max': max,
        'order': request.form['order'] == '1',
        'unknown_price': request.form['unknown_price'],
        'in_stock': request.form['in_stock'],
        'out_of_stock': request.form['out_of_stock'],
        'discontinued_stock': request.form['discontinued_stock'],
        'unknown_stock': request.form['unknown_stock'],
    }
    result = db.load_data(**condition)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
