import collections
import pickle
from operator import attrgetter

Post = collections.namedtuple('Post', ['title', 'price', 'date', 'url', 'area'])


def strip_unicode(word):
    """
    Returns a string with non-ascii characters stripped from it.
    :param word: str
    :return: str, ascii only
    """
    clean_string = ''
    return ''.join([clean_string + letter for letter in word if ord(letter) < 128])


def post_to_string(post):
    """
    Returns a human readable string for a result_tracker.Post
    :param post: result_tracker.Post
    :return: string
    """
    output_format = 'Title: {}\nPrice: {}\nDate: {}\nPost URL: {}\nArea: {}\n\n'

    cleaned_strings = [strip_unicode(str(post_data)) for post_data in post]
    return output_format.format(*cleaned_strings)


class ResultTracker(object):

    date_format_string = '%y_%m_%d_%H%M'

    def __init__(self, posts=None):
        """
        Stores the results of a Craigslist search and the time of the most recent post.
        :param posts: list of result_tracker.Post tuples or None
        :return: ResultTracker instance
        """
        if not posts:
            self.posts = posts
            self.last_post_date = None
        else:
            self.posts = sorted(posts, key=attrgetter('date'), reverse=True)
            self.last_post_date = posts[0].date

    def update_posts(self, new_posts):
        """
        If no tracker.posts exist, sets tracker.posts to new_posts.  If there are already tracker.posts, then
        a logical difference between new_posts and tracker.posts is set to tracker.posts.
        :param new_posts: list of Post namedtuples
        :return: None
        """
        if self.posts:
            old_posts = set(self.posts)
            new_posts = set(new_posts)
            post_diff = new_posts - old_posts
            if post_diff:
                self.posts = sorted(list(post_diff), key=attrgetter('date'), reverse=True)
                self.last_post_date = self.posts[0].date
        else:
            self.posts = sorted(new_posts, key=attrgetter('date'), reverse=True)
            self.last_post_date = self.posts[0].date

    def dump_posts(self, storage_path, file_type=None):
        """
        Saves self.posts to a file.  If 'p' is passed as file_type, then the data is pickled as a list of
        result_tracker.Post objects.  Otherwise it is saved as a human readable text file.
        :param storage_path: relative path to storage directory
        :param file_type: str, 'p' for pickle, 't' or None for text
        :return: None
        """
        if file_type == 'p':
            full_filename = '{}{}.pkl'.format(storage_path, self.last_post_date.strftime(self.date_format_string))
            with open(full_filename, 'wb') as storage_file:
                pickle.dump(self.posts, storage_file)
        else:
            full_filename = '{}{}.txt'.format(storage_path, self.last_post_date.strftime(self.date_format_string))
            with open(full_filename, 'w') as text_file:
                text_file.writelines([post_to_string(post) for post in self.posts])

    def print_posts(self):
        """
        Prints the contents of self.posts to the console.
        :return: None
        """
        output_format = 'Title: {}\nPrice: {}\nDate: {}\nPost URL: {}\nArea: {}\n'
        for post in self.posts:
            title, price, date, url, area = post
            print output_format.format(title, price, date, url, area)


if __name__ == '__main__':
    pass
