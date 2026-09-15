import unittest

from fastapi.testclient import TestClient

from api import create_app


class TestAPI(unittest.TestCase):
    def setUp(self):
        # Every test receives fresh application data.
        self.client = TestClient(create_app())
        self.client.__enter__()

        items = self.client.get("/items").json()
        members = self.client.get("/members").json()

        self.loan = {
            "item_id": items[0]["item_id"],
            "member_id": members[0]["member_id"],
        }

    def tearDown(self):
        self.client.__exit__(None, None, None)

    def test_list_items(self):
        response = self.client.get("/items")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)

    def test_borrow_and_return(self):
        borrowed = self.client.post("/loans", json=self.loan)
        self.assertEqual(borrowed.status_code, 201)
        self.assertIsNone(borrowed.json()["return_date"])

        returned = self.client.post("/returns", json=self.loan)
        self.assertEqual(returned.status_code, 200)
        self.assertIsNotNone(returned.json()["return_date"])

    def test_duplicate_borrow(self):
        self.client.post("/loans", json=self.loan)
        response = self.client.post("/loans", json=self.loan)
        self.assertEqual(response.status_code, 409)

    def test_missing_item(self):
        data = {**self.loan, "item_id": 999999999}
        response = self.client.post("/loans", json=data)
        self.assertEqual(response.status_code, 404)

    def test_invalid_input(self):
        data = {**self.loan, "item_id": -1}
        response = self.client.post("/loans", json=data)
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()