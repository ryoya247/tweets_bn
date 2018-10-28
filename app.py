from flask import Flask, render_template, request
from janome.tokenizer import Tokenizer
from getTweets import get_tweets
import pprint, math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def show_result():
    all_words_count = 0
    word_dic = {}
    tfidf_word_dic = {}
    result_dic = {}
    all_tweets_list = []
    tweets = []
    labels = []
    values = []
    timelines = []
    colors = ["#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA","#ABCDEF", "#DDDDDD"]

    t = Tokenizer()

    if request.method == 'POST':
        name = request.form['name']
        timelines = get_tweets(name)
    else:
        name = 'no name'
        return render_template('no-result.html', title="no-result", name=name)

    if timelines:
        for line in timelines:
            # tweet一つ一つ
            text = line['text']
            if text.find('http') == -1:
                if text.find('\n'):
                    text = text.replace('\n','')
                all_tweets_list.append(text)

                malist = t.tokenize(text)

                for w in malist:
                    word = w.surface
                    ps = w.part_of_speech
                    hinsi = ps.split(',')[0]
                    if hinsi != '形容詞':
                        continue

                    if not word in word_dic:
                        word_dic[word] = 1
                    word_dic[word] += 1
        all_words_count = sum(word_dic.values())

        # tf値の算出
        for wd,cnt in word_dic.items():
            tf = int(cnt) / all_words_count
            tfidf_word_dic[wd] = [tf]

        # idf値の算出
        for wd in word_dic.keys():
            df = 0
            for tweet in all_tweets_list:
                if tweet.find(wd) > -1:
                    df += 1
            tfidf_word_dic[wd].append(math.log(len(all_tweets_list) / df) + 1)

        # tf-idf値の算出
        for wd, ary in tfidf_word_dic.items():
            result_dic[wd] = ary[0] * ary[1]

        keys = sorted(result_dic.items(), key=lambda x:x[1], reverse=True)

        pprint.pprint(keys)
        print('all_words_count',all_words_count)
        print('all_tweets_num',len(all_tweets_list))

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
