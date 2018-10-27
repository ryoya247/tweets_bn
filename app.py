from flask import Flask, render_template, request
from janome.tokenizer import Tokenizer
from getTweets import get_tweets

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

    if request.method == 'POST':
        name = request.form['name']
    else:
        name = 'no name'

    timelines = get_tweets(name)

    if timelines:
        for line in timelines:
            text = line['text']
            if text.find('http') == -1:
                if text.find('\n'):
                    text = text.replace('\n','')
                malist = t.tokenize(text)
                for w in malist:
                    word = w.surface
                    ps = w.part_of_speech
                    if ps.find('名詞') < 0 or len(word) < 2 or word == "こと" or word == "これ" or word =="そう" or word =="さん" or word =="今日" or word =="昨日" or word =="明日" or word =="時間" or word =="やつ" or word.isdigit() or not word.isalpha(): continue
                    if not word in word_dic:
                        word_dic[word] = 0
                    word_dic[word] += 1
        keys = sorted(word_dic.items(), key=lambda x:x[1], reverse=True)
        for word,cnt in keys[:6]:
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
    app.run(debug=True)
