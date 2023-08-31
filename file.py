import os.path
import config


def save_unknown_messages(message):
    read_file(config.UNKNOWN_MESSAGES_FILENAME)
    with open(config.UNKNOWN_MESSAGES_FILENAME, 'w', encoding='utf-16') as text_file:
        config.UNKNOWN_MESSAGES.add(message)
        for i in config.UNKNOWN_MESSAGES:
            print(i, file=text_file)


def read_file(file_name):
    if os.path.exists(file_name):
        with open(config.UNKNOWN_MESSAGES_FILENAME, 'r', encoding='utf-16') as text_file:
            res = []
            for i in text_file.readlines():
                res.append(i.replace('\n', ''))
            config.UNKNOWN_MESSAGES.update(res)
