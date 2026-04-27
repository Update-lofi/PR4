from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime

app = Flask(__name__)
FILE_NAME = 'tasks.json'

def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

tasks = load_tasks()

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    new_task_text = request.form.get('task', '').strip()
    if new_task_text:
        new_task = {
            "text": new_task_text,
            "date": datetime.now().strftime("%d.%m.%Y %H:%M")
        }
        tasks.append(new_task)
        save_tasks(tasks)
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect('/')

@app.route('/clear_all')
def clear_all_tasks():
    tasks.clear()
    save_tasks(tasks)
    return redirect('/')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    # функция получает номер (индекс) редактируемой задачи.
    if task_id < 0 or task_id >= len(tasks):
        # Проверка: если индекс отрицательный или выходит за границы списка задач,
        return "Задача не найдена", 404
        # то возвращаем сообщение об ошибке и HTTP-статус 404 (Not Found).

    if request.method == 'POST':
        # Если метод запроса POST (пользователь отправил форму с изменениями)...

        new_text = request.form.get('task', '').strip()
        # Из данных формы извлекаем значение поля с именем 'task'.
        # .get() возвращает '' если поля нет (безопаснее, чем прямая индексация).
        # .strip() удаляет лишние пробелы в начале и конце строки.

        if new_text:
            # Если после удаления пробелов строка не пуста...

            tasks[task_id]['text'] = new_text
            # Обращаемся к задаче по индексу (это словарь) и обновляем её ключ 'text' новым текстом.
            # Важно: мы не заменяем весь словарь           
# а меняем только одно поле. Остальные поля (например, 'date') остаются нетронутыми.

            save_tasks(tasks)
            # Сохраняем обновлённый список задач в файл JSON.

        return redirect('/')
        # Перенаправляем пользователя на главную страницу (список задач).

    else:
        # Иначе (если метод GET — пользователь только перешёл по ссылке "Редактировать")...

        return render_template('edit.html', task=tasks[task_id])
        # Отображаем шаблон edit.html, передавая в него словарь задачи (task).


if __name__ == '__main__':
    app.run(debug=True)