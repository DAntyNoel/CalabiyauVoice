import configparser, os

config = configparser.ConfigParser()

def init():
    global config
    config["DEFAULT"] = {
        "thisdir": os.path.dirname(os.path.dirname(__file__)),
        "newest": "0.10.2.38"
    }
    config["csv_controller"] = { # type: ignore
        "csv_file": "index.csv",
        "history_file": "histroy.txt",
        "tags": ['星绘', '玛德蕾娜', '白墨', '绯莎', '奥黛丽', '香奈美', '明', '令', '梅瑞狄斯', '拉薇', '心夏', '伊薇特', '信', '米雪儿', '系统语音', '香奈美系统语音', '其他', '未知', 'NEW']
    }

def write_conf():
    global config
    with open(os.path.join(os.path.dirname(__file__), "db.ini"), "w") as configfile:
        config.write(configfile)

def read_conf():
    global config
    config.read(os.path.join(os.path.dirname(__file__), "db.ini"))

if not os.path.exists(os.path.join(os.path.dirname(__file__), "db.ini")):
    init()
    write_conf()
read_conf()


def examples():

    # 获取所有的节名
    sections = config.sections()
    print(sections)

    # 获取"localdb"节中的所有键值对
    items = config.items("localdb")
    print(items)

    # 获取"remotedb"节中的"host"参数
    host = config.get("remotedb", "host")
    print(host)

    # 获取"DEFAULT"节中的"port"参数，并转换为整数
    port = config.getint("DEFAULT", "port")
    print(port)

