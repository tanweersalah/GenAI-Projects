from tensorflow.keras.models import  load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.datasets import imdb

start_char = 1
oov_char = 2
index_from = 3
vocab_size = 10000
max_len = 50

word_index = imdb.get_word_index()

index_word = {value+index_from:key for key,value in word_index.items()}
index_word[start_char] = "[START]"
index_word[oov_char] = "[OOV]"


ann_model = load_model('simple_ann_imdb.h5')
rnn_model = load_model('simple_rnn_imdb.h5')

def preprocess_text(text):
    print(text)
    encoded_text = [word_index.get(word, 2)+3  for word in text.lower().split(' ')]
    return pad_sequences([encoded_text], maxlen= max_len)

def predict_with_ann(review):
    
    prediction = ann_model.predict(review)
    sentiment = 'Positive' if prediction[0][0] > 0.5 else 'Negative'
    return sentiment,  prediction[0][0]

def predict_with_rnn(review):
    prediction = rnn_model.predict(review)
    sentiment = 'Positive' if prediction[0][0] > 0.5 else 'Negative'
    return sentiment,  prediction[0][0]




# streamlit ap
import streamlit as st

st.title('IMDB sentiment analysis')
st.write('Enter movie review and predict the sentiment')
user_input = st.text_area('Movie review')

#I found this movie interesting, it was not boring


if st.button('Predict'):
    review = preprocess_text(user_input.strip())
    ann_sentiment,  ann_prediction_score = predict_with_ann(review)

    st.write('ANN Result:')
    st.write('Sentiment : ', ann_sentiment)
    st.write('Prediction score : ', ann_prediction_score)

    rnn_sentiment,  rnn_prediction_score = predict_with_rnn(review)

    st.write('\nRNN Result:')
    st.write('Sentiment : ', rnn_sentiment)
    st.write('Prediction score : ', rnn_prediction_score)

    
