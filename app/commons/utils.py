import json


def initialize_google_credentials(class_object, params: dict):
    """Initialize a Google client class with service account credentials.

    Parameters:
    -----------
    class_object: Any
        The Google client class to instantiate (e.g., bigquery.Client).
    params: dict
        Dictionary of parameters including optional 'credentials' JSON string.

    Returns:
    --------
    Instantiated Google client object with proper authentication.
    """
    if not params.get("credentials"):
        if "credentials" in params:
            del params["credentials"]
        return class_object(**params)

    credentials: dict = json.loads(params.get("credentials", ""))
    from google.oauth2 import service_account  # type: ignore

    credentials_object = service_account.Credentials.from_service_account_info(
        info=credentials
    )
    params["credentials"] = credentials_object
    return class_object(**params)
