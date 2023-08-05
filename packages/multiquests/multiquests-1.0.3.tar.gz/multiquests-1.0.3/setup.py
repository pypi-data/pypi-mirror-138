from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="multiquests",  #包名
    version="1.0.3",    #版本号
    author="Bohan Li",
    author_email="lbhllbyz@163.com",
    description="A simple crawler framework for multi-coroutine and multi-process",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Haloherooo/multiquests",          #项目主页
    packages=find_packages(),  #你要安装的包，通过 find_packages 找到当前目录下有哪些包
    install_requires=["asyncio",
	                  "aiohttp",
					  "nest_asyncio"],
	license = "MIT Licence",
	#说明包的分类信息
    classifiers=[
		"Development Status :: 2 - Pre-Alpha",
		"Operating System :: OS Independent",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Programming Language :: Python :: 3.10",
		"Programming Language :: Python :: 3.11",  
    ],
)