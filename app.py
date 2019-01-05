from flask import Flask, render_template, request
from janome.tokenizer import Tokenizer
from gensim.models import word2vec
from getTweets import get_tweets
from getStopWord import create_stopwords
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

    r = []
    results = []

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
            # tweet一つ一つ
            text = line['text']

            # httpが含まれてないtweetを対象とする
            if not 'http' in text:
                # 文を平たくする
                if text.find('\n'):
                    text = text.replace('\n','')
                # idf値算出用に対象tweetを配列に格納する
                all_tweets_list.append(text)

                # janomeで形態素解析
                tokens = t.tokenize(text)
                r = []
                for token in tokens:
                    # 単語の基本形を採用する
                    if token.base_form == '*':
                        w = token.surface
                    else:
                        w = token.base_form
                    ps = token.part_of_speech
                    hinsi = ps.split(',')[0]
                    if hinsi in ['名詞', '動詞', '形容詞']:
                        if not w in stop_words:
                            r.append(w)

                    # 名詞以外は弾く
                    if hinsi != '名詞' or w in stop_words or len(w) == 1:
                        continue

                    # 単語辞書になかったら追加
                    if not w in word_dic:
                        word_dic[w] = 1
                    word_dic[w] += 1
                rl = (' '.join(r)).strip()
                results.append(rl)
                print(rl)

        # wakati_file = 'tweet_wakati.txt'
        # with open(wakati_file, 'w', encoding='utf-8') as fp:
        #     fp.write('\n'.join(results))
        #
        # data = word2vec.LineSentence(wakati_file)
        # model = word2vec.Word2Vec(data, size = 200, window = 10, hs = 1, min_count = 2, sg = 1)
        # model.save('tweet.model')

        # # 全単語（名詞）の出現回数の合計
        # all_words_count = sum(word_dic.values())
        #
        # # tf値の算出
        # for wd,cnt in word_dic.items():
        #     tf = int(cnt) / all_words_count
        #     tfidf_word_dic[wd] = [tf]
        #
        # # idf値の算出
        # for wd in word_dic.keys():
        #     df = 0
        #     for tweet in all_tweets_list:
        #         if tweet.find(wd) > -1:
        #             df += 1
        #     tfidf_word_dic[wd].append(math.log(1 / df) + 1)
        #
        # # tf-idf値の算出
        # for wd, ary in tfidf_word_dic.items():
        #     result_dic[wd] = ary[0] * ary[1]
        #
        # pprint.pprint(result_dic)
        #
        keys = sorted(word_dic.items(), key=lambda x:x[1], reverse=True)
        #
        # print('all_words_count',all_words_count)
        # print('all_tweets_num',len(all_tweets_list))

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
