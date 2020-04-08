### 一、说明

**由于国家线快出了，故写了一份爬取小木虫网站调剂信息的爬虫代码，方便信息查看。此代码仅用于学习，不作为任何商业用途。**

### 二、代码使用参数说明

```python
def parameters(pro_='', pro_1='', pro_2='', year=''):
    paramsList = [pro_, pro_1, pro_2, year]
    return paramsList

def main():
    url = 'http://muchong.com/bbs/kaoyan.php?'
    path = './data_info.csv'
    pre_params = ['r1%5B%5D=', 'r2%5B%5D=', 'r3%5B%5D=', 'year=']
    params = parameters(pro_='08', pro_1='0801')
    dataList = []
    getDataInfo(dataList, url, pre_params, *params)
    outputCSV(dataList, path)
```

主体代码已写完，只需要修改main函数中`params`中的相关参数，即可使用。

`parameters`函数主要用于返回查询的参数。默认参数都为空。如果都不填，则是爬取小木虫全部年份，全部专业的所有调剂信息。

`params`具体参数说明：

- `pro_`

  所要查询的学科门类。可查询的见下图:

  <img src="https://s1.ax1x.com/2020/04/09/Ghfaa6.png" style="zoom:60%;" />

  只要查询填写对应学科门类前的数字即可。例如工学，则:`pro_='08'`

  **注意:填写的为字符串格式**

- `pro_1`

  填写的一级学科代码。如下图：

  <img src="https://s1.ax1x.com/2020/04/09/GhfBGD.png" style="zoom:40%;" />

  以电子科学与技术为例，同样只需要填写前面代码即可。如：`pro_2='0806'`

  如果这一项不填，则查询的是前一个填写的整个学科门类所有信息。

- `pro_2`

  填写的二级学科代码。如图:

  ![](https://s1.ax1x.com/2020/04/09/GhfdIK.png)

  例如查询物理电子学调剂信息，同上。则填:`pro_2='080901'`。如果不填，则默认查询的是上一级学科下的所有调剂信息。例如，这里就是全部的电子科学与技术的调剂信息。

- `year`

  查询年份。例如查询2020年。`year='2020'`。**注意:同样是字符串类型**。如果不填，则是查询全部的年份。

  其中，`main()`函数中的保存路径`path`,可自定义修改。

**总结:**只需修改`params`和保存路径`url`即可。

### 三、效果图

![](https://s1.ax1x.com/2020/04/09/GhfDRe.png)

![](https://s1.ax1x.com/2020/04/09/Ghf0PO.png)

### 附

小木虫调剂信息网站:http://muchong.com/bbs/kaoyan.php

### 写在最后

由于代码能力较弱，代码质量并不是很高，欢迎**Pull**。