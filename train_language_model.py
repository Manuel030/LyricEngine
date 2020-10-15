import tensorflow as tf
import numpy as np
import os
import vocabulary
import model

# CHOSE ARTISTS FOR WHICH TO BUILD A LANGUAGE MODEL
artists = ['pink_floyd', 'red_hot_chili_peppers', 'journey', 'oasis',
           'supertramp', 'the_beatles', 'wu_tang_clan']


# getting the data
def read_text(filepath):
    with open(filepath, mode="r", newline='\n', encoding='utf-8') as lyrics:
        text = [line.lower().strip() + '\n' for line in lyrics if
                line[0] != '[']  # ignore \n, \r and lines with [verse], [refrain] etc. gathered from genius.com
        lyrics.close()

    # list of sentences into one long string
    text_flat = ''
    for sentence in text:
        text_flat += ' ' + sentence
    return text_flat


# prepare data for ML algo
def text_to_int(text):
    l = []
    for char in text:
        try:
            l.append(vocabulary.char2idx(char))
        # handle characters that shouldn't be processed (are not part of vocabulary)
        except KeyError:
            pass
    return np.array(l)


# get X and y
def split_input_target(chunk):
    input_text = chunk[:-1]
    target_text = chunk[1:]
    return input_text, target_text


for artist in artists:
    artistpath = "data/{}/{}_lyrics.txt".format(artist, artist)
    text_flat = read_text(artistpath)
    # pretraining of model is done with following reddits dumps for 200 epochs
    # text_flat = read_text('data/hacker_news.txt') + read_text('data/reddit_apple_android.txt') \
    #            + read_text('data/reddit_rarepuppers_politics.txt') + read_text('data/reddit_relationshipadvice_legaladvice.txt')

    # length of text is the number of characters in it
    print('Length of text: {} characters'.format(len(text_flat)))

    text_as_int = text_to_int(text_flat)

    # Model input size in characters
    SEQ_LENGTH = 100
    examples_per_epoch = len(text_flat) // (SEQ_LENGTH + 1)

    # Create training examples and targets
    char_dataset = tf.data.Dataset.from_tensor_slices(text_as_int)
    sequences = char_dataset.batch(SEQ_LENGTH + 1, drop_remainder=True)

    dataset = sequences.map(split_input_target)

    # Create training batches
    BATCH_SIZE = 64

    # Buffer size to shuffle the dataset
    # (TF data is designed to work with possibly infinite sequences,
    # so it doesn't attempt to shuffle the entire sequence in memory. Instead,
    # it maintains a buffer in which it shuffles elements).
    BUFFER_SIZE = 10000

    dataset = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)

    # Build the model
    # Length of the vocabulary in chars
    vocab_size = len(vocabulary.vocab)

    # The embedding dimension
    embedding_dim = 100

    # Number of RNN units
    rnn_units = 512

    rnn = model.build_model(
        vocab_size=len(vocabulary.vocab),
        embedding_dim=embedding_dim,
        rnn_units=rnn_units,
        batch_size=BATCH_SIZE)

    checkpoint_dir = 'data/pretrained_weights/training_checkpoints'
    rnn.load_weights(tf.train.latest_checkpoint(checkpoint_dir))


    def loss(labels, logits):
        return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)


    rnn.compile(optimizer='adam', loss=loss)

    # Directory where the checkpoints will be saved
    checkpoint_dir = 'data/{}/training_checkpoints'.format(artist)
    # Name of the checkpoint files
    checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}")

    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_prefix,
        save_weights_only=True)

    EPOCHS = 50
    history = rnn.fit(dataset, epochs=EPOCHS, callbacks=[checkpoint_callback])
