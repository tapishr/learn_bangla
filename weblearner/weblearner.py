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
    
    def next_question(self):
        if self.idx == self.length:
            self.idx = 0
        q = self.questions[self.idx]["question"]
        self.idx = self.idx + 1
        return q
    
    def validate_answer(self, ans):
        if ans == self.questions[self.idx-1]["answer"]:
            return True
        return False


qobj = Questions()


class ReusableForm(Form):
    question = Label('question', qobj.next_question())
    answer = TextAreaField('answer', validators=[validators.required()])


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    if request.method == 'POST':
        ans=request.form['answer']

        if form.validate():
            if qobj.validate_answer(ans):
                flash('Correct!!')
            else:
                flash('Wrong!!')

        else:
            flash('Error: All Fields are Required')

    return render_template('index.html', form=form)