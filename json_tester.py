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
        html_head = """
        {
                <table border=1 class="dataTable">
                <tr>
                <td><strong>Found error  </strong></td>
                <td><strong>Error text</strong></td>
                <td><strong>Advice</strong></td>
                </tr>
                    """

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

        for i in range(len(schemes_data)):
            for j in range(len(jsons_data)):
                try:
                    validate(instance=jsons_data[j], schema=schemes_data[i])
                except jsonschema.exceptions.ValidationError as err:
                    error = 'Error during validation scheme: ' + str(schemes_list[i]) + ' with file:' + str(jsons_list[j])
                    error_text = str(err).split('\n')[0]

                    error_help = str(err).split('\n')[0].split(' ')[0]
                    if error_help == 'None':
                        advice = 'Please, open file and chek it...'
                    else:
                        advice = 'Add required property:' + str(error_help)

                    html_table = """
                                    <tr>
                                        <td>{}</td>
                                        <td>{}</td>
                                        <td>{}</td>
                                    </tr>                            
                                """.format(error, error_text, advice)
                    html_head += html_table

        html_head += """

            }
        """

        with open('README.md', 'w') as file:
            file.write(html_head)

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
