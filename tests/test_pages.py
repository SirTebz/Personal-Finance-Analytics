import pytest


@pytest.mark.parametrize("path", ["/", "/transactions", "/budgets", "/categories", "/import"])
def test_management_pages_load(client, path):
    assert client.get(path).status_code == 200
