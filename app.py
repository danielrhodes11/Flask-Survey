from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


responses = []

@app.route('/')
def start_page():
    return render_template('start.html', survey=survey)



@app.route('/begin', methods=['POST'])
def start_survey():
    """ clear session of responses"""
    session['responses'] = []
    return redirect('/questions/0')



@app.route('/questions/<int:qid>')
def show_questions(qid):
    """display current question"""

    responses = session.get('responses')
    if (responses is None):
        """trying to access quesiton page too soon"""
        return redirect('/') 
    
    if (len(responses) == len(survey.questions)):
        """answered all the questions"""
        return redirect ('/complete')

    if (len(responses) != qid):
        flash("Invalid question access. Please proceed in order.")
        return redirect(f"/questions/{len(responses)}")
    
    
    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)


@app.route('/answers', methods=['POST'])
def handle_answers():
    """save response and redirect to next question"""
    answer = request.form['answer']

    responses = session['responses']
    responses.append(answer)
    session['responses']=responses

    next_question = len(responses)

    if next_question == len(survey.questions):
        return redirect('/complete')
    else:
        return redirect(f"/questions/{next_question}")
    
@app.route('/complete')
def complete_form():
    """thank you page"""
    return render_template('complete.html')

    

    







