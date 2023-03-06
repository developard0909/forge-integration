import os
import json
import pandas as pd
import requests

from pathlib import Path
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


class Shiphero(object):
    def __init__(self):
        # self.access_token = self.shiphero_login()
        
        self.refresh_token = os.getenv('shiphero_refresh_token', 'cWyA_xnSPwOdB9zfn-9XlIlj50E0MY172IY7Diq8ZTGiI')

        self.access_token = self.regenerate_access_token()

    def get_input_json(self):
        
        input_data = {}

        dir = Path(__file__).parents[1]

        json_path = os.path.join(dir, 'input.json')

        if (os.path.exists(json_path) and os.path.isfile(json_path)):

            with open(json_path) as json_data:

                input_data = json.load(json_data)

        return input_data

    # Login of Shiphero    
    def shiphero_login(self):
        
        auth_address = {
            "username": "supertopdev@gmail.com",
            "password": "P@ssw0rd"
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.request("POST", data=json.dumps(auth_address), headers=headers)

        access_token = None

        if response.status_code == 200:

            json_resp = json.loads(response.text)

            access_token = json_resp.get("access_token")

        return access_token
        
    def regenerate_access_token(self):
        
        url = "https://public-api.shiphero.com/auth/refresh"
        
        headers= {
            "Content-Type": "application/json"
        }

        data = {
            "refresh_token": self.refresh_token
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(data))

        access_token = None

        if response.status_code == 200:

            access_token = json.loads(response.text).get("access_token")

        return access_token

    # Get products
    def get_products(self):
        
        client = self.set_client()

        query = gql(""" { products { request_id complexity data(first: 10) { edges { node { id sku } } } } } """)
        
        response = client.execute(query)

        print(response)

        return

    # Create new Kit
    def create_kit(self):

        try:

            client = self.set_client()

            input_json = self.get_input_json()
            
            skus = input_json.get("listing skus")

            components = []

            if skus:
                
                for sk in skus:

                    for key, value in sk.items():

                        if 'sku' in key:
                            
                            response = self.create_product(value)

                            components.append({
                                "sku": value, "quantity": 1
                            })

            else:
                
                sku = input_json.get("foundry master sku")

                response = self.create_product(sku)

                components.append({
                    "sku": sku, "quantity": 1
                })


            kitInput = {
                "sku": "107DS",
                "components": components,
                "kit_build": False
            }
            
            query = """ mutation kit_build($data: BuildKitInput!) { 
                kit_build(data: $data) { 
                    request_id 
                    complexity 
                    product { 
                        id 
                        sku 
                        components { 
                            id 
                            sku 
                        } 
                    } 
                } 
            }"""
            
            query = gql(query)

            response = client.execute(query, variable_values={
                "data": kitInput
            })

        except Exception as e:
            print(e)
        
        print(response)

        return
    
    # Create new product
    def create_product(self, sku):
        
        response = None

        try:
            
            client = self.set_client()

            input_json = self.get_input_json()

            productInput = {
                "sku": sku,
                "name": input_json.get("name"),
                "kit": False,
                "kit_build": True,
                "warehouse_products": [
                    {
                        "warehouse_id": "V2FyZWhvdXNlOjgwNzU=",
                        "on_hand": 123
                    }
                ]

            }

            query = """ mutation product_create($data: CreateProductInput!) { 
                product_create(data: $data) { 
                    request_id 
                    complexity 
                    product { 
                        id 
                        sku
                        kit
                        kit_build
                        created_at
                    } 
                } 
            }"""
                
            query = gql(query)

            response = client.execute(query, variable_values={
                "data": productInput
            })

        except Exception as e:
            print(e) 

        return response

    # Set client
    def set_client(self):

        _transport = RequestsHTTPTransport( url='https://public-api.shiphero.com/graphql', use_json=True, )
        
        _transport.headers = { 
            "User-Agent": "Mozilla/5.0 (X11; buntu; " + "Linux x86_64; rv:58.0) Gecko/0100101 Firefox/58.0", 
            "Authorization": "Bearer {}".format(self.access_token), 
            "content-type": "application/json"
        }
        
        client = Client( transport=_transport, fetch_schema_from_transport=True, )

        return client

if __name__ == "__main__":
    Shiphero()
