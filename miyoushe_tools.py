import json
import reply

import web_tools

article_replies = []


def get_article_info(article_id):
    post_url = f'https://bbs-api.miyoushe.com/post/wapi/getPostFull?gids=2&post_id={article_id}&read=1'
    page = web_tools.get_web_page(post_url)
    if page:
        article_info = json.loads(page)
        return article_info
    return None


def get_page_article_replies(article_id, last_id):
    post_replies_url = ('https://bbs-api.miyoushe.com/post/wapi/getPostReplies?gids=2&is_hot=false&order_type=1'
                        f'&last_id={last_id}&post_id={article_id}&size=50')
    page = web_tools.get_web_page(post_replies_url)
    if page:
        article_reply = json.loads(page)
        return article_reply
    return None


def get_page_article_sub_replies(article_id, floor_id):
    post_replies_url = ('https://bbs-api.miyoushe.com/post/wapi/getSubReplies?gids=2&is_hot=false&order_type=1'
                        f'&floor_id={floor_id}&post_id={article_id}&size=50')
    page = web_tools.get_web_page(post_replies_url)
    if page:
        article_reply = json.loads(page)
        return article_reply
    return None


def get_article_replies(article_id, file_path=None, last_id=0):
    global article_replies
    last_id = last_id
    if last_id != 0:
        with open(file_path, 'r', encoding='utf-8') as f:
            article_replies = json.load(f)
    page = 1
    last_count = 0
    while True:
        try:
            replies = get_page_article_replies(article_id, last_id)
            sub_reply_count = 0
            if not replies:
                break
            for _reply in replies['data']['list']:
                # convert to Reply class
                new_reply = reply.Reply(_reply['reply']['content'], _reply['user']['nickname'],
                                        _reply['user']['level_exp']['level'], _reply['user']['ip_region'],
                                        _reply['user']['uid'], [], _reply['reply']['created_at'],
                                        _reply['reply']['floor_id'])
                # add sub_replies
                if 'sub_replies' in _reply:
                    # get sub_replies
                    sub_replies = get_page_article_sub_replies(article_id, _reply['reply']['floor_id'])
                    for sub_reply in sub_replies['data']['list']:
                        new_reply.sub_replies.append(reply.Reply(sub_reply['reply']['content'],
                                                                 sub_reply['user']['nickname'],
                                                                 sub_reply['user']['level_exp']['level'],
                                                                 sub_reply['user']['ip_region'],
                                                                 sub_reply['user']['uid'], [],
                                                                 sub_reply['reply']['created_at'],
                                                                 sub_reply['reply']['floor_id']))
                        sub_reply_count += 1
                article_replies.append(new_reply)
            last_id = replies['data']['last_id']
            if replies['data']['is_last']:
                break
            # print(f'抓取到第{page}页上有{len(article_replies) - last_count}条回复，有{sub_reply_count}条子回复')
            last_count = len(article_replies)
            page += 1
        except Exception as e:
            print("抓取回复时发生错误：" + str(e))
            print("Last ID: " + str(last_id))
            continue

    with open(file_path, 'w', encoding='utf-8') as f:
        # append new replies to the file
        json.dump(article_replies, f, default=reply.json_serializer, ensure_ascii=False, indent=4)
    return article_replies


def file_exists(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8'):
            return True
    except FileNotFoundError:
        return False
    except Exception as e:
        print(e)
        return False
