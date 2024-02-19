import os
import jinja2
import asyncio
import asyncpg
import sqlite3
# import logging

from typing import List
from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask, render_template, request, jsonify
from cachetools import TTLCache
# from colorlog import ColoredFormatter

from db.main import Database
from db.tables.item import Exhibit, InventoryNumber

# logging.basicConfig(level=logging.INFO, filename="log.log")
# logger = logging.getLogger(__name__)

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

# console = logging.StreamHandler()
# console.setLevel(logging.INFO)

# formatter = ColoredFormatter(
#     "%(log_color)s%(levelname)-8s%(reset)s %(white)s%(message)s",
#     datefmt=None,
#     reset=True,
#     log_colors={
#         'DEBUG': 'cyan',
#         'INFO': 'green',
#         'WARNING': 'yellow',
#         'ERROR': 'red',
#         'CRITICAL': 'red,bg_white',
#     }
# )

# console.setFormatter(formatter)
# logger.addHandler(console)

load_dotenv()
database_url = os.getenv("DATABASE_URL")

app = Flask(__name__, template_folder='templates', static_folder="templates/static")
CORS(app)

CACHE_TTL_SECONDS = 60 * 5  # 5 минут
exhibits_cache = TTLCache(maxsize=1, ttl=CACHE_TTL_SECONDS)


async def get_data() -> List[Exhibit]:
    if 'exhibits' in exhibits_cache:
        return exhibits_cache['exhibits']

    pool = await main()
    db = Database(pool)
    data = await db.items.get_all()

    # Сохраняем данные в кэше
    exhibits_cache['exhibits'] = data
    return data


async def check_for_updates():
    while True:
        await asyncio.sleep(60 * 10)  # Проверять каждые 10 минут

        # Получаем новые данные из базы данных
        pool = await main()
        db = Database(pool)
        new_data = await db.items.get_all()

        # Проверяем наличие изменений
        if new_data != exhibits_cache.get('exhibits'):
            exhibits_cache['exhibits'] = new_data
            # logger.info("Данные в кэше обновлены")


@app.before_request
async def startup():
    await get_data()
    asyncio.create_task(check_for_updates())


@app.errorhandler(404)
@app.errorhandler(jinja2.exceptions.UndefinedError)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/')
@app.route("/index/")
@app.route("/index.html/")
def index():
    return render_template('/index.html')


@app.route("/table/")
@app.route("/table.html/")
def table():
    data = asyncio.run(get_data())
    return render_template('/table.html', data=data)


@app.route("/contacts/")
@app.route("/contacts.html/")
def contacts():
    return render_template('/contacts.html')


@app.route("/item/")
@app.route('/item.html')
def item():
    data = asyncio.run(get_data())
    loop_index = request.args.get('value')
    loop_index_mod = loop_index.replace("/", "")
    return render_template(f'/item.html', data=data, item_number=int(loop_index_mod))


@app.route("/api/test/", methods=['GET'])
def test_foo():
    return jsonify({"aboba": ["aboba1", "aboba2"]})


@app.route("/api/item/", methods=['GET'])
def item_by_number():
    data = asyncio.run(get_data())
    loop_index = request.args.get('value')
    l = int(loop_index.replace("/", ""))
    exh = data[l-1]
    exhibit = {
            'name': exh['name'],
            'quantity': exh['quantity'],
            'obtaining': exh['obtaining'],
            'discovery': exh['discovery'],
            'description': exh['description'],
            'assignment': exh['assignment'],
            # 'image': exh['image'],
            'inventory_number': {
                'number': exh['number'],
                'collection': exh['collection'],
                'fund': exh['fund']
            }
        }
    return jsonify(exhibit)


@app.route("/api/exhibits/", methods=['GET'])
async def exhibits():
    data = await get_data()  # Получаем данные из кэша или из базы данных
    exhibits_list = []
    for record in data:
        exhibit = {
            'name': record['name'],
            'quantity': record['quantity'],
            'obtaining': record['obtaining'],
            'discovery': record['discovery'],
            'description': record['description'],
            'assignment': record['assignment'],
            # 'image': record['image'],
            'inventory_number': {
                'number': record['number'],
                'collection': record['collection'],
                'fund': record['fund']
            }
        }
        exhibits_list.append(exhibit)
    return jsonify(exhibits_list)


async def main():
    try:
        pool = await asyncpg.create_pool(database_url)
    except Exception as e:
        # logging.warning("Failed to connect to database", exc_info=e)
        return
    if not pool:
        raise AssertionError
    return pool


if __name__ == '__main__':
    
    app.run(debug=True, port=8080)
