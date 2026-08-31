import copy
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient
from app import app, activities as initial_activities


client = TestClient(app)


def setup_function():
    import app as app_module

    app_module.activities = copy.deepcopy(initial_activities)


def test_unregister_participant_removes_email_from_activity():
    email = "new.student@mergington.edu"

    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 200

    response = client.delete(f"/activities/Chess Club/unregister?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Chess Club"

    activity = client.get("/activities").json()["Chess Club"]
    assert email not in activity["participants"]
