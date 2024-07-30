from datetime import datetime
import time


class Reply:
    def __init__(self, content, username, level, region, uid, sub_replies, create_time, floor_id):
        self.content = content
        self.username = username
        self.level = level
        self.region = region
        self.uid = uid
        self.sub_replies = sub_replies
        self.create_time = create_time
        self.floor_id = floor_id

    def to_dict(self):
        return {
            'content': self.content,
            'username': self.username,
            'level': self.level,
            'region': self.region,
            'uid': self.uid,
            'sub_replies': [sub_reply.to_dict() for sub_reply in self.sub_replies],
            'create_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.create_time)),
            'floor_id': self.floor_id
        }


def json_serializer(obj):
    if isinstance(obj, Reply):
        return obj.to_dict()
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f'Type {type(obj)} not serializable')
