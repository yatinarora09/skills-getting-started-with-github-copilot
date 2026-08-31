import copy
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import app as app_module


@pytest.fixture
def client():
    app_module.activities = copy.deepcopy(app_module.activities)
    with TestClient(app_module.app) as test_client:
        yield test_client

    app_module.activities = copy.deepcopy(app_module.activities)


def test_unregister_participant_removes_email_from_activity(client):
    # Arrange
    email = "new.student@mergington.edu"

    # Act
    signup_response = client.post(f"/activities/Chess Club/signup?email={email}")
    unregister_response = client.delete(f"/activities/Chess Club/unregister?email={email}")

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Unregistered {email} from Chess Club"

    activity = client.get("/activities").json()["Chess Club"]
    assert email not in activity["participants"]


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/Chess Club/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_get_activities_returns_activity_list(client):
    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert "Chess Club" in body
    assert "participants" in body["Chess Club"]
