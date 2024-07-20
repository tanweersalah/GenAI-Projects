from tensorflow.keras.models import  load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.datasets import imdb
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pathlib
code_dir = pathlib.Path(__file__).parent.resolve()
print(code_dir)

start_char = 1
oov_char = 2
index_from = 3
vocab_size = 20000
max_len = 50

word_index = imdb.get_word_index()

index_word = {value+index_from:key for key,value in word_index.items()}
index_word[start_char] = "[START]"
index_word[oov_char] = "[OOV]"


ann_model = load_model(str(code_dir) +'/model/simple_ann_imdb.h5')
rnn_model = load_model(str(code_dir) + '/model/simple_rnn_imdb.h5')
lstm_model = load_model(str(code_dir) + '/model/simple_lstm_imdb.h5')




def preprocess_text(text):
    print(text)
    encoded_text = [min(word_index.get(word, vocab_size) + 3, vocab_size - 1) for word in text.lower().split(' ')]

    return pad_sequences([encoded_text], maxlen= max_len)

def predict_with_ann(review):
    
    prediction = ann_model.predict(review)
    sentiment = 'Positive' if prediction[0][0] > 0.5 else 'Negative'
    return sentiment,  prediction[0][0]

def predict_with_rnn(review):
    prediction = rnn_model.predict(review)
    sentiment = 'Positive' if prediction[0][0] > 0.5 else 'Negative'
    return sentiment,  prediction[0][0]

def predict_with_lstm(review):
    prediction = lstm_model.predict(review)
    sentiment = 'Positive' if prediction[0][0] > 0.5 else 'Negative'
    return sentiment,  prediction[0][0]






def convert_range(value):
    if value < 0 or value > 1:
        raise ValueError("Input value must be in the range [0, 1].")
    
    return value * 2 - 1

def create_bidirectional_bar(value):
    value = convert_range(value)
    fig, ax = plt.subplots(figsize=(12, 3))
    
    # Set the range and ticks
    ax.set_xlim(-1, 1)
    ax.set_xticks(np.arange(-1, 1.1, 0.25))
    
    # Remove y-axis
    ax.yaxis.set_visible(False)
    
    # Add vertical line at 0
    ax.axvline(x=0, color='#333333', linestyle='-', linewidth=1)
    
    # Create custom colormap
    colors = ['#FF0000', '#808080', '#00FF00']  # Red, Grey, Green
    n_bins = 100  # Number of color segments
    cmap = LinearSegmentedColormap.from_list("custom", colors, N=n_bins)
    
    # Create the gradient bar
    if value >= 0:
        gradient = np.linspace(0, value, int(n_bins * value))
        for i in range(len(gradient)-1):
            ax.barh(0, gradient[i+1]-gradient[i], left=gradient[i], height=0.6, 
                    align='center', color=cmap(0.5 + (i+0.5)/(len(gradient)*2)), alpha=0.8)
    else:
        gradient = np.linspace(value, 0, int(n_bins * abs(value)))
        for i in range(len(gradient)-1):
            ax.barh(0, gradient[i+1]-gradient[i], left=gradient[i], height=0.6, 
                    align='center', color=cmap(0.5 - (len(gradient)-i-0.5)/(len(gradient)*2)), alpha=0.8)
    
    # Add value label
    ax.text(value, 0, f'{value:.2f}', 
            verticalalignment='center',
            horizontalalignment='left' if value >= 0 else 'right',
            fontweight='bold', fontsize=12, color='#333333')
    
    # Customize the chart appearance
    ax.set_facecolor('#f0f2f6')
    fig.patch.set_facecolor('#f0f2f6')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#333333')
    ax.tick_params(axis='x', colors='#333333')
    
    plt.title('Sentiment Bar Chart', fontsize=16, fontweight='bold', color='#333333')
    plt.tight_layout()
    return fig

    


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

    
    # Create and display the chart
    fig_ann = create_bidirectional_bar(ann_prediction_score)
    st.pyplot(fig_ann)

    rnn_sentiment,  rnn_prediction_score = predict_with_rnn(review)
    st.write('\nRNN Result:')
    st.write('Sentiment : ', rnn_sentiment)

    # Create and display the chart
    fig_rnn = create_bidirectional_bar(rnn_prediction_score)
    st.pyplot(fig_rnn)

    rnn_sentiment,  rnn_prediction_score = predict_with_lstm(review)
    st.write('\LSTM Result:')
    st.write('Sentiment : ', rnn_sentiment)

    # Create and display the chart
    fig_rnn = create_bidirectional_bar(rnn_prediction_score)
    st.pyplot(fig_rnn)




