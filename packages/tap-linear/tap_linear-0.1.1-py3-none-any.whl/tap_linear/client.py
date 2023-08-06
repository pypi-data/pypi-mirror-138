"""GraphQL client handling, including LinearStream base class."""

from datetime import timedelta
import requests
from typing import Any, Optional, Iterable
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.streams import GraphQLStream


class LinearStream(GraphQLStream):
    """Linear stream class."""

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="Authorization",
            value=self.config.get("auth_token"),
            location="header",
        )

    @property
    def url_base(self) -> str:
        return self.config.get("api_url")

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def get_next_page_token(
        self, response: requests.models.Response, previous_token: Optional[Any]
    ) -> Any:
        """Return the next page token."""
        resp_json = response.json()
        if resp_json["data"]["issues"]["pageInfo"]["hasNextPage"]:
            return resp_json["data"]["issues"]["pageInfo"]["endCursor"]
        else:
            return None

    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        """Return the request payload."""
        value = (self.get_starting_timestamp(context) + timedelta(seconds=1)).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        self.logger.info(f"Previous state timestamp: {value}")
        body = {
            "query": self.query,
            "variables": {"next": next_page_token, "replicationKeyValue": value},
        }
        return body

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        resp_json = response.json()
        for row in resp_json["data"]["issues"]["nodes"]:
            yield row
