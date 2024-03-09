from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import config

app = Flask(__name__)

app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        app.logger.info('Received POST request to add student: Name - %s, Email - %s', name, email)
        
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO students (name, email) VALUES (%s, %s)", (name, email))
            mysql.connection.commit()
            app.logger.info('Student added successfully: Name - %s, Email - %s', name, email)
        except Exception as e:
            app.logger.error('Error adding student to database: %s', str(e))
        finally:
            cur.close()
        
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)