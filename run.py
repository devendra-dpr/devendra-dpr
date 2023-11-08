from datetime import datetime
import csv, yaml
from pathlib import Path
from typing import List
from flask import Flask, render_template, redirect, url_for, jsonify
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
    staff_smile: str = "smile_rating"       # staff_smile_rating
    staff_star: str = "star_rating"         # staff_star_rating


class ReviewType(enum.Enum):
    good: str = "Good" 
    neutral: str = "Neutral" 
    bad: str = "Bad" 


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


@app.route('/<store_name>')
def stores(store_name):
    is_store =  db.session.query(Stores).filter(Stores.store_name == store_name).first()
    questions = is_store.questions
    print("questions : ", questions)
    return "None"
    # ======================================
    question_file:Path = resource_path / 'store' / store_name / "confQ.yml"
    render_question = []
    config = None
    if question_file.exists() and question_file.is_file():
        with open(question_file) as qf:     # Contains a list of question with question file location
            conf_questions = yaml.load(qf, yaml.Loader)
            questions = conf_questions.get("Questions")
            if questions:
                for que in questions:
                    good, neutral, bad = [], [], []
                    que_ans_file:Path = question_file.parent /  que.get("sugg_file")
                    if que_ans_file.exists() and que_ans_file.is_file():
                        with open(que_ans_file) as qaf: # opening ans if Question file 
                            csv_dictreader = csv.DictReader(qaf)
                            for i in csv_dictreader:
                                if i.get('good') and i.get('good').strip():
                                    good.append(i.get('good').strip())
                                if i.get('neutral') and i.get('neutral').strip():
                                    neutral.append(i.get('neutral').strip())
                                if i.get('bad') and i.get('bad').strip():
                                    bad.append(i.get('bad').strip()) 
                    render_question.append([que, {"good":good, "neutral":neutral, "bad":bad}])
            config = conf_questions.get("config")
        store_ = db.session.query(Stores).filter(Stores.store_name == store_name).first()
        count = db.session.query(func.count(UserClicks.id)).scalar() # all()[0][0]
        if count and count >= store_.max_clicks:
            return "<h1>You Trial Limit have been Completed.</h1>"
        store_.user_clicks.append(UserClicks())
        db.session.commit()
        return render_template('index.html', questions=render_question, store_name=store_name, config=config)
    else:
        return "<h1>No Store Found!</h1>"


@app.route('/<store_name>/question')
def store_question(store_name):
    question_file:Path = resource_path / 'store' / store_name / "confQ.yml"
    render_question = []
    if question_file.exists() and question_file.is_file():
        with open(question_file) as qf:     # Contains a list of question with question file location
            conf_questions = yaml.load(qf, yaml.Loader)
            questions = conf_questions.get("Questions")
            if questions:
                for que in questions:
                    good, neutral, bad = [], [], []
                    que_ans_file:Path = question_file.parent /  que.get("sugg_file")
                    if que_ans_file.exists() and que_ans_file.is_file():
                        with open(que_ans_file) as qaf: # opening ans if Question file 
                            csv_dictreader = csv.DictReader(qaf)
                            for i in csv_dictreader:
                                if i.get('good') and i.get('good').strip():
                                    good.append(i.get('good').strip())
                                if i.get('neutral') and i.get('neutral').strip():
                                    neutral.append(i.get('neutral').strip())
                                if i.get('bad') and i.get('bad').strip():
                                    bad.append(i.get('bad').strip()) 
                    render_question.append({
                        "question": que.get("question"), 
                        "sugg": {"good":good, "neutral":neutral, "bad":bad}, 
                        "question_type": que.get("question_type"),
                        "staffs": que.get("staffs")})
        return jsonify({"questions": render_question})
    else:
        return "No Store Found!"



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5015)
