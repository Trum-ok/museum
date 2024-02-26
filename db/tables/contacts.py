import os
import json

from pydantic import BaseModel, Field


JSON_PATH = "E:\\PyProjects\\museum\\db\\contacts.json"
DEFAULT_CONTACTS_DATA = {
    "address": "ул. 1-я Крестьянская, 14, Мытищи, Московская обл., 141014",
    "phone": "7(xxx)xxx xx xx",
    "email": "somemail@mail.ru",
    "working_hours": {
        "пн": "xx:xx - xx:xx",
        "вт": "xx:xx - xx:xx",
        "ср": "xx:xx - xx:xx",
        "чт": "xx:xx - xx:xx",
        "пт": "xx:xx - xx:xx",
        "сб": "xx:xx - xx:xx",
        "вс": "xx:xx - xx:xx"
    },
    "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d279.6706167773242!2d37.71882571769209!3d55.89103002446313!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46b5316c13d0ec4d%3A0x5f327e1cdc9b40de!2z0KHRgNC10LTQvdGP0Y8g0L7QsdGJ0LXQvtCx0YDQsNC30L7QstCw0YLQtdC70YzQvdCw0Y8g0YjQutC-0LvQsCDihJYgNQ!5e0!3m2!1sru!2sru!4v1681766947883!5m2!1sru!2sru"
}


class Hours(BaseModel):
    mon: str = Field(default="xx:xx - xx:xx")
    tue: str = Field(default="xx:xx - xx:xx")
    wed: str = Field(default="xx:xx - xx:xx")
    thu: str = Field(default="xx:xx - xx:xx")
    fri: str = Field(default="xx:xx - xx:xx")
    sat: str = Field(default="xx:xx - xx:xx")
    sun: str = Field(default="xx:xx - xx:xx")


class Info(BaseModel):
    address: str = Field(default="ул. 1-я Крестьянская, 14, Мытищи, Московская обл., 141014")  # noqa: E501
    phone: str = Field(default="7(xxx)xxx xx xx")
    email: str = Field(default="somemail@mail.ru")
    hours: Hours
    map: str = Field(default="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d279.6706167773242!2d37.71882571769209!3d55.89103002446313!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46b5316c13d0ec4d%3A0x5f327e1cdc9b40de!2z0KHRgNC10LTQvdGP0Y8g0L7QsdGJ0LXQvtCx0YDQsNC30L7QstCw0YLQtdC70YzQvdCw0Y8g0YjQutC-0LvQsCDihJYgNQ!5e0!3m2!1sru!2sru!4v1681766947883!5m2!1sru!2sru")


class ContactsTable:
    def __init__(self):
        self.create()
        self.data = self.load_data_from_json()

    def load_data_from_json(self) -> Info:
        with open(JSON_PATH, 'r') as file:
            json_data = json.load(file)
            return Info(**json_data)

    def get_address(self) -> str:
        return self.data.address

    def get_phone(self) -> str:
        return self.data.phone

    def get_email(self) -> str:
        return self.data.email

    def get_hours(self) -> Hours:
        return self.data.hours
    
    def create(self) -> None:
        if not os.path.exists(JSON_PATH):
            with open(JSON_PATH, 'w') as file:
                json.dump(DEFAULT_CONTACTS_DATA, file, indent=4)

    def update(self, data) -> None:
        try:
            with open(JSON_PATH, 'w') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
            print("Data successfully updated.")
        except Exception as e:
            print(f"Error while updating data: {e}")
