from datetime import datetime
import json, csv
from pathlib import Path
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


app = Flask(__name__)


class Base(DeclarativeBase): pass

# SQLAlchemy
db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

db.init_app(app)


class UserClicks(db.Model):
    __tablename__ = "user_clicks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_name: Mapped[str] = mapped_column(String, nullable=False)
    dt: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow(), nullable=False)

    def __repr__(self):
        return f"<UserClicks(id={self.id}, store_name='{self.store_name}')>"


@app.shell_context_processor
def make_shell_context():
    return dict(db=db)

resource_path = Path(__file__).absolute().parent / 'resources'


@app.route('/')
def index():
    return redirect(url_for("stores", store_name="ManMandir"))

@app.route('/<store_name>')
def stores(store_name):
    question_file:Path = resource_path / store_name / "question.json"
    render_question = []
    config = None
    if question_file.exists() and question_file.is_file():
        with open(question_file) as qf:     # Contains a list of question with question file location
            conf_questions = json.load(qf)
            questions = conf_questions.get("Questions")
            if questions:
                for que, que_file in questions:
                    good, neutral, bad = [], [], []
                    que_ans_file:Path = question_file.parent /  que_file
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
        # print("\n\n\n render_question : ", json.dumps(render_question, indent=3), "\n\n\n")
        db.session.add(UserClicks(store_name=store_name))
        db.session.commit()
        return render_template('index.html', questions=render_question, store_name=store_name, config=config)
    else:
        return "<h1>No Store Found!</h1>"



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5015)
