import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
import sys
from model import Books, Author, APP, db, book_lends
from auth.auth import AuthError, requires_auth
from datetime import datetime



CORS(APP)
@APP.after_request
def after_request(response):
    response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization,true"
        )
    response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        
    return response


# ROUTES
@APP.route('/books', methods=['GET'])
def get_all_books():
    try:
        book_data = Books.query.order_by(Books.id).all()
        print(book_data)
    except:
        abort(404)
    
    return jsonify({
        "message":"OK",
        "books": [book.short() for book in book_data],
        "success": True
    }),200
    

@APP.route('/book-detail', methods=['GET'])
@requires_auth('get:book-detail')
def get_all_books_detail(jwt):
    try:
        book_data = Books.query.order_by(Books.id).all()
    except:
        abort(404)
    return jsonify({
        "message":"OK",
        "books": [book.long() for book in book_data],
        "success": True
    }),200


@APP.route('/books', methods=['POST'])
@requires_auth("post:books")
def add_book(jwt):
    body = request.get_json()
    author_name = body['author']
    author_id = 0
    author = Author.query.filter(Author.name == author_name).first()
    authors = Author.query.all()
    error = False
    if author is not None:
        author_id = author.id
    else:
        author_id = len(authors) + 1
    print(author_id)
    try:
        new_book = Books(
            title=body['title'], 
            author=body['author'], 
            numbers_in_stock= body['numbers_in_stock'],
            add_date=datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            genres=body['genres'],
            pages=body['pages'], 
            status=body['status'], 
            author_id=author_id, 
            days_for_borrow=body['days_for_borrow'])
        db.session.add(new_book)
        db.session.commit()
    except:
        error = True    
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if not error:
            return jsonify({
                "message":"Book added successfully",
                "statusCode":201
            }),201
        else:
            abort(500)


# @app.route('/books/<int:book_id>', methods=['PATCH'])
# @requires_auth("patch:books")
# def update_drink(jwt,book_id):
#     body = request.get_json()
#     drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
#     if drink is None:
#         return jsonify({
#             "message": "Drink not exists",
#             "success": False
#         }), 404
#     if body is None:
#         return jsonify({
#             "message":"Invalid body",
#             "success": False
#         }),422
#     if 'title' in body:
#         new_title = body['title']
#         drink.title = new_title
   
#     if 'recipe' in body:
#         new_recipe = body['recipe']
#         drink.recipe = json.dumps(new_recipe)
#     try:
#         drink.update()
#         drinks = Drink.query.order_by(Drink.id).all()
#     except:
#         abort(500)    
#     return jsonify({
#         "message":"OK",
#         "success": True,
#         "drinks": [drink.long() for dink in drinks]
#     }),200


# @app.route('/drinks/<int:drink_id>', methods=['DELETE'])
# @requires_auth('delete:drinks')
# def delete_drink(jwt, drink_id):
#     drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
#     if drink is not None:
#         try:
#             drink.delete()
#             drinks = Drink.query.order_by(Drink.id).all()
#         except:
#             abort(500)
#     else:
#         abort(404)
#     return jsonify({
#         "message": "OK",
#         "success":True,
#         "drinks":[drink.long() for dink in drinks]
#     })

# # Error Handling
# '''
# Example error handling for unprocessable entity
# '''


# @app.errorhandler(422)
# def unprocessable(error):
#     return jsonify({
#         "success": False,
#         "error": 422,
#         "message": "unprocessable"
#     }), 422


@APP.errorhandler(404)
def not_found(error):
        return (
            jsonify({
                "success":False,
                "error":404,
                "message":"resource not found"
            }),
            404
        )

# @app.errorhandler(401)
# def not_permitted(error):
#         return (
#             jsonify({
#                 "success":False,
#                 "error":401,
#                 "message":"Unauthorized"
#             }),
#             401
#         )
        
        
# @app.errorhandler(403)
# def not_permitted(error):
#         return (
#             jsonify({
#                 "success":False,
#                 "error":403,
#                 "message":"Forbidden"
#             }),
#             403
#         )