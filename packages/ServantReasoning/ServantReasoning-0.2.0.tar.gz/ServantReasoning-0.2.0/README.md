# ServantReasoningGame
**一个适用于[Nonebot2](https://github.com/nonebot/nonebot2)的从者推理游戏插件**  
**思路好像是来自[Hoshino](https://github.com/Ice-Cirno/HoshinoBot)的某个插件，但代码并无借鉴之处！**  
__自项目上传完成共收录了245位从者的信息（其中有2位为开发者彩蛋（懒得删了））__  
![功能介绍](https://github.com/suhexia/the-bag/blob/master/screenshortImg/chooseFunction.gif)
## 安装
通过pip安装

`pip install ServantReasoning`

通过Nonebot商店安装

`nb plugin install ServantReasoning`

## 相关指令
+ 开始游戏：从者推理  
+ 游戏进行中的回答：直接发送从者名字，匹配即正确  
+ 强制结束游戏（适用于卡到某些不知名bug时的情况）  
	+终止从者推理  
	+结束从者推理  
	+中止从者推理  


## 数据存储
___本插件使用的数据库为Mongodb（用于记录群友回答胜利的积分），默认已注释掉了，_function_doc.py文件中存放的就是数据存储的相关功能___

