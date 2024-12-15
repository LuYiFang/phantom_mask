import pytest


class TestUserRoutes:
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, request, client, db_session):
        request.cls.client = client
        request.cls.db_session = db_session

    @pytest.mark.parametrize("start_date, end_date, limit, expected", [
        ("2024-10-01", "2024-10-31", 1,
         [{"id": 1, "name": "User One", "total_amount": 50.00}]),
        ("2024-10-01", "2024-10-31", 2,
         [{"id": 1, "name": "User One", "total_amount": 50.00},
          {"id": 2, "name": "User Two", "total_amount": 40.00}]),
        ("2024-10-01", "2024-11-08", 2,
         [{"id": 2, "name": "User Two", "total_amount": 90.00},
          {"id": 1, "name": "User One", "total_amount": 50.00}]),
        ("2024-11-01", "2024-11-30", 1,
         [{"id": 2, "name": "User Two", "total_amount": 50.00}])
    ])
    def test_get_top_users_by_transaction_amount(self, start_date: str,
                                                 end_date: str, limit: int,
                                                 expected: list):
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "limit": limit
        }
        response = self.client.get("/users/transaction_amount", params=params)
        assert response.status_code == 200
        data = response.json()
        print('data\n', data)
        assert isinstance(data, list)
        assert len(data) == len(expected)
        for i, user_summary in enumerate(expected):
            for key, value in user_summary.items():
                assert data[i][key] == value
