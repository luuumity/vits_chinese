## 本项目是基于BERT-VITS的音色克隆（微调）
### 本分支不需要auxiliary data，只需提供20条～40条5s音频数据，训练40min左右就可以得到不错的音色克隆效果。建议录音时放慢语速。

```
- bert_vits.json 中，"n_speakers" 改为 0 ，"gin_channels" 改为 0。
- log_interval和eval_interval默认的太大了，分别改为10和100。
- train.py中，L124行，加入了加载预训练模型的代码：
- utils.load_model("AISHELL3_G.pth", net_g)
- utils.load_model("AISHELL3_D.pth", net_g)
- 无法使用 Duration Predictor (dp) 进行训练或推理，因为AISHELL3底模型用的就是 Stochastic Duration Predictor (sdp)。
```

## 使用该笔记本在Colab上进行测试：[BERT_vits_without_auxiliary(new)](https://github.com/luuumity/vits_chinese/blob/bert_vits_aishell3/BERT_vits_without_auxiliary(new).ipynb)
## 生成的音频样例：[📎Attached Audios](https://valuable-odometer-38c.notion.site/Attached-Audios-ce736be5be6c46cc951b635d6d81c004?pvs=4)

</br>

## 一些注意事项：

### 一、关于数据预处理：

#### 0.自己的微调数据集放在 data/xxx/ 中（xxx为角色名，我这里是SJY）
#### 0.预处理前应先手动创建 vits_data/ 目录

#### 1.重采样：目的是重采样至16kHz。

#### 2.拼音标注及格式规范化

- 原始文本请放在input.txt，默认输出到vits_data/labels.txt。

- 原始文本样式（input.txt）： ”角色名(仅含字母) 数字 .wav  内容(可含标点符号)“
```
SJY001.wav 一帆风顺虽然令人羡慕，可是有的时候逆水行舟更让人钦佩。
SJY002.wav 我们必须与其他生物共同分享我们的地球。
```
- 拼音标注和规范化后的样式（labels.txt）
```
SJY001.wav 一帆风顺虽然令人羡慕，可是有的时候逆水行舟更让人钦佩。
	yi1 fan2 feng1 shun4 sui1 ran2 ling4 ren2 xian4 mu4 ke3 shi4 you3 de5 shi2 hou4 ni4 shui3 xing2 zhou1 geng4 rang4 ren2 qin1 pei4
SJY002.wav 我们必须与其他生物共同分享我们的地球。
	wo3 men5 bi4 xu1 yu3 qi2 ta1 sheng1 wu4 gong4 tong2 fen1 xiang3 wo3 men5 de5 di4 qiu2
```
#### 3.使用bert预处理
- 默认前1/5的数据作为 valid 集，后4/5的数据作为 train 集。

- 会打印并过滤数据中本项目不支持的**儿化音**条目

- filelists中的格式：
```
我的数据集会生成这样的：
1|vits_data/waves-16k/SJY/SJY001.wav|vits_data/temps/SJY/SJY001.spec.pt|vits_data/berts/SJY/SJY001.wav.npy|sil ^ i1 f an2 f eng1 sh uen4 s uei1 r an2 l ing4 r en2 x ian4 m u4 sp k e3 sh iii4 ^ iou3 d e5 sh iii2 h ou4 n i4 sh uei3 x ing2 zh ou1 g eng4 r ang4 r en2 q in1 p ei4 sp sil
1|vits_data/waves-16k/SJY/SJY002.wav|vits_data/temps/SJY/SJY002.spec.pt|vits_data/berts/SJY/SJY002.wav.npy|sil ^ uo3 m en5 b i4 x v1 ^ v3 q i2 t a1 sh eng1 ^ u4 g ong4 t ong2 f en1 x iang3 ^ uo3 m en5 d e5 d i4 q iou2 sp sil
```

#### 4.循环复制train的条目，直到>800条。为了加大每epoch中的数据数量，避免频繁读写。

#### 5.数据读取测试。  

</br>

### 二、关于训练：
1.每个短语/字的**尾音问题**明显跟底模型有关，底模型尾音就有明显问题，我克隆后还好了点。。。  

2.虽说在BERT-VITS中使用Duration Predictor（dp）似乎效果会更好，但本项目**无法使用 Duration Predictor（dp）**，因为AISHELL3预训练模型**用的就是 Scholastic Duration Predictor（sdp）**。如果微调时想用dp，加载底模型权重时会报错。  

3.微调的本质就是加载预训练模型，用它的权重为自己的各个层初始化，然后（通常）再在另一个数据集上继续训练。  
所以用一个不是在BERT-VITS架构上训练的预训练VITS模型也是可以微调的，只是需要手动初始化一下连接处的线性层之类的，可能要改代码，而且收敛可能慢一点（毕竟要新学一两层）。  
不过用AISHELL3底模型的话不用改，因为那本来就是在BERT-VITS架构上训练的底模型。  
同理，如果你能够手动初始化dp的代码，也是可以用AISHELL3微调dp的，就相当于从AISHELL3取需要的权重，再把不需要的sdp权重扔掉……——其实这就已经是在处理2个不同形状的模型了。  

</br>

### 三、关于推理：
1.可以修改 length_scale、noise_scale_w、noise_scale 参数控制生成的音频总语速、单个音素语速、变化等。（sdp的特性）  

2.如果发现有拼音标注不正确的，请在 text/pinyin-local.txt 中手动标注上正确的读音，如“一帆风顺 yi1 fan1 feng1 shun4”、“似 si4”，也可以标注一些常用轻声的，如“羡慕 xian4 mu5”。  

3.如果想要看看没有BERT是什么样子，使用vits_infer_no_bert.py推理即可。  
测试的感觉是：  
no BERT确实更棒读一些（**重音**和**语速**都很**平均**，而且**偏快**），在短句和诗句上可能不明显，但在长句上很明显。  
有BERT则更符合人的**连读习惯**，会有根据**语义**而定的**停顿**/分词/**重音**，也会有**加速和减速**，**而非一直匀速**。  
这可能要归功于BERT_Prosody Model学习到的对prosody label的预测（标点->2，短语/词->0111...），0111...这种标注法可能确实会带有变速过渡或重音的信息？。
