import tensorflow as tf
import vocabulary


def build_model(vocab_size, embedding_dim, rnn_units, batch_size):
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(vocab_size, embedding_dim,
                                  batch_input_shape=[batch_size, None]),
        tf.keras.layers.LSTM(rnn_units,
                            return_sequences=True,
                            stateful=True,
                            recurrent_initializer='glorot_uniform'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.LSTM(rnn_units,
                            return_sequences=True,
                            stateful=True,
                            recurrent_initializer='glorot_uniform'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(vocab_size)
    ])
    return model


def generate_text(model, start_string, num_generate, temperature):
    # Converting start string to numbers
    input_eval = [vocabulary.char2idx(s) for s in start_string]
    input_eval = tf.expand_dims(input_eval, 0)

    # Empty lists to store results
    word_generated = [start_string]
    sentence_generated = []
    text_generated = []

    # Low temperatures results in more predictable text.
    # Higher temperatures results in more surprising text.
    # Experiment to find the best setting.
    temperature = temperature

    # for that section to work, batch size needs to be == 1
    model.reset_states()
    for i in range(num_generate):
        predictions = model(input_eval)
        # remove the batch dimension
        predictions = tf.squeeze(predictions, 0)

        # using a categorical distribution to predict the character returned by the model
        predictions = predictions / temperature
        predicted_id = tf.random.categorical(predictions, num_samples=1)[-1, 0].numpy()

        # Pass the predicted character as the next input to the model
        # along with the previous hidden state
        input_eval = tf.expand_dims([predicted_id], 0)

        new_char = vocabulary.idx2char(predicted_id)
        word_generated.append(new_char)

        # when a whitespace is hit, start a new word
        if new_char == ' ':
            sentence_generated.append(''.join(word_generated))
            word_generated = []
        # when \n is hit, start a new line
        elif new_char == '\n':
            text_generated.append(''.join(sentence_generated))
            word_generated = []
            sentence_generated = []

    return text_generated

#rnn = build_model(len(vocabulary.vocab), 256, 1024, batch_size=1)
#print(rnn.summary())