import wordcloud
import jieba
import json


def get_words(file_path):
    print('正在读取文件...')
    with open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        replies = ''
        for data in json_data:
            replies += data['content'] + '\n'
    print('正在分词...')
    arr = jieba.cut(replies, use_paddle=True)
    return " ".join(arr)


def generate_word_cloud(file_path):
    words = get_words(file_path)
    wc = wordcloud.WordCloud(font_path='SDK_SC_Web.ttf', width=1920, height=1080, background_color='white')
    print('正在生成词云...')
    wc.generate(words)
    wc.to_file('word_cloud.png')
    print('词云生成成功！')
