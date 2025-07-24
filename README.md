项目绝对可以运行起来，我们没有漏传任何一个文件 ～(∠・ω< )⌒★~

# 部署运行流程

1. 虚拟环境安装python3.11.13及以上的版本

2. 进去之后在终端使用
```
pip install -r requirements.txt
```
安装依赖包

3. 启动 app.py 即可

## 文件说明
### views
|  所在文件夹   | 文件名  |                                  功能                                  | 说明  |
|  :----:  | :----:  |:--------------------------------------------------------------------:| :----:  |
|  page    |  page.py  |                               作为一个蓝图组件                               | 接收前缀为 /page/ 的url路由，匹配对应的视图函数，返回对应的数据分析图表，是整个项目最核心的文件（之一？O(∩_∩)O哈哈~）  |
|  user    |  user.py  |                              应该是登录注册页面                               | 接收前缀为 /user/ 的url路由，匹配对应的视图函数，返回对应的数据分析图表 |
|  page/template    |  ——  | 这个文件夹存放的是flask框架的模板文件，但是实际上前端页面应该放到根目录下的templates文件夹中的，只不过我们把它们放到了这里 | 接收前缀为 /user/ 的url路由，匹配对应的视图函数，返回对应的数据分析图表 |


### spider
|  所在文件夹   | 文件名  |  功能   | 说明  |
|  :----:   | :----:  |  :----:  | :----:  |
|  spider   |  hourse_info.csv  |  原数据库数据  | 由spider_main.py爬虫直接获取到的数据，还没经过数据清洗的原数据  |
|  spider   | hourse_info_cleaned.csv | 清洗后的数据表  | hourse_info.csv经过数据清洗得到的文件 |
|  spider   | spider_address_url.py | 爬取 城市-链接 数据  | —— |
|  spider   | spider_data_main.py | 爬取城市具体信息的数据  | 爬取hourse_info.csv的爬虫文件 |
|  spider   | city.Data.csv | 城市-链接 csv文件  | spider_address_url.py爬取得到的文件 |
