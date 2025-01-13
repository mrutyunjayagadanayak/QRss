import sqlite3
import feedparser

class DataStore:
    def __init__(self):
        self.db_name = 'feeds.db'
        self.create_tables()

    def create_tables(self):
        # Create the tables if they don't already exist
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS feeds 
                          (id INTEGER PRIMARY KEY, title TEXT, url TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS items 
                          (feed_id INTEGER, title TEXT, details TEXT, 
                           FOREIGN KEY(feed_id) REFERENCES feeds(id))''')
        connection.commit()
        connection.close()

    def add_to_feed(self, url):
        # Parse the feed from the URL using feedparser
        new_feed = feedparser.parse(url)
        title = new_feed['feed']['title']

        # Save the feed to the database
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        # Check if the feed is already there
        cursor.execute('''SELECT id FROM feeds WHERE title = ?''',(title,))
        existing_feed = cursor.fetchone()

        if existing_feed:
            return "Feed exists"

        cursor.execute('''INSERT INTO feeds (title, url) VALUES (?, ?)''', (title, url))
        feed_id = cursor.lastrowid  # Get the ID of the newly inserted feed

        # Add feed items to the database
        for entry in new_feed.entries:
            cursor.execute('''INSERT INTO items (feed_id, title, details) 
                              VALUES (?, ?, ?)''', (feed_id, entry.title, entry.summary))

        connection.commit()
        connection.close()
        return title

    def remove_feed(self, feed_name):
        # Remove feed and its items by title
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        cursor.execute('''SELECT id FROM feeds WHERE title = ?''', (feed_name,))
        feed_id = cursor.fetchone()

        if feed_id:
            cursor.execute('''DELETE FROM items WHERE feed_id = ?''', (feed_id[0],))
            cursor.execute('''DELETE FROM feeds WHERE id = ?''', (feed_id[0],))

        connection.commit()
        connection.close()

    def get_title_dict(self, title):
        # Retrieve feed items by feed title
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        cursor.execute('''SELECT id, title FROM feeds WHERE title = ?''', (title,))
        feed_data = cursor.fetchone()

        if feed_data:
            feed_id = feed_data[0]
            cursor.execute('''SELECT title, details FROM items WHERE feed_id = ?''', (feed_id,))
            items = cursor.fetchall()
            connection.close()

            # Return a list of items for this feed
            return [{'title': item[0], 'details': item[1]} for item in items]
        else:
            connection.close()
            return []

    def get_item_text(self, title, item):
        # Retrieve the details of an item given a feed title and item title
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        cursor.execute('''SELECT id FROM feeds WHERE title = ?''', (title,))
        feed_id = cursor.fetchone()

        if feed_id:
            cursor.execute('''SELECT details FROM items WHERE feed_id = ? AND title = ?''',
                           (feed_id[0], item))
            details = cursor.fetchone()
            connection.close()
            return details[0] if details else ""
        else:
            connection.close()
            return ""

    def get_all_titles(self):

        connection = sqlite3.connect(self.db_name)
        curses = connection.cursor()

        curses.execute('''SELECT title FROM feeds''')
        titles = curses.fetchall()
        connection.close()

        return [title[0] for title in titles]


