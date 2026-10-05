import pytest

PUBLIC_ROUTES = [
    "/",
    "/a-propos",
    "/services",
    "/menus",
    "/realisations",
    "/contact",
    "/demande-de-devis",
]


@pytest.mark.parametrize("path", PUBLIC_ROUTES)
def test_public_pages_return_html(client, path):
    response = client.get(path)
    assert response.status_code == 200
    assert "text/html" in response.content_type
    assert b"DNP DECO" in response.data


def test_home_contains_primary_navigation_and_quote_cta(client):
    response = client.get("/")
    assert b"Accueil" in response.data
    assert b"Services" in response.data
    assert b"Menus" in response.data
    assert b"Contact" in response.data
    assert b"Demander un devis" in response.data


def test_home_has_mobile_viewport_and_seo_metadata(client):
    response = client.get("/")
    assert b'name="viewport"' in response.data
    assert b'name="description"' in response.data
    assert b'property="og:title"' in response.data
    assert b'application/ld+json' in response.data
    assert "Traiteur &amp; Événementiel à Yaoundé" in response.get_data(as_text=True)


def test_quote_page_does_not_claim_estimate_is_final_quote(client):
    response = client.get("/demande-de-devis")
    text = response.get_data(as_text=True)
    assert "n’est pas un devis contractuel" in text


def test_contact_does_not_fake_submission(client):
    response = client.get("/contact")
    text = response.get_data(as_text=True)
    assert "Aucun message n’est actuellement enregistré ou envoyé" in text
    assert "Envoi en ligne bientôt disponible" in text


def test_unknown_page_uses_branded_404(client):
    response = client.get("/cette-page-n-existe-pas")
    assert response.status_code == 404
    assert b"DNP DECO" in response.data
    assert b"404" in response.data
