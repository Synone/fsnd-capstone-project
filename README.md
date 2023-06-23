# Library management - Backend Service Only

- The application provides endpoints to manage library database, including books, authors, patrons and book loan tickets.
- There are 3 main roles:
  1. Owner: who has all permission (ADD, DELETE, UPDATE books, GET book details; ADD and DELETE patron membership, GET patron details).
  2. Librarian: who has almost all permission except DELETE books and DELETE patorn membership.
  3. Patron: who can only see all avaiable books and see patron detail in scenario provided its id.

## APPLICATION URI:

- https://capstone-project-fe80.onrender.com

### To get Auth0 token for testing

- Login: http://fsnd-sony-dev.us.auth0.com/authorize?audience=library&response_type=token&client_id=gcSFQLonNh6evPtrDTKPzhwaWqGuOByX&redirect_uri=http://localhost:4200
- Token available for all permissions - (Update date: ): `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNXemNmRXdUb2Ywc2pfdWZLbzNNcSJ9.eyJ1c2VyLWVtYWlsIjoic29uaWU5MjMzQGdtYWlsLmNvbSIsImlzcyI6Imh0dHBzOi8vZnNuZC1zb255LWRldi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjQ2NzMyZDdjM2YzYThlMDhhY2ZjMjM0IiwiYXVkIjoibGlicmFyeSIsImlhdCI6MTY4NzMzMjkzMCwiZXhwIjoxNjg3MzQwMTMwLCJhenAiOiJnY1NGUUxvbk5oNmV2UHRyRFRLUHpod2FXcUd1T0J5WCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmJvb2tzIiwiZ2V0OmJvb2stZGV0YWlsIiwiZ2V0OmJvb2tzIiwiZ2V0OnBhdHJpb24tZGV0YWlsIiwicG9zdDpib29rLWxvYW4tdGlja2V0IiwicG9zdDpib29rcyIsInBvc3Q6cGF0cm9uIiwidXBkYXRlOmJvb2tzIl19.mf0zusOK7BE149sJ9jB78R4dk4zQpi4cs7yA8MpelzGv4ovok6JE5X06nFo0e9bZNSLMLQ\_\_T3QhFDLUfJjBmclaonBvPnd5rk0jnBQqjMAH7kf8zn4JRP73ztLpgWaDIjRebStREQzpayWXormYUKHQQfI5oH7t8sRhfES3knZuiWBKtxD7hdM8F4AAscU4nf7yEGjhzorPw_g7oRt6oKNtuuzt3B05XtQZ5R8SN41h17l33psNjQgXfs9fVLJcIVaheGR_rpTmC5zwfdKVlYfzwHM0cS4UvSibHKH8eUAKgaT6QTjscYOJcjv8SA1uRqjCRXXpUi0C4qr44RLKRQ`
- Token for librarian, cannot delete books:
- Token only for get general information about books:

- Account with role Library Owner, who has all permission: username: udacityadmin@gmail.com - password: Udacitypass3
- Account with role Librarian, who has almost permission but not delete books: udacitymanager@gmail.com - password: Udacitypass2
- Account with role Patron, who can only see available books: udacitybarista@gmail.com - password: Udacitypass1
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
