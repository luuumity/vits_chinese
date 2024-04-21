## 本项目用于微调测试
## 这次更改的逻辑是：

- bert_vits.json 中，"n_speakers" 共有几个设几个（默认是使用1个人的辅助训练数据，所以默认是2） ，"gin_channels" 保留为 256。
- log_interval 和 eval_interval 分别为 10 和 100。
- train.py中，L124行，加入加载预训练模型的代码：
```
utils.load_model("AISHELL3_G.pth", net_g)
utils.load_model("AISHELL3_D.pth", net_g)
```
- utils.py中，引用vits-fast-fine-tuning项目的方式，更改了load_checkpoint的代码。


## 材料准备：
### 下载预训练的vits模型（基于AISHELL多发言人训练）（放到项目目录下）
https://github.com/PlayVoice/vits_chinese/releases/v4.0

### 下载BERT韵律预测模型（文字->embedding）（放到bert/路径中）
https://github.com/PlayVoice/vits_chinese/releases/tag/v1.0

### AISHELL原训练数据下载
http://www.openslr.org/93/

### 项目环境搭建：（改过requirements.txt)
```
# 安装相关依赖：
pip install -r requirements.txt

# set up MAS对齐
cd monotonic_align
mkdir monotonic_align
python setup.py build_ext --inplace
ls monotonic_align
%cd ..
```

### 底模型推理测试
```
python vits_infer.py -c configs/bert_vits.json -m AISHELL3_G.pth -i 6
```
-i 为发音人序号，取值范围：0 ~ 173


## 微调前数据预处理：

### 0.自己的微调数据集放在 data/SJY/ 中
### 0.预处理前应先手动创建 vits_data/ 目录

### 1.重采样：
```
# --wav 要写角色的父文件夹，这是由代码决定的。
# waves-16k目录应该会自动创建。
python prep_resample.py --wav data/ --out vits_data/waves-16k
# 采样率检验（我自己的声音）：
file vits_data/waves-16k/SJY/SJY001.wav
```

### 2.拼音标注及格式规范化
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
```
- 拼音标注及格式规范化（labels.txt）
```
SJY001.wav 一帆风顺虽然令人羡慕，可是有的时候逆水行舟更让人钦佩。
	yi1 fan2 feng1 shun4 sui1 ran2 ling4 ren2 xian4 mu4 ke3 shi4 you3 de5 shi2 hou4 ni4 shui3 xing2 zhou1 geng4 rang4 ren2 qin1 pei4
SJY002.wav 我们必须与其他生物共同分享我们的地球。
	wo3 men5 bi4 xu1 yu3 qi2 ta1 sheng1 wu4 gong4 tong2 fen1 xiang3 wo3 men5 de5 di4 qiu2
SJY003.wav 落红不是无情物，化作春泥更护花。
	luo4 hong2 bu2 shi4 wu2 qing2 wu4 hua4 zuo4 chun1 ni2 geng4 hu4 hua1
```
### 3.使用bert预处理
- ⚠️注：默认前20条数据作为 valid 集，20条以后的作为 train 集。所以数据要够，或者改代码。
```
python prep_bert.py --conf configs/bert_vits.json --data vits_data/
```

- 打印信息，会过滤本项目不支持的**儿化音**

- 生成 vits_data/speakers.txt
```
AISHELL3数据集会生成这样的：
{'SSB0005': 0, 'SSB0009': 1, 'SSB0011': 2..., 'SSB1956': 173}
我的数据集会生成这样的：
❓这里是否有隐患？
请在 Colab 上跑跑看，这应该时macOS隐藏文件造成的，不应该出现！
{'.DS_Store': 0, 'SJY': 1}
```
- 生成 filelists
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
### 4.数据调试
```
python prep_debug.py
```

## 启动训练（输出默认都在logs/路径下）

```
# ❓train.py里明明好像有可视化代码，但colab上并没有唤起tensorboard，为什么？
python train.py -c configs/bert_vits.json -m bert_vits
```

