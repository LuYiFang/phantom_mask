import pytest
from api.enums import DayOfWeek, SortType, ComparisonType


class TestPharmacyRoutes:
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, request, client, db_session):
        request.cls.client = client
        request.cls.db_session = db_session

    @pytest.mark.parametrize("query_time, day_of_week, expected_status", [
        ('14:30', DayOfWeek.MON.value, 200),
        ('07:00', DayOfWeek.SUN.value, 200),
        ('20:00', DayOfWeek.MON.value, 200),
        ('11:00', DayOfWeek.FRI.value, 200),
    ])
    def test_get_pharmacies_open_at(self, query_time, day_of_week,
                                    expected_status):
        params = {"query_time": query_time, "day_of_week": day_of_week}
        response = self.client.get("/pharmacies/open/at", params=params)
        assert response.status_code == expected_status
        data = response.json()
        assert isinstance(data, list)
        if day_of_week == DayOfWeek.MON and query_time == '14:30':
            assert len(data) > 0
            assert data[0]["name"] == "Pharmacy One"
        else:
            assert len(data) == 0

    @pytest.mark.parametrize("params, expected", [
        (
                {"sort_by": SortType.NAME.value, "skip": 0, "limit": 10},
                [{"name": "Adult Mask"}, {"name": "Child Mask"}]
        ),
        (
                {"sort_by": SortType.PRICE.value, "skip": 0, "limit": 10},
                [{"price": 30.00}, {"price": 50.00}]
        ),
        (
                {"sort_by": SortType.NAME.value, "skip": 0, "limit": 1},
                [{"name": "Adult Mask"}]
        ),
        (
                {"sort_by": SortType.NAME.value, "skip": 1, "limit": 1},
                [{"name": "Child Mask"}]
        ),
    ])
    def test_list_masks(self, params, expected):
        response = self.client.get("/pharmacies/1/masks", params=params)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == len(expected)
        for i, mask in enumerate(expected):
            for key, value in mask.items():
                assert data[i][key] == value

    @pytest.mark.parametrize(
        "comparison, count, min_price, max_price, expected", [
            (
                    ComparisonType.MORE.value, 1, 30.00, 50.00,
                    [
                        {"id": 1, "name": "Pharmacy One", "mask_count": 2},
                    ]
            ),
            (
                    ComparisonType.LESS.value, 2, 50.00, 70.00,
                    [
                        {"id": 1, "name": "Pharmacy One", "mask_count": 1},
                    ]
            ),
            (
                    ComparisonType.MORE.value, 0, 30.00, 70.00,
                    [
                        {"id": 1, "name": "Pharmacy One", "mask_count": 2},
                        {"id": 2, "name": "Pharmacy Two", "mask_count": 2}
                    ]
            ),
            (
                    ComparisonType.LESS.value, 1, 70.00, 100.00,
                    []
            )
        ])
    def test_list_pharmacies_by_mask_count(self, comparison, count,
                                           min_price, max_price, expected):
        params = {
            "comparison": comparison,
            "count": count,
            "min_price": min_price,
            "max_price": max_price,
            "skip": 0,
            "limit": 10
        }
        response = self.client.get("/pharmacies/filters/masks/count",
                                   params=params)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == len(expected)
        for i, pharmacy in enumerate(expected):
            for key, value in pharmacy.items():
                assert data[i][key] == value
