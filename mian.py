from scrapy.cmdline import execute

import sys
import os


# os.path.dirname(os.path.abspath(__file__))# 获取当前目录的绝对目录的父目录

sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # 可以将模块路径加到当前模块扫描的路径里：sys.path.append('你的模块的名称')。
execute(["scrapy", "crawl", "login"])
