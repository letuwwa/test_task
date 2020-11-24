from os import listdir
from os.path import isfile, join
import json
import jsonschema
from jsonschema import validate


class JsonTester:
    def __init__(self, json_dir='./task_folder/event/', schemes_dir='./task_folder/schema/'):
        self.json_dir = json_dir
        self.schemes_dir = schemes_dir

    def validate(self):
        schemes_list = self.__get_schemes_filenames()
        jsons_list = self.__get_jsons_filenames()

        schemes_data = []
        for schema in schemes_list:
            data = self.__get_schema(schema)
            schemes_data.append(data)

        jsons_data = []
        for json_file in jsons_list:
            data = self.__get_json(json_file)
            jsons_data.append(data)

        test_count = 0
        errors_count = 0
        for schema_data in schemes_data:
            for json_data in jsons_data:
                try:
                    test_count += 1
                    validate(instance=json_data, schema=schema_data)
                except jsonschema.exceptions.ValidationError as err:
                    errors_count += 1
                    error_text = str(err)
                    # print(err)
                    print(error_text.split('\n')[0])

        print(test_count)
        print(errors_count)

    def __get_schema(self, schema_name):
        with open(self.schemes_dir + schema_name, 'r') as file:
            schema = json.load(file)
        return schema

    def __get_json(self, json_name):
        with open(self.json_dir + json_name, 'r') as file:
            jsonfile = json.load(file)
        return jsonfile

    def __get_jsons_filenames(self):
        jsons_files_list = [f for f in listdir(self.json_dir) if isfile(join(self.json_dir, f))]
        return jsons_files_list

    def __get_schemes_filenames(self):
        schemes_files_list = [f for f in listdir(self.schemes_dir) if isfile(join(self.schemes_dir, f))]
        return schemes_files_list


JsonTester().validate()
