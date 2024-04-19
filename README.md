## 本项目用于微调测试
## 主要更改的逻辑是
```
bert_vits.json 中，"n_speakers" 改为 0 ，"gin_channels" 改为 0。
train.py中，L124行加入加载预训练模型的代码：
utils.load_model("AISHELL3_G.pth", net_g)
utils.load_model("AISHELL3_D.pth", net_g)
```

## AISHELL数据下载
http://www.openslr.org/93/

## 自己的微调数据集可以放在 data/ 中
## 预处理前应先手动创建 vits_data/ 目录

## 1.重采样：
```
# --wav 要写角色的父文件夹，这是由代码决定的。
# waves-16k目录应该会自动创建。
python prep_resample.py --wav data/ --out vits_data/waves-16k
# 采样率检验（我自己的声音）：
file vits_data/waves-16k/SJY/SJY001.wav
```

## 2.拼音标注及格式规范化
```
# 原始文本请放在input.txt，默认输出到vits_data/labels.txt。
python prep_pinyin.py
```

- 原始文本样式（input.txt）
⚠️注：原始文本请按照这个格式写： ”角色名(仅含字母)+数字+.wav  内容(可含标点符号)“
```
SJY001.wav 一帆风顺虽然令人羡慕，可是有的时候逆水行舟更让人钦佩。
SJY002.wav 我们必须与其他生物共同分享我们的地球。
SJY003.wav 落红不是无情物，化作春泥更护花。
SJY004.wav 所有的改变都是一种深思熟虑过后的奇迹。
```
- 拼音标注及格式规范化（labels.txt）
```
SJY001.wav 一帆风顺虽然令人羡慕，可是有的时候逆水行舟更让人钦佩。
	yi1 fan2 feng1 shun4 sui1 ran2 ling4 ren2 xian4 mu4 ke3 shi4 you3 de5 shi2 hou4 ni4 shui3 xing2 zhou1 geng4 rang4 ren2 qin1 pei4
SJY002.wav 我们必须与其他生物共同分享我们的地球。
	wo3 men5 bi4 xu1 yu3 qi2 ta1 sheng1 wu4 gong4 tong2 fen1 xiang3 wo3 men5 de5 di4 qiu2
SJY003.wav 落红不是无情物，化作春泥更护花。
	luo4 hong2 bu2 shi4 wu2 qing2 wu4 hua4 zuo4 chun1 ni2 geng4 hu4 hua1
SJY004.wav 所有的改变都是一种深思熟虑过后的奇迹。
	suo3 you3 de5 gai3 bian4 dou1 shi4 yi1 zhong3 shen1 si1 shu2 lv4 guo4 hou4 de5 qi2 ji4
```
## 3.使用bert预处理
```
# 默认是前20条数据作为 valid 集，20以后的作为 train 集，所以数据要够，或者改代码。
python prep_bert.py --conf configs/bert_vits.json --data vits_data/
```

打印信息，在过滤本项目不支持的**儿化音**

生成 vits_data/speakers.txt
```
AISHELL3数据集会生成这样的：
{'SSB0005': 0, 'SSB0009': 1, 'SSB0011': 2..., 'SSB1956': 173}
我的微调数据集会生成这样的：
{'.DS_Store': 0, 'SJY': 1}
```
生成 filelists
```
AISHELL3原数据集会生成这样的：
0|vits_data/waves-16k/SSB0005/SSB00050001.wav|vits_data/temps/SSB0005/SSB00050001.spec.pt|vits_data/berts/SSB0005/SSB00050001.npy|sil g uang3 zh ou1 n v3 d a4 x ve2 sh eng1 d eng1 sh an1 sh iii1 l ian2 s ii4 t ian1 j ing3 f ang1 zh ao3 d ao4 ^ i2 s ii4 n v3 sh iii1 sil
0|vits_data/waves-16k/SSB0005/SSB00050002.wav|vits_data/temps/SSB0005/SSB00050002.spec.pt|vits_data/berts/SSB0005/SSB00050002.npy|sil zh uen1 zh ong4 k e1 x ve2 g uei1 l v4 d e5 ^ iao1 q iou2 sil
0|vits_data/waves-16k/SSB0005/SSB00050004.wav|vits_data/temps/SSB0005/SSB00050004.spec.pt|vits_data/berts/SSB0005/SSB00050004.npy|sil h ei1 k e4 x van1 b u4 zh iii3 ^ iao4 b o1 d a2 m ou3 ^ i2 g e4 d ian4 h ua4 sil
我的数据集会生成这样的：
1|vits_data/waves-16k/SJY/SJY001.wav|vits_data/temps/SJY/SJY001.spec.pt|vits_data/berts/SJY/SJY001.wav.npy|sil ^ i1 f an2 f eng1 sh uen4 s uei1 r an2 l ing4 r en2 x ian4 m u4 sp k e3 sh iii4 ^ iou3 d e5 sh iii2 h ou4 n i4 sh uei3 x ing2 zh ou1 g eng4 r ang4 r en2 q in1 p ei4 sp sil
1|vits_data/waves-16k/SJY/SJY002.wav|vits_data/temps/SJY/SJY002.spec.pt|vits_data/berts/SJY/SJY002.wav.npy|sil ^ uo3 m en5 b i4 x v1 ^ v3 q i2 t a1 sh eng1 ^ u4 g ong4 t ong2 f en1 x iang3 ^ uo3 m en5 d e5 d i4 q iou2 sp sil
1|vits_data/waves-16k/SJY/SJY003.wav|vits_data/temps/SJY/SJY003.spec.pt|vits_data/berts/SJY/SJY003.wav.npy|sil l uo4 h ong2 b u2 sh iii4 ^ u2 q ing2 ^ u4 sp h ua4 z uo4 ch uen1 n i2 g eng4 h u4 h ua1 sp sil
```
## 数据调试
```
python prep_debug.py
```

## 启动训练

```
cd monotonic_align

python setup.py build_ext --inplace

cd -

python train.py -c configs/bert_vits.json -m bert_vits
```

## 下载权重
AISHELL3_G.pth：https://github.com/PlayVoice/vits_chinese/releases/v4.0

## 推理测试
```
python vits_infer.py -c configs/bert_vits.json -m AISHELL3_G.pth -i 6
```
-i 为发音人序号，取值范围：0 ~ 173

## 训练的AISHELL3模型，使用小米K2社区开源的AISHELL3模型来初始化训练权重，以节约训练时间
K2开源模型 https://huggingface.co/jackyqs/vits-aishell3-175-chinese/tree/main 下载模型

K2在线试用 https://huggingface.co/spaces/k2-fsa/text-to-speech
