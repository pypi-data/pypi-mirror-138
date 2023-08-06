"""Linear tap class."""

from typing import List
from singer_sdk import Tap, Stream
from singer_sdk import typing as th
from tap_linear.streams import IssuesStream

STREAM_TYPES = [
    IssuesStream,
]


class TapLinear(Tap):
    """Linear tap class."""

    name = "tap-linear"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType,
            required=True,
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "api_url",
            th.StringType,
            default="https://api.linear.app/graphql",
            description="The URL for the API service",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
            default="2010-01-01T00:00:00.000Z",
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
