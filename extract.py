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
        url = self.baseurl + "industries?"
        industry = requests.get(url, params=self.params, headers=self.headers)
        industry_data = industry.json()
        return industry_data

    def fetchingproductlines(self, nodeID):
        url = self.baseurl+f"industries/{nodeID}?"
        productline = requests.get(url, params=self.params, headers=self.headers)
        product_line = productline.json()
        return product_line

    def fetchingproducts(self,rightID):
        url = self.baseurl+f"product-lines/{rightID}?"
        pro = requests.get(url, params=self.params, headers=self.headers)
        products = pro.json()
        return products

    def fetchingproductdetails(self,nodeID):
        url = self.baseurl+f"products/{nodeID}?"
        pd = requests.get(url, params=self.params, headers=self.headers)
        p_details = pd.json()
        return p_details

    def fetchingproductspecifications(self,equipmentID):
        url = self.baseurl+f"equipment/{equipmentID}/specifications?"
        ps = requests.get(url, params=self.paramspecs, headers=self.headers)
        p_specs = ps.json()
        return p_specs
