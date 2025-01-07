import feedparser

class DataStore:
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

        return title

    def remove_feed(self, feed_name):
        if feed_name in self.feeds_data:
            del self.feeds_data[feed_name]

    def get_title_dict(self, title):
        if title in self.feeds_data:
            return self.feeds_data[title]

    def get_item_text(self, title, item):
        items_list = self.feeds_data[title]

        for i in items_list:
            if item == i['title']:
                return i['details']