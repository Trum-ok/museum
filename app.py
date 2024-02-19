import os
import jinja2
import asyncio
import asyncpg
import sqlite3

from typing import List
from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask, render_template, request, jsonify
from cachetools import TTLCache

from db.main import Database
from db.tables.item import Exhibit, InventoryNumber


load_dotenv()
database_url = os.getenv("DATABASE_URL")

app = Flask(__name__, template_folder='templates', static_folder="templates/static")
CORS(app)

CACHE_TTL_SECONDS = 60 * 5  # 5 минут
exhibits_cache = TTLCache(maxsize=1, ttl=CACHE_TTL_SECONDS)


async def get_data() -> List[Exhibit]:
    """Retrieving the list of exhibits from cache or database."""
    if 'exhibits' in exhibits_cache:
        return exhibits_cache['exhibits']

    pool = await main()
    db = Database(pool)
    data = await db.items.get_all()

    exhibits_cache['exhibits'] = data
    return data


async def check_for_updates():
    while True:
        await asyncio.sleep(60 * 10)  # Проверять каждые 10 минут

        pool = await main()
        db = Database(pool)
        new_data = await db.items.get_all()

        if new_data != exhibits_cache.get('exhibits'):
            exhibits_cache['exhibits'] = new_data
            # logger.info("Данные в кэше обновлены")


@app.before_request
async def startup():
    await get_data()
    asyncio.create_task(check_for_updates())


@app.errorhandler(404)
@app.errorhandler(Exception)
@app.errorhandler(IndexError)
def page_not_found(error):
    return jsonify({'error': 'Page not found', 'redirect': '/404'}), 404


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


async def main() -> asyncpg.Pool:
    """Database connection"""
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
