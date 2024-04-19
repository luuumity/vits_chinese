from pypinyin import pinyin, Style
import re

def convert_to_pinyin(text):
    # 用正则匹配去掉中文标点符号：
    # pattern = "[，。：；、！？“”「」《》]"
    # ｜区分两个方式。前者是匹配任意字符加.wav，后者是匹配大部分中文标点符号。
    # 注： A|B，A满足时不再尝试匹配B。
    pattern = ".+\.wav\s|[，。：；、！？“”「」《》]"
    filtered_text = re.sub(pattern,'',text)
    pinyin_line = pinyin(filtered_text, style=Style.TONE3, heteronym=False)
    # 修正，本项目中的“轻声”用的是5，而不是没有数字！
    # 也可以用正则表达式match做。
    for p in pinyin_line:
        if p[0].isalpha():  # 如果元素只包含字母
            p[0] += "5"  # 在元素后面添加数字5
    # TypeError: sequence item 0: expected str instance, list found
    # 原因是它认为join的这个列表里不是所有元素都是 string ！
    # 而本质原因是pinyin的返回值是双重列表，每个元素也是列表，而不是字符串（可能是为了应对多音字情况），所以用map将每个元素str()转换也不行，
    # 所以这个join()中才要这么写：
    pinyin_line = ' '.join(p[0] for p in pinyin_line)
    # 保留原文（给bert用），和对应拼音。
    out = text + '\n\t' + pinyin_line
    return out

def convert_file_to_pinyin(file_path):
    pinyin_text = []
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.readline()
        while text:
            pinyin_text.append(convert_to_pinyin(text.strip()))
            text = file.readline()
    return pinyin_text

# 读取中文文本文件，并将内容转换为拼音
file_path = 'input.txt'  # 替换为你的文件路径
pinyin_text = convert_file_to_pinyin(file_path)

# 将拼音输出到文件
output_file_path = './vits_data/labels.txt'  # 替换为你的输出文件路径
with open(output_file_path, 'w', encoding='utf-8') as file:
    for item in pinyin_text:
        file.write(item+'\n')

print("拼音已成功输出到文件。")