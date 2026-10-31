"""Verifica o contrato HTTP, incluindo erros e isolamento do armazenamento."""
import unittest

from fastapi.testclient import TestClient

from app.main import create_app


class ApiContractTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(create_app())
        self.addCleanup(self.client.close)

    def test_health_and_empty_list(self):
        self.assertEqual(self.client.get("/health").json(), {"status": "ok"})
        self.assertEqual(self.client.get("/tarefas").json(), [])

    def test_create_read_update_and_list(self):
        response = self.client.post("/tarefas", json={"titulo": "estudar APIs"})
        self.assertEqual(response.status_code, 201)
        original = {"id": 1, "titulo": "estudar APIs", "concluida": False}
        self.assertEqual(response.json(), original)
        self.assertEqual(self.client.get("/tarefas/1").json(), original)
        updated = {"id": 1, "titulo": "estudar APIs REST", "concluida": True}
        response = self.client.put("/tarefas/1", json={
            "titulo": updated["titulo"], "concluida": True,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), updated)
        self.assertEqual(self.client.get("/tarefas/1").json(), updated)
        self.assertEqual(self.client.get("/tarefas").json(), [updated])
        second = self.client.post("/tarefas", json={"titulo": "segunda"}).json()
        self.assertEqual(second["id"], 2)
        self.assertIs(second["concluida"], False)

    def test_missing_resources_are_not_created_by_put(self):
        self.assertEqual(self.client.get("/tarefas/999").status_code, 404)
        response = self.client.put("/tarefas/999", json={
            "titulo": "ausente", "concluida": True,
        })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.client.get("/tarefas").json(), [])

    def test_validation_rejects_invalid_payloads(self):
        for body in ({}, {"titulo": ""}, {"titulo": "   "}):
            self.assertEqual(self.client.post("/tarefas", json=body).status_code, 422)
        self.client.post("/tarefas", json={"titulo": "valida"})
        for body in ({"titulo": "sem status"}, {"titulo": "x", "concluida": "true"}):
            self.assertEqual(self.client.put("/tarefas/1", json=body).status_code, 422)

    def test_new_application_starts_with_empty_store(self):
        self.client.post("/tarefas", json={"titulo": "antiga"})
        with TestClient(create_app()) as fresh:
            self.assertEqual(fresh.get("/tarefas").json(), [])
            self.assertEqual(fresh.post("/tarefas", json={"titulo": "nova"}).json()["id"], 1)


if __name__ == "__main__":
    unittest.main()

