import pytest

import api.database.db_models as db_mod
from api.enums import SearchType


class TestSearchRoutes:
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, request, client, db_session):
        request.cls.client = client
        request.cls.db_session = db_session

        self._cleanup_search_test_data()
        self._prepare_search_test_data()
        request.addfinalizer(self._cleanup_search_test_data)

    def _prepare_search_test_data(self):
        print('_prepare_search_test_data')
        pharmacy3 = db_mod.Pharmacy(name="Wired dog", cash_balance=700)
        pharmacy4 = db_mod.Pharmacy(name="Wizard cat", cash_balance=700)
        mask3 = db_mod.Mask(name="N95")
        mask4 = db_mod.Mask(name="3M")

        self.db_session.add_all([pharmacy3, pharmacy4, mask3, mask4])
        self.db_session.commit()

    def _cleanup_search_test_data(self):
        self.db_session.query(db_mod.Pharmacy).filter(
            db_mod.Pharmacy.name.in_(["Wired dog", "Wizard cat"])
        ).delete(synchronize_session=False)
        self.db_session.query(db_mod.Mask).filter(
            db_mod.Mask.name.in_(["N95", "3M"])
        ).delete(synchronize_session=False)
        self.db_session.commit()

    @pytest.mark.parametrize(
        "search_term, search_type, offset, limit, expected_results", [
            ("N95", SearchType.MASK.value, 0, 10,
             [{"name": "N95", "type": "mask"}]),
            ("3M", SearchType.MASK.value, 0, 10,
             [{"name": "3M", "type": "mask"}]),
            ("dog", SearchType.PHARMACY.value, 0, 10,
             [{"name": "Wired dog", "type": "pharmacy"}]),
            ("cat", SearchType.PHARMACY.value, 0, 10,
             [{"name": "Wizard cat", "type": "pharmacy"}]),
            ("NN", SearchType.ALL.value, 0, 10,
             [{"name": "N95", "type": "mask"}]),
            ("WW", SearchType.ALL.value, 0, 10,
             [{"name": "Wired dog", "type": "pharmacy"},
              {"name": "Wizard cat", "type": "pharmacy"}]),
        ])
    def test_search_entities(self, search_term, search_type, offset, limit,
                             expected_results):
        response = self.client.get(
            "/search",
            params={
                "search_term": search_term,
                "search_type": search_type,
                "offset": offset,
                "limit": limit,
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == len(expected_results)

        for item, expected in zip(data, expected_results):
            assert item["name"] == expected["name"]
            assert item["type"] == expected["type"]
