
from run import *

st_in_txt = Stores(
        store_name = "xxx",
        max_clicks = 20,
        redirect_url = "https://g.page/r/XXXX-YYYYYZZZZZ/review",
        welcome_text = "welcome text"
    )
db.session.add(st_in_txt)
db.session.commit()
db.session.refresh(st_in_txt)

st_in_txt.questions.extend([
    Questions(
        question="How is our Clothes Pricing?", 
        type_=Question_type.smile, 
        reviews=[
            Reviews(review="Discover sarees with good pricing that offer both value and style.", type_=ReviewType.good),
            Reviews(review="Sarees that redefine value for money.", type_=ReviewType.good),
            Reviews(review="Affordable sarees for every budget.", type_=ReviewType.good),
            Reviews(review="Quality sarees at prices you'll love", type_=ReviewType.good),
            Reviews(review="Trendy sarees for everyone's financial range.", type_=ReviewType.good),
            Reviews(review="Budget-friendly sarees that doesn't compromise on style.", type_=ReviewType.good),
            Reviews(review="Shopping sarees without straining your budget.", type_=ReviewType.good),
            Reviews(review="Experience the delight of shopping for sarees with good pricing", type_=ReviewType.good),
            Reviews(review="Traditonal saree options that provide to all budgets.", type_=ReviewType.good),
            Reviews(review="Saree's that's are  accessible to all budgets.", type_=ReviewType.good),

            Reviews(review="The price of the saree was mediocre.", type_=ReviewType.neutral),
            Reviews(review="It didn't quite meet our budget expectations, but it was middle-of-the-road in terms of pricing.", type_=ReviewType.neutral),
            Reviews(review="It fell short of affordability, yet it was reasonably priced.", type_=ReviewType.neutral),
            Reviews(review="It was not a bargain, but it was not overpriced either.", type_=ReviewType.neutral),
            Reviews(review="The pricing wasn't remarkable, but it was in line with similar sarees", type_=ReviewType.neutral),
            Reviews(review="While not cheap, it was still within the middle range of pricing", type_=ReviewType.neutral),
            Reviews(review="It didn't come at a discount, but it was still reasonably priced.", type_=ReviewType.neutral),
            Reviews(review="While it wasn't a budget-friendly option, it was still within the average price range.", type_=ReviewType.neutral),
            Reviews(review="It was just averagely priced.", type_=ReviewType.neutral),
            Reviews(review="It didn't have a particularly low price, but it wasn't exorbitant either.", type_=ReviewType.neutral),
            Reviews(review="The saree's cost was unremarkable, though it was fair.", type_=ReviewType.neutral),
            Reviews(review="It didn't offer significant cost savings, but it was still within the average range.", type_=ReviewType.neutral),
            Reviews(review="The pricing wasn't impressive, but it wasn't overly high either.", type_=ReviewType.neutral),
            Reviews(review="It didn't offer substantial discounts, but it was fairly priced.", type_=ReviewType.neutral),
            Reviews(review="It didn't have a particularly low cost, but it wasn't excessively high either.", type_=ReviewType.neutral),
            Reviews(review="The saree's pricing didn't dazzle us, but it was still within the average spectrum.", type_=ReviewType.neutral),
            
            Reviews(review="Beautiful sarees, but with a over price tag", type_=ReviewType.bad),
            Reviews(review="Quality and style, but at a premium price point.", type_=ReviewType.bad),
            Reviews(review="Steer clear of sarees with bad pricing that offer no value for your money.", type_=ReviewType.bad),
            Reviews(review="Excessive pricing for the saree", type_=ReviewType.bad),
            Reviews(review="Quality comes at a cost in our saree shop.", type_=ReviewType.bad),
            Reviews(review="Luxury meets high pricing in there saree collection", type_=ReviewType.bad),
            Reviews(review="Choose sarees that offer reasonable pricing without sacrificing quality.", type_=ReviewType.bad),
            Reviews(review="Avoid the disappointment of overpaying for sarees with bad pricing", type_=ReviewType.bad),
            Reviews(review=" bad pricing that compromise on style and durability.", type_=ReviewType.bad),
            Reviews(review="The sarees are stunning, but they come with a hefty price tag.", type_=ReviewType.bad),
            Reviews(review="These sarees are gorgeous, but they are quite expensive.", type_=ReviewType.bad),
            Reviews(review="Beautiful sarees, but they are overpriced.", type_=ReviewType.bad),
            Reviews(review="sarees are lovely, but they are a bit too pricey.", type_=ReviewType.bad),
            Reviews(review="sarees are elegant, but they are on the expensive side.", type_=ReviewType.bad),
            Reviews(review="Beautiful sarees, but they have a high price tag", type_=ReviewType.bad),
            Reviews(review="they are not budget-friendly.", type_=ReviewType.bad),
            Reviews(review="Beautiful sarees, but they are costly.", type_=ReviewType.bad),
            Reviews(review="These sarees are appealing, but they are over the top in terms of pricing.", type_=ReviewType.bad),
            Reviews(review="sarees are lovely, has they come with a premium cost.", type_=ReviewType.bad),
        ],
    ),
    Questions(
        question="How is our Staff Behaviour?", 
        type_=Question_type.staff_star, 
        staffs=[
            Staffs(name="Mohan"),
            Staffs(name="Sohan"),
            Staffs(name="Rohan"),
        ]
    ),

])

db.session.commit()
