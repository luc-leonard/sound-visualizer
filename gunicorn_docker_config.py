workers = 1              # number of workers Gunicorn will spawn

bind = '0.0.0.0:80'  # this is where you declare on which address your
                         # gunicorn app is running.
                         # Basically where Nginx will forward the request to

daemon = False          # this is only to tell gunicorn to deamonize the server process
