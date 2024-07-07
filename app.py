from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///members.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    members = db.relationship('Member', backref='company', lazy=True)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(100), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False)
    payment_date = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

@app.route('/')
def index():
    companies = Company.query.all()
    return render_template('index.html', companies=companies)

@app.route('/company/<int:company_id>')
def company_members(company_id):
    company = Company.query.get_or_404(company_id)
    return render_template('company_members.html', company=company)

@app.route('/add_member/<int:company_id>', methods=['GET', 'POST'])
def add_member(company_id):
    if request.method == 'POST':
        name = request.form['name']
        photo = request.form['photo']
        payment_status = request.form['payment_status']
        payment_date = request.form['payment_date']
        amount = int(request.form['amount'])
        new_member = Member(name=name, photo=photo, payment_status=payment_status, payment_date=payment_date, amount=amount, company_id=company_id)
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('company_members', company_id=company_id))
    return render_template('add_member.html', company_id=company_id)

@app.route('/delete_member/<int:member_id>')
def delete_member(member_id):
    member = Member.query.get_or_404(member_id)
    company_id = member.company_id
    db.session.delete(member)
    db.session.commit()
    return redirect(url_for('company_members', company_id=company_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
