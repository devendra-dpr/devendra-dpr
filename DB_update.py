
# flask shell

from run import *
from sqlalchemy import update

# ==================== Store
# -- Query 
# select * from stores where store_name = "xxx" limit 1;
db.session.query(Stores).filter_by(store_name = "xxx").first()

# -- Insert
# insert into stores(store_name, max_clicks, redirect_url, welcome_text) values ("xxx", 20, "yyyy", "zzzz");
st_in_txt = Stores(
        store_name = "xxx",
        max_clicks = 20,
        redirect_url = "https://g.page/r/XXXX-YYYYYZZZZZ/review",
        welcome_text = "welcome text"
    )
db.session.add(st_in_txt)
db.session.commit()
db.session.refresh(st_in_txt)

# -- Update 
# update stores set welcome_text="welcome to my store" where id=0;
st_up_txt = update(Stores).where(Stores.id == 1).values(
    max_clicks = 20
)
# or multiple values update
st_up_txt = update(Stores).where(Stores.id == 1).values(
    {
        Stores.max_clicks: 20,
        Stores.welcome_text: "welcome text"
    }
)
db.session.execute(st_up_txt)
db.session.commit()



# ==================== Questions

# -- Query 
# select * from Questions where store_id=1; 
ques_q_txt = db.session.query(Questions).filter_by(store_id = "1").first()


# add Questions
st_in_txt = db.session.query(Stores).filter_by(store_name = "ManMandir").first()

st_in_txt.questions.extend([
    Questions(
        question="", 
        type_=Question_type.smile, 
        reviews=[
            Reviews(review="", type_=ReviewType.good),

            Reviews(review="", type_=ReviewType.neutral),
            
            Reviews(review="", type_=ReviewType.bad),
        ],
        staffs=[
            Staffs(name=""),
        ]
    ),
    
])
db.session.commit()
