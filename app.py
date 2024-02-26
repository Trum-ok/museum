import os
import jwt
import asyncio
import asyncpg

from typing import List
from functools import wraps
from datetime import datetime
from dotenv import load_dotenv
from cachetools import TTLCache

from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from db.main import Database
from db.tables.item import Exhibit, ExhibitColumns
from db.tables.events import EventType, Event


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET_TOKEN = os.getenv("JWT_SECRET_TOKEN")

app = Flask(__name__, template_folder='templates', static_folder="templates/static")
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

app.config['JWT_SECRET_KEY'] = JWT_SECRET_TOKEN
JWTManager(app)


CACHE_TTL_SECONDS = 60 * 5  # 5 минут
ADMIN_CACHE_TTL_SECONDS = 60  # 1 минутa
exhibits_cache = TTLCache(maxsize=256, ttl=CACHE_TTL_SECONDS)
admins_cache = TTLCache(maxsize=128, ttl=ADMIN_CACHE_TTL_SECONDS)


def requires_token(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        try:
            token = request.headers.get('Authorization', '').split(' ')[1]
            secret_key = JWT_SECRET_TOKEN
            decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
            return await f(*args, token=decoded, **kwargs, token_valid=True)
        except jwt.ExpiredSignatureError:
            return await f(*args, token=None, **kwargs, token_valid=False)
        except jwt.InvalidTokenError:
            return await f(*args, token=None, **kwargs, token_valid=False)
        except IndexError:
            return jsonify({"error": "no token"}), 401
        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500
    return decorated_function


async def get_data() -> List[Exhibit]:
    """Retrieving the list of exhibits from cache or database."""
    # if 'exhibits' in exhibits_cache:
    #     return exhibits_cache['exhibits']

    pool = await main()
    async with pool:
        db = Database(pool)
        data = await db.items.get_all()

    exhibits_cache['exhibits'] = data
    return data


async def get_deleted_items() -> List[Exhibit]:
    pool = await main()
    async with pool:
        db = Database(pool)
        data = await db.deleted.get_all()
    return data


async def get_events() -> List[Event]:
    pool = await main()
    async with pool:
        db = Database(pool)
        data = await db.events.get_all()
    return data


async def get_columns(name: str, columns: list):
    pool = await main()
    async with pool:
        db = Database(pool)
        data = await db.items.get(name, columns=columns)
    return data


async def check_for_updates():
    while True:
        await asyncio.sleep(60 * 10)  # Проверять каждые 10 минут
        pool = await main()
        async with pool:
            db = Database(pool)
            new_data = await db.items.get_all()
            if new_data != exhibits_cache.get('exhibits'):
                exhibits_cache['exhibits'] = new_data


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

    pool = await main()
    async with pool:
        db = Database(pool)
        result = await db.admins.check_lp(data["login"], data["password"])
    
    if result:
        token = jwt.encode({'sub': data["login"]}, key=JWT_SECRET_TOKEN, algorithm='HS256')
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
    serialized_data = [exhibit.model_dump() for exhibit in data if exhibit.visible]
    return jsonify(serialized_data), 200


@app.route("/api/adm/", methods=['GET'])    
@requires_token
async def exhibits_admin(token_valid, token):
    if token_valid:
        data = await get_data()
        serialized_data = [exhibit.model_dump() for exhibit in data]
        return jsonify(serialized_data), 200
    return jsonify({"error": "Unauthorized"}), 401
    

@app.route("/api/deleted_exhibits/", methods=['GET'])
@requires_token
async def del_exhibits(token_valid, token):
    if token_valid:
        data = await get_deleted_items()
        serialized_data = [exhibit.model_dump() for exhibit in data]
        return jsonify(serialized_data), 200
    return jsonify({"error": "Unauthorized"}), 401


@app.route("/api/events/", methods=['GET'])
@requires_token
async def events(token_valid, token):
    if token_valid:
        data = await get_events()
        serialized_data = [exhibit.model_dump() for exhibit in data]
        return jsonify(serialized_data), 200
    return jsonify({"error": "Unauthorized"}), 401


@app.route("/api/add/", methods=["POST"])
@requires_token
async def add_item(token_valid, token):
    if token_valid:
        try:
            user_id = token.get('sub')
            
            new_exhibit = request.json
            exhibit = Exhibit(**new_exhibit)
            
            pool = await main()
            db = Database(pool)
            event = Event(
                type_=EventType.ADD,
                now=f"{exhibit.inventory_number.number}/{exhibit.inventory_number.collection}/{exhibit.inventory_number.fund}",
                admin=user_id
            )
            await db.events.insert(event)


            return jsonify({'success': True, 'user_id': user_id, 'exhibit': new_exhibit}), 200
        except Exception as e:
            print(e)
            return jsonify({"error": "К сожалению сервер не смог обработать ваш запрос"}), 401
    return jsonify({"error": "Unauthorized"}), 401


@app.route("/api/hide_unhide/", methods=["POST"])
@requires_token
async def hide_or_unhide(token_valid, token):
    if token_valid:
        exhibit = Exhibit(**request.json)
        user_id = token.get('sub')

        visible = await get_columns(exhibit.name, columns=[ExhibitColumns.VISIBLE])
        print(visible)
        t = EventType.HIDE if visible else EventType.UNHIDE

        event = Event(
                type_=t,
                was=str(visible),
                now=str(not visible),
                admin=user_id
            )

        pool = await main()
        async with pool:
            db = Database(pool)
            await db.events.insert(event)
            await db.items.update(exhibit.id, visible=not visible)
        return jsonify({'msg': f"{visible} -> {not visible}", 'visible': not visible}), 200
    return jsonify({"error": "Unauthorized"}), 401
    
 
@app.route("/api/delete/", methods=["POST"])
@requires_token
async def delete_exhibit(token_valid, token):
    if token_valid:
        data = request.json
        user_id = token.get('sub')
        exhibit = Exhibit(**data)

        pool = await main()
        async with pool:
            db = Database(pool)

            e = Event(
                type_=EventType.DELETE,
                admin=user_id
            )

            await db.events.insert(event=e)
            await db.deleted.insert(exhibit)
            print(exhibit.id)
            await db.items.delete(exhibit.id)

        return(jsonify(data)), 200
    return jsonify({"error": "Unauthorized"}), 401



@app.route("/api/restore/", methods=["POST"])
@requires_token
async def restore_exhibit(token_valid, token):
    if token_valid:
        user_id = token.get('sub')
        exhibit = Exhibit(**request.json)

        event = Event(
            type_=EventType.RESTORE,
            admin=user_id
        )

        pool = await main()
        async with pool:
            db = Database(pool)
            await db.events.insert(event=event)
            await db.items.insert(exhibit)
            await db.deleted.delete(exhibit.id)

        return jsonify({"msg": "ok"}), 200
    return jsonify({"error": "Unauthorized"}), 401


async def main() -> asyncpg.Pool:
    """Database connection"""
    try:
        pool = await asyncpg.create_pool(DATABASE_URL)
    except Exception as e:
        # logging.warning("Failed to connect to database", exc_info=e)
        print(e)
        return e
    if not pool:
        raise AssertionError
    return pool


async def setup_db():
    """Database setup"""
    pool = await main()
    async with pool:
        db = Database(pool)
        await db.create()


if __name__ == '__main__':    
    asyncio.run(setup_db())
    app.run(debug=True, port=8080)
