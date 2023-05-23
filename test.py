import revTongYi
import json


def convert_cookies(cookies: list) -> dict:
    """转换cookies"""
    cookies_dict = {}
    for cookie in cookies:
        cookies_dict[cookie["name"]] = cookie["value"]
    return cookies_dict


def test():
    firstQuery = "人工智能将对人类社会发展产生什么影响？"

    # 读取cookies.json

    cookies_dict = {}

    with open("cookies.json", "r") as f:
        cookies_dict = convert_cookies(json.load(f))

    sess = revTongYi.Session(
        cookies=cookies_dict,
        firstQuery=firstQuery
    )

    print(next(sess.ask(firstQuery)))


if __name__ == "__main__":
    test()