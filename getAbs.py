import sys
import requests
import json
import re
from my_scopus import MY_API_KEY

def getAbs(SCOPUS_ID):
    #受け取ったIDの論文から抄録を取得
    #cf. https://api.elsevier.com/documentation/AbstractRetrievalAPI.wadl
    url = ("https://api.elsevier.com/content/abstract/scopus_id/"
           + SCOPUS_ID + "?field=dc:description")
    resp = requests.get(url, headers={'Accept':'application/json',
                                      'X-ELS-APIKey': MY_API_KEY})
    return resp.json()['abstracts-retrieval-response']['coredata']

def removeCopyright(original):
    #コピーライト表記部分の除去処理
    #目視で確認(これ以外のパターンもあるかもしれない)
    ABS = original[(original.find("."))+1:]
    if ABS[0:1] == " ":
        ABS = ABS[1:]
    if ABS.startswith("V."):
        ABS = ABS[(ABS.find("."))+1:]
        if ABS[0:1] == " ":
            ABS = ABS[1:]
    if ABS.startswith("and"):
        ABS = ABS[(ABS.find("."))+1:]
        if ABS[0:1] == " ":
            ABS = ABS[1:]
    if re.match("[12]\d{3}", ABS) == 0:
        ABS = ABS[(ABS.find("."))+1:]
        if ABS[0:1] == " ":
            ABS = ABS[1:]
    if ABS.startswith("Ltd."):
        ABS = ABS[(ABS.find("."))+1:]
        if ABS[0:1] == " ":
            ABS = ABS[1:]
    if ABS.startswith("All rights reserved.") or ABS.startswith("All right reserved.") or\
       ABS.startswith("All Rights Reserved."):
        ABS = ABS[(ABS.find("."))+1:]
        if ABS[0:1] == " ":
            ABS = ABS[1:]

    return ABS

def main():
    argvs = sys.argv
    if len(argvs) == 1:
        print("---------------- No input file!! ----------------")
        exit()
    elif len(argvs) > 2:
        print("-------- Only one file can be accepted!! --------")
        exit()

    f_id = open(argvs[1], "r", encoding="UTF-8")

    keyword = argvs[1][(argvs[1].find("<")+1):argvs[1].find(">")]      #キーワード内に"<",">"が含まれるとうまくいかない…
    f_abs = open("Abs-List<"+keyword+">.txt", "w", encoding="UTF-8")

    #IDのリストから抄録のリストを作成しテキスト形式で保存
    progress = 0
    string = f_id.readline()
    while string:
        SCOPUS_ID = string[:string.find("\n")]
        result = getAbs(SCOPUS_ID)

        if result == None:
            f_abs.write("############ Abstract is not registered ############\n")
        else :
            original = str(result['dc:description'])
            if (original.startswith("©") or original.startswith("Copyright ©")
                or original.startswith("ï¿½") or original.startswith("Copyright ï¿½")
                or original.startswith("Â©") or original.startswith("�")):
                ABS = removeCopyright(original)
            else:
                ABS = original
            f_abs.write(ABS + "\n")

        progress += 1
        print(str(progress) + "/1000")
        string = f_id.readline()

    print("------------------- Complete!! ------------------")

    f_id.close()
    f_abs.close()

if __name__ == "__main__":
    main()
