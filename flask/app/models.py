from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from operator import itemgetter
import time

from pprint import pprint

db = SQLAlchemy()

class User(UserMixin, db.Model):
    
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique = True)
    password = db.Column(db.String(150))
    telegram = db.Column(db.String(50), unique = True)
    score = db.Column(db.Integer, default = 0)
    tasks_solve  = db.relationship('Solve', backref='pwner')

    def __init__(self, username, password, telegram, score):
        self.username = username
        self.password = password
        self.telegram = telegram
        self.score = score

    def __repr__(self):
        return "{}".format(self.username)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_solves_by_username(cls, username):
        return [x for x in cls.query.filter_by(username=username).first().tasks_solve]

    @classmethod
    def clear_solves_for_all(cls):
        Solve.clear_solves()
        for user in cls.query.all():
            user.tasks_solve = []
            user.score = 0
        db.session.commit()
        
    @classmethod
    def update_score_by_username(cls, username, score):
        user = cls.get_user_by_username(username)
        user.score += score
        db.session.commit()
    
    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def check_telegram(cls, telegram):
        for user in cls.query.all():
            if telegram == user.telegram:
                return True
        return False
    
    @classmethod
    def get_top_users(cls, graph = False):
        all_users = cls.query.all()
        if graph:
            top =[
                    {
                        "name": user.username,
                        "score": user.score,
                        "place": cls.get_place_by_username(user.username),
                        "solve" : [{"task_name": Task.get_task_by_id(x.task_id).name, "score": Task.get_task_by_id(x.task_id).score} for x in cls.get_solves_by_username(user.username)]
                    }
                for user in all_users]
        else:
            top =   [{
                    "name": user.username,
                    "score": user.score,
                    "place": cls.get_place_by_username(user.username)
                 }
                for user in all_users]

        return sorted(top, key=itemgetter('place'), reverse=False)
    
    @classmethod
    def get_score_by_username(cls, username):
        return cls.query.filter_by(username=username).first().score
    
    @classmethod
    def get_place_by_username(cls, username):
        all_users = cls.query.order_by(cls.score.desc()).all()
        place = 1
        for user in all_users:
            if user.username == username:
                return place
            else:
                place +=1

    @classmethod
    def get_max_count_solve(cls):
        max_count = 0
        for user in cls.query.all():
            if len(user.tasks_solve) > max_count:
                max_count = len(user.tasks_solve)
        return max_count

    @classmethod
    def get_info(cls):
        return [
            "username: {}| telegram: {}| score: {}| task count: {}\n\n".format(str(user.username).center(20), str(user.telegram).center(40), str(user.score).center(10), str(len(user.tasks_solve)).center(6)) 
            for user in cls.query.all()]

class Solve(UserMixin, db.Model):

    __tablename__ = 'solve'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer)
    task_name = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time = db.Column(db.String(50), default = time.ctime(int(time.time())))
    
    def save_to_db(self):
        db.session.add(self)
        Task.add_solve_by_id(self.task_id)
        db.session.commit()
    
    @classmethod
    def clear_solves(cls):
        cls.query.delete()
        db.session.commit()

    @classmethod
    def check_user_solve_before(cls, user_id, task_id):
        for solve in cls.query.filter_by(user_id=user_id).all():
            if task_id == solve.task_id:
                return True
        return False


class Task(UserMixin, db.Model):
    
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), unique = True)
    discription = db.Column(db.String(800))
    category = db.Column(db.String(150))
    score = db.Column(db.Integer, default = 0)
    answer = db.Column(db.String(500))
    files = db.Column(db.String(150))
    author = db.Column(db.String(50))
    solves = db.Column(db.Integer)
    training = db.Column(db.Boolean)
    view = db.Column(db.Boolean)

    def __init__(self, name, discription, category, score, answer, files, author, training, view):
        self.name = name
        self.discription = discription
        self.category = category
        self.score = score
        self.answer = answer
        self.files = files
        self.author = author
        self.solves = 0
        self.training = training
        self.view = view

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_answer_by_id(cls, id):
        return cls.query.filter_by(id=id).first().answer

    @classmethod
    def clear_task(cls):
        cls.query.delete()
        db.session.commit()
    
    @classmethod
    def add_solve_by_id(cls, id):
        task = cls.get_task_by_id(id)
        task.solves += 1
        db.session.commit()
    
    @classmethod
    def get_all_categories(cls):
        return list(set([x[0] for x in cls.query.with_entities(cls.category).all()]))

    @classmethod
    def get_task_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_task_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_tasks(cls, training = False):
        categories = cls.get_all_categories()
        tasks = []
        for category in categories:
            task_dict = dict()
            tasks_with_category = cls.query.filter_by(category=category).all()
            temp_list_for_category = list()
            for task in tasks_with_category:
                if training and task.training:
                    temp_list_for_category.append({ 
                                    "id": task.id,
                                    "name": task.name,
                                    "score": task.score,
                                    "solves": task.solves,
                                    "view" : task.view,
                                    "author": task.author
                                })
                elif training is False and task.training is False:
                    temp_list_for_category.append({ 
                                    "id": task.id,
                                    "name": task.name,
                                    "score": task.score,
                                    "solves": task.solves,
                                    "view" : task.view,
                                    "author": task.author
                                })
            
            task_dict['category'] = category
            task_dict['data'] = list()
            task_dict['data'].append(temp_list_for_category)
            tasks.append(task_dict)
        
        for category in tasks:
            category['view_category'] = False
            for t_tasks in category['data']:
                for task in t_tasks:
                    if task['view'] is True:
                        category['view_category'] = True
        for category in tasks:
            if category['view_category'] == True and len(category['data']) != 0:
                return tasks
        return []