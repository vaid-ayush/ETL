import requests
import json
import config
from requests import Session


class Loading():
    def __init__(self):
        self.token = config.api_key
        self.baseurl = config.baseurl
        self.params = config.params
        self.paramspecs = config.paramspecs
        self.headers = {"Accepts": "application/json", "keyid": self.token}
        # self.session = Session()
        # self.session.header.update(headers=self.headers)

    def industries(self):
        url = self.baseurl+f"industries?"
        try:
            industry = requests.get(url, params=self.params, headers=self.headers)
            if industry.status_code == 200:
                industry_data = industry.json()
                return industry_data
        except:
            print("status code is not 200")

    def fetchingproductlines(self, nodeID):
        url = self.baseurl+f"industries/{nodeID}?"
        try:
            productline = requests.get(url, params=self.params, headers=self.headers)
            if productline.status_code == 200:
                product_line = productline.json()
                return product_line
        except:
            print("status code is not 200")


    def fetchingproducts(self,rightID):
        url = self.baseurl+f"product-lines/{rightID}?"
        try:
            pro = requests.get(url, params=self.params, headers=self.headers)
            if pro.status_code == 200:
                products = pro.json()
                return products
        except:
            print("status code is not 200")
    def fetchingproductdetails(self,nodeID):
        url = self.baseurl+f"products/{nodeID}?"
        try:
            pd = requests.get(url, params=self.params, headers=self.headers)
            if pd.status_code == 200:
                p_details = pd.json()
                return p_details
        except:
            print("status code is not 200")
    def fetchingproductspecifications(self,equipmentID):
        url = self.baseurl+f"equipment/{equipmentID}/specifications?"
        try:
            ps = requests.get(url, params=self.paramspecs, headers=self.headers)
            if ps.status_code == 200:
                p_specs = ps.json()
                return p_specs
        except:
            print("status code is not 200")