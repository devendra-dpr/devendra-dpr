from datetime import datetime
import csv, yaml
from pathlib import Path
from typing import List
from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime, ForeignKey, func, Enum, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_migrate import Migrate
import enum

app = Flask(__name__)


class Base(DeclarativeBase): pass

# SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
db = SQLAlchemy(app=app, model_class=Base)
migrate = Migrate(app, db)


class Question_type(enum.Enum):
    smile: str = "smile"                    # simple_smile_rating
    star: str = "star"                      # simple_star_rating
    staff_smile: str = "staff_smile"       # staff_smile_rating
    staff_star: str = "staff_star"         # staff_star_rating


class ReviewType(enum.Enum):
    good: str = "good" 
    neutral: str = "neutral" 
    bad: str = "bad"


class Stores(db.Model):
    __tablename__ = "stores"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    max_clicks: Mapped[int] = mapped_column(Integer, nullable=True)
    redirect_url: Mapped[str] = mapped_column(String(100), nullable=False)
    welcome_text: Mapped[str] = mapped_column(String(250), nullable=False)

    user_clicks: Mapped[List["UserClicks"]] = relationship(back_populates="store")
    questions: Mapped[List["Questions"]] = relationship(back_populates="store")
    review_sugg: Mapped[List["ReviewSugg"]] = relationship(back_populates="store")

    def __repr__(self):
        return f"<Stores(id={self.id}, store_name='{self.store_name}')>"


class UserClicks(db.Model):
    __tablename__ = "user_clicks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    dt: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow(), 
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")   # returns the current date and time
    )
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"))
    
    store: Mapped["Stores"] = relationship(back_populates="user_clicks")
    
    def __repr__(self):
        return f"<UserClicks(id={self.id}, store_name='{self.store.store_name}')>"


class Questions(db.Model):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(String, nullable=False)
    type_: Mapped[enum.Enum] = mapped_column(
        Enum(Question_type), 
        default=Question_type.smile, 
        nullable=False,
        server_default=Question_type.smile.name
    )
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"))
    
    store: Mapped["Stores"] = relationship(back_populates="questions")
    reviews: Mapped[List["Reviews"]] = relationship(back_populates="questions")
    staffs: Mapped[List["Staffs"]] = relationship(back_populates="questions")
    review_sugg: Mapped[List["ReviewSugg"]] = relationship(back_populates="questions")

    def __repr__(self):
        return f"<Questions(id={self.id}, question='{self.question}')>"


class Staffs(db.Model):
    __tablename__ = "staffs" 

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id'), nullable=False)

    questions: Mapped["Questions"] = relationship(back_populates="staffs")


class Reviews(db.Model):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    review: Mapped[str] = mapped_column(String, nullable=False)
    type_: Mapped[enum.Enum] = mapped_column(
        Enum(ReviewType), 
        nullable=False
    )
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))

    questions: Mapped["Questions"] = relationship(back_populates="reviews")

    def __repr__(self):
        return f"<Reviews(id={self.id})>"    


class ReviewSugg(db.Model):
    __tablename__ = "review_sugg"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sugg_count: Mapped[int] = mapped_column(Integer, nullable=False)
    type_: Mapped[enum.Enum] = mapped_column(
        Enum(ReviewType), 
        nullable=False
    )
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"))
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    # review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id"))

    store: Mapped["Stores"] = relationship(back_populates="review_sugg")
    questions: Mapped["Questions"] = relationship(back_populates="review_sugg")

    def __repr__(self):
        return f"<ReviewSugg(id={self.id}, store_name='{self.store.store_name}')>"


@app.shell_context_processor
def make_shell_context():
    return dict(db=db)
 
resource_path = Path(__file__).absolute().parent / 'resources'


@app.route('/')
def index():
    return redirect(url_for("stores", store_name="ManMandir"))


@app.route('/<store_name>', methods=['GET', "POST"])
def stores(store_name):
    if request.method == "POST":
        generated_review = []
        print("request.form :-> ", request.json)
        form_data = request.json
        for i in form_data:
            try:
                print(i)
                question = db.session.query(Questions).filter(Questions.id == int(i)).first()
                print("question : ", question)
                if question.type_ == Question_type.staff_star:
                    staff_info = db.session.query(Staffs).filter(Staffs.id == int(form_data[i+"-staff"]) ).first()
                    star_review = f"{staff_info.name} - {form_data[i]}"
                    generated_review.append(star_review)
                    continue
                if question.type_ == Question_type.smile:
                    rev_lists = db.session.query(Reviews).filter(Reviews.question_id == question.id).filter(Reviews.type_ ==  ReviewType(form_data[i]) ).all()
                    review_count = len(rev_lists)
                    rev_sugg = db.session.query(ReviewSugg).filter(ReviewSugg.question_id == question.id).filter(ReviewSugg.type_ == ReviewType(form_data[i])).first()
                    if rev_sugg:
                        txt_review_tmp = rev_lists[rev_sugg.sugg_count%review_count].review
                        generated_review.append(txt_review_tmp)
                        rev_sugg.sugg_count = rev_sugg.sugg_count + 1
                        db.session.commit()
                    else:
                        db.session.add(
                            ReviewSugg(sugg_count=1, type_= ReviewType(form_data[i]), store_id=question.store.id, question_id=question.id)
                        )
                        db.session.commit()
                        txt_review_tmp = rev_lists[0].review
                        generated_review.append(txt_review_tmp)
            except Exception as e:
                print("Exception :- ", e)
        return ".\n".join(generated_review)
    else:       # Get and other methods
        print("store_name : ", store_name)
        is_store =  db.session.query(Stores).filter(Stores.store_name == store_name).first()
        print("questions : ", is_store.questions)
        return render_template('index.html', questions=is_store.questions, store=is_store)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5015)
