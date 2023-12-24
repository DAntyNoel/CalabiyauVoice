import base64
import os, time, logging, traceback
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.asr.v20190614 import asr_client, models

import logging
logging.basicConfig(filename="log.txt", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

thisdir = os.path.dirname(__file__)

def init():
    global client
    with open(os.path.join(thisdir, 'tencent_cloud_secretkey'), 'r') as f:
        SecretId = f.readline().strip()
        SecretKey = f.readline().strip()

    cred = credential.Credential(SecretId, SecretKey)
    clientProfile = ClientProfile()
    clientProfile.signMethod = "TC3-HMAC-SHA256"
    client = asr_client.AsrClient(cred, "ap-shanghai", clientProfile)

# 获取文件夹下的所有ogg文件
# path = "WemOutput"
# recog_path = "RecogOutput"
# files = [f for f in os.listdir(path) if f.endswith(".ogg")]
    
def _translate_ogg(oggfile, ignore_er = False) -> str:
    from convert2wav import ogg2wav
    try:
        with open(ogg2wav(oggfile), "rb") as f:
            data = f.read()
        data = base64.b64encode(data).decode()
        req = models.SentenceRecognitionRequest()
        req.ProjectId = 0 # 项目ID，为0表示默认项目
        req.SubServiceType = 2 # 子服务类型，为2表示实时流式识别
        req.EngSerViceType = "16k_zh" # 引擎模型类型，为16k_zh表示16k中文普通话通用
        req.SourceType = 1 # 语音数据来源，为1表示语音URL
        req.VoiceFormat = "wav" # 语音格式，为ogg
        req.UsrAudioKey = oggfile # 用户端唯一标识，建议使用文件名
        req.Data = data # 语音数据，为Base64格式的字符串
        req.DataLen = len(data) # 语音数据长度，单位字节
        resp = client.SentenceRecognition(req)
        text = resp.Result
        print(text)
        return text
    
    except Exception as e:
        if not ignore_er:
            raise e
        else:
            logging.error("%s\n%s" % (e, traceback.format_exc()))

def translate_wav(wavfile, ignore_er = False) -> str:
    try:
        with open(wavfile, "rb") as f:
            data = f.read()
        data = base64.b64encode(data).decode()
        req = models.SentenceRecognitionRequest()
        req.ProjectId = 0 # 项目ID，为0表示默认项目
        req.SubServiceType = 2 # 子服务类型，为2表示实时流式识别
        req.EngSerViceType = "16k_zh" # 引擎模型类型，为16k_zh表示16k中文普通话通用
        req.SourceType = 1 # 语音数据来源，为1表示语音URL
        req.VoiceFormat = "wav" # 语音格式，为ogg
        req.UsrAudioKey = wavfile # 用户端唯一标识，建议使用文件名
        req.Data = data # 语音数据，为Base64格式的字符串
        req.DataLen = len(data) # 语音数据长度，单位字节
        resp = client.SentenceRecognition(req)
        text = resp.Result
        # print(text)
        return text
    
    except Exception as e:
        if not ignore_er:
            raise e
        else:
            logging.error("%s\n%s" % (e, traceback.format_exc()))

def translate_wavs(wavfile_list) -> list[str]:
    text_list = []
    for file in wavfile_list:
        text = translate_wav(file, ignore_er=True)
        text_list.append(text)
        time.sleep(0.1)

    print('\n\nTips: Check log.txt for more infos')

init()
if __name__ == '__main__':
    _translate_ogg('Chinese/651433486.ogg')