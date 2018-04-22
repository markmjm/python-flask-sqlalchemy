from models.store import StoreModel
from flask_restful import Resource, reqparse


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {'message': 'store not found'}, 404

    def post(self, name):

        if StoreModel.find_by_name(name):
            return {"message": "Store already exists."}, 400

        # user = UserModel(data['username'], data['password'])  simplify
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occured while crating a sroe'}, 500

        return {"message": "Store created successfully."}, 201

    def delete(self, name):
        store = Store.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message' : 'Store deleted'}

class StoreList(Resource):
    def get(self):
        # return {'items': [item.json() for item in ItemModel.query.all()]}
        # or
        # map takes (function, iterator)
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}