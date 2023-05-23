import requests

import json
import uuid


def gen_msg_id() -> str:
    """生成msgId"""
    # uuid无分隔符
    msg_id = uuid.uuid4().hex
    return msg_id


def get_content_length(data):
    #计算=和&的字节数
    length = len(data.keys()) * 2 - 1
    #计算键值的字节数。最后的encode是对字符串进行utf编码，
    #如果键值包含中文，那么一个汉字字符对应三个字节，len()方法只能计算字符的个数
    #而content length是字节数
    total = ''.join(list(data.keys()) + list(data.values())).encode()
    length += len(total)
    return str(length)


class Session:

    cookies: dict
    
    cookies_str: str

    title: str
    """名称"""

    headers: dict

    userId: str

    sessionId: str

    parentId: str = "0"
    """上一次请求获取的msgId"""

    def __init__(self, cookies: dict, firstQuery: str):
        self.cookies = cookies

        self.cookies_str = ""
        for key in self.cookies:
            self.cookies_str += "{}={}; ".format(key, self.cookies[key])

        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            # "content-length": "20",
            "content-type": "application/json",
            "origin": "https://tongyi.aliyun.com",
            "referer": "https://tongyi.aliyun.com/chat",
            "sec-ch-ua": '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50",
            "x-xsrf-token": "50f6b58b-4251-42e9-906d-97dc5d1eee61",
            "cookie": self.cookies_str
        }

        data = {
            "firstQuery": firstQuery
        }

        self.headers['content-length'] = get_content_length(data)

        resp = requests.post(
            url="https://tongyi.aliyun.com/qianwen/addSession".format(firstQuery),
            cookies=self.cookies,
            data="{}".format(json.dumps(data)),
            headers=self.headers,
            timeout=5
        )
        
        resp_json = resp.json()
        if resp_json['success']:
            self.userId = resp_json['data']['userId']
            self.sessionId = resp_json['data']['sessionId']
            self.title = resp_json['data']['summary']
        else:
            raise Exception("创建会话失败: {}".format(resp_json))

    def ask(self, prompt: str, open_search: bool = False, timeout: int = 17, stream: bool = False) -> dict:
        """提问"""
        resp = requests.post(
            url="https://tongyi.aliyun.com/qianwen/conversation",
            cookies=self.cookies,
            data=json.dumps({
                "action":"next",
                "msgId":gen_msg_id(),
                "parentMsgId":self.parentId,
                "contents":[
                    {
                        "contentType":"text",
                        "content":prompt
                    }
                ],
                "timeout":timeout,
                "openSearch":open_search,
                "sessionId":self.sessionId,
                "model":""
            }),
            timeout=timeout,
            headers=self.headers,
            stream=True
        )

        index = 0

        pending = ""

        result = {}

        for chunk in resp.iter_content(chunk_size=4096, decode_unicode=True):
            if chunk:
                # print("====================={}=====================".format(index))
                # print(chunk)
                index += 1
                
                chunk = str(chunk).strip()

                pending += chunk
                # 检查是否以}结尾
                if not chunk.endswith("}"):
                    continue
                else:  # 完整
                    try:
                        # 删掉pending前的"data: "
                        pending = pending.split("\n")[-1]
                        pending = pending[6:]
                        # 转换为json
                        resp_json = json.loads(pending)
                        # 重置pending
                        pending = ""

                        self.parentId = resp_json['msgId']
                        result = resp_json
                        if resp_json['stopReason'] == 'stop' and not stream:
                            yield result
                        elif stream:
                            yield resp_json
                    except Exception as e:
                        print("解析失败: {}".format(e))
                        # print("pending: {}".format(pending))
                        continue
