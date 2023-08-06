import requests

from .utils import as_list


class YelpReviewsClient(object):
    """YelpReviewsClient - Python SDK that returns reviews from Yelp businesses.
    ```python
    from yelp_reviews_scraper import YelpReviewsClient
    client = YelpReviewsClient(api_key='API_KEY_FROM_OUTSCRAPER.COM')
    results = client.get_reviews(['eggcellent-waffles-san-francisco'])
    ```
    https://github.com/meta-scraper/yelp-reviews-scraper-python
    """

    _api_url = 'https://api.app.outscraper.com'
    _api_headers = {}

    def __init__(self, api_key: str) -> None:
        self._api_headers = {
            'X-API-KEY': api_key,
            'client': 'Python Yelp Reviews SDK'
        }

    def get_reviews(self, query: list, limit: int = 100, sort: str = 'relevance_desc', cutoff: int = None) -> list:
        '''
            Returns reviews from Yelp businesses.

                    Parameters:
                            query (list | str): links, or IDs of any Yelp business (e.g., https://www.yelp.com/biz/cancha-boutique-gastrobar-san-francisco, eggcellent-waffles-san-francisco, iXoLJWjbcXCO43RT-H0uQQ) Using a lists allows multiple queries (up to 25) to be sent in one request and save on network latency time.
                            limit (list): limit (str): parameter specifies the limit of reviews to get from one business.
                            sort (str): parameter specifies one of the sorting types ("relevance_desc", "date_desc", "date_asc", "rating_desc", "rating_asc", or "elites_desc").
                            cutoff (int): parameter specifies the oldest timestamp value for reviews. Using the cutoff parameter overwrites sort parameter to date_desc. Therefore, the latest reviews will be at the beginning.

                    Returns:
                            list: json result
        '''
        response = requests.get(f'{self._api_url}/yelp/reviews', params={
            'query': as_list(query),
            'limit': limit,
            'sort': sort,
            'cutoff': cutoff,
            'async': False,
        }, headers=self._api_headers)

        if 199 < response.status_code < 300:
            return response.json().get('data', [])

        raise Exception(f'Response status code: {response.status_code}')
