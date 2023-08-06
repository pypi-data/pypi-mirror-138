"""Client for Wikipedia REST API."""
from dataclasses import dataclass

import click
import desert
import marshmallow
import requests

API_URL = "https://{language}.wikipedia.org/api/rest_v1/page/random/summary"


@dataclass
class Page:
    """Page resource.

    Attributes:
        title: Title of the Wikipedia page
        extract: A plain text summary
    """

    title: str
    extract: str


schema = desert.schema(Page, meta={"unknown": marshmallow.EXCLUDE})


def random_page(language: str = "en") -> Page:
    """Return a random page from Wikipedia in the given `language`.

    Args:
        language: The Wikipedia language edition. Defaults to English ("en").

    Returns:
        A page resource

    Raises:
        ClickException: The HTTP request failed, or the HTTP response contained an
                        invalid body

    Example:
        >>> from hypermodern_python import wikipedia
        >>> page = wikipedia.random_page(language="en")
        >>> bool(page.title)
        True
    """
    url = API_URL.format(language=language)
    try:
        with requests.get(url) as response:
            response.raise_for_status()
            data = response.json()
            return schema.load(data)
    except (requests.RequestException, marshmallow.ValidationError) as error:
        raise click.ClickException(str(error)) from error
