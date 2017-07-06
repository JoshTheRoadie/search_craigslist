import sys
import time
from result_tracker import ResultTracker
import search
import config

URL_TEMPLATE = 'https://{}.craigslist.org'
DATE_STRIP_FORMAT = '%Y-%m-%d %H:%M'


if __name__ == '__main__':
    try:
        config_key = sys.argv[1]
    except IndexError:
        raise ValueError('You must use one argument that corresponds to a key in the config.py file.')

    search_info = config.query_data[config_key]

    url_base = URL_TEMPLATE.format(search_info['location'].lower())
    url_search = url_base + search_info['search_url']
    storage_path = search_info['storage_path']
    search_keys = search_info['search_keys']

    tracker = ResultTracker()

    while True:
        print 'Process running.....................................................................'
        print 'Process will run every {} seconds.'.format(str(config.SLEEP_TIME))
        print 'The current item being searched is {}.'.format(config_key)
        if tracker.last_post_date:
            last_post = tracker.last_post_date
        else:
            last_post = None

        html = search.search_craigslist(url_search, params=search_keys)
        if html:
            tracker.update_posts(search.get_new_posts(html, url_base))
            if tracker.last_post_date != last_post:
                print 'New Posts added and dumped!'
                tracker.dump_posts(storage_path)
            else:
                print 'There are no new posts at this time.'
        else:
            print 'Last attempt to connect failed.'
        time.sleep(config.SLEEP_TIME)
