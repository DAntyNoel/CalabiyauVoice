
import asyncio
import aiohttp
import json, os, random
from bs4 import BeautifulSoup
from fuzzywuzzy import process

# base_url = 'https://wiki.biligame.com/klbq/'
base_redirect_url = 'https://wiki.biligame.com/klbq/Special:Redirect/file/'
thisdir = os.path.dirname(__file__)
_id = 0


def get_index_json():
    global index_dict
    if not os.path.exists(os.path.join(thisdir, 'WIKI', 'index.json')):
        print('WIKI/index.json 未找到，请下载后重试\nTips:查看 wiki_init.ipynb 以获取帮助')
        raise
        
    with open(os.path.join(thisdir, 'WIKI', 'index.json'), 'r', encoding='utf-8') as f:
        index_dict = json.load(f)

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def parse(name):
    global _id
    min_id = _id
    url = index_dict[name]['url']
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        result = {}

        tables = soup.find_all('table', class_='voice-table')
        for table in tables:
            tag = ''
            for tr in table.find_all('tr'): # type: ignore
                td_list = tr.find_all('td')
                if len(td_list) == 3:
                    tag = td_list[0].text.strip()
                text_td = td_list[-1]
                u_tag = text_td.find("u")
                if u_tag != None:
                    text_tip = u_tag.text
                    u_tag.decompose()
                    text = text_td.text.strip() + f"({text_tip})"
                else:
                    text = text_td.text.strip()
                # contents = td_list[-1].contents
                # if len(contents) == 3:
                #     text = contents[0] + f"({contents[2].text})"
                value = tr.find('div', class_='media-audio')['data-file']
                result[value] = {
                    'text':text,
                    'tag':tag,
                    '_id': _id
                }
                _id += 1
            # print(result)

        tables = soup.find_all('table', class_='voice-table nojp')
        for table in tables:
            tag = ''
            for tr in table.find_all('tr'): # type: ignore
                td_list = tr.find_all('td')
                tag = td_list[0].text.strip()
                text_td = td_list[-1]
                u_tag = text_td.find("u")
                if u_tag != None:
                    text_tip = u_tag.text
                    u_tag.decompose()
                    text = text_td.text.strip() + f"({text_tip})"
                else:
                    text = text_td.text.strip()
                # contents = td_list[-1].contents
                # if len(contents) == 3:
                #     text = contents[0] + f"({contents[2].text})"
                value = tr.find('div', class_='media-audio')['data-file']
                result[value] = {
                    'text': text,
                    'tag': tag,
                    '_id': _id
                }
                _id += 1
            # print(result)

        tables = soup.find_all('table', class_='voice-table-other')
        for table in tables:
            for tr in table.find_all('tr'): # type: ignore
                text = tr.find_all('td')[0].text.strip()
                value_list = tr.find_all('div', class_='media-audio')
                for i in range(len(value_list)):
                    result[value_list[i]['data-file']] = {
                        'text': text + str(i),
                        'tag': text,
                        '_id': _id
                    }
                    _id += 1
            # print(result)
        index_dict[name]['min_id'] = min_id
        index_dict[name]['max_id'] = _id - 1
        json_str = json.dumps(index_dict, indent=4, ensure_ascii=False)
        with open(os.path.join(thisdir, 'WIKI', 'index.json'), 'w', encoding='utf-8') as f:
            f.write(json_str)
        json_str = json.dumps(result, indent=4, ensure_ascii=False)
        with open(os.path.join(thisdir, 'WIKI', name + '.json'), 'w', encoding='utf-8') as f:
            f.write(json_str)
        return result

async def download_index_json(main_url = 'https://wiki.biligame.com/klbq/首页'):
    if not os.path.exists(os.path.join(thisdir, 'WIKI')):
        os.system(f"mkdir {os.path.exists(os.path.join(thisdir, 'WIKI'))}")
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, main_url)
        soup = BeautifulSoup(html, 'html.parser')
        result = {}
        for nav_chara in soup.find_all('div', class_='nav-chara')[:3]:
            for a in nav_chara.find_all('a'):
                result[a['title']] = {
                    'url': 'https://wiki.biligame.com' + a['href'],
                    'min_id': -1,
                    'max_id': -1
                }
        print(result)
        json_str = json.dumps(result, indent=4, ensure_ascii=False)
        with open(os.path.join(thisdir, 'WIKI', 'index.json'), 'w', encoding='utf-8') as f:
            f.write(json_str)

        return result

def get_chara_file_dict(chara) -> dict:
    '''
    "星绘语音-072CN.mp3": {
        "text": "守护星芒！",
        "tag": "技能释放",
        "_id": 2298
    },
    '''
    with open(os.path.join(thisdir, 'WIKI', chara + '.json'), 'r', encoding='utf-8') as f:
        data_dict = json.load(f)
    return data_dict


def main1():
    asyncio.run(parse('星绘'))

async def update_all():
    for key in index_dict.keys():
        await parse(key)

