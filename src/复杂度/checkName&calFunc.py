import json
import os
import urllib.parse,urllib.request
from spellchecker import SpellChecker
import nltk
from nltk.corpus import wordnet
import re

def checkName(path):
    fp = open(path, encoding='utf8')
    count_unnormal=0
    count_func=1
    for line in fp.readlines():
        line = line.lstrip()
        line.replace('-',' ');line.replace('=',' ');line.replace('+',' ');line.replace('(',' ');line.replace(')',' ');line.replace('{',' ')
        line.replace('}',' ');line.replace('/',' ');line.replace('*',' ');line.replace('.',' ');line.replace(':',' ');line.replace('_',' ')
        words=line.split(' ')
        for word in words:
            if str.isalpha(word)and not wordnet.synsets(word):
                count_unnormal+=1
            if word=='def':
                count_func+=1
    return count_unnormal,count_func

def check_import(path,count_import):
    fp = open(path, encoding='utf8')
    for line in fp.readlines():
        line = line.lstrip()
        if line.startswith("import"):
            print()
            try:
                count_import[line[7:]]+=1
            except:
                count_import[line[7:]]=0
    return count_import

f=open('handled_data.json',encoding='gbk')
res=f.read()
data=json.loads(res)
data=list(dict.values(data))
print(data)

output_dict={}
count_import={}
for user in data:
    cases=user["cases"]
    print(cases)

    for case in cases:
         print(case["case_id"],case["case_type"])
         for record in case["upload_records"]:
                filename=urllib.parse.unquote(os.path.basename(record["code_url"]))

                if not record["cheat"]:
                    print(filename)
                    py_name="code_data\\user_"+str(user["user_id"])+"\\"+filename+"_unzip\\"+"main.py"
                    not_eng,count_func=checkName(py_name)
                    print(not_eng,count_func)
                    record["not_eng"]=not_eng
                    record["count_func"]=count_func
                else:
                    record["not_eng"] = -1
                    record["count_func"] = -1
                count_import=check_import("code_data\\user_"+str(user["user_id"])+"\\"+filename+"_unzip\\"+"main.py",count_import)

    output_dict[user["user_id"]]=user
json_out=json.dumps(output_dict,ensure_ascii=False,indent=2)
with open('handled_data.json', 'w') as f:
     f.write(json_out)
json_out=json.dumps(count_import,ensure_ascii=False,indent=2)
with open('count_import.json', 'w') as f:
     f.write(json_out)