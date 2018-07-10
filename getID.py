import sys
import datetime
import requests
import json
from my_scopus import MY_API_KEY

numOfData = 1000

def getID(keyword, year):
    #TITLE・ABS・KEYにキーワードを含む文献のSCOPUS_IDを200件取得
    #cf. https://dev.elsevier.com/documentation/ScopusSearchAPI.wadl
    url = ("http://api.elsevier.com/content/search/scopus?query=TITLE-ABS-KEY%28"
           +keyword+"%29&field=dc:identifier&date="+str(year)+"&count=200")
    resp = requests.get(url, headers={'Accept':'application/json',
                                      'X-ELS-APIKey': MY_API_KEY})
    return resp.json()

def main():
    argvs = sys.argv
    year = datetime.date.today().year
    idCount = 0
    no_ID_Years = 0

    #コマンドライン引数で与えたキーワードをURL形式に
    for i in range(len(argvs)):
        if i==1:
            keyword = str(argvs[i])
        elif i>1:
            keyword += "+AND+" + str(argvs[i])

    #IDを取得しテキスト形式で保存
    f = open("ID-List<"+keyword+">.txt", "w", encoding="UTF-8")

    while(idCount < numOfData):
        results = getID(keyword, year)

        #文献が1件も見つからない年が10年間続いた場合終了
        if results['search-results']["entry"] == [{'@_fa': 'true', 'error': 'Result set was empty'}]:
            no_ID_Years += 1
            if no_ID_Years == 10:
                print("---------- There is not enough paper!! -----------")
                break
            year -= 1
            continue
        else:
            no_ID_Year = 0

        #文献が見つかった場合IDを書き込む
        for r in results['search-results']["entry"]:
            f.write(str(r['dc:identifier'])+"\n")
            idCount += 1
            if idCount == numOfData:
                print("------------------ Complete!! -------------------")
                break

        year -= 1

    f.close()

if __name__ == "__main__":
    main()
