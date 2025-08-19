from dlt.sources.rest_api import (
    check_connection,
    rest_api_source,
)


class SourceBase:
    def connect(self):
        raise NotImplementedError

class RestAPISource(SourceBase):
    def __init__(self, config):
        self.config = config
    def connect(self):
        source = rest_api_source(self.config)

        def check_network_and_authentication() -> None:
            (can_connect, error_msg) = check_connection(source)
            if not can_connect:
                pass  # do something with the error message

        check_network_and_authentication()

        return source
    

def identify_source(source_type: str, source_config: dict):
    if source_type == "rest_api":
        return RestAPISource(source_config)
    # Add more source types here as needed
    raise ValueError(f"Unknown source type: {source_type}")
