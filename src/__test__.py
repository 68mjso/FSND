import unittest
from app import create_app
from models import setup_db, Movie, Actor
import json
import os

api_1 = os.environ("API_KEY_1")
api_2 = os.environ("API_KEY_2")
api_3 = os.environ("API_KEY_3")


class CastingAssistantTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        # setup_db(self.app)

        # Replace the tokens below with actual JWTs for each role
        self.casting_assistant_headers = {"Authorization": f"Bearer {api_1}"}
        self.casting_director_headers = {"Authorization": f"Bearer {api_2}"}
        self.executive_producer_headers = {"Authorization": f"Bearer {api_3}"}

        # Sample data
        self.new_movie = {
            "title": "Inception",
            "release_date": "2010-07-16",
            "actors": [],
        }
        self.new_actor = {"name": "Leonardo DiCaprio", "age": 45, "gender": "male"}

    def tearDown(self):
        """Executed after each test"""
        pass

    # Tests for Casting Assistant (view-only permissions)
    def test_casting_assistant_can_view_movies(self):
        res = self.client().get("/movies", headers=self.casting_assistant_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertTrue(isinstance(data["data"], list))

    def test_casting_assistant_can_view_actors(self):
        res = self.client().get("/actors", headers=self.casting_assistant_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertTrue(isinstance(data["data"], list))

    def test_casting_assistant_cannot_create_movie(self):
        res = self.client().post(
            "/movies", headers=self.casting_assistant_headers, json=self.new_movie
        )
        self.assertEqual(res.status_code, 403)

    def test_casting_assistant_cannot_create_actor(self):
        res = self.client().post(
            "/actors", headers=self.casting_assistant_headers, json=self.new_actor
        )
        self.assertEqual(res.status_code, 403)

    def test_casting_director_can_add_actor(self):
        res = self.client().post(
            "/actors", headers=self.casting_director_headers, json=self.new_actor
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertTrue(data["success"])

    def test_casting_director_can_delete_actor(self):
        res = self.client().delete("/actors/1", headers=self.casting_director_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertTrue(data["success"])

    def test_casting_director_can_update_movie(self):
        # Assuming movie with ID 1 exists
        res = self.client().patch(
            "/movies/1",
            headers=self.casting_director_headers,
            json={
                "title": "Inception Updated",
                "release_date": "2010-07-17",
                "actors": [],
            },
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertTrue(data["success"])

    def test_casting_director_cannot_delete_movie(self):
        res = self.client().delete("/movies/1", headers=self.casting_director_headers)
        self.assertEqual(res.status_code, 403)

    def test_executive_producer_can_add_movie(self):
        res = self.client().post(
            "/movies", headers=self.executive_producer_headers, json=self.new_movie
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertTrue(data["success"])

    def test_executive_producer_can_delete_movie(self):
        res = self.client().delete("/movies/1", headers=self.executive_producer_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertTrue(data["success"])

    def test_executive_producer_can_view_actors(self):
        res = self.client().get("/actors", headers=self.executive_producer_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertTrue(isinstance(data["data"], list))

    def test_unauthorized_access(self):
        res = self.client().get("/movies")
        self.assertEqual(res.status_code, 401)


if __name__ == "__main__":
    unittest.main()
