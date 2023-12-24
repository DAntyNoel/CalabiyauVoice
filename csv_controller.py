import csv, os, shutil

_thisdir = os.path.dirname(__file__)
csv_file = 'index.csv'
history_file = 'history.txt'
newest = '0.10.2.38'
tags = ['星绘', '玛德蕾娜', '白墨', '绯莎', '奥黛丽', '香奈美', '明', '令', '梅瑞狄斯', '拉薇', '心夏', '伊薇特', '信', '米雪儿', '系统语音', '香奈美系统语音', '其他', '未知', 'NEW']
data_dict_sample = {
    'id' : {
        'tag': '星绘',
        'text': '守护星芒',
        # 'confidence': 1, # float 置信度
        'valid' : False # 验证路径
    }
}

def read_csv(csv_path = os.path.join(_thisdir, csv_file)) -> dict:
    data_dict = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        # 跳过第一行（表头）
        next(reader)
        for row in reader:
            id = row[0]
            tag = row[1]
            text = row[2]
            assert tag in tags, f"{tag} not in tags"
            data_dict[id] = {
                'tag' : tag,
                'text' : text,
                'valid' : False
            }
    return data_dict

def write_csv(data_dict:dict, csv_path = os.path.join(_thisdir, csv_file)):
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "tag", "text"])
        for file, content in data_dict.items():
            writer.writerow([file, content['tag'], content['text']])
        f.close()

def checkout(data_dict:dict, oggfile_dir = os.path.join(_thisdir, '0.10.2.38'), ign_ogg = False, ign_ind = False) -> bool:
    '''Returns: Ture iff No changes found'''
    IND_ERROR = 0
    OGG_ERROR = 0
    for id in data_dict.keys():
        if not os.path.exists(os.path.join(
            oggfile_dir, id + '.ogg'
        )):
            OGG_ERROR += 1
            if not ign_ogg:
                print(f"Ogg file not found: {id}.ogg (tag: {data_dict[id]['tag']}, text: {data_dict[id]['text']})")
            
    for file in os.listdir(oggfile_dir):
        if file.endswith('.ogg'):
            id = file[:-4]
            if str(id) not in data_dict.keys():
                IND_ERROR += 1
                if not ign_ind:
                    print(f"Index not found: {file}")
                # data_dict[id] = {
                #     'tag' : 'NEW',
                #     'text' : '',
                #     'valid' : False
                # }

    print(f'Total indexed {len(data_dict.keys())} ogg files.')
    if IND_ERROR == OGG_ERROR == 0:
        print('Checked. No changes found.')
        return True
    else:
        print(f'{OGG_ERROR} Ogg files not found.\n{IND_ERROR} Index not found.')
        return False

def get_ogg_file_by_id(id) -> str:
    return os.path.join(_thisdir, newest, id + '.ogg')

def get_ogg_files_by_tag(data_dict:dict, tag) -> list[str]:
    assert tag in tags
    results = []
    for id, content in data_dict.items():
        if content['tag'] == tag:
            results.append(get_ogg_file_by_id(id))
    return results

def modify_content(data_dict:dict, id, tag = None, text = None, imme_write = True):
    assert id in data_dict.keys()
    old_tag = data_dict[id]['tag']
    old_text = data_dict[id]['text']
    if tag != None:
        assert tag in tags
        data_dict[id]['tag'] = tag
    if text != None:
        data_dict[id]['text'] = text
    
    if imme_write:
        write_csv(data_dict)
    
    with open(os.path.join(_thisdir, history_file), 'a') as f:
        f.write(f"id:{id}" + f"tag:{old_tag}-->{tag}" if tag != None else "" + f"text:{old_text}-->{text}" if text != None else "")


if __name__ == '__main__':
    data_dict = read_csv()
    checkout(data_dict, ign_ind=True)
    
