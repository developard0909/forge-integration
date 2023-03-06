import os
import json
import requests

from utils.input_parameters import MakeInputJson
from utils.create_anvyl_identifiers import MakeIdentifiers


class Anvyl(object):
    def __init__(self):
        
        self.api_key = os.getenv("ANVYL_API_KEY", "ntvZNU3H.E4tAf8YoCDD2zP6QaW5ZiAj2BgEKqQ2I")

        self.get_input_json = MakeInputJson().run()


    # Create part
    def create_part(self):

        teams = self.get_anvyl_teams()
        
        if teams:

            teamId = teams[1].get("id")

            url = "https://api.anvyl.com/api/v1/teams/{}/parts".format(teamId)

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": self.api_key
            }

            input_json = self.get_input_json
            
            part_identifiers = MakeIdentifiers().run(input_json)

            skus = []

            if input_json:

                name = input_json.get("name")

                master_sku = input_json.get("foundry master sku")

                payload = {"part": {"name": name} }

                skus = input_json.get("listing skus", [])

                if skus:

                    for sk in skus:

                        sku_part_identifiers = part_identifiers
                        
                        sku = None

                        for key, value in sk.items():

                            if 'sku' in key:

                                sku = value

                            if 'asin' in key:

                                sku_part_identifiers.append({ # Add Asin as part identifiers
                                    "label": "Asin",
                                    "value": value
                                })
                                
                        if sku and name:

                            exist_part = self.existing_part(teamId, sku, name)

                            if exist_part:

                                print(f"Existing part with sku: {sku} and name: {name}")

                            else:
                                
                                payload["part"]["sku"] = sku

                                payload["part"]["part_identifiers"] = sku_part_identifiers

                                print(self.print_result(url, payload, headers))

                elif self.existing_part(teamId, master_sku, name):
                    
                    print(f"Existing part with sku: {master_sku} and name: {name}")

                else:

                    payload["part"]["sku"] = master_sku

                    payload["part"]["part_identifiers"] = part_identifiers

                    print(self.print_result(url, payload, headers))
        
        return


    @staticmethod
    def print_result(url, payload, headers):

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 201:

            part_id = json.loads(response.text).get("parts")[0].get("id")

            result = f"created part {part_id} successfully"

        else:

            result = "Error, {}".format(response.text)

        return result


    # Get the suppliers data on team
    def get_suppliers(self, teamId):
        
        url = "https://api.anvyl.com/api/v1/teams/{}/suppliers?page=1&per_page=100".format(teamId)

        headers = {"Accept": "application/json", "Authorization": self.api_key}

        response = requests.get(url, headers=headers)

        suppliers = []

        if response.status_code == 200:

            suppliers = json.loads(response.text).get("parts")

        return suppliers
    

    # Check existing part with sku and name on team
    def existing_part(self, teamId, sku, name):

        parts = self.get_parts(teamId)

        is_exist = False

        for part in parts:
            
            if part.get("sku") == sku and part.get("name") == name:
                
                is_exist = True

                break

        return is_exist


    # Get the detailed part data
    def single_part(self, teamId):

        url = "https://api.anvyl.com/api/v1/teams/{}/parts/{}"

        headers = {"Accept": "application/json", "Authorization": self.api_key}

        parts = self.get_parts(teamId)

        for p in parts:
            
            partId = p.get("id")
            
            url = url.format(teamId, partId)

            response = requests.get(url, headers=headers)

            part = json.loads(response.text).get("part")

            break

        return part


    # Get parts on team
    def get_parts(self, teamId):

        url = "https://api.anvyl.com/api/v1/teams/{}/parts?page=1&per_page=100".format(teamId)

        headers = {"Accept": "application/json", "Authorization": self.api_key}

        response = requests.get(url, headers=headers)

        parts = []

        if response.status_code == 200:

            parts = json.loads(response.text).get("parts")

        return parts


    # Get the teams on anvyl
    def get_anvyl_teams(self):

        url = "https://api.anvyl.com/api/v1/teams"

        headers= {
            "Accept": "application/json",
            "Authorization": self.api_key
        }

        try:
            
            teams = []

            resp = requests.get(url, headers=headers)
            
            if resp.status_code == 200:

                teams = json.loads(resp.text).get("teams")

            return teams

        except Exception as e:
            
            import traceback
            
            response = {}
            
            response["error"] = traceback.format_exc(str(e))
            
            return response

    # Get purchase order

    def get_purchase_order(self):

        import datetime
        
        teams = self.get_anvyl_teams()

        teamId = teams[1].get("id")

        created_from = "2022-04-25"
        
        created_to = "2022-05-24"

        url = "https://api.anvyl.com/api/v1/teams/{}/purchase_orders?filter[created_from]={}&filter[created_to]={}".format(teamId, created_from, created_to)

        headers = {"Accept": "application/json", "Authorization": self.api_key}

        orders = self.run_orders(url, headers)

        if not orders:

            url = "https://api.anvyl.com/api/v1/teams/{}/purchase_orders".format(teamId)

            orders = self.run_orders(url, headers)

        return orders
        
    def run_orders(url, headers):

        response = requests.get(url, headers=headers)

        orders = []

        if response.status_code == 200:

            orders = json.loads(response.text)

        return orders

    def run(self):

        # self.create_part()

        self.get_purchase_order()


if __name__ == "__main__":
    Anvyl()
