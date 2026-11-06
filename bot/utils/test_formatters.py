import pytest

from bot.testing.database import a_route, a_user, an_ad
from bot.utils.formatters import format_ad, format_route


@pytest.mark.parametrize("field", ["description", "price", "from_city", "to_country"])
def test_format_ad_renders_html_in_ad_fields_as_plain_text(field: str) -> None:
    ad = an_ad(a_user(telegram_id=10))
    setattr(ad, field, '<a href="https://phishing.example">оплата</a>')

    text = format_ad(ad)

    assert '&lt;a href="https://phishing.example"&gt;оплата&lt;/a&gt;' in text


@pytest.mark.parametrize("field", ["luggage", "conditions", "from_city", "to_country"])
def test_format_route_renders_html_in_route_fields_as_plain_text(field: str) -> None:
    route = a_route(a_user(telegram_id=10))
    setattr(route, field, '<a href="https://phishing.example">оплата</a>')

    text = format_route(route)

    assert '&lt;a href="https://phishing.example"&gt;оплата&lt;/a&gt;' in text
