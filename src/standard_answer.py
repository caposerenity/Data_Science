import json
import os
import subprocess
import time
import urllib.parse,urllib.request

import psutil

f=open('handled_data.json',encoding='gbk')
res=f.read()
data=json.loads(res)
data=list(dict.values(data))

problem_data={}
for user in data:
    cases=user["cases"]
    print(cases)

    for case in cases:
         print(case["case_id"],case["case_type"])


         for record in case["upload_records"]:
                filename=urllib.parse.unquote(os.path.basename(record["code_url"]))
                testcase_url = "code_data\\user_" + str(user["user_id"]) + "\\" + filename + "_unzip\\.mooctest\\" + "testCases.json"
                answer_url="code_data\\user_" + str(user["user_id"]) + "\\" + filename + "_unzip\\.mooctest\\" + "answer.py"
                problem_name=filename.split('_')[0]
                print(problem_name)
                if not problem_data.__contains__(problem_name):
                    problem_data[problem_name]={}
                    fcase = open(testcase_url, encoding='utf8')
                    t = fcase.read()
                    testcases = json.loads(t)
                    t_use=0
                    for testcase in testcases:
                        ins = testcase["input"]
                        outs = testcase["output"]
                        try:
                            time_start = time.time()
                            r = subprocess.Popen(["python", answer_url], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                            r.stdin.write(ins.encode('utf-8'))
                            print(str(psutil.Process(r.pid).memory_info().rss / (1024 * 1024)) + " MB")
                            r_out = bytes.decode(r.communicate()[0])
                            r_out = r_out.replace('\r\n', '\n')
                            if r_out == outs:
                                t_use += time.time() - time_start
                                print(t_use)
                                r.kill()
                            else:
                                problem_data[problem_name]['standard_time_use'] = -1
                                r.kill()
                                break
                        except Exception as e:
                            print(e)
                            problem_data[problem_name]['standard_time_use'] = -1
                            break
                    problem_data[problem_name]['standard_time_use'] = t_use

                else:
                    break
json_out=json.dumps(problem_data,ensure_ascii=False,indent=2)
with open('problem_data.json', 'w') as f:
     f.write(json_out)