from dataclasses import dataclass, field
import requests
from enum import Enum
from typing import Dict, Any, Optional, Union, cast


class DataKind(Enum):
    STRING = "STRING"
    JSON = "JSON"


class APIResponse:
    data: str
    data_kind: DataKind



class RequestMethod(Enum):
    GET = "GET"
    POST = "POST"


@dataclass
class RzApi:
    path: str
    response_data_kind: DataKind
    request_method: RequestMethod
    auth_required: bool = False


class APIs:
    FeaturedMatchesSummary = RzApi(
        path="/v5/freeapis/featured-matches-summary/",
        response_data_kind=DataKind.STRING,
        request_method=RequestMethod.GET,
        auth_required=False
    )


@dataclass
class RzApp:
    project_key: Optional[str] = None # This property is required for paid APIs
    session: requests.Session = field(init=False)

    def __post_init__(self) -> None:
        self.session = requests.Session()

    def featured_matches_summary(self) -> str:
        api = APIs.FeaturedMatchesSummary
        return cast(str, self.start_request(api))

    def start_request(
            self, api: RzApi, params: Dict[str, Any] = {},
            body: Dict[str, Any] = {},
            headers: Dict[str, Any] = {}) -> Union[str, Dict[str, Any]]:
        HOST = "https://api.sports.roanuz.com"
        PATH = api.path
        URL = HOST + PATH
        if api.request_method == RequestMethod.GET:
            with self.session.get(URL, params=params, headers=headers) as response:
                if api.response_data_kind == DataKind.JSON:
                    return response.json()
                return response.text
        return None






