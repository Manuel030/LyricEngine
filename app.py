from flask import Flask, render_template, request, jsonify
import random
import tensorflow as tf
import psycopg2
from datetime import datetime
from logging import FileHandler, WARNING
import vocabulary
import model

app = Flask(__name__)

# enable logging
file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)
app.logger.addHandler(file_handler)


@app.route('/')
def mainpage():
    return render_template("mainpage.html")


@app.route('/pyjstalk', methods=['GET', 'POST'])
def pyjstalk():
    # POST request
    if request.method == 'POST':
        print('Incoming')
        print(request.get_json()['artist'])
        artist = request.get_json()['artist']
        artist = artist.lower().split()
        artist = '_'.join(artist)

        rnn = model.build_model(len(vocabulary.vocab), 100, 512, batch_size=1)  # play with rnn units

        checkpoint_dir = 'data/{}/training_checkpoints'.format(artist)
        rnn.load_weights(tf.train.latest_checkpoint(checkpoint_dir))

        rnn.build(tf.TensorShape([1, None]))

        # generate text by choosing random start_string
        chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u']
        s = random.sample(chars, 1)[0]
        verse_one = model.generate_text(rnn, s, 300, 0.2)
        s = random.sample(chars, 1)[0]
        chorus = model.generate_text(rnn, s, 180, 0.2)
        s = random.sample(chars, 1)[0]
        verse_two = model.generate_text(rnn, s, 300, 0.2)

        text = {'verse_one': verse_one, 'chorus': chorus, 'verse_two': verse_two}
        text = jsonify(text)

        return text, 200
    # GET request
    else:
        message = {'greeting': 'hello from FLASK'}
        return jsonify(message)


@app.route('/lyrics', methods=['GET', 'POST'])
def lyrics():
    return render_template("servelyrics.html")


@app.route('/request')
def request_artist():
    args = request.args
    artist = args['who']

    # connect to the db
    connect = psycopg2.connect(
        # host and port are at default value
        database="artistdb",
        user="postgres",
        host='localhost',
        port='5432',
        password="YOUR PASSWORD"
    )
    # establish cursor
    cur = connect.cursor()
    now = datetime.today().strftime('%Y-%m-%d')

    # insert request into db
    cur.execute('INSERT INTO artists (name, request_time) VALUES (%s, DATE %s)',
                (artist, now))  # do not put variables directly into query bc of sql injection

    # cur.execute('SELECT * FROM artists limit 1000;')
    # rows = cur.fetchall()
    # for r in rows:
    #    print(r)

    connect.commit()  # commit changes when inserting
    cur.close()
    connect.close()

    return render_template('request.html', artist=artist)


@app.route('/how_it_works')
def how_it_works():
    return render_template('howitworks.html')


if __name__ == '__main__':
    app.run()
