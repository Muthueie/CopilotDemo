"""Tests for Mergington High School API using AAA pattern."""

from src.app import activities


def test_get_activities(client):
    # Arrange
    expected_names = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Art Studio",
        "Music Band",
        "Debate Team",
        "Science Club",
    ]

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    for name in expected_names:
        assert name in data
        assert "participants" in data[name]
        assert isinstance(data[name]["participants"], list)


def test_signup_success(client):
    # Arrange
    email = "copytest1@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]
    assert email in activities[activity]["participants"]


def test_signup_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_invalid_activity(client):
    # Arrange
    activity = "No Such Club"
    email = "notreal@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_delete_participant_success(client):
    # Arrange
    activity = "Tennis Club"
    email = "sarah@mergington.edu"

    assert email in activities[activity]["participants"]

    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]


def test_delete_participant_not_found(client):
    # Arrange
    activity = "Tennis Club"
    email = "notthere@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_delete_activity_not_found(client):
    # Arrange
    activity = "No Such Club"
    email = "somebody@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
