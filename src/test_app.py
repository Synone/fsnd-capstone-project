import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from model import setup_db, Books, Author, Patrons
from model import db

database_test_name  = os.getenv('DATABASE_TEST_NAME','library_test')
# for local testing
db_user = "postgres"
db_password = "03031998"
db_host = "localhost:5432"
token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNXemNmRXdUb2Ywc2pfdWZLbzNNcSJ9.eyJ1c2VyLWVtYWlsIjoic29uaWU5MjMzQGdtYWlsLmNvbSIsImlzcyI6Imh0dHBzOi8vZnNuZC1zb255LWRldi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjQ2NzMyZDdjM2YzYThlMDhhY2ZjMjM0IiwiYXVkIjoibGlicmFyeSIsImlhdCI6MTY4NzQ4ODMwNCwiZXhwIjoxNjg3NDk1NTA0LCJhenAiOiJnY1NGUUxvbk5oNmV2UHRyRFRLUHpod2FXcUd1T0J5WCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmJvb2tzIiwiZGVsZXRlOnBhdHJvbiIsImdldDphbGwtcGF0cm9ucyIsImdldDpib29rLWRldGFpbCIsImdldDpib29rcyIsImdldDpwYXRyaW9uLWRldGFpbCIsInBvc3Q6Ym9vay1sb2FuLXRpY2tldCIsInBvc3Q6Ym9va3MiLCJwb3N0OnBhdHJvbiIsInVwZGF0ZTpib29rcyJdfQ.xhY5DsmLIcAtD-kgrOSKWtf35rVIrY97TFz6BfP40d6i9XK-Gwxb7F_7PYLnB4MRvrx1iSw_xYuOXgAAUOQDSeLCcXGNTmkrRgy852egfND5-99PpTVuBqU_I6vOvtj4mIFy_-PcWaH9XHWaP-MTtstrwLeMRWvP1B0uRKRsCpq3K3XCgDrRHe1Hr9_RKXwqikpad6NNmmuLn6N2K8Je1vKPxWjIivpT1XBEKLgZPwg8qwV5dB2gdmw_ZlzLZjg047mBSXu15n9DiTIqqqWWJOg2-z0PLpVkrN6aDFdmfOsKZN4S2ZblZ-tkLffFJqhA2_VNIQqXez3KhjD3ZIAdFA"

class LibraryTestCase(unittest.TestCase):
    
    def setUp(self):
        self.database_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(db_user,db_password,db_host, database_test_name)
        self.app_test = create_app(self.database_path)
        self.client = self.app_test.test_client
        # setup_db(self.app_test, self.database_path)
        self.new_book = {"title":"Harry potter chapter2",
                        "author":"J.K Rowling",
                        "numbers_in_stock":12,
                        "days_for_borrow": 12,
                        "genres": "Thriller, Fiction, Mystery",
                        "pages":356,
                        "status":"new",
                        "author_gender":"female",
                        "author_country":"America"}
        self.invalid_book={"title":"Fail book",
                        "author":"J.K Rowling",
                        "numbers_in_stock":12,
                        "days_for_borrow": 12,
                        "genres": "Thriller, Fiction, Mystery",
                        "pages":356,
                        "status":"new",
                        "author_gender":"female"}
        self.headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
    def tearDown(self):
        pass    

    def test_retrieve_all_books(self):
        res = self.client().get('/books')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
    def test_add_new_book(self):
        res = self.client().post('/books', headers=self.headers, json=self.new_book, )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["message"],'Book added successfully')
    def test_400_creat_can_not_process(self):
        res = self.client().post("/books",headers=self.headers, json=self.invalid_book)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['message'],"Cannot process request due to inappropriate request payload")
        
    
    
if __name__ == "__main__":
    unittest.main()
    