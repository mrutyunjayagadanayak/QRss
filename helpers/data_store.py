import feedparser

class Data_Store:
    def __init__(self):
        self.feeds_data = {}

    def add_to_feed(self,url):
        new_feed = feedparser.parse(url)
        title = new_feed['feed']['title']

        items = []

        for entry in new_feed.entries:
            item = {
                'title' : entry.title,
                'details' : entry.summary
            }
            items.append(item)

        self.feeds_data[title] = items
        print(self.feeds_data[title])
        return title

    def remove_feed(self, feed_name):
        if feed_name in self.feeds_data:
            del self.feeds_data[feed_name]
