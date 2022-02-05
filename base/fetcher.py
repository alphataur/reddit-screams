from psaw import PushshiftAPI
from datetime import datetime, date, timedelta
import os
import json


def date2epoch(dt):
    return datetime(dt.year, dt.month, dt.day).timestamp()

def epoch2date(epoch):
    return datetime.fromtimestamp(epoch)

class Fetched:
    def __init__(self, subreddit, days=10, time_from=None, time_to=None):
        self.filters = ["id", "score", "author", "created_utc", "title"]
        self.subreddit = subreddit
        if time_from is None:
            yesterday = date.today() - timedelta(days=days)
            time_from = date2epoch(yesterday)
        if time_to is None:
            today = date.today()
            time_from = date2epoch(today)
        self.time_from = time_from
        self.time_to = time_to
        self.api = PushshiftAPI()

    def gather(self):
        for submission in self.api.search_submissions(subreddit=self.subreddit, filters=self.filters):

            idx = submission.id
            score = submission.score
            author = submission.author
            created = epoch2date(submission.created_utc)
            title = submission.title

            year = created.year
            month = created.month
            day = created.day

            print(f"found {idx} of {day}/{month}/{year}")

            dpath = f"dumps/{year}/{month}/{day}"
            fpath = f"{idx}.json"

            os.makedirs(dpath, exist_ok=True)

            payload = { "id": idx, "score": score, "author": author, "created": submission.created_utc, "title": title}

            with open(os.path.join(dpath, fpath), "w") as f:
                json.dump(payload, f, indent=4, sort_keys=True)


if __name__ == "__main__":
    a = Fetched("india")
    a.gather()


