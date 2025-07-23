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
|  文件名   | 路径  |  功能   | 说明  |
|  :----:  | :----:  |  :----:  | :----:  |
|  page.py   | page  |  作为一个蓝图组件  | 接收前缀为 /page/ 的url路由，匹配对应的视图函数，返回对应的数据分析图表，是整个项目最核心的文件（之一？O(∩_∩)O哈哈~）  |
|  | page | 清洗后的数据表  | —— |
|  | user | 爬取 城市-链接 数据  | —— |
|  | user | 爬取城市具体信息的数据  | 爬取hourse_info.csv的爬虫文件 |
|  | user | 城市-链接 csv文件  | spider_address_url.py爬取得到的文件 |

### spider
|  文件名   | 路径  |  功能   | 说明  |
|  :----:  | :----:  |  :----:  | :----:  |
|  hourse_info.csv   | spider  |  原数据库数据  | 由spider_main.py爬虫获取到的未处理前的数据  |
| hourse_info_cleaned.csv  | spider | 清洗后的数据表  | —— |
| spider_address_url.py  | spider | 爬取 城市-链接 数据  | —— |
| spider_data_main.py  | spider | 爬取城市具体信息的数据  | 爬取hourse_info.csv的爬虫文件 |
| city.Data.csv  | spider | 城市-链接 csv文件  | spider_address_url.py爬取得到的文件 |
