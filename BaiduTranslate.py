import json
import os
import hashlib
import random
import requests
import __main__

# 使用绝对路径来确保符号链接在不同驱动器上能正确处理
def get_absolute_path(relative_path):
    base_path = os.path.dirname(os.path.abspath(__main__.__file__))
    abs_path = os.path.abspath(os.path.join(base_path, relative_path))
    
    # 检查路径是否有效
    if not os.path.exists(abs_path):
        base_path = os.path.dirname(__file__)  # 切换到当前文件所在目录
        abs_path = os.path.abspath(os.path.join(base_path, relative_path))
    
    return abs_path

# 确保配置文件的正确路径
config_path = get_absolute_path('config.json')

# 从 JSON 文件中加载配置
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

# 从配置中提取 appid 和 appkey
appid = config['baidu_translate']['appid']
appkey = config['baidu_translate']['appkey']

class BaiduTrans_devapi:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            'required': {
                'text': ('STRING', {'multiline': True, "forceInput": False}),
                'Translate_to_language': (['en', 'zh'], {'default': 'en'}),
            },
        }

    RETURN_TYPES = ('STRING',)
    FUNCTION = 'translation_devapi'
    CATEGORY = '百度翻译(DEV-api)'

    def translation_devapi(self, Translate_to_language, text):
        from_lang = 'auto'
        to_lang = Translate_to_language
        endpoint = 'http://api.fanyi.baidu.com'
        path = '/api/trans/vip/translate'
        url = endpoint + path
        query = text
        translate_result = ''

        if query:
            salt = random.randint(32768, 65536)
            s = appid + query + str(salt) + appkey
            sign = hashlib.md5(s.encode('utf-8')).hexdigest()
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

            try:
                r = requests.post(url, params=payload, headers=headers)
                response = r.json()
                if 'trans_result' in response:
                    result = ''
                    for line in response['trans_result']:
                        result += line['dst'] + '\n'
                    translate_result = result.rstrip()
                else:
                    translate_result = "百度翻译 API 错误!，请检查是否填写正确的 API Key 并且有足够的 API 流量?"
            except Exception as e:
                translate_result = "百度翻译 API 错误!，请检查是否填写正确的 API Key 并且有足够的 API 流量?"
                print(e)
        else:
            translate_result = ""

        print(f'百度翻译(DEV-api):---->\n{translate_result}')
        return (translate_result,)

NODE_CLASS_MAPPINGS = {
    'BaiduTrans_DevApi': BaiduTrans_devapi,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    'BaiduTrans_DevApi': '百度翻译api',
}
