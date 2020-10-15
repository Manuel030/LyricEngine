# LyricEngine

LyricEngine is a machine learning backed web app to generate unique song lyrics in the style of famous artists.
It runs on Flask, PostgreSQL and JavaScript. The Python client https://github.com/johnwmillr/LyricsGeniusfor the genius.com API is used to scrape all the textual data. 
LyricEngine is greatly inspired by @karpathy's char-rnn and his blog post about it. 
The language model is a recurrent neural network (RNN) built in TensorFlow with a straightforward 
architecture suited for language generation. Input characters are converted into vectors of 
size 100 to make the data ready for the subsequent multilayer long short-term memory (LSTM) 
recurrent network. Each layer has 100 hidden cells and each hidden cell has 512 hidden units. 
Between the LSTM layers and the final dense layer a dropout layer is used to mitigate overfitting issues.

Finally, LyricEngine generates text by initializing the RNN with a random start character and predicting the 
next characters where each predicted character is fed back into the model so that it has more context.