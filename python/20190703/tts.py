from aip import AipSpeech

APP_ID = '16707980'
API_KEY = 'v9iWBNX8usLfy2MuDWQGSX2Q'
SECRET_KEY = 'xBOEUHxuFh6SmwCEjmag147fzsGgTVfF'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

result = client.synthesis('你好百度,我是王鹏，你是什么东西啊', 'zh', 1, {
    'vol': 5,
})

# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
if not isinstance(result, dict):
    with open('demo.pcm', 'wb') as f:
        f.write(result)

import os
# import numpy as np
# f1 = open("demo.wav",errors='ignore')
# f1.seek(0)
# f1.read(44)
# data = np.fromfile(f1, dtype=np.int16)
# data.tofile("demo.pcm")
#
# import wave
# import os
#
# f = open("demo.pcm",'rb')
# str_data  = f.read()
# wave_out=wave.open("out.wav",'wb')
# wave_out.setnchannels(1)
# wave_out.setsampwidth(2)
# wave_out.setframerate(8000)
# wave_out.writeframes(str_data)
