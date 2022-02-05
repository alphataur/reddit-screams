import dotenv
dotenv.load_dotenv()

import praw
import os

class Comments:
    def __init__(self, id):
        self.idx = id
        self.api = praw.Reddit(client_secret=os.environ["client_secret"],
                client_id=os.environ["client_id"],
                user_agent=os.environ["user_agent"],
                username=os.environ["username"])

    def parse_comments(self, reply, depth=0):
        if depth == 0:
            spaces = ""
        else:
            spaces = depth * "-"
        print(f"{spaces}| {reply.body}")
        for reply in reply.replies:
            self.parse_comments(reply, depth+1)

    def gather(self):
        res = self.api.submission(id=self.idx)
        for comment in res.comments:
            self.parse_comments(comment)

if __name__ == "__main__":
    a = Comments(id="sl5zxb")
    a.gather()

