import pytest
from django.conf import settings
from django.test import override_settings

@pytest.mark.django_db
def test_security_headers(client):
    response = client.get("/")
    assert response["X-Frame-Options"] == "DENY"
    assert response["X-Content-Type-Options"] == "nosniff"
    # SECURE_BROWSER_XSS_FILTER is mostly deprecated and not always visible in modern responses

@pytest.mark.django_db
@pytest.mark.parametrize("url", [
    "/login/",
    "/assets/",
    "/customers/",
])
def test_security_headers_on_important_views(client, url):
    response = client.get(url)
    assert response["X-Frame-Options"] == "DENY"
    assert response["X-Content-Type-Options"] == "nosniff"

@pytest.mark.django_db
def test_session_cookie_secure(client):
    response = client.get("/")
    # Only check if SECURE_COOKIE is enabled in settings
    if getattr(settings, "SESSION_COOKIE_SECURE", False):
        assert response.cookies['sessionid']['secure'] is True

@pytest.mark.django_db
def test_https_redirect(client, settings):
    # Enable SECURE_SSL_REDIRECT for this test
    settings.SECURE_SSL_REDIRECT = True
    response = client.get("/", secure=False)
    assert response.status_code in (301, 302)
    assert response["Location"].startswith("https://")