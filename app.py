from flask import Flask, render_template, url_for, request, session
from get_questions_and_category_options import *
from session_variables import create_session_variables, update_session_variables
from flask_login import LoginManager, current_user
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
print("SESSION STARTS HERE WITH KEY : ",app.config['SECRET_KEY'])
# @app.route('/')
# def index():
#     if 'username' in session:
#         print("Currents user's ID is %s" % session['id']
#         return 'Logged in as %s' % escape(session['username'])
#     return 'You are not logged in'

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         session['email'] = request.form['email']
#         session['id'] = request.form['id']
#         return redirect(url_for('index'))
#     return '''
#         <form method="post">
#             <p><input type=text name=username>
#             <p><input type=submit value=Login>
#         </form>
#     '''

# @app.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     session.pop('username', None)
#     session.pop('email', None)
#     session.pop('id', None)
#     return redirect(url_for('index'))


data = get_data_from_json_file()
question_categories_list = get_question_categories(data)
print("question_categories_list : ", question_categories_list)

@app.before_request
def before_request():
    # if current_user.is_active:
        #edit or add your session var
    if('session_variables_created_hbd' not in app.config):
        app.config['session_variables_created_hbd'] = True
        create_session_variables(session, question_categories_list)
        
    return None

@app.route('/', methods=['GET', 'POST'])
def start():
    # if(app.config['session_variables_created_hbd'] == False):
        # app.config['session_variables_created_hbd'] = True 
    # if('session_variables_created_hbd' not in globals()):
    #     globals()['session_variables_created_hbd'] = True
    #     create_session_variables(session, question_categories_list)
    if request.method == 'GET':
        show_answer = False
        
        update_session_variables(session)

        info = create_question_dict(data, question_categories_list, session)
        print("info : ", info)
        # print("info[0] : ", info[0])
        # print("info[1] : ", info[1])
        session['question_dict'] = info[0]
        # set the correct answer
        session['correct_answer'] = info[1]
        # set the gifs
        session['correct_gif'] = info[2]
        session['incorrect_gif'] = info[3]

        session['options'] = shuffle_button_options(info[0])
    
        return render_template('index.html', show_answer=show_answer, S=session)
        
    if request.method == 'POST':
        show_answer = True 
        # create the request dictionary
        request_dict = {}
        for item in request.form.items():
            request_dict['value'] = item[1]

        is_finished = False
        # set is_correct variable for answer.html file
        if request_dict['value'] == session['correct_answer']:
            session['user_correct_answers'] = session.get('user_correct_answers') + 1
            is_correct = True 
        else:
            session['user_wrong_answers'] = session.get('user_wrong_answers') + 1
            is_correct = False
        
        # set the button value to "NEXT QUESTION" or "START OVER"
        if session.get('current_question') == session['number_of_questions']:
            is_finished = True
            button_value = "START OVER (or don't)"
        else:
            button_value = "NEXT QUESTION"

        return render_template('index.html', show_answer=show_answer, S=session, is_correct=is_correct, is_finished=is_finished, B_value=button_value)
    


if __name__ == '__main__':
    app.run(debug=True, threaded=True)