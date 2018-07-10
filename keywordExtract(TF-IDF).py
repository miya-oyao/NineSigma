import sys
from pprint import pprint
from gensim import corpora, models
from operator import itemgetter

def make_absList(inputfile):
    #入力されたテキストファイルを1行ごとのリストに変換
    absList = []

    item = inputfile.readline()
    while(item):
        if(item == "############ Abstract is not registered ############\n"):
            item = inputfile.readline()
            continue
        if(item[-1:]=="\n"):
            item = item[:-1]
        absList.append(item)
        item = inputfile.readline()

    return absList

def make_wordsList(inputlist):
    #渡されたリストの各要素をスペースで区切って単語に分割
    wordsList = []
    for i in range(len(inputlist)):
        wordsList.append(inputlist[i].split(" "))

    return wordsList

def calc_TFIDF(inputlist):
    tfidfList = []
    global dictionary
    global IDF

    dictionary = corpora.Dictionary(inputlist)
    corpus = [dictionary.doc2bow(text) for text in inputlist]
    model = models.TfidfModel(corpus, normalize=True) #ユークリッドノルムによる正規化
    corpus_tfidf = model[corpus]

    for text in corpus_tfidf:
        tfidfList.append(text)

    return tfidfList

def sort_by_TFIDF(inputlist):
    #TF-IDFの高い順に各テキスト内の単語をソート
    sortedList = []
    for text in inputlist:
        sortedText = sorted(text, key=itemgetter(1), reverse=True)
        sortedList.append(sortedText)

    return sortedList

def keyword_extract(inputlist):
    # id -> 単語表示 に変更
    texts_tfidf = []
    for text in inputlist:
        text_tfidf = []
        for word in text:
            text_tfidf.append([dictionary[word[0]],word[1]])
        texts_tfidf.append(text_tfidf)

    #テキストごとに上位５件を抽出
    keywordsList = []
    for text in texts_tfidf:
        keywords = []
        count = 0
        for word in text:
            if(count >= 5):
                break
            keywords.append(word)
            count += 1
        keywordsList.append(keywords)

    pprint(keywordsList)


def main():
    argvs = sys.argv
    if len(argvs) == 1:
        print("---------------- No input file!! ----------------")
        exit()
    elif len(argvs) > 2:
        print("-------- Only one file can be accepted!! --------")
        exit()

    f_abs = open(argvs[1], "r", encoding="UTF-8")

    absList = make_absList(f_abs)
    wordsList = make_wordsList(absList)

    tfidfList = calc_TFIDF(wordsList)
    sortedList = sort_by_TFIDF(tfidfList)
    keyword_extract(sortedList)
    print("------------------- Complete!! ------------------")

if __name__ == "__main__":
    main()
