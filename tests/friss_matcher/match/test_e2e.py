"""End to End tests for /match endpoint."""
import pytest

from functools import partial


@pytest.fixture
def client_match_post(client_auth):
    return partial(client_auth.post, "/match/", format="json")


pytestmark = pytest.mark.django_db


class TestMatch:

    ENDPOINT = "/match/"
    NOT_IMPLEMENTED_METHODS = (
        'put',
        'delete',
        'patch',
        'trace',
    )

    @pytest.mark.parametrize("http_method", NOT_IMPLEMENTED_METHODS)
    def test_not_implemented_methods(self, client_auth, http_method):
        method = getattr(client_auth, http_method)
        r = method(self.ENDPOINT)

        assert r.status_code == 405

    def test_without_trailing_slash(self, client_auth):
        r = client_auth.post("/match", data={})

        assert r.status_code == 301

    def test_empty_data(self, client_match_post):
        expected_response = {
            "person_1": ["This field is required."],
            "person_2": ["This field is required."],
        }
        r = client_match_post(data={})

        assert r.status_code == 400
        assert r.json() == expected_response

    def test_missing_one_person(self, client_match_post):
        expected_response = {
            "person_1": ["This field is required."],
            "person_2": {
                "first_name": ["This field is required."],
                "last_name": ["This field is required."],
            },
        }
        r = client_match_post(data={"person_2": {}})

        assert r.status_code == 400
        assert r.json() == expected_response

    def test_empty_persons(self, client_match_post):
        expected_response = {
            "person_1": {
                "first_name": ["This field is required."],
                "last_name": ["This field is required."],
            },
            "person_2": {
                "first_name": ["This field is required."],
                "last_name": ["This field is required."],
            },
        }
        r = client_match_post(data={"person_1": {}, "person_2": {}})

        assert r.status_code == 400
        assert r.json() == expected_response
