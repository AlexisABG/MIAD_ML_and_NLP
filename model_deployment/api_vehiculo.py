#!/usr/bin/python
from flask import Flask
from flask_restx import Api, Resource, fields
import joblib
from deploy_model_vehicle import predict_proba

app = Flask(__name__)

api = Api(
    app, 
    version='1.0', 
    title='Car Price Predictio API',
    description='car price prediction API')

ns = api.namespace('predict', 
     description='vehicle price predictor')
   
parser = api.parser()

parser.add_argument(
    'Year', 
    type=int, 
    required=True, 
    help='vehicle price', 
    location='args', 
    )

parser.add_argument(
    'Mileage', 
    type=int, 
    required=True, 
    help='vehicle Mileage', 
    location='args', 
    )

parser.add_argument(
    'State', 
    type=str, 
    required=True, 
    help='vehicle state', 
    location='args', 
    )
parser.add_argument(
    'Make', 
    type=str, 
    required=True, 
    help='vehicle brand', 
    location='args', 
    )

parser.add_argument(
    'Model', 
    type=str, 
    required=True, 
    help='vehicle model', 
    location='args', 
    )

resource_fields = api.model('Resource', {
    'result': fields.String,
})

@ns.route('/')
class VehicleApi(Resource):

    @api.doc(parser=parser)
    @api.marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()
        
        return {
         "result": predict_proba(args['Year'],args['Mileage'],args['State'],args['Make'],args['Model'])
        }, 200
    
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=8888)
