# revTongYi

阿里通义千问Python逆向API

```bash
pip install revTongYi --upgrade
```

```python
import revTongYi

question = "人工智能将对人类社会发展产生什么影响？"

session = revTongYi.Session(
    cookies=cookies_dict,
    firstQuery=question
)

print(
    next(
        session.ask(
            prompt=question
        )
    )
)
```