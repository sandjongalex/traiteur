from tests.helpers import create_user, login


def test_public_ui_shell_renders(client):
    response = client.get("/")
    text = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Vos moments, notre" in text
    assert "Configurer mon événement" in text
    assert 'data-nav-toggle' in text


def test_configurator_ui_renders(client):
    response = client.get("/demande-de-devis")
    text = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Événement" in text
    assert "Prestations" in text
    assert "Coordonnées" in text
    assert "Récapitulatif" in text
    assert "n’est pas un devis contractuel" in text


def test_admin_login_ui_renders(client):
    response = client.get("/admin/login")
    text = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Back-office sécurisé" in text
    assert "Se connecter" in text


def test_admin_shell_and_main_modules_render(client, app):
    create_user()
    login(client)

    for path, marker in [
        ("/admin/", "Dashboard"),
        ("/admin/catalogue/", "Catalogue"),
        ("/admin/demandes-de-devis/", "Demandes de devis"),
        ("/admin/materiel/", "Matériel"),
        ("/admin/users/", "Utilisateurs"),
        ("/admin/roles/", "Rôles"),
        ("/admin/audit/", "Journal d’audit"),
    ]:
        response = client.get(path)
        text = response.get_data(as_text=True)
        assert response.status_code == 200
        assert marker in text
        assert "admin-sidebar" in text


def test_branded_errors_render(client):
    response = client.get("/route-ui-inconnue")
    assert response.status_code == 404
    assert "Retour à l’accueil" in response.get_data(as_text=True)
