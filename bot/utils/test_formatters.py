import pytest

from bot.testing.database import a_route, a_user, an_ad
from bot.utils.formatters import format_ad, format_author, format_route


@pytest.mark.parametrize("field", ["description", "price", "from_city", "to_country"])
def test_format_ad_renders_html_in_ad_fields_as_plain_text(field: str) -> None:
    ad = an_ad(a_user(telegram_id=10))
    setattr(ad, field, '<a href="https://phishing.example">оплата</a>')

    text = format_ad(ad)

    assert '&lt;a href="https://phishing.example"&gt;оплата&lt;/a&gt;' in text


@pytest.mark.parametrize(
    ("entered_price", "shown_price"),
    [("10", "💵 10$"), ("12.5", "💵 12.5$"), ("10$", "💵 10$"), ("договорная", "💵 договорная")],
    ids=["integer", "decimal", "with-dollar-sign", "text"],
)
def test_format_ad_adds_dollar_sign_only_to_bare_number(entered_price: str, shown_price: str) -> None:
    ad = an_ad(a_user(telegram_id=10))
    ad.price = entered_price

    text = format_ad(ad)

    assert text.endswith(shown_price)


@pytest.mark.parametrize("field", ["luggage", "conditions", "from_city", "to_country"])
def test_format_route_renders_html_in_route_fields_as_plain_text(field: str) -> None:
    route = a_route(a_user(telegram_id=10))
    setattr(route, field, '<a href="https://phishing.example">оплата</a>')

    text = format_route(route)

    assert '&lt;a href="https://phishing.example"&gt;оплата&lt;/a&gt;' in text


@pytest.mark.parametrize(
    ("username", "author_line"),
    [("traveler", "👤 @traveler"), (None, "👤 Связаться можно через кнопку ниже")],
    ids=["with-username", "without-username"],
)
def test_format_author_points_to_contact_button_only_without_username(username: str | None, author_line: str) -> None:
    author = a_user(telegram_id=10, username=username)

    text = format_author(author)

    assert text == author_line
