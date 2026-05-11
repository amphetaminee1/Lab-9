from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
db = SQLAlchemy(app)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    rate = db.Column(db.Integer)
    is_visible = db.Column(db.Boolean, default=True)


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        t = request.form['text']
        r = request.form.get('rate')
        if not r: r = 5

        new_obj = Review(text=t, rate=int(r), is_visible=True)
        db.session.add(new_obj)
        db.session.commit()
        return redirect('/')

    visible_data = Review.query.filter_by(is_visible=True).all()
    return render_template('task.html', reviews=visible_data)


@app.route('/clear', methods=['POST'])
def clear_view():
    visible_reviews = Review.query.filter_by(is_visible=True).all()
    for r in visible_reviews:
        r.is_visible = False

    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)