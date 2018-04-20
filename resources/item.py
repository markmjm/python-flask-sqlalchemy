import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'message': 'item not found'}, 400

    def post(self, name):
        # check if item exists
        if ItemModel.find_by_name(name):
            return {'message': "An with name '{}' already exists.".format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name,data['price'])
        try:
            ItemModel.insert(item)
        except:
            return {'message': "An error occured inserting the item"}, 500

        return item.json(), 201

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
        item = ItemModel.find_by_name(name)
        data = Item.parser.parse_args()
        updated_item = ItemModel(name, data['price'])
        if item is None:
            try:
                updated_item.insert(updated_item)
            except:
                return {'message': "An error occured inserting the item"}, 500
        else:
            try:
                updated_item.update()
            except:
                return {'message': "An error occured update the item"}, 500
        return updated_item.json()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "select * from items"
        results = cursor.execute(query)
        items = []
        for row in results:
            items.append({
                'name': row[0],
                'price': row[1],
            })
        connection.close()
        return {'items': items}, 200
