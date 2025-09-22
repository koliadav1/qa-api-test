def test_create_question(client):
    response = client.post(
        "/questions/",
        json={"text": "Test question?"}
    )
    assert response.status_code == 201
    assert response.json()["text"] == "Test question?"
    assert "id" in response.json()

def test_create_answer(client, test_question):
    response = client.post(
        f"/questions/{test_question['id']}/answers",
        json={"text": "Test answer", "user_id": "test-user-123"}
    )
    assert response.status_code == 201
    assert response.json()["text"] == "Test answer"
    assert response.json()["user_id"] == "test-user-123"

def test_get_question_with_answers(client, test_question):
    answer_response = client.post(
        f"/questions/{test_question['id']}/answers",
        json={"text": "Test answer", "user_id": "test-user-123"}
    )
    assert answer_response.status_code == 201

    response = client.get(f"/questions/{test_question['id']}")
    assert response.status_code == 200
    assert response.json()["text"] == test_question["text"]
    assert len(response.json()["answers"]) == 1

def test_delete_question_cascades(client, test_question):
    answer_response = client.post(
        f"/questions/{test_question['id']}/answers",
        json={"text": "Test answer", "user_id": "test-user-123"}
    )
    assert answer_response.status_code == 201
    answer_id = answer_response.json()["id"]

    delete_response = client.delete(f"/questions/{test_question['id']}")
    assert delete_response.status_code == 204

    answer_check = client.get(f"/answers/{answer_id}")
    assert answer_check.status_code == 404

def test_get_nonexistent_question(client):
    response = client.get("/questions/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Question not found"

def test_create_answer_nonexistent_question(client):
    response = client.post(
        "/questions/999/answers",
        json={"text": "Test answer", "user_id": "test-user-123"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Question not found"

def test_get_nonexistent_answer(client):
    response = client.get("/answers/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Answer not found"

def test_validation_empty_text(client):
    response = client.post(
        "/questions/",
        json={"text": ""}
    )
    assert response.status_code == 422

    question_response = client.post(
        "/questions/",
        json={"text": "Valid question?"}
    )
    assert question_response.status_code == 201
    question_id = question_response.json()["id"]

    response = client.post(
        f"/questions/{question_id}/answers",
        json={"text": "", "user_id": "test-user"}
    )
    assert response.status_code == 422