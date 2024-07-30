import json

import miyoushe_tools
import analysis_tools
import reply

if __name__ == '__main__':
    while True:
        # 55221094
        article_id = input('Enter the article ID: ')
        # judge whether the input is a number
        try:
            int(article_id)
        except ValueError:
            print('Please enter a number.')
            continue
        break
    article_info = miyoushe_tools.get_article_info(str(abs(int(article_id))))
    file_name = f'{article_info["data"]["post"]["post"]["subject"]}.json'
    if int(article_id) > 0:
        print(f'正在抓取: {article_info["data"]["post"]["post"]["subject"]}')
        last_id = 0
        # file exists
        if miyoushe_tools.file_exists(file_name):
            with open(file_name, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                print(f'已经抓取到{len(json_data)}条回复')
                # get the last reply floor_id
                last_id = json_data[-1]['floor_id']
                print(f'最后一条回复的楼层号为{last_id}')
        try:
            article_replies = miyoushe_tools.get_article_replies(article_id,
                                                                 file_name,
                                                                 last_id)
            print(f'共抓取到{len(article_replies)}条回复')
        except KeyboardInterrupt as e:
            print('程序中断！正在保存文件……')
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(miyoushe_tools.article_replies, f, default=reply.json_serializer, ensure_ascii=False,
                          indent=4)
            exit(1)
    print('准备分析：')
    # analyze the replies
    analysis_tools.generate_word_cloud(file_name)
    print('程序结束！')
