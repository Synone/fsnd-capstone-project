import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from model import setup_db, Books, Author, Patrons
from model import db

database_test_name  = os.getenv('DATABASE_TEST_NAME','library_test')
# for local testing
db_user = "postgres" #replace with your db user
db_password = "03031998" #replace with your db password for db user
db_host = "localhost:5432" 
token_admin = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNXemNmRXdUb2Ywc2pfdWZLbzNNcSJ9.eyJ1c2VyLWVtYWlsIjoic29uaWU5MjMzQGdtYWlsLmNvbSIsImlzcyI6Imh0dHBzOi8vZnNuZC1zb255LWRldi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjQ2NzMyZDdjM2YzYThlMDhhY2ZjMjM0IiwiYXVkIjoibGlicmFyeSIsImlhdCI6MTY4NzQ4OTk3MiwiZXhwIjoxNjg3NTc2MzcyLCJhenAiOiJnY1NGUUxvbk5oNmV2UHRyRFRLUHpod2FXcUd1T0J5WCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmJvb2tzIiwiZGVsZXRlOnBhdHJvbiIsImdldDphbGwtcGF0cm9ucyIsImdldDpib29rLWRldGFpbCIsImdldDpib29rcyIsImdldDpwYXRyaW9uLWRldGFpbCIsInBvc3Q6Ym9vay1sb2FuLXRpY2tldCIsInBvc3Q6Ym9va3MiLCJwb3N0OnBhdHJvbiIsInVwZGF0ZTpib29rcyJdfQ.NPaN33eTXBP5bP3-9oEuvrR0G5oGMMgHf2WeqwQ7C6v2RsLUbAOm49oNDTTGHfnSSpL3qbrhUYZby-llucZsekLEiOlxvhAf1jD6_KGgiVmhU5185-Qz-hwwGLxmkeA6fRka0sa3TP3SFiMscjpp0Bc2xfeRdI4I5uuohUvI6qN_4eD69SnAYla_52FSlx7z1_PYVt7XNANUgmteHLtrZcKXKLwOmT531PC49W3_myxBKuuhMPnEvk-Rx5zL1oRnF24KT2M7pMfgWIAA7NhJtWq59n0NmmlOQPP_yhC6LPCvPDDuZRNGu216nlCd0RP1OHMm6mG_M100ukuVH_8RpA"
toekn_patron ="Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNXemNmRXdUb2Ywc2pfdWZLbzNNcSJ9.eyJ1c2VyLWVtYWlsIjoidWRhY2l0eWJhcmlzdGFAZ21haWwuY29tIiwiaXNzIjoiaHR0cHM6Ly9mc25kLXNvbnktZGV2LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NDcwNTllNDkzNDhlNjljNmNjYWM5ZjQiLCJhdWQiOiJsaWJyYXJ5IiwiaWF0IjoxNjg3NDkwNjg0LCJleHAiOjE2ODc1NzcwODQsImF6cCI6ImdjU0ZRTG9uTmg2ZXZQdHJEVEtQemh3YVdxR3VPQnlYIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6Ym9va3MiLCJnZXQ6cGF0cmlvbi1kZXRhaWwiXX0.ouqtakV6YWfWTfJMlSHo9Lhrs4Nda9VEdYaKQr72CCnQkBwhd8FqsCtMhe3cLruW4OeYXWMnzyk9LDNoTgZ3_Zy83ztUpKFZRzWKYblkRxE-6oKz7uJR_vIxF-BSkZbjlJ78d1MZoneVZOxKVTJcCku2bbqejkvy__YGCD_Rpn8PF9mAOuPA5F752BMVHJ-ruKAe2_qC90YqE3RMGho1uo5YzRDaBXw8943zjzxdQfnX63JYkuwV1WlhE8dyZhgxpPD7w-BaxBjACcfoey3kTAwHJSng4wfJbl2EF3bd-fp5BsFyB6GmpNmz6BuBhhI9ys-pcmr8vaJ69z27cMfbpg"

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
            'Authorization': token_admin,
            'Content-Type': 'application/json'
        }
        self.headers_patron = {
            'Authorization': toekn_patron,
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
        
    def test_delete_book_with_libowner_token(self):
        res = self.client().delete('/books/2', headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,202)
        self.assertEqual(data['message'],'Remove book successfully')
        
    def test_403_unauthorized_post_book_with_patron_token(self):
        res = self.client().post('/books',headers = self.headers_patron, json=self.new_book)
        self.assertEqual(res.status_code,403)
    def test_403_unauthorized_delete_book_with_patron_token(self):
        res = self.client().delete('/books/2',headers = self.headers_patron)
        self.assertEqual(res.status_code,403)
    
    
if __name__ == "__main__":
    unittest.main()
    