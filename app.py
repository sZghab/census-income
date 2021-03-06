import pandas as pd
from flask import Flask, jsonify, request
import pickle

# load model
print('to load')
model = pickle.load(open('final_prediction.pickle', 'rb'))
print('loaded')
# app
app = Flask(__name__)

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

# routes
@app.route('/post/', methods=['POST'])
def predict():
    # get data
    data = request.get_json(force=True)

    # convert data into dataframe
    data.update((x, [y]) for x, y in data.items())
    data_df = pd.DataFrame.from_dict(data)

    # predictions
    result = model.predict(data_df)

    # send back to browser
    output = {'results': int(result[0])}

    # return data
    return jsonify(results=output)

if __name__ == "__main__":
    app.run(threaded=True, port=5000)
