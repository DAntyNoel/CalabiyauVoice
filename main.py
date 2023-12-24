from convert2wav import convert2wav, _clear_wav_output
from tencent_speech_recog import translate_wav
from csv_controller import *
import asyncio
import os

data_dict_sample = {
    'id' : {
        'tag': '星绘',
        'text': '守护星芒',
        # 'confidence': 1, # float 置信度
        'valid' : False # 验证路径
    }
}

async def process_file(ogg_file, output):
    wav_file = convert2wav(ogg_file, output_dir=output)
    text = translate_wav(wav_file)
    dir, file_name = os.path.split(wav_file)
    return (dir, file_name, text)

async def process_all_files(file_list, output):
    data_dict = {}
    tasks = []

    for file in file_list:
        if file.endswith(".ogg"):
            task = asyncio.create_task(process_file(file, output))
            tasks.append(task)

    print(f'Process started. Total {len(file_list)} files. Please wait...\nTips: Check log.txt for more info.')
    results = await asyncio.gather(*tasks)
    print(f'Process finished. Please check {output}')
    for dir, wav_file, text in results:
        data_dict[wav_file[:-4]] = {
            'tag': '',
            'text':text,
            'valid': False
        }
    return data_dict

def main(input_dir = '.', output_dir = 'WavOutput'):
    _clear_wav_output(output_dir=output_dir)
    file_list = [os.path.join(input_dir, f) for f in os.listdir(input_dir)]
    data_dict = asyncio.run(process_all_files(file_list[:40], output_dir))
    print(data_dict)

if __name__ == "__main__":
    main('Chinese')
