from flask import Flask, render_template, request
from janome.tokenizer import Tokenizer
from getTweets import get_tweets
from getStopWord import create_stopwords

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def show_result():
    word_dic = {}
    tweets = []
    labels = []
    values = []
    timelines = []
    colors = ["#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA","#ABCDEF", "#DDDDDD"]

    t = Tokenizer()

    path = "stop_words.txt"
    stop_words = create_stopwords(path)

    if request.method == 'POST':
        name = request.form['name']
        timelines = get_tweets(name)
    else:
        name = 'no name'
        return render_template('no-result.html', title="no-result", name=name)

    if timelines:
        for line in timelines:
            text = line['text']

            if not 'http' in text:
                if text.find('\n'):
                    text = text.replace('\n','')
                tokens = t.tokenize(text)

                for token in tokens:
                    if token.base_form == '*':
                        w = token.surface
                    else:
                        w = token.base_form

                    ps = token.part_of_speech
                    hinsi = ps.split(',')[0]

                    if hinsi != '名詞' or w in stop_words or len(w) == 1:
                        continue

                    if not w in word_dic:
                        word_dic[w] = 1
                    word_dic[w] += 1

        results = sorted(word_dic.items(), key=lambda x:x[1], reverse=True)

        for word,cnt in results[:6]:
            labels.append(word)
            values.append(cnt)
            tweets.append('{0}({1})'.format(word,cnt))
    else:
        return render_template('no-result.html', title="no-result", name=name)
    if len(labels) < 6:
        return render_template('no-result.html', title="no-result", name=name)
    else:
        return render_template('result.html', title='result', name=name, tweets=tweets, labels=labels, values=values, colors=colors)


if __name__ == "__main__":
    app.run(debug=False)
