from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
db = SQLAlchemy(app)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    rate = db.Column(db.Integer)


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        t = request.form['text']
        r = request.form['rate']

        if r == "":
            r = 5

        new_obj = Review(text=t, rate=int(r))
        db.session.add(new_obj)
        db.session.commit()
        return redirect('/')

    all_data = Review.query.all()
    return render_template('task.html', reviews=all_data)


if __name__ == '__main__':
    app.run(debug=True)