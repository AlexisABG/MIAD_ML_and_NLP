import pandas as pd
import joblib

def predict_proba(values):

    loaded_model = joblib.load(os.path.dirname(__file__) + '/vehicle_model_proyect.pkl') 

    df = pd.DataFrame(values, columns=['Year', 'Mileage', 'State', 'Make', 'Model'])
    def transformar(x_data):

        url = 'https://parseapi.back4app.com/classes/Car_Model_List?limit=10000&excludeKeys=Year'
        headers = {
        'X-Parse-Application-Id': 'hlhoNKjOvEhqzcVAJ1lxjicJLZNVv36GdbboZj3Z', # This is the fake app's application id
        'X-Parse-Master-Key': 'SNMJJF0CZZhTPhLDIqGhTlUNV9r60M2Z5spyWfXW'}  # This is the fake app's readonly master key

        data = json.loads(requests.get(url, headers=headers).content.decode('utf-8'))

        models = pd.DataFrame.from_dict(data["results"])
        models = models.iloc[:,1:4]
        models = models.apply(lambda x: x.str.lower())
        models["Model_1"] = models.Model.apply(lambda x: x.split(" ")[0])
        models.drop_duplicates(subset="Model", inplace=True)
        models["Category"] = models.Category.str.replace('hatchback, sedan','sedan, hatchback')
        models["Category"] = models.Category.str.replace('convertible, sedan, coupe','sedan, coupe, convertible')
        models["Category"] = models.Category.str.replace('wagon, sedan','sedan, wagon')
        models["Category"] = models.Category.str.replace('suv1992',"suv")

        x_data["Make"], x_data["Model"] = df.Make.str.lower(), df.Model.str.lower()
        x_data["Segment"] = ""
        for n, model in enumerate(models.Model_1):
            x_data.loc[((x_data.Make.str.contains(models.Make.iloc[n])) & (x_data.Model.str.contains(model)),"Segment")] = models.Category.iloc[n]

        conditions = [(x_data.Make=='bentley') | (x_data.Make=='tesla') | (x_data.Make=='porsche') | (x_data.Make=='land') | (x_data.Make=='mercedes-benz') | (x_data.Make=='ram'),
        (x_data.Make=='jeep') | (x_data.Make=='chevrolet') | (x_data.Make=='bmw') | (x_data.Make=='cadillac') | (x_data.Make=='gmc') | (x_data.Make=='ford')
        | (x_data.Make=='volvo') | (x_data.Make=='acura') | (x_data.Make=='jaguar')  | (x_data.Make=='lincoln') | (x_data.Make=='audi') | (x_data.Make=='lexus'), (x_data.Make=='toyota') | (x_data.Make=='buick') | (x_data.Make=='volkswagen')
        | (x_data.Make=='hyundai') | (x_data.Make=='mitsubishi') | (x_data.Make=='honda') | (x_data.Make=='nissan') | (x_data.Make=='mazda') | (x_data.Make=='kia')
        | (x_data.Make=='subaru') | (x_data.Make=='chrysler') | (x_data.Make=='infiniti') | (x_data.Make=='mercury') | (x_data.Make=='fiat') | (x_data.Make=='scion') | (x_data.Make=='pontiac') | (x_data.Make=='suzuki')
        | (x_data.Make=='freightliner') | (x_data.Make=='dodge') | (x_data.Make=='mini')]
        choices = ["High","medium","low"]
        x_data["Gama"]= np.select(condlist=conditions,choicelist=choices, default=np.nan)
        x_data = x_data.iloc[:,]
        

        return x_data
    
    complete_columns = ['Year', 'Mileage', 'Segment_', 'Segment_convertible', 'Segment_coupe',
       'Segment_coupe, convertible', 'Segment_coupe, sedan, convertible',
       'Segment_coupe, sedan, wagon, convertible', 'Segment_hatchback',
       'Segment_hatchback, convertible', 'Segment_pickup', 'Segment_sedan',
       'Segment_sedan, coupe', 'Segment_sedan, coupe, convertible',
       'Segment_sedan, hatchback', 'Segment_sedan, wagon', 'Segment_suv',
       'Segment_van/minivan', 'Segment_wagon', 'Gama_High', 'Gama_low',
       'Gama_medium']

    df = transformar(df)
    df = pd.get_dummies(columns=["Segment","Gama"], drop_first=False, data =df)
    df = df.reindex(columns=complete_columns, fill_value=0)
    #loaded_model = joblib.load(r'C:\Users\maste\OneDrive\PDF\Maestria inteligencia Analitica de Datos\Machine learning y NLP\Semana III\vehicle_model_proyect.pkl')
    price = loaded_model.predict(df)
    return price 