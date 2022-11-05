import urllib.request
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import string 
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import pandas

url = 'https://www.gutenberg.org/cache/epub/1232/pg1232.txt'

def get_text(url):
    """
    This function pulls data from the project Gutenberg API. This function pulls "Prince" text by Machiavelli
    Then the text is processed through utf-8 in order to make it processable through Python
    Finally text.replace is used so that every time there is enter pressed in the text, making it go to the next
    Line, this just makes the file one string  
    """
    with urllib.request.urlopen(url) as f:
        response = urllib.request.urlopen(url)
        data = response.read()
        text = data.decode('utf-8')
    return text.replace('\n', '') #every time press enter in word document, one string 

x = get_text(url)

def clean_text(text):
    """
    This converts all punctuation into an empty space
    This source was used for support: https://stackoverflow.com/questions/34293875/how-to-remove-punctuation-marks-from-a-string-in-python-3-x-using-translate
    """
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

yy = x.replace('/r', ' ')
y = clean_text(x)
y = y.replace('\r', ' ')

def word_frequency_with_stopwords(text):
    """
    This function returns a dictionary which finds the frequency of words in the book
    This function returns the key as the word and the value as the number of times the word was used
    """
    d = {}
    for word in text.split(' '):
        word = word.lower()
        d[word] = d.get(word, 0) + 1
    return d

e = word_frequency_with_stopwords(y)

def total_words(text):
    """
    This function takes all words into consideration, including stopwords, and returns the number of words
    There are in the entire text. This also takes into account header, chapter titles
    """
    total = 0 
    for freq in e.values():
        total += freq
    return total

def word_frequency(text):
    """
    This function returns a dictionary which finds the frequency of words in the book
    This function returns the key as the word and the value as the number of times the word was used
    """
    d = {}
    d_stopwords = {}
    with open('data/stopwords.txt', 'r') as f:
        stopwords = f.read().splitlines() # I asked Benji for help for the stopwords section
    for word in text.split(' '):
        word = word.lower()
        d[word] = d.get(word, 0) + 1
    for word, frequency in d.items():
        if word not in stopwords and word.isalnum():
            d_stopwords[word] = frequency
    return d_stopwords

d = word_frequency(y)

def unique_words():
    """
    This function returns the number of unique words in the entire book
    This is achieved through counting the number of keys from the dictionary from the last functio
    Number of keys in the previous dictionary 
    """
    new_variable = word_frequency(y) 
    return len(new_variable)

def word_frequency_hist():
    """
    This function displays a histogram function which shows the top 10 most used words in the text
    These values are gotten from the dictionary made in the word frequency function
    I used help from online for this from the below link
    https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value

    """
    sorted_frequency = (dict(sorted(d.items(), key=lambda item: item[1],reverse=True)))
    keys = []
    values = []
    for i in list(sorted_frequency.values())[:10]:
        values.append(i)
    z = list(sorted_frequency.keys())
    for i in z[:10]:
        keys.append(i)
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(keys,values)
    plt.show()
    for i, z in zip(keys, values):
        print(i, z)


"""
Below represents the different sections of the book 
Intro through the man and his works is a biography about Machiavelli, not written by Machiavelli
The dedication and machiavelli writing are both written by Niccolo Machiavelli
"""
intro = y[3436:4532]
youth = y[4561:6760]
office = y[6793:12527]
literature_and_death = y[12569:18115]
the_man_and_his_works = y[18140:23886]
dedication = y[25452:27930]
machiavelli_writing = y[28040:276920]

def sentiment_analysis(x):
    """
    This function takes the different sections of the text and performs a sentiment analysis
    The following source was used for help
    https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_features.html
    """
    score = SentimentIntensityAnalyzer().polarity_scores(x)
    print(score)

def sentiment_analysis_graph(x):
    """
    This function uses the sentiment analysis scores and makes a pie chart out of them
    This allows us to visualise the sentiment for the different sections input in the function
    The following source was used for help: https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_features.html
    By inputing the name of the different sections selected above, this function will return a polarity score
    """
    score = SentimentIntensityAnalyzer().polarity_scores(x)
    del score['compound']
    labels = score.keys()
    sizes = score.values()
    explode = (0, 0, 0.1)
    fig1, ax1 = plt.subplots() 
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    plt.show()

# def main():
    # d = word_frequency(y)
    # print(d)

    # print("Total number of words in the book:", total_words(y))
    # print(y)

    # print("Total number of unique words in the entire book is", unique_words())

    # word_frequency_hist() 

    # sentiment_analysis_all = sentiment_analysis(intro), sentiment_analysis(youth), sentiment_analysis(office), sentiment_analysis(literature_and_death), sentiment_analysis(the_man_and_his_works), sentiment_analysis(dedication), sentiment_analysis(machiavelli_writing)

#     sentiment_analysis_graph(machiavelli_writing)
# if __name__ == '__main__':
#     main()