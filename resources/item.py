import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank")

    @jwt_required()
    def get(self, name):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = 'SELECT * FROM items WHERE name = ?'
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()
        item = Item.find_by_name(name)
        if item:
            return item
        else:
            return {'message': 'item not found'}, 400

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM items WHERE name = ?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):
        # check if item exists
        if Item.find_by_name(name):
            return {'message': "An with name '{}' already exists.".format(name)}, 400
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        try:
            Item.insert(item)
        except:
            return {'message': "An error occured inserting the item"}, 500

        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES(?,?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "Delete from items where name = ?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        global items
        return {'message': "Item {} deleted".format(name)}, 200

    def put(self, name):
        item =  Item.find_by_name(name)
        data = Item.parser.parse_args()
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            try:
                Item.insert(updated_item)
            except:
                return {'message': "An error occured inserting the item"}, 500
        else:
            try:
                Item.update(updated_item)
            except:
                return {'message': "An error occured update the item"}, 500
        return updated_item

    @classmethod
    def update(self, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "update items set price = ? where name =?"
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "select * from items"
        results = cursor.execute(query)
        items=[]
        for row in results:
            items.append({
                'name': row[0],
                'price': row[1],
            })
        connection.close()
        return {'items': items}, 200
