from utils.input_parameters import MakeInputJson


class MakeIdentifiers(object):
    def __init__(self):
        
        self.input_json = {}

    def run(self, input_json):

        part_identifiers = []

        if input_json:

            for key, value in input_json.items(): # make the part identifiers as multiple

                if key.lower() == "netsuite sku":

                    part_identifiers.append({
                        "label": "Netsuite SKU",
                        "value": value
                    })

                if key.lower() == 'brand':

                    part_identifiers.append({
                        "label": "Brand",
                        "value": value.get("brand name")
                    })

                    part_identifiers.append({
                        "label": "Brand ID",
                        "value": value.get("id")
                    })

                if key.lower() == "foundry master sku":

                    part_identifiers.append({
                        "label": "Foundry Master SKU",
                        "value": value
                    })
        
        return part_identifiers
    
  
if __name__ == "__main__":
    MakeIdentifiers()
