import json
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from utils import *
import pathlib

code_dir = pathlib.Path(__file__).parent.resolve()

VOCAB_SIZE = 10000
OOV_TOKEN = '<OOV>'
MAX_LEN = 50
EMB_DIMENSION = 12

df = pd.DataFrame(columns= ['headline', 'is_sarcastic'])


row_list = []
with open(str(code_dir) + '/data/Sarcasm_Headlines_Dataset_v2.json', 'r') as file :
    for jsonText in file.readlines():
        row_list.append(json.loads(jsonText))

df = pd.DataFrame(row_list)

df.drop('article_link', axis=1 , inplace=True)

tokenizer = Tokenizer(num_words=VOCAB_SIZE, oov_token=OOV_TOKEN)

tokenizer.fit_on_texts(df['headline'])

model = load_model(str(code_dir) + '/model/sarcasm.h5')

def predict(text):
    sequence =  tokenizer.texts_to_sequences([text])
    print(text , sequence)
    padded =  pad_sequences(sequence, maxlen=MAX_LEN)
    prediction_score =  model.predict(padded)[0][0]
    return  prediction_score > 0.5 , prediction_score


# streamlit app
# streamlit ap
import streamlit as st

st.title('Sarcasm Detection ')
st.write('Enter text and predict the sentiment')
user_input = st.text_area('Text')

#I found this movie interesting, it was not boring


if st.button('Predict'):
    review = user_input.strip()
    
    is_sarcastic,  prediction_score = predict(review)
    st.write('Result:')
    st.write('Is Sarcastic : ', is_sarcastic)
    st.write('Sarcasm Score : ', prediction_score)

    # Create and display the chart
    fig_rnn = create_bidirectional_bar(prediction_score)
    st.pyplot(fig_rnn)
