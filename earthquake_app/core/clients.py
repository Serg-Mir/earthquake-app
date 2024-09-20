import logging

from requests import Session
from tenacity import before_sleep_log, retry, stop_after_attempt, wait_exponential


from earthquake_app.config.settings import get_settings

logger = logging.getLogger(__name__)


class USGSClient:
    def __init__(self, headers: dict | None = None):
        self.url = get_settings().USGS_API_URL

        self.headers = headers
        self.session = Session()

    @retry(
        wait=wait_exponential(multiplier=1, min=2, max=10),
        stop=stop_after_attempt(5),
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.DEBUG),
    )
    def request(self, method: str, params, data: dict | None = None):
        with self.session:
            url = self.url
            response = self.session.request(method, url, params=params, data=data)
            return response
