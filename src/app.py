import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
import sys
from model import Books, Author, db, book_lends,Patrons, setup_db
from auth.auth import AuthError, requires_auth
from datetime import datetime, timedelta


def create_app(test_config=None):
    app = Flask(__name__)
    app.app_context().push()
    setup_db(app)
    CORS(app)
    
    
    @app.after_request
    def after_request(response):
        response.headers.add(
                "Access-Control-Allow-Headers", "Content-Type, Authorization,true"
            )
        response.headers.add(
                "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
            )
            
        return response

    

# ROUTES
    @app.route('/')
    def welcome_page():
        return jsonify({
            "message":"Welcome to Flask app",
            "status":"OK"
        }),200


    @app.route('/books', methods=['GET'])
    def get_all_books():
        try:
            book_data = Books.query.order_by(Books.id).all()
        except:
            abort(404)
        return jsonify({
            "message":"OK",
            "data": [book.short() for book in book_data],
            "success": True
        }),200
        

    @app.route('/book-detail/<int:book_id>', methods=['GET'])
    @requires_auth('get:book-detail')
    def get_all_books_detail(jwt,book_id):
        result = {}
        try:
            book_data = Books.query.filter(Books.id==book_id).first()
        except:
            abort(404)
        return jsonify({
            "message":"Query book detail successfully",
            "status":"success",
            "statusCode":200,
            "data": book_data.long()
            }),200


    @app.route('/books', methods=['POST'])
    @requires_auth("post:books")
    def add_book(jwt):
        body = request.get_json()
        author_name = body['author']
        author_id = 0
        author = Author.query.filter(Author.name == author_name).first()
        error = False
        if author is not None:
            author_id = author.id
            author.books_in_lib= author.books_in_lib + 1
            db.session.commit()
        else:
            try:
                new_author = Author(
                name=author_name,
                gender=body['author_gender'],
                country=body['author_country'],
                books_in_lib=1
            )
                db.session.add(new_author)
                db.session.commit()
                print('PASSS')
            except:
                db.session.rollback()
                print(sys.exc_info())
                abort(500)
        try:
            new_author = Author.query.filter(Author.name == body['author']).first()
            author_id = new_author.id
            new_book = Books(
                title=body['title'], 
                author=body['author'], 
                numbers_in_stock= body['numbers_in_stock'],
                add_date=datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                genres=body['genres'],
                pages=body['pages'], 
                status=body['status'], 
                author_id=author_id, 
                days_for_borrow=body['days_for_borrow'],
                author_gender=body['author_gender'],
                author_country=body['author_country']
                )
                
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

    @app.route('/books/<int:book_id>', methods=['DELETE'])
    @requires_auth("delete:books")
    def remove_book(book_id):
        error = False
        try:
            target_book = Books.query.filter(Books.id==book_id).first()
            if target_book is None:
                abort(404)
            else:
                db.session.delete(target_book)
                db.session.commit()
                return jsonify({
                    'message':'Remove book successfully',
                    'statusCode':202
                }),202
        except:
            error= True
            db.session.rollback()
            print(sys.exc_info())
            abort(404)

            
    @app.route('/books/<int:book_id>', methods=['POST'])
    @requires_auth('update:books')
    def update_book(jwt, book_id):
        # Allow updating numbers of book in lib, status, days_for_borrow
        body = request.get_json()
        try:
            target_book = Books.query.filter_by(id=book_id).first()
            if target_book is None:
                abort(404)
            else:
                target_book.days_for_borrow = body['days_for_borrow']
                target_book.status = body['status']
                target_book.numbers_in_stock = body['numbers_in_stock']
                db.session.commit()
        except:
            db.session.rollback()
            abort(404)
            print(sys.exc_info())
        db.session.close()
        return jsonify({
            'message':'Update book successfully',
            'status': 200
        })
        
        
    @app.route('/book-loan', methods=['POST'])
    @requires_auth("post:book-loan-ticket")
    def create_book_loan_ticket(jwt):
        error = False
        body = request.get_json()
        book_lend = Books.query.filter(Books.id == body['book_id']).first()
        days_for_borrow = book_lend.days_for_borrow
        ticket_created_time = datetime.now()
        return_date = ticket_created_time + timedelta(days=days_for_borrow)
        try:
            statement = book_lends.insert().values(book_id=body['book_id'],patron_id=body['patron_id'], 
                                                time_lend = ticket_created_time.strftime("%Y/%m/%d"),
                                                return_date = return_date.strftime("%Y/%m/%d"),
                                                status = 'active'
                                                )
            db.session.execute(statement)
            db.session.commit()
        except:
            db.session.rollback()
            error=True
            print(sys.exc_info())
        finally:
            if not error:
                db.session.close()
                return jsonify({
                'message':'Book loan ticket created successfully',
                'status':'success'
                }),201
            else:
                abort(500)

    @app.route('/patron',methods=['POST'])
    @requires_auth('post:patron')
    def add_new_patron(jwt):
        body = request.get_json()
        try:
            new_patron = Patrons(
                name=body['name'],
                date_of_birth=body['date_of_birth'],
                gender=body['gender'],
                address=body['address'],
                books_borrowed=0,
                membership_time=body['membership_time'],
                books_borrowing=0
            )
            db.session.add(new_patron)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
            abort(500)
        return jsonify({
            "message": "Added new patron successfully", 
            "status":201,
            "patron_name": body['name']
            
        }),201
        
        
    @app.route('/patrons', methods=['GET'])
    def get_all_patrons():
        try:
            all_patron = Patrons.query.order_by(Patrons.id).all()
        except:
            abort(404)
        return jsonify({
            "message":"OK",
            "success":True,
            "data": [ pat.short() for pat in all_patron]
        }),200
        
    @app.route('/patrons/<int:patron_id>', methods=['GET'])
    def get_patron_detail(patron_id):
        try:
            patron = Patrons.query.filter_by(id=patron_id).first()
        except:
            abort(404)
        return jsonify({
            "message":"OK",
            "success":True,
            "data": patron.long()
        })
        pass
    @app.route('/patrons/<int:patron_id>', methods=['DELETE'])
    def delete_patron(patron_id):
        try:
            patron =  Patrons.query.filter_by(id=patron_id).first()
            if patron is None:
                abort(404)
                
            db.session.delete(patron)
            db.session.commit()
            return jsonify({
            "message":"Delete successfully",
            "success":False
        }),200
        except:
            db.session.rollback()
            print(sys.exc_info())
            abort(500)
        
    
    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    @app.errorhandler(404)
    def not_found(error):
            return (
                jsonify({
                    "success":False,
                    "error":404,
                    "message":"resource not found"
                }),
                404
            )

    @app.errorhandler(401)
    def not_permitted(error):
            return (
                jsonify({
                    "success":False,
                    "error":401,
                    "message":"Unauthorized"
                }),
                401
            )
            
            
    @app.errorhandler(403)
    def not_permitted(error):
            return (
                jsonify({
                    "success":False,
                    "error":403,
                    "message":"Forbidden"
                }),
                403
            )
    @app.errorhandler(500)
    def not_permitted(error):
            return (
                jsonify({
                    "success":False,
                    "error":500,
                    "message":"Internal server error"
                }),
                500
            )
    
    return app
app = create_app()

if __name__ == '__main__':
    app.run()