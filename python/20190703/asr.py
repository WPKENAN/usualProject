from aip import AipSpeech

""" 你的 APPID AK SK """

APP_ID = '16707980'
API_KEY = 'v9iWBNX8usLfy2MuDWQGSX2Q'
SECRET_KEY = 'xBOEUHxuFh6SmwCEjmag147fzsGgTVfF'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 识别本地文件

# result=client.asr(get_file_content('16k.pcm'), 'pcm', 16000, {'dev_pid': '1536',})
result=client.asr(get_file_content('16k.wav'), 'wav', 16000, {'dev_pid': '1536',})
# result=client.asr(get_file_content('demo.pcm'), 'wav', 16000, {'dev_pid': '1536',})
print(result)
