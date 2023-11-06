from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
from config import host, user, password, db_name

app = Flask(__name__)

# Функция для установления соединения с базой данных
def create_db_connection():
    try:
        conn = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as ex:
        print('Ошибка при подключении к базе данных:', ex)
        return None

# Создание таблицы (однократное выполнение)
@app.route('/api/create_table', methods=['POST'])
def create_table():
    connection = create_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                create_table_query = "CREATE TABLE my_worcks(id int AUTO_INCREMENT, link varchar(100), title varchar(100), image varchar(100), about varchar(100), PRIMARY KEY (`id`))"
                cursor.execute(create_table_query)
                connection.commit()
                return 'Таблица создана'
        except Exception as ex:
            return 'Ошибка при создании таблицы: ' + str(ex)
        finally:
            connection.close()
    else:
        return 'Ошибка при подключении к базе данных'

# Добавление строки
@app.route('/api/add_row', methods=['POST'])
def add_row():
    data = request.get_json()
    link = data['link']
    title = data['title']
    image = data['image']
    about = data.get('about', '')
    print(data)

    connection = create_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                insert_query = "INSERT INTO my_worcks(link, title, image, about) VALUES (%s, %s, %s, %s)"
                cursor.execute(insert_query, (link, title, image, about))
                connection.commit()
                return 'Запись добавлена'
        except Exception as ex:
            return 'Ошибка при добавлении записи: ' + str(ex)
        finally:
            connection.close()
    else:
        return 'Ошибка при подключении к базе данных'

# Получение всех записей
@app.route('/api/get_all', methods=['GET'])
def get_all():
    connection = create_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                select_all = "SELECT * FROM my_worcks"
                cursor.execute(select_all)
                rows = cursor.fetchall()
                print(jsonify(rows))
                return jsonify(rows)
        except Exception as ex:
            return 'Ошибка при получении данных: ' + str(ex)
        finally:
            connection.close()
    else:
        return 'Ошибка при подключении к базе данных'

if __name__ == '__main__':
    app.run(debug=True)
    
