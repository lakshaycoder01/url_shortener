from pickle import load, dump
from flask_cors import CORS, cross_origin
from gevent.pywsgi import WSGIServer
from werkzeug.serving import run_with_reloader
from werkzeug.debug import DebuggedApplication
import logging
import random
import string
from flask import Flask, flash, render_template, redirect, request, url_for
import csv
import os

log_folder = os.path.basename('log')
app = Flask(__name__)
CORS(app)

app.config['log_folder'] = log_folder
app.secret_key = 'MAKE_THIS_VERY_HARD_TO_GUESS'


def write_csv(data):
    with open('urls.csv', 'a', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)


# index route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = str(request.form.get('url'))

        url_list = csv.reader(open('urls.csv'))
        Data = list(url_list)
        dataLen = len(Data)
        for i in range(dataLen):
            if url == Data[i][0]:
                shortened_url = 'http://zyla/%s' % Data[i][1]
                return render_template('shortened.html', url=shortened_url)

        letters = string.ascii_letters + string.digits  # a-Z + 0-9
        url_hash = ''.join(random.SystemRandom().choice(letters)
                           for n in range(7))

        row = [url, url_hash]
        write_csv(row)

        shortened_url = 'http://zyla/%s' % url_hash
        return render_template('shortened.html', url=shortened_url)

    else:

        return render_template('index.html')


def run_server():
    if(app.debug):
        application = DebuggedApplication(app)
    else:
        application = app
    logger = logging.getLogger()
    fh = logging.FileHandler(os.path.join(app.config['log_folder'], 'log.txt'))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    server = WSGIServer(('0.0.0.0', 8556), application, log=logger)
    print("Server Start")
    server.serve_forever()


if __name__ == '__main__':
    run_with_reloader(run_server)
