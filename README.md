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

