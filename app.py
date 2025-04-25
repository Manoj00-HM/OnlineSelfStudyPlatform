from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
import MySQLdb
import config

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key
bcrypt = Bcrypt(app)

# Database connection
def get_db():
    return MySQLdb.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        passwd=config.DB_PASSWORD,
        db=config.DB_NAME
    )

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                           (name, email, hashed_pw))
            conn.commit()
            flash("Signup successful! Please login.", "success")
            return redirect(url_for('login'))
        except MySQLdb.IntegrityError:
            flash("Email already exists!", "danger")
        finally:
            cursor.close()
            conn.close()
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and bcrypt.check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['name'] = user[1]
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials", "danger")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please login to access dashboard", "warning")
        return redirect(url_for('login'))
    return render_template('dashboard.html', name=session['name'])

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for('login')) 

@app.route('/courses')
def courses():
    name = session.get('name')  # assuming you saved the user name in session
    return render_template('courses.html', name=name)

@app.route('/python_course')
def python_course():
    return render_template('python.html')

@app.route('/java_course')
def java_course():
    return render_template('java.html')

@app.route('/os_course')
def os_course():
    return render_template('os.html')

@app.route('/ds_course')
def ds_course():
    return render_template('ds.html')

@app.route('/cn_course')
def cn_course():
    return render_template('cn.html')

@app.route('/dbms_course')
def dbms_course():
    return render_template('dbms.html')


if __name__ == '__main__':
    app.run(debug=True)
