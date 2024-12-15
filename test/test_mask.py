import pytest
from api.enums import SortType


class TestMaskRoutes:
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, request, client, db_session):
        request.cls.client = client
        request.cls.db_session = db_session

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
        response = self.client.get("/masks/pharmacies/1", params=params)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == len(expected)
        for i, mask in enumerate(expected):
            for key, value in mask.items():
                assert data[i][key] == value

    @pytest.mark.parametrize("start_date, end_date, expected", [
        ("2024-10-01", "2024-10-31", [
            {"mask_id": 1, "mask_name": "Adult Mask", "mask_count": 2,
             "total_value": 50.00},
            {"mask_id": 2, "mask_name": "Child Mask", "mask_count": 1,
             "total_value": 40.00}
        ]),
        ("2024-10-01", "2024-10-01", [
            {"mask_id": 1, "mask_name": "Adult Mask", "mask_count": 1,
             "total_value": 20.00}
        ]),
        ("2024-10-01", "2024-11-08", [
            {"mask_id": 1, "mask_name": "Adult Mask", "mask_count": 2,
             "total_value": 50.00},
            {"mask_id": 2, "mask_name": "Child Mask", "mask_count": 2,
             "total_value": 90.00}
        ]),
        ("2024-11-01", "2024-11-30", [
            {"mask_id": 2, "mask_name": "Child Mask", "mask_count": 1,
             "total_value": 50.00}
        ])
    ])
    def test_get_mask_summary(self, start_date, end_date, expected):
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        response = self.client.get("/masks/transactions/summary",
                                   params=params)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == len(expected)
        for i, mask_summary in enumerate(expected):
            for key, value in mask_summary.items():
                assert data[i][key] == value
