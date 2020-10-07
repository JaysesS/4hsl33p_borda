from app import app
from flask import render_template, redirect, url_for, flash, jsonify, make_response, send_from_directory, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from flask_wtf.csrf import CSRFError

from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from .models import db, User, Task, Solve
from .forms import RegisterForm, LoginForm, FlagForm
import json, os

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/signin'
# login_manager.session_protection = 'basic'

class AdminViewModels(ModelView):
    column_display_pk = True

    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.username == 'Jayse':
                return True
        else:
            return False
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))

class AdminViewIndex(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.username == 'Jayse':
                return True
        else:
            return False
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))

admin = Admin(app, "4hsl33p", index_view=AdminViewIndex(), endpoint='admin')
admin.add_view(AdminViewModels(User, db.session))
admin.add_view(AdminViewModels(Task, db.session))
admin.add_view(AdminViewModels(Solve, db.session))

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400

@app.before_first_request
def before_first_request_func():
    if User.get_user_by_username('Jayse') is None:
        new_user = User(username = 'Jayse', 
                        password = '***',
                        telegram = '@Jaysess',
                        score = 0
                        )
        new_user.save_to_db()

# @app.route('/delete_me')
# @login_required
# def delete_me():
#     User.delete_user_by_username(current_user.username)
#     return 'Done!'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    signup = RegisterForm()
    if signup.validate_on_submit():
        username = (signup.username.data).capitalize()
        user = User.get_user_by_username(username)
        if user is None:
            if User.check_telegram(signup.telegram.data) is False:
                new_user = User(username = username, 
                                password = signup.password.data,
                                telegram = signup.telegram.data,
                                score = 0)
                new_user.save_to_db()
                flash('Successful registration!', 'success')
                return redirect(url_for('signin'))
            else:
                flash('This telegram is already belong to smesharik..', 'danger')
        else:
            flash('This user is already smesharik..', 'danger')
    # return render_template("signup_close.html") # close reg
    return render_template("signup.html", signup = signup)

@app.route('/signin', methods = ['GET', 'POST'])
def signin():
    signin = LoginForm()
    if signin.validate_on_submit():
        username = (signin.username.data).capitalize()
        user = User.get_user_by_username(username)
        if user and user.password == signin.password.data:
            login_user(user, remember=signin.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Incorrect username or password..', 'danger')
    return render_template("signin.html", signin = signin)

@app.route('/faq')
def faq():
    path = os.path.join(os.path.abspath("."), "data/")
    with open(path + "qa.json", "r") as qa_file:
        qa = json.load(qa_file)
    with open(path + "tool.json", "r") as tool_file:
        tool = json.load(tool_file)
    return render_template("faq.html", QA = qa, TOOL = tool)

@app.route("/score_data", methods=["GET"])
def score_data():
    top = User.get_top_users(graph=True)[:5]
    count = [x for x in range(User.get_max_count_solve() + 1)]
    return make_response(jsonify({"data": top, "labels": count}), 200)

@app.route("/score")
@login_required
def score():
    top = User.get_top_users()
    score = User.get_score_by_username(current_user.username)
    place = User.get_place_by_username(current_user.username)
    count_solve = len(User.get_solves_by_username(current_user.username))
    return render_template('score.html', score = score, place = place, count_solve = count_solve, top = top)

@app.route('/send_presentation/<string:name>')
@login_required
def send_presentation(name):
    path = os.path.join(os.path.abspath("."), "data/presentation/")
    return send_from_directory(path, name)

@app.route('/send_info')
@login_required
def send_info():
    if current_user.username == 'Jayse':
        path = os.path.join(os.path.abspath("."), "data/")
        name = 'info.txt'
        info = User.get_info()
        file = open(os.path.join(path, name), 'w')
        for user in info:
            file.write(user)
        file.close()
        return send_from_directory(path, name)
    else:
        return redirect(url_for('tasks'))

@app.route("/tasks")
@login_required
def tasks():
    task_data = Task.get_tasks()
    solves = [solve.task_id for solve in User.get_solves_by_username(current_user.username)]
    return render_template('tasks.html', TASK_DATA = task_data, solves = solves, view = "all")

@app.route('/tasks/<int:id>', methods=['GET', 'POST'])
@login_required
def view_task(id):
    task = Task.get_task_by_id(id)
    flagform = FlagForm()
    if flagform.validate_on_submit():
        answer = Task.get_answer_by_id(id)
        if answer == flagform.answer.data:
            user = User.get_user_by_username(current_user.username)
            if Solve.check_user_solve_before(user.id, task.id):
                flash('True, but you\'ve already solved it!', 'success')
            else:
                solve = Solve(task_id = id, task_name = task.name, pwner = user)
                solve.save_to_db()
                User.update_score_by_username(current_user.username, task.score)
                flash('Right!', 'success')
        else:
            flash('Incorrect flag..', 'danger')
    return render_template('tasks.html', task = task, flagform = flagform, view = "one")

@app.route('/tasks_manage/<string:operation>')
@login_required
def tasks_manage(operation):
    if current_user.username == 'Jayse':
        path = os.path.join(os.path.abspath("."), "data/")
        if operation == 'refill' or operation == 'update':
            with open(path + "tasks.json", "r") as task_file:
                tasks = json.load(task_file)["data"]
                if operation == 'refill':
                    Task.clear_task()
                    User.clear_solves_for_all()
                    for task in tasks:
                        new_task = Task(task['name'], task['discription'], task['category'], task['score'], task['answer'], task['files'], task['author'], task['view'])
                        new_task.save_to_db()
                    flash('REFILL done!', 'success')
                elif operation == 'update':
                    for task in tasks:
                        check = Task.get_task_by_name(task['name'])
                        if check:
                            check.discription = task['discription']
                            check.category = task['category']
                            check.author = task['author']
                            check.view = task['view']
                            check.files = task['files']
                            check.answer = task['answer']
                            db.session.commit()
                        else:
                            new_task = Task(task['name'], task['discription'], task['category'], task['score'], task['answer'], task['files'], task['author'], task['view'])
                            new_task.save_to_db()
                    flash('UPDATE done!', 'success')
        elif operation == 'hide_all' or operation == 'open_all':
            tasks_file = open(path + "tasks.json", "r")
            tasks = json.load(tasks_file)["data"]
            tasks_file.close()
            tasks_db = Task.get_all()
            if operation == "hide_all":
                for task_db in tasks_db:
                    task_db.view = False
                for task in tasks:
                    task['view'] = False
                tasks_file = open(path + "tasks.json", "w")
                json.dump({ "data" : tasks}, tasks_file, indent=4)
                tasks_file.close()
                db.session.commit()
                flash('HIDE done!', 'success')
            elif operation == "open_all":
                for task_db in tasks_db:
                    task_db.view = True
                for task in tasks:
                    task['view'] = True
                tasks_file = open(path + "tasks.json", "w")
                json.dump({ "data" : tasks}, tasks_file, indent=4)
                tasks_file.close()
                db.session.commit()
        
                flash('OPEN done!', 'success')
        else:
            flash('Wrong operation =/', 'danger')
        return redirect(url_for('admin.index'))
    return redirect(url_for('signin'))

@app.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('index'))
    return redirect(url_for('index'))