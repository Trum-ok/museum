import os
import jwt
import asyncio
import asyncpg

from typing import List
from dotenv import load_dotenv
from cachetools import TTLCache
from flask_cors import CORS
from flask import Flask, request, jsonify

from db.main import Database
from db.tables.item import Exhibit
from dev.utils import cookie_gen


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

app = Flask(__name__, template_folder='templates', static_folder="templates/static")
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})


CACHE_TTL_SECONDS = 60 * 5  # 5 минут
ADMIN_CACHE_TTL_SECONDS = 60  # 1 минутa
exhibits_cache = TTLCache(maxsize=256, ttl=CACHE_TTL_SECONDS)
admins_cache = TTLCache(maxsize=128, ttl=ADMIN_CACHE_TTL_SECONDS)


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
    await asyncio.create_task(get_data())
    asyncio.create_task(check_for_updates())


@app.errorhandler(404)
# @app.errorhandler(Exception)
@app.errorhandler(IndexError)
def page_not_found(error):
    return jsonify({'error': 'Page not found', 'redirect': '/404'}), 404


@app.route("/api/auth/", methods=["POST"])
async def auth():
    data = request.json
    print(data)

    pool = await main()
    db = Database(pool)
    result = await db.admins.check_lp(data["login"], data["password"])
    
    if result:
        key = "_Yr019xMxv6ZM1TGTWMbgRK-W3RjdMYpdq_g9yHUw8jGWDlpc85gvm0ExXPNqNnVKNoQcB6OvIcPKCBtVrClsw"
        token = jwt.encode({'login': data["login"]}, key=key, algorithm='HS256')
        print(token)
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401



@app.route("/api/item/", methods=['GET'])
def item_by_number():
    data = asyncio.run(get_data())
    loop_index = request.args.get('value')
    i = int(loop_index.replace("/", ""))
    return jsonify(data[i-1].model_dump())


@app.route("/api/exhibits/", methods=['GET'])
async def exhibits():
    data = await get_data()
    serialized_data = [exhibit.model_dump() for exhibit in data]
    return jsonify(serialized_data)


async def main() -> asyncpg.Pool:
    """Database connection"""
    try:
        pool = await asyncpg.create_pool(DATABASE_URL)
    except Exception as e:
        # logging.warning("Failed to connect to database", exc_info=e)
        return
    if not pool:
        raise AssertionError
    return pool


async def setup_db():
    """Database setup"""
    # try:
    pool = await main()
    db = Database(pool)
    await db.create()
    # except Exception as e:
    #     # logging.warning(exc_info=e)
    #     return


if __name__ == '__main__':    
    asyncio.run(setup_db())
    app.run(debug=True, port=8080)
