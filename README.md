# CTF比赛题目仓库-2020

## 仓库说明

1. 这里将会保存我参与的每一次的CTF比赛题目呢(￣▽￣)

2. 因为没有Web源码(Ｔ▽Ｔ)，也没钱买Pwn服务器╮(╯﹏╰）╭

   所以目前Web仅收录题目描述，也不做Pwn搭建~(〃'▽'〃)

   敬请谅解(^_−)☆

⚠️：请注意，自2020年起，题目保存将使用脚本自动化存储，在一代脚本中，所有附件名将被统一重命名为题目名，请在做题时使用file命令自行检查文件类型。

## 自动存题脚本说明(`Auto_save_problem_for_*.py`)

因为每次存题好费时间哇~

存一次题好几个小时就过去了emmm

于是就写了以下脚本用于解放双手收获快乐hhhhhh

⚠️：**所有脚本均需要在Python3环境运行**，默认的赛题文件主目录均为`~/Desktop/CTF_question/`，如需修改，请直接替换脚本的`Save`函数起始部分。

有运行问题欢迎提交issue~

### Auto_save_problem_for_XCTF.py

用于存储支撑平台是赛宁网安的比赛题目

使用前需要打开脚本文件，修改用户自定义部分

```
#以下为用户预定义部分↓
# 你打算把本赛事的题目丢到哪个文件夹去呢~
race_name = ''
# 请从浏览器获取该字段然后填在这里哦~
Headers['X-CSRF-Token'] = ''
Cookies['session'] = ''
Cookies['X-CSRF-Token'] = Headers['X-CSRF-Token']
evt = ''
#以上为用户预定义部分↑
```

![image-20200225180711709](http://img.lhyerror404.cn/error404/2020-02-25-100712.png)

程序将会自动在主目录下形成以下目录结构：

```
->race_name
->->Auto_Save_Result.txt
->->赛题类别1
->->->赛题1
->->->->题目描述.txt
->->->->Hint.txt(若存在)
->->->->附件1(若存在)
->->->->附件2(若存在)
->->->->Auto_save.flag
->->->赛题2
->->->->题目描述.txt
->->->->Hint.txt(若存在)
->->->->附件1(若存在)
->->->->附件2(若存在)
->->->->Auto_save.flag
->->赛题类别2
->->->赛题1
->->->->题目描述.txt
->->->->Hint.txt(若存在)
->->->->附件1(若存在)
->->->->附件2(若存在)
->->->->Auto_save.flag
->->->赛题2
->->->->题目描述.txt
->->->->Hint.txt(若存在)
->->->->附件1(若存在)
->->->->附件2(若存在)
->->->->Auto_save.flag
```

其中

```
Auto_Save_Result.txt：用于存储log，但请注意，程序仅会保留成功日志，也就是说，用户中断脚本将导致本次log不做存储！
Auto_save.flag：当此标志文件存在，重复运行脚本将直接跳过对应题目，当此文件被删除，将会更新题目描述文件和Hint文件。但是！附件将不做更新，如需更新，请删除需要更新的题目文件夹。
```

![image-20200225182136287](http://img.lhyerror404.cn/error404/2020-02-25-102136.png)

#### 更新记录

```
2020-02-25 正式发布 V1.0 
V1.0 新功能：
1. 将会自动根据附件的链接获取文件名进行存储。
2. 加入了题目存在标志文件，替代了原来使用题目描述作为标志的机制。
```

### Auto_save_problem_for_CTFd.py

用于存储支撑平台是CTFd以及基于CTFd二次开发平台的比赛题目

使用前需要打开脚本文件，修改用户自定义部分

```
#以下为用户预定义部分↓
# 你打算把本赛事的题目丢到哪个文件夹去呢~
race_name = ''
# 请从浏览器获取该字段然后填在这里哦~
url = ''
Cookies['session'] = ''
#以上为用户预定义部分↑
```

#### 更新记录

```
2020-02-25 正式发布 V1.0 
V1.0 新功能：
1. 将会自动根据附件的链接获取文件名进行存储。
2. 加入了题目存在标志文件，替代了原来使用题目描述作为标志的机制。
```

### Auto_save_problem_for_ichunqiu.py

用于存储支撑平台是i春秋的比赛题目

使用前需要打开脚本文件，修改用户自定义部分

```
#以下为用户预定义部分↓
# 你打算把本赛事的题目丢到哪个文件夹去呢~
race_name = ''
# 请从浏览器获取该字段然后填在这里哦~
Headers['SIGN'] = ''
Cookies['__jsluid_s'] = ''
Cookies['chkphone'] = ''
Cookies['ci_session_race'] = ''
post_data = {
	'k': '',
	'rs': ''
}
#以上为用户预定义部分↑
```

⚠️：由于i春秋平台的特殊性，无法存储附件，附件需要自行手动存储~

#### 更新记录

```
2020-02-25 正式发布 V1.0 
```

## 版权声明

1. 本仓库的所有题目文件来源均为窝参加的各次比赛中放出的题目。
2. 自动存题脚本遵循GPL-3.0协议。
3. 本仓库向BUUOJ开放题目使用授权，允许其**免费**搭建并开放给各位CTFer练习。
4. 在未经出题方允许的情况下，任何组织或个人不得以任何形式商业化使用。
5. 如果涉及题目侵权，请发送邮件至 [hebtuerror404@vip.qq.com](mailto:hebtuerror404@vip.qq.com)，我将及时删除相关题目。
6. 若发现除出题方以外的任何组织或个人以任何形式商业化使用本仓库题目，请及时转告相关竞赛组委会。

## 合作

如果有未收录的题目欢迎合作~可将题目发送至 [hebtuerror404@vip.qq.com](mailto:hebtuerror404@vip.qq.com) 灰常感谢φ(>ω<*)

## 高速下载

如果需要高速下载服务，可以临时开通阿里云-OSS子账户提供下载，需要支付一定的流量费用，流量费用由阿里云自动计算生成，我不会收取任何额外费用。 

## 友链传送门：

[中南大学新人赛(ACTF_Junior_2020)](https://github.com/CSUAuroraLab/ACTF_Junior_2020)

[安恒杯系列比赛(AnhengCTF)](https://github.com/hebtuerror404/Anheng_cup_month)

[河北师范大学网络安全竞赛(HECTF)](https://github.com/HECTF)

[经典赛题复现环境 CTF Training](https://github.com/CTFTraining/CTFTraining)

[CTF比赛题目仓库-2018](https://github.com/hebtuerror404/CTF_competition_warehouse_2018)

[CTF比赛题目仓库-2019](https://github.com/hebtuerror404/CTF_competition_warehouse_2019)

