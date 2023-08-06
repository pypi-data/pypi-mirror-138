import requests

from .utils import as_list


class MetaClient(object):
    """MetaClient - Python SDK that returns data from Facebook (Meta).
    ```python
    from meta_scraper import MetaClient
    client = MetaClient(api_key='API_KEY_FROM_OUTSCRAPER.COM')
    results = client.get_page_data(['outscraper'])
    results = client.get_page_reviews(['outscraper'])
    ```
    https://github.com/meta-scraper/facebook-scraper-python
    """

    _api_url = 'https://api.app.outscraper.com'
    _api_headers = {}

    def __init__(self, api_key: str) -> None:
        self._api_headers = {
            'X-API-KEY': api_key,
            'client': 'Python Facebook SDK'
        }

    def get_page_data(self, query: list, fields: list = None) -> list:
        '''
            Returns information about Facebook (Meta) pages.

                    Parameters:
                            query (list | str): links to Facebook pages or Page usernames (e.g., https://www.facebook.com/outscraper, outscraper). Using a lists allows multiple queries (up to 25) to be sent in one request and save on network latency time.
                            fields (list): parameter defines which fields you want to include with each item returned in the response. By default, it returns all fields. Use &fields=query,name to return only the specific ones.

                    Returns:
                            list: json result
        '''
        response = requests.get(f'{self._api_url}/facebook/pages', params={
            'query': as_list(query),
            'fields': ','.join(fields) if fields else '',
            'async': False,
        }, headers=self._api_headers)

        if 199 < response.status_code < 300:
            return response.json().get('data', [])

        raise Exception(f'Response status code: {response.status_code}')

    def get_page_reviews(self, query: list, limit: int = 50) -> list:
        '''
            Returns reviews from Facebook (Meta) pages.

                    Parameters:
                            query (list | str): links to Facebook pages or Page usernames (e.g., https://www.facebook.com/outscraper, outscraper). Using a lists allows multiple queries (up to 25) to be sent in one request and save on network latency time.
                            limit (list): limit (str): parameter specifies the limit of reviews to get from one page.

                    Returns:
                            list: json result
        '''
        response = requests.get(f'{self._api_url}/facebook/reviews', params={
            'query': as_list(query),
            'limit': limit,
            'async': False,
        }, headers=self._api_headers)

        if 199 < response.status_code < 300:
            return response.json().get('data', [])

        raise Exception(f'Response status code: {response.status_code}')
