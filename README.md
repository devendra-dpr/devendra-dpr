A single static page to show the Menu of the store.

feature:
1. storing page refresh count.


# Run the app
```sh
nohup gunicorn -w 4 run:app -b 0.0.0.0:5015 &

nohup gunicorn -w 4 --certfile=/home/ecommerce/.cert/chat.cert.pem --keyfile=/home/ecommerce/.cert/chat.privkey.pem --bind 0.0.0.0:5015 run:app &

# Use sudo Command to run it
nohup gunicorn -w 4 --certfile=/etc/letsencrypt/live/review.whatifretalytics.com/cert.pem --keyfile=/etc/letsencrypt/live/review.whatifretalytics.com/privkey.pem --bind 0.0.0.0:5015 run:app &
```

## add new Store 
open the db file using `sqlite3 db.sqlite3`. Then run the below given command.

```sql
-- syntax
insert into stores values(ID, STORE_NAME, MAX_CLICK_COUNT);
-- eg.
insert into stores values(1, "ManMandir", 20);
```