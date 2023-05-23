# revTongYi


[![PyPi](https://img.shields.io/pypi/v/revTongYi.svg)](https://pypi.python.org/pypi/revTongYi)
[![Downloads](https://static.pepy.tech/badge/revTongYi)](https://pypi.python.org/pypi/revTongYi)

阿里通义千问Python逆向API

```bash
pip install revTongYi --upgrade
```

- 需要通义千问测试资格
- 到通义千问对话页面，获取cookies，以key: value的dict形式提供给构造函数
- 您也可以使用`Cookies Editor`插件([参考](https://github.com/xw5xr6/revERNIEBot))获取cookies的json，并参考`test.py`中的代码处理cookies

```python
import revTongYi

question = "人工智能将对人类社会发展产生什么影响？"

session = revTongYi.Session(
    cookies=<cookies_dict>,  # cookies的key: value形式，dict类型
    firstQuery=question
)

print(
    next(
        session.ask(  # ask方法实际上是一个迭代器，可以提供参数stream=True并换用for的方式迭代
            prompt=question
        )  # ask方法接收的详细参数请查看源码
    )
)
```

## CLI模式

1. 安装 [Chrome/Edge](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) 或 [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/) 上的Cookies Editor插件
2. 前往https://tongyi.aliyun.com/chat 并登录
3. 打开此插件，点击`Export`->`Export as JSON`，将复制的Cookies内容保存到文件`cookies.json`

```bash
python -m revTongYi.__init__
```
