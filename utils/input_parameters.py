import os
import json
from pathlib import Path


class MakeInputJson(object):
    def __init__(self):

        dir = Path(__file__).parents[1]

        self.json_path = os.path.join(dir, 'input.json')


    def run(self):
        
        input_data = {}

        try:

            if (os.path.exists(self.json_path) and os.path.isfile(self.json_path)):

                with open(self.json_path) as json_data:

                    input_data = json.load(json_data)

        except Exception as e:
            print(e)

        return input_data

if __name__ == "__main__":
    MakeInputJson()
