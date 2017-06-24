import datetime
import requests
from bs4 import BeautifulSoup
from result_tracker import Post


def search_craigslist(url_search, params=None):
    """
    Attempts to retrieve the HTML of the given url from craigslist.org by adding a query string to the url based on
    the parameters passed.
    :param url_search: string, the url for the search desired on craigslist
    :param params: dict, {'craigslist_param_name': 'value', ...}
    :return: string, html of search results
    """
    try:
        html = requests.get(url_search, params=params).text
        return html
    except requests.ConnectionError:
        return None


def get_post_data(soup_result):
    """
    Extracts text data from the result of a BeautifulSoup.find call.
    :param soup_result: the result of a BeautifulSoup.find call
    :return: str or None, the text of the give soup_result
    """
    if soup_result:
        return soup_result.text
    else:
        return None


def get_new_posts(html, base_url):
    """
    Parses the HTML search results from craigslist.org pulling and storing the title, price, area,
    time, and url of each post.
    :param html: string, the HTML resulting from a search on craigslist.org
    :param base_url: string, the URL for the craiglist.org for the location searched
    :return: list, list of posts stored in namedtuples called Post
    """
    date_format = '%Y-%m-%d %H:%M'
    soup = BeautifulSoup(html, 'html.parser')
    all_posts = []
    for section in soup.find_all(class_='result-row'):
        title = get_post_data(section.find(class_='result-title hdrlnk'))
        price = get_post_data(section.find(class_='result-price'))
        area = get_post_data(section.find(class_='result-hood'))
        post_time = datetime.datetime.strptime(section.find('time')['datetime'], date_format)
        post_url = base_url + section.find('a').get('href')
        all_posts.append(Post(title=title, price=price, date=post_time, url=post_url, area=area))
    return all_posts


if __name__ == '__main__':
    pass


