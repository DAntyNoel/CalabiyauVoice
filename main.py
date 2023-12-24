from convert2wav import ogg2wav, _clear_wav_output
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

async def process_file(ogg_file, output, save = True):
    wav_file = ogg2wav(ogg_file, output_dir=output)
    text = translate_wav(wav_file)
    dir, file_name = os.path.split(wav_file)
    if not save:
        os.system(f'rm {wav_file}')
    return (dir, file_name, text)

async def process_all_files(file_list, output, save = True):
    data_dict = {}
    tasks = []

    for file in file_list:
        if file.endswith(".ogg"):
            task = asyncio.create_task(process_file(file, output, save=save))
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

def convert_and_translate(input_dir = '.', file_list:list = [], output_dir = 'WavOutput', save = True) -> dict:
    _clear_wav_output(output_dir=output_dir)
    if file_list == []:
        file_list = [os.path.join(input_dir, f) for f in os.listdir(input_dir)]
    data_dict = asyncio.run(process_all_files(file_list, output_dir, save=save))
    return data_dict

def convert(input_dir = '.', output_dir = 'WavOutput'):
    _clear_wav_output(output_dir=output_dir)
    file_list = [os.path.join(input_dir, f) for f in os.listdir(input_dir)]
    for file in file_list:
        ogg2wav(file, output_dir)
    print(f'Finished. {len(file_list)} files to {output_dir}')

if __name__ == "__main__":
    data_dict = read_csv()
    checkout(data_dict)
    file_list = ['0.10.2.38/' + f + '.ogg' for f in data_dict.keys()]
    data_dict_new = convert_and_translate(file_list=file_list, save=False)
    write_csv(data_dict_new, 'index_new.csv')

# if __name__ == "__main__":
#     convert(input_dir='Chinese')
