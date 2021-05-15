from random import randint
from time import strftime
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, Label
import json
import os


DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


class Questions:
    questionfile = 'questions.json'

    def __init__(self):
        with open(self.questionfile) as f:
            self.questions = json.load(f)['questions']
            self.idx = 0
            self.length = len(self.questions)
            self.score = 0
            self.q = None
    
    def question(self):
        if not self.q:
            return self.questions[self.idx]["question"]
        else:
            return self.q
    
    def next_question(self):
        if self.idx + 1 == self.length:
            self.idx = 0
        else:
            self.idx = self.idx + 1
        self.q = self.questions[self.idx]["question"]
        return self.q
    
    def get_score(self):
        return self.score
    
    def validate_answer(self, ans):
        if ans == self.questions[self.idx]["answer"]:
            self.score = self.score + 1
            return True
        return False
    
    def reset(self):
        self.score = 0


qobj = Questions()


class ReusableForm(Form):
    score = Label('score', 'Streak: ' + str(qobj.get_score()))
    question = Label('question', qobj.question())
    answer = TextAreaField('answer', validators=[validators.required()])

    def next_question(self):
        self.question = Label('question', qobj.next_question())
        self.score = Label('score', 'Streak: ' + str(qobj.get_score()))
    
    def refresh_form(self):
        qobj.reset()
        self.score = Label('score', 'Streak: ' + str(qobj.get_score()))
        self.question = Label('question', qobj.question())
        

@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
    if request.method == 'POST':
        ans=request.form['answer']
        if form.validate():
            if qobj.validate_answer(ans):
                form.next_question()
                flash('Correct!!')
            else:
                form.refresh_form()
                flash('Wrong!!')
        else:
            flash('Error: All Fields are Required')        

    return render_template('index.html', form=form)