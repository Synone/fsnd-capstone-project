# Library management - Backend Service Only

- The application provides endpoints to manage library database, including books, authors, patrons and book loan tickets.
- There are 3 main roles:
  1. Owner: who has all permission (ADD, DELETE, UPDATE books, GET book details; ADD and DELETE patron membership, GET patron details).
  2. Librarian: who has almost all permission except DELETE books and DELETE patorn membership.
  3. Patron: who can only see all avaiable books and see patron detail in scenario provided its id.

## APPLICATION URI:

- https://capstone-project-fe80.onrender.com

### To get Auth0 token for testing

- Login URI: http://fsnd-sony-dev.us.auth0.com/authorize?audience=library&response_type=token&client_id=gcSFQLonNh6evPtrDTKPzhwaWqGuOByX&redirect_uri=http://localhost:4200
- Account with role Library Owner, who has all permission: username: udacityadmin@gmail.com - password: Udacitypass3
- Account with role Librarian, who has almost permission but not delete books: udacitymanager@gmail.com - password: Udacitypass2
- Account with role Patron, who can only see available books: udacitybarista@gmail.com - password: Udacitypass3
- Token available for all permissions - (Update time: ): `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNXemNmRXdUb2Ywc2pfdWZLbzNNcSJ9.eyJ1c2VyLWVtYWlsIjoic29uaWU5MjMzQGdtYWlsLmNvbSIsImlzcyI6Imh0dHBzOi8vZnNuZC1zb255LWRldi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjQ2NzMyZDdjM2YzYThlMDhhY2ZjMjM0IiwiYXVkIjoibGlicmFyeSIsImlhdCI6MTY4NzQ4OTk3MiwiZXhwIjoxNjg3NTc2MzcyLCJhenAiOiJnY1NGUUxvbk5oNmV2UHRyRFRLUHpod2FXcUd1T0J5WCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmJvb2tzIiwiZGVsZXRlOnBhdHJvbiIsImdldDphbGwtcGF0cm9ucyIsImdldDpib29rLWRldGFpbCIsImdldDpib29rcyIsImdldDpwYXRyaW9uLWRldGFpbCIsInBvc3Q6Ym9vay1sb2FuLXRpY2tldCIsInBvc3Q6Ym9va3MiLCJwb3N0OnBhdHJvbiIsInVwZGF0ZTpib29rcyJdfQ.NPaN33eTXBP5bP3-9oEuvrR0G5oGMMgHf2WeqwQ7C6v2RsLUbAOm49oNDTTGHfnSSpL3qbrhUYZby-llucZsekLEiOlxvhAf1jD6_KGgiVmhU5185-Qz-hwwGLxmkeA6fRka0sa3TP3SFiMscjpp0Bc2xfeRdI4I5uuohUvI6qN_4eD69SnAYla_52FSlx7z1_PYVt7XNANUgmteHLtrZcKXKLwOmT531PC49W3_myxBKuuhMPnEvk-Rx5zL1oRnF24KT2M7pMfgWIAA7NhJtWq59n0NmmlOQPP_yhC6LPCvPDDuZRNGu216nlCd0RP1OHMm6mG_M100ukuVH_8RpA`
- Token for librarian, cannot delete books: `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNXemNmRXdUb2Ywc2pfdWZLbzNNcSJ9.eyJ1c2VyLWVtYWlsIjoidWRhY2l0eW1hbmFnZXJAZ21haWwuY29tIiwiaXNzIjoiaHR0cHM6Ly9mc25kLXNvbnktZGV2LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NDcwNTk5OWIwODdmNTc4ZGNjOGFkZDAiLCJhdWQiOiJsaWJyYXJ5IiwiaWF0IjoxNjg3NDkxNTE0LCJleHAiOjE2ODc1Nzc5MTQsImF6cCI6ImdjU0ZRTG9uTmg2ZXZQdHJEVEtQemh3YVdxR3VPQnlYIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWxsLXBhdHJvbnMiLCJnZXQ6Ym9vay1kZXRhaWwiLCJnZXQ6Ym9va3MiLCJnZXQ6cGF0cmlvbi1kZXRhaWwiLCJwb3N0OmJvb2stbG9hbi10aWNrZXQiLCJwb3N0OmJvb2tzIiwicG9zdDpwYXRyb24iLCJ1cGRhdGU6Ym9va3MiXX0.vvEF1k57HXTY7h-arwourMa_JuZCeduFKlKIoDxG_jlE8O7d8Y84MWS0xqt_D9Hl2vB5rG2r04Sr-WbXbM2CKiICSYLj4FYXhb-pIqANoXLA7v7mfWLG07r7XuOwjynz7f2KZsdj-8NZ1SPE_hiaRdVZeYRN7hmuPXgnJWk6YnNb8nFYBTZ_EGXcm7CZnhhe98Slo5uEhIWeHCeKoy-2q3Sa7zAHt7x94B-oDsOu_mokBRNEYj16Xw69l8NS7mtAVCeZj_2zQz-RLjev0y9IP4NX4hue7hqMJyM2L6lQAuGGef253EhHGcPfMsRtE-THvxzcSd2Reu9lPcbM3GQKkA`
- Token only for get general information about books: `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNXemNmRXdUb2Ywc2pfdWZLbzNNcSJ9.eyJ1c2VyLWVtYWlsIjoidWRhY2l0eWJhcmlzdGFAZ21haWwuY29tIiwiaXNzIjoiaHR0cHM6Ly9mc25kLXNvbnktZGV2LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NDcwNTllNDkzNDhlNjljNmNjYWM5ZjQiLCJhdWQiOiJsaWJyYXJ5IiwiaWF0IjoxNjg3NDkwNjg0LCJleHAiOjE2ODc1NzcwODQsImF6cCI6ImdjU0ZRTG9uTmg2ZXZQdHJEVEtQemh3YVdxR3VPQnlYIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6Ym9va3MiLCJnZXQ6cGF0cmlvbi1kZXRhaWwiXX0.ouqtakV6YWfWTfJMlSHo9Lhrs4Nda9VEdYaKQr72CCnQkBwhd8FqsCtMhe3cLruW4OeYXWMnzyk9LDNoTgZ3_Zy83ztUpKFZRzWKYblkRxE-6oKz7uJR_vIxF-BSkZbjlJ78d1MZoneVZOxKVTJcCku2bbqejkvy__YGCD_Rpn8PF9mAOuPA5F752BMVHJ-ruKAe2_qC90YqE3RMGho1uo5YzRDaBXw8943zjzxdQfnX63JYkuwV1WlhE8dyZhgxpPD7w-BaxBjACcfoey3kTAwHJSng4wfJbl2EF3bd-fp5BsFyB6GmpNmz6BuBhhI9ys-pcmr8vaJ69z27cMfbpg`
  > Provided token will stay valid for 24hrs since update-time.
  > Note that login successfully will return token in the URL, use the token for testing endpoints on postman. No Interface provided.
  > Valid token will be updated initially when submitting project, in case any errors occur, please login to get the token.

