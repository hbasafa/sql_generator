import re


def test_check_health(test_client):
    http_response = test_client.get("/health")

    assert http_response.status_code == 200
    response = http_response.json()

    assert "status" in response
    assert response["status"] == "ok"


def test_generate_sql(test_client):
    http_response = test_client.post("/generate_sql", json={"question": "What is the total revenue for the year 2022?"})

    assert http_response.status_code == 200
    response = http_response.json()

    assert "sql_query" in response
    assert re.match(r"SELECT[.\s\(\)\n]+", response["sql_query"])

    assert "summary" in response
    assert re.match(r".+", response["summary"])


# TODO: add http error tests
