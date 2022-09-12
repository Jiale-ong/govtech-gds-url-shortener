import json
import sys

# Python has a weird thing with relative imports cuz the root folder changes when testing locally vs testing on bitbucket, hence we need add this
sys.path.append(".") 

from Backend.controller.controller import app

#run flask
test_client = app.test_client()


def test_home_route():
    response = test_client.get('/all')
    assert response.status_code == 200

# def test_generate_portfolio_get_sector_sentiment():
#     response = test_client.get('/generate-portfolio_get_sector_sentiment')
#     assert response.status_code == 200
    
#     data = json.loads(response.get_data(as_text=True))
#     # Get the table headers and test if it is the same 
#     assert list(map(lambda x: x[0], data)) == industries 

# def test_generate_portfolio_get_cross_corr():
#     response = test_client.get('/generate-portfolio_get_cross_corr')
#     assert response.status_code == 200

# def test_generate_portfolio_get_cross_corr_bond_gold():
#     response = test_client.get('/generate-portfolio_get_cross_corr_bond_gold')
#     assert response.status_code == 200

# def test_generate_portfolio_predict_no_prediction():
#     response = test_client.post("/generate-portfolio_predict", 
#                                 json={"stocks": False, "num_stocks": "12", "time_horizon": "1000"})
#     assert response.status_code == 200

#     data = json.loads(response.get_data(as_text=True))
#     assert data == {"message":"No predictions"}