## ENDPOINT EXAMPLES

`GET '/books'`

- Fetches a list of all books
- Request Arguments: None
- Returns: An object with a list of book objects, message and status

```json
{
  "data": [
    {
      "author": "John Grisham",
      "id": 1,
      "title": "The Testament"
    }
  ],
  "message": "OK",
  "success": true
}
```

`GET '/book-detail/book_id'`

- Get book detail by id
- Request Payload: book_id to query and see a specific book

```json
{
  "data": {
    "add_date": "2023/06/22 12:36:12",
    "author": "John Grisham",
    "days_for_borrow": 14,
    "genres": "Fiction, Novel, Modern Love",
    "id": 1,
    "in_stock": 6,
    "pages": 192,
    "status": "not available",
    "title": "The Testament"
  },
  "message": "Query book detail successfully",
  "status": "success",
  "statusCode": 200
}
```

`POST '/books' `

- Add new book to database
- Returns: A message confirm added book successfully, and status code 201
- Request Payload: A json represent the book data

```json
{
  "title": "Harry potter chapter 1",
  "author": "J.K Rowling",
  "numbers_in_stock": 42,
  "days_for_borrow": 14,
  "genres": "Thriller, Fiction, Mystery",
  "pages": 432,
  "status": "ready",
  "author_gender": "female",
  "author_country": "America"
}
```

`POST 'books/book_id'` <!--update books -->

- Update existing books, only update numbers in stock, status and days allowed for borrowing
- Returns: A message and status
- Request Payload: A json represent the update fields

```json
{
  "days_for_borrow": 10,
  "status": "not in good state",
  "numbers_in_stock": 1
}
```

`DELETE /books/book_id`

- Delete book from library
- Returns: A message confirms delete successfully and statusCode

```json
{
  "message": "Remove book successfully",
  "statusCode": 202
}
```

- Implements similar as books'endpoints:
  `GET /patrons`, `POST /patron`, `GET /patron-detail/patron_id`, `DELETE /patrons/patron_id`

`POST /book-loan`

- Create ticket for lending books to patrons
- Returns: A message confirm created ticket successfully, and a statuscode
- Request payload: book_id and patron_id

```json
    "book_id":"1",
    "patron_id":"1"
```

# Testing

- Please create a 'library_test' database and insert some recorsd for testing
