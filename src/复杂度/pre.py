import json
import os
import urllib.parse, urllib.request
import zipfile


def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            L.append(os.path.join(root, file))
    return L


def unzip_file(zip_src, dst_dir):
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
    else:
        print('This is not zip')


def remove_file(path):
    if os.path.exists(path):  # 如果文件存在
        os.remove(path)
        print("解压完成,已删除" + path)


def checkCheat(path):
    fp = open(path, encoding="utf8")
    # try:
    #     line = fp.readline()
    # except Exception as e:
    #     print(e)
    cheat = False
    count_line = 0
    suspected = 0
    before_line = ""
    for line in fp.readlines():
        line = line.lstrip()
        if not (line.startswith("#") or len(line) <= 1):
            count_line += 1
        else:
            before_line = line
            continue
        if line.startswith("if") and suspected == 0:
            suspected = 1
        elif line.startswith("print") and (
                before_line.startswith("if") or before_line.startswith("print") or before_line.startswith(
            "elif") or before_line.startswith("else")):
            suspected += 1
        elif line.startswith("elif") and suspected >= 2:
            suspected += 1
        elif line.startswith("else") and suspected >= 2:
            suspected += 1
        elif (before_line.startswith("if") or before_line.startswith("elif") or before_line.startswith("else")) and (
        not line.startswith("print")):
            suspected -= 1
        before_line = line
        # try:
        #     line = fp.readline()
        # except Exception as e:
        #     print(e)
    if suspected >= 5 or (suspected >= 3 and count_line <= 5) or (suspected >= 4 and count_line <= 10):
        cheat = True
    return cheat, count_line


f = open('test_data.json', encoding='utf8')
res = f.read()
data = json.loads(res)
data = list(dict.values(data))
print(data)

output_dict = {}
for user in data:
    cases = user["cases"]
    print(cases)

    if not os.path.exists("code_data\\user_" + str(user["user_id"])):
        os.mkdir("code_data\\user_" + str(user["user_id"]))

    for case in cases:
        print(case["case_id"], case["case_type"])
        max_score = 0
        case["final_cheat"] = False
        for record in case["upload_records"]:
            filename = urllib.parse.unquote(os.path.basename(record["code_url"]))
            print(filename)
            if not os.path.exists("code_data\\user_" + str(user["user_id"]) + "\\" + filename + "_unzip\\"):

                try:
                    urllib.request.urlretrieve(record["code_url"],
                                               "code_data\\user_" + str(user["user_id"]) + "\\" + filename)
                except Exception as e:
                    print(e)

                try:
                    os.mkdir("code_data\\user_" + str(user["user_id"]) + "\\" + filename + "_unzip\\")

                    unzip_file("code_data\\user_" + str(user["user_id"]) + "\\" + filename,
                               "code_data\\user_" + str(user["user_id"]) + "\\" + filename + "_unzip\\")  # 外层解压
                    remove_file("code_data\\user_" + str(user["user_id"]) + "\\" + filename)  # 解压后删除压缩包

                    zip_name = file_name("code_data\\user_" + str(user["user_id"]) + "\\" + filename + "_unzip\\")[0]
                    unzip_file(zip_name,
                               "code_data\\user_" + str(user["user_id"]) + "\\" + filename + "_unzip\\")  # 内层解压
                    remove_file(zip_name)  # 解压后删除压缩包
                except Exception as e:
                    print(e)

            py_name = "code_data\\user_" + str(user["user_id"]) + "\\" + filename + "_unzip\\" + "main.py"
            cheat, count_line = checkCheat(py_name)
            if count_line <= 2 and record["score"] > 0:
                cheat = True
            print(cheat)
            print(count_line)
            if cheat:
                record["score"] = 0
                record["cheat"] = True
                case["final_cheat"] = True
            else:
                all_cheat = False
                record["cheat"] = False
            record["count_line"] = count_line
            max_score = max(max_score, record["score"])
        case["final_score"] = max_score

    output_dict[user["user_id"]] = user
json_out = json.dumps(output_dict, ensure_ascii=False, indent=2)
with open('handled_data.json', 'w') as f:
    f.write(json_out)
