# 这个脚本用来复制 /filelists/train.txt 中的“真数据”部分，请上传到GitHub，并在colab预处理环节执行。
import os
import re
import random

real_data = []
auxiliary_data = []

# 使用./的话就无需绝对路径？
train_path = "./filelists/train.txt"

with open(train_path, 'r') as f:
    line = f.readline()
    while line:
        # 应该用search！因为在执行bert预处理之后的train.txt不再是以音频文件开头的了！应该用search。
        if re.search(r"SJY[0-9]+.wav", line):
            real_data.append(line)
        else:
            auxiliary_data.append(line)

        line = f.readline()

while len(real_data) <= len(auxiliary_data) :
    real_data += real_data

data = real_data + auxiliary_data
# 重新shuffle
random.shuffle(data)
with open(train_path, 'w') as f:
    for item in data:
        f.write(item)

print(f"现在train.txt中共有{len(data)}条记录。")

