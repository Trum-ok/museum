import pandas as pd
from sqlalchemy import create_engine


class new_data:
    def __init__(self, filepath):
        super().__init__()
        self.file_path = filepath

    def new_data_(self):
        # data = pd.read_excel('templates/static/tables/dbv2.xlsx')
        data = pd.read_excel(self.file_path)

        data['am'] = data['am'].astype(int)
        data['inventory'] = data['inventory'].astype(int)

        engine = create_engine('sqlite:///exhibits.db', echo=True)
        sqlite_connection = engine.connect()

        data.to_sql('exhibits', sqlite_connection, if_exists='replace', index=False)


if __name__ == '__main__':
    filepath = "templates/static/tables/dbv2.xlsx"
    new_data(filepath).new_data_()