async def download_all_voice_file():
    url = 'https://wiki.biligame.com/klbq/Special:Redirect/file/'
    for chara in index_dict.keys():
        if not os.path.exists(os.path.join(thisdir, "WIKI", chara)):
            os.system(f'mkdir {os.path.join(thisdir, "WIKI", chara)}')
        data_dict = get_chara_file_dict(chara)
        for tag in data_dict.keys():
            if os.path.exists(os.path.join(thisdir, 'WIKI', chara, tag)):
                continue
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url + tag) as response:
                        if response.status == 200:
                            data = await response.read()
                            with open(os.path.join(thisdir, 'WIKI', chara, tag), 'wb') as file:
                                file.write(data)
            except Exception as e:
                print(f"{chara} {tag}")


def get_mp3_file(chara, file_name):
    return os.path.join(thisdir, 'WIKI', chara, file_name)

def get_voice_text_list(chara = '', lang = 'CN') -> list:
    '''lang: zh/cn, jp, all 
    Return type: [(卡拉彼丘, 星绘, 星绘语音-022CN.mp3, _id), ...]'''
    chara_list = list(index_dict.keys())
    result = []
    lang = lang.upper()
    if lang == 'ZH': lang = 'CN'

    if chara in chara_list:
        data_dict = get_chara_file_dict(chara)
        if lang in ['CN', 'JP']:
            for file, content in data_dict.items():
                if lang in file:
                    result.append((content['text'], chara, file, content['_id']))
        else:
            for file, content in data_dict.items():
                result.append((content['text'], chara, file, content['_id']))
    
    elif chara.upper() == 'ALL':
        for chara in chara_list:
            with open(os.path.join(thisdir, "WIKI", chara + '.json'), 'r') as f:
                data_dict = json.load(f)
            if lang in ['CN', 'JP']:
                for file, content in data_dict.items():
                    if lang in file:
                        result.append((content['text'], chara, file, content['_id']))
            else:
                for file, content in data_dict.items():
                    result.append((content['text'], chara, file, content['_id']))
    
    else:
        # TODO
        return []
    
    return result
            
def get_best_items_by_text_list(text_list:list, text, _threshold = 60) -> list[tuple]:
    '''Return type: [((卡拉彼丘, 星绘, 星绘语音-022CN.mp3, _id), score)]'''
    matches = process.extract(text, text_list, limit=10)
    results = [match for match in matches if match[1] >= _threshold]
    return results

def get_voice_file_list(file = '', chara = '', text = '', no = -1, _id = -1, lang = 'CN') -> list:
    '''Return type: [((卡拉彼丘, 星绘, 星绘语音-022CN.mp3, _id), score)]'''
    chara_list = list(index_dict.keys())
    result = []
    lang = lang.upper()
    def has(f, no) -> bool:
        try:
            x = f.split('-')[1][:3]
            return int(no) == int(x)
        except:
            return False
    if _id > 0: #指定id
        for chara in index_dict.keys():
            data_dict = get_chara_file_dict(chara=chara)
            min_id = index_dict[chara]['min_id']
            max_id = index_dict[chara]['max_id']
            if min_id > _id or max_id < _id:
                continue
            file_list = list(data_dict.keys())
            result = [((data_dict[f]['text'], chara, f, data_dict[f]['_id']), 100) for f in file_list if data_dict[f]['_id'] == _id]
            return result
    if chara in chara_list: #给定角色
        data_dict = get_chara_file_dict(chara=chara)
        file_list = list(data_dict.keys())
        if no > -1: #用no指定文件
            if lang == 'ALL':
                results = [f for f in file_list if has(f,no)]
                result = [((data_dict[f]['text'], chara, f, data_dict[f]['_id']), 100) for f in results]
            elif lang in ['CN', 'JP']:
                results = [f for f in file_list if has(f,no) and f.endswith(lang + '.mp3')]
                result = [((data_dict[f]['text'], chara, f, data_dict[f]['_id']), 100) for f in results]
        elif text != '': #用语音内容指定文件
            text_list = get_voice_text_list(chara=chara, lang=lang)
            filter_text_list = get_best_items_by_text_list(text_list=text_list, text=text)
            # result = [x[0][2] for x in filter_text_list]
            result = filter_text_list
        else: #随机选取
            if lang in ['CN', 'JP']:
                results = [f for f in file_list if f.endswith(lang + '.mp3')]
                results = [random.choice(results)]
            else:
                results = [random.choice(file_list)]
            result = [((data_dict[f]['text'], chara, f, data_dict[f]['_id']), 100) for f in results]
    else: #未给定角色
        if text != '': #用语音内容指定文件
            text_list = get_voice_text_list(chara='ALL', lang=lang)
            filter_text_list = get_best_items_by_text_list(text_list=text_list, text=text)
            result = filter_text_list
    # TODO
    return result



get_index_json()
if __name__ == '__main__':
    asyncio.run(download_index_json())
    # asyncio.run(update_all())
    # asyncio.run(download_all_voice_file())
    # get_voice_text_dict('星绘', 'jp')
    x = get_voice_file_list(text='火力大', lang='cn')
    print(x)
