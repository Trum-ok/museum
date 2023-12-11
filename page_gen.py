import os


class Generate:
    def __init__(self):
        super().__init__()

    def get_data(self):
        conn = sqlite3.connect('exhibits.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM exhibits')
        self.data = cur.fetchall()
        conn.close()
        return self.data

    def pages(self):
        self.data = self.get_data()
        i = 1

        # Генерация HTML-страниц на основе данных
        for column in self.data:
            html_content = f"""
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Музей "Наша Перловка"</title>
                <link rel="stylesheet" href="../static/style.css">
                <link rel="icon" type="image/png" href="../static/img/logo_mus.png">
            </head>
            <body>
            <nav class="main-nav">
                <div class="logo-container">
                    <a href="/index/">
                        <img src="../static/img/logo_mus.png" alt="Наша Перловка">
                    </a>
                </div>
                <div class="default_menu">
                    <ul>
                        <li><a href="/index/">Главная</a></li>
                        <li><a href="/table/">Таблица</a></li>
                        <li><a href="/contacts/">Контакты</a></li>
                    </ul>
                </div>
                <label for="burger_toggle" class="burger">
                    <span></span>
                    <span></span>
                    <span></span>
                </label>
            </nav>

            <main>
                <a href="/table/">< назад</a>
                <h1>{column[0]}</h1>
                <section class="example_exhib">
                    <div class="example_exhib_text">
                        <p><b>Кол-во:</b> {column[1]} шт</p>
                        <p><b>Способ получения:</b> {column[2]}</p>
                        <p><b>Место обнаружения:</b> {column[3]}</p>
                        <p><b>Описание:</b> {column[4]}</p>
                        <p><b>Назначение:</b> {column[5]}</p>
                        <p><b>Инвентарный №:</b> {column[6]}/{column[7]}/{column[8]}</p>
                    </div>
                    <img src="../static/img/pic_miss.png" alt="">
                </section>

            </main>
            <footer>
                <p>&copy; Наша Перловка 2023</p>
            </footer>
            </body>
            </html>
            """

            # Сохранение HTML-страницы
            output_path = '/Users/trum/Downloads/PycharmPr/Museum/templates/table_pages'  # изменить путь
            page_filename = f'item_{i}.html'
            page_path = os.path.join(output_path, page_filename)
            with open(page_path, 'w') as f:
                f.write(html_content)
            i += 1


# for i in data:
#     for j in range(len(i)):
#         print(i[j])
#     print("="*15)


if __name__ == '__main__':
    Generate.pages()
