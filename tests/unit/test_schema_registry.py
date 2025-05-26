import requests

def test_register_schema(schema_registry_url):
    url = f"{schema_registry_url}/subjects/product-value/versions"
    schema = {
        "schema": '{"type": "record", "name": "Product", "fields": [{"name": "id", "type": "int"}, {"name": "name", "type": "string"}]}'
    }
    response = requests.post(url, json=schema)
    assert response.status_code == 200, f"Expected 200 OK, but got {response.status_code}"
    assert "id" in response.json()

def test_get_versions(schema_registry_url):
    url = f"{schema_registry_url}/subjects/product-value/versions"
    response = requests.get(url)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert 1 in response.json()

def test_get_schema_version(schema_registry_url):
    # Register the schema first
    url = f"{schema_registry_url}/subjects/product-value/versions"
    schema = {
        "schema": '{"type": "record", "name": "Product", "fields": [{"name": "id", "type": "int"}, {"name": "name", "type": "string"}]}'
    }
    response = requests.post(url, json=schema)
    assert response.status_code == 200

    # Now get the registered schema version
    url = f"{schema_registry_url}/subjects/product-value/versions/1"
    response = requests.get(url)
    assert response.status_code == 200
    assert "schema" in response.json()

