## 本项目是基于BERT-VITS的音色克隆（微调）
## 这分支是根据vfft项目中的add auxiliary data（添加辅助数据）训练方法设计的，但实际效果并没有多好，所以暂时遗弃。

```
- bert_vits.json 中，"n_speakers" 保留为 174（和底模型一样） ，"gin_channels" 保留为 256。
- 训练的结果是只覆盖原底模型中的2个speaker，其余的speaker都会保留。
- vfft项目的“快速微调”的主要原理是在utils.py的load_checkpoint()中舍弃其他没有用到的speaker权重，我把它的代码放在了utils_vfft.py中，默认是不启用的。
- 可以手动指定想要在哪个speaker上进行微调（只需修改prep_bert中生成speaker id那里的代码即可，改为硬编码）。但是效果往往和那个speaker本身的质量有关，所以除非确定哪个speaker生成效果很好，否则没有必要刻意指定以男声或女声为基础微调。
- log_interval 和 eval_interval 分别为 10 和 100。
```
