from flask import Flask, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
import os

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'verysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finansdb.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Define the Transaction model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Transaction {self.amount} - {self.description}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Implementation of your login logic
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Example data fetching for the dashboard
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.timestamp.desc()).all()
    return render_template('dashboard.html', transactions=transactions)

@app.route('/transactions')
@login_required
def transactions():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    return render_template('transactions.html', transactions=transactions)

@app.route('/reports')
@login_required
def reports():
    # Reports data fetching logic
    return render_template('reports.html')

if __name__ == '__main__':
    app.run(debug=True)




