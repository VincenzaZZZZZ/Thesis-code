from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
from check_answer import check_answer

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

TXT_DIR = os.path.join(app.static_folder, 'exercises')
JSON_DIR = os.path.join(app.static_folder, 'json')

db = SQLAlchemy(app)

# database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    points = db.Column(db.Integer, default=0)

class SolvedExercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise_filename = db.Column(db.String(100), nullable=False)
    used_hint =db.Column(db.Boolean, default=False)

    db.UniqueConstraint('user_id', 'exercise_filename')

#get progress based on solved exercises
def get_progress(username):
    prefix = ""
    user = User.query.filter_by(username=username).first()
    solved = SolvedExercise.query.filter_by(user_id=user.id).all()

    progress = {}
    for i in range(1, 6):
        progress[f'Exercise {i}'] = [0, 0, 0]

    for item in solved:
        for i in range(1, 6):
            if i == 1:
                prefix = "if-statement"
            elif i == 2:
                prefix = "loop"
            elif i == 3:
                prefix = "function"
            elif i == 4:
                prefix = "sorting"
            elif i == 5:
                prefix = "real-world-example"
            for j, level in enumerate(['easy', 'medium', 'hard']):
                if f"{prefix}-{level}" == item.exercise_filename:
                    progress[f'Exercise {i}'][j] = 1

    return progress

# calculate working on exercise
def get_working_on(progress):
    index = 1
    for i in range(5, 0, -1):
        levels = progress.get(f'Exercise {i}', [0, 0, 0])
        if any(levels):
            index = i
            break
    return index

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['pwd']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, pwd):
            session['username'] = user.username
            return redirect(url_for('profile'))
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login_user'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        pwd = request.form['pwd']
        confirmed_pwd = request.form['confirmed_pwd']

        if pwd != confirmed_pwd:
            return render_template('signup.html', error="Passwords do not match")
        if len(pwd) < 6:
            return render_template('signup.html', error="Password too short")
        if User.query.filter_by(username=username).first():
            return render_template('signup.html', error="Username already exists")

        hashed_pwd = generate_password_hash(pwd)
        new_user = User(username=username, email=email, password=hashed_pwd)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('profile'))
    return render_template('signup.html')

@app.route('/information')
def information():
    if 'username' not in session:
        return redirect(url_for('login_user'))
    return render_template('information.html', username=session['username'])

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login_user'))

    username = session['username']
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()

    # leaderboard
    leaderboard = User.query.order_by(User.points.desc()).limit(5).all()

    leaderboard_info = []
    for u in leaderboard:
        user_progress = get_progress(u.username)
        user_working_on = get_working_on(user_progress)
        leaderboard_info.append({
            'username': u.username,
            'points': u.points,
            'working_on': user_working_on
        })

    # progress for leaderboard and badge
    progress = get_progress(username)
    working_on = get_working_on(progress)

    # badge function
    badge_map = {
        'Exercise 1': 'badges/moth1.png',
        'Exercise 2': 'badges/moth2.png',
        'Exercise 3': 'badges/moth3.png',
        'Exercise 4': 'badges/moth4.png',
        'Exercise 5': 'badges/moth5.png'
    }

    badge_img = []

    for exercise_num, levels in progress.items():
        if isinstance(levels, list) and len(levels) == 3 and levels[2] == 1:
            badge_img.append(badge_map[exercise_num])

    badge_img.sort(reverse=True)

    badge_img = badge_img[:2]

    while len(badge_img) < 2:
        badge_img.append('badges/empty.png')

    return render_template('profile.html',
                           username=username,
                           points=user.points,
                           badges=badge_img,
                           leaderboard=leaderboard_info,
                           progress=progress,
                           working_on=working_on)

@app.route('/badges')
def badges():
    if 'username' not in session:
        return redirect(url_for('login_user'))

    username = session['username']
    progress = get_progress(username)

    return render_template('badges.html', username=username, progress=progress)

@app.route('/exercise/<filename>', methods=['GET', 'POST'])
def exercise(filename):
    if 'username' not in session:
        return redirect(url_for('login_user'))

    full_filename = filename + '.json'
    filepath = os.path.join(JSON_DIR, full_filename)

    if not os.path.exists(filepath):
        return f"Exercise JSON '{full_filename}' not found.", 404

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    user = User.query.filter_by(username=session['username']).first()

    level = data.get('level')
    points_map = {"easy": 10, "medium": 20, "hard": 30}
    feedback = ""
    used_hint_flag = False

    if request.method == 'POST':
        user_lines = request.form.get('bug-position', '')
        user_inputs = request.form.get('bug-input-text', '')
        used_hint_flag = request.form.get('used_hint', 'false') == 'true'

        # bug lines
        submitted_lines = set(int(x.strip()) for x in user_lines.split(',') if x.strip().isdigit())
        correct_lines = set(map(int, data.get("bug_location", [])))

        # bug inputs
        correct_inputs = data.get("expected_inputs", [])

        # check answer
        input_correct = check_answer(filename, user_inputs, correct_inputs)

        line_correct = not correct_lines.isdisjoint(submitted_lines)
        existing = SolvedExercise.query.filter_by(user_id=user.id, exercise_filename=filename).first()

        # print feedback
        if line_correct and input_correct:
            if not existing:
                points = points_map[level]
                if used_hint_flag:
                    points -= 3
                user.points += points
                db.session.add(SolvedExercise(user_id=user.id, exercise_filename=filename))
                db.session.commit()
                feedback = f"Good Job! Correct! You have earned {points} points."
            else:
                feedback = "Good Job! But already correct before. No extra points awarded."
        elif line_correct:
            feedback = "Almost! Bug location is correct, but input is not."
        elif input_correct:
            feedback = "Almost! Input is correct, but bug location is not."
        else:
            feedback = "Try Again! Both bug location and input are incorrect."

    return render_template('exercise.html', **data, username=session['username'], feedback=feedback, used_hint=used_hint_flag)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="127.0.0.1", port=5000)

