### idea_bench相关位于idea_text文件夹
#### idea.ipynb
* idea_text中的idea.ipynb记录了生成idea过程和结果（input，启发or解答，几次...）
* 测试了其他平台使用的prompt
* prompt打分遇到的有一些问题和解决思路
#### idea_new.ipynb
* idea_new.ipynb 使用gpt进行自评测和根据idea相似的文章被引量/年限打分结果。
* gpt评测方法：输入$5 \times n$的表格（5是每个平台生成5条idea，n是平台的数量）。表格通过shuffle进行乱序拼接。输出$3 \times n$的矩阵（3代表新颖性，影响力可行性3个指标）。得分由idea在3个指标的排序计算得出，最高分是1，最低分是0。
* 相似文献法： 找寻数据库中和idea相似的top10文献，然后分别计算他们的被引量和出版时间。比较top10文章的平均被引量和数据库的平均被引量；比较top10文章和数据库文章的在近五年发表的比例。
### 总结和自优化位于optimal文件夹下optimal.ipynb文件
#### 自优化位于ipy文件大纲optimal下
#### 总结位于大纲summary下，内容包括：
* 单片文献总结
* 领域总结。（1）直接联网搜索。（2）将文件夹下所有md文件进行简短的总结，然后将这些总结拼接输入gpt让其总结领域研究现状。