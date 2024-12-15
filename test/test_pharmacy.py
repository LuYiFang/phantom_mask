import pytest

from api.enums import DayOfWeek


class TestPharmacyRoutes:
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, request, client, db_session):
        request.cls.client = client
        request.cls.db_session = db_session
        self.client = client
        self.db_session = db_session

    @pytest.mark.parametrize("query_time, day_of_week, expected_status", [
        ('14:30', 'Mon', 200),
        ('07:00', 'Sun', 200),
        ('20:00', 'Mon', 200),
        ('11:00', 'Fri', 200),
    ])
    def test_get_pharmacies_open_at(self, query_time,
                                    day_of_week, expected_status):
        response = self.client.get(
            "/pharmacies/open/at",
            params={"query_time": query_time,
                    "day_of_week": day_of_week}
        )
        assert response.status_code == expected_status
        data = response.json()
        assert isinstance(data, list)
        if day_of_week == DayOfWeek.Mon and query_time == '14:30':
            assert len(data) > 0
            assert data[0]["name"] == "Pharmacy One"
        else:
            assert len(data) == 0
