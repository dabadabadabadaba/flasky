def test_get_all_breakfasts_with_empty_db_returns_empty_list(client): #taking in our client fixture in conftest.py
    response = client.get("/breakfast") #will run a GET request
    response_body = response.get_json()

    assert response.status_code == 200 # attribute that let's us get the status from the response
    assert response_body == []


def test_get_one_breakfast_with_empty_db_returns_404(client): # with every new test we write with client, an entirely new database is created and then removed
    response = client.get("/breakfast/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert "msg" in response_body

def test_get_one_breakfast_with_populated_db_returns_breakfast_json(client, two_breakfasts):
    response = client.get("/breakfast/1")
    response_body = response.get_json()
    
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "doughnut", 
        "rating": 5.0, 
        "prep_time" : 1
    }

def test_post_one_breakfast_creates_breakfast_in_db(client, two_breakfasts):
    response = client.post("/breakfast", json={
        "name": "New Breakfast",
        "prep_time": 3,
        "rating": 3.0
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert "msg" in response_body
    assert response_body["msg"] == "Successfully created Breakfast with id# 3"



