from random import randint
from time import strftime
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, Label
from weblearner import questions

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'
q = questions.Questions()

class ReusableForm(Form):
    question = Label('question', q.next_question())
    answer = TextAreaField('answer', validators=[validators.required()])


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    if request.method == 'POST':
        ans=request.form['answer']

        if form.validate():
            if q.validate_answer(ans):
                flash('Correct!!')
            else:
                flash('Wrong!!')

        else:
            flash('Error: All Fields are Required')

    return render_template('index.html', form=form)