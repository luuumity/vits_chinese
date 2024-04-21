# 由于重采样的时候小于3s的音频会被略过，所以需要将input.txt中对应的音频也删掉，所以要在colab上重采样后，执行这个代码：
import os
import re

folder_path = "./vits_data/waves-16k/SJY"

# 获取文件夹中所有文件的列表
file_list = os.listdir(folder_path)
# 需要按字母顺序排列一下，以免最后文本和音频对不上！
file_list = sorted(file_list)

print(f"重采样后共有{len(file_list)}条音频。")

# 重新整理文本，从原文本中选取与选用的辅助音频对应的文本
content = "./input.txt"
inputtxt = []
i = 0
L = len(file_list)
with open(content, 'r') as f:
    line = f.readline()
    while line and i < L:
        matches = re.match(r"(SJY[0-9]+.wav)(.*)", line)
        if matches:
            name = matches.group(1)
            # print(name)
            # print(file_list[i])
            if name == file_list[i]:
                inputtxt.append(line)
                i += 1
        else:
            print("正则匹配出现问题。")
        line = f.readline()

# 重写input文件
with open(content, 'w') as f:
    for item in inputtxt:
        f.write(item)  # 原句有换行符，所以不用换了。

print(f"现在input.txt中共有{len(inputtxt)}行。")