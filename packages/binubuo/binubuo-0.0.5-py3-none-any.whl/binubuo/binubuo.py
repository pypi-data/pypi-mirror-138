import configparser
import requests
import json

class binubuo:
    def __init__(self, apikey=None):
        if(apikey is None):
            print("No API key specified. Did you register with https://rapidapi.com/auth/sign-up to get your API key?")
        else:
            self.rapidapi_key = apikey
            self.readconfig()

    def readconfig(self):
        self.rapidapi_host = "binubuo.p.rapidapi.com"
        self.baseurl = "https://" + self.rapidapi_host
        self.default_generator_rows = 1
        self.default_dataset_rows = 10
        self.locale_set = None
        self.tag_set = None
        self.tz_set = None
        self.csv_set = None
        self.load_as = "json"
        self.generator_dict_cache = 0
        self.dataset_dict_cache = 0
        self.dict_cache = {}

    def setheaders(self):
        self.headers = {}
        self.headers["x-rapidapi-host"] = self.rapidapi_host
        self.headers["x-rapidapi-key"] = self.rapidapi_key

    def call_binubuo(self, rest_path, query_string):
        self.setheaders()
        if(self.locale_set is not None):
            query_string["locale"] = self.locale_set
        if(self.tag_set is not None):
            query_string["tag"] = self.tag_set
        if(self.tz_set is not None):
            query_string["tz"] = self.tz_set
        if(self.category is None) and (self.csv_set is not None):
            query_string["csv"] = 1
        if(self.category is not None):
            self.resp = requests.request("GET", self.baseurl + self.category + rest_path, headers=self.headers, params=query_string)
        else:
            self.resp = requests.request("GET", self.baseurl + self.dataset_type + rest_path, headers=self.headers, params=query_string)
        if self.resp.ok:
            if self.load_as == "json":
                self.response_json = json.loads(self.resp.text)
            elif(self.category is None) and (self.csv_set is not None):
                self.response_csv = self.resp.text
            else:
                # Default to loads json
                self.response_json = json.loads(self.resp.text)
        else:
            if self.resp.status_code == 403:
                print("Invalid API key specified. Did you register with https://rapidapi.com/auth/sign-up to get your API key?")
            elif self.resp.status_code == 404:
                print("Generator not found. Category: " + self.category + ". Generator: " + rest_path)
            else:
                print("Communication failure")

    def call_binubuo_to_file(self, rest_path, query_string):
        self.setheaders()
        if(self.locale_set is not None):
            query_string["locale"] = self.locale_set
        if(self.tag_set is not None):
            query_string["tag"] = self.tag_set
        if(self.tz_set is not None):
            query_string["tz"] = self.tz_set
        if(self.category is None) and (self.csv_set is not None):
            query_string["csv"] = 1
        if(self.category is not None):
            url_call = self.baseurl + self.category + rest_path
            #self.resp = requests.request("GET", self.baseurl + self.category + rest_path, headers=self.headers, params=query_string)
        else:
            url_call = self.baseurl + self.dataset_type + rest_path
            #self.resp = requests.request("GET", self.baseurl + self.dataset_type + rest_path, headers=self.headers, params=query_string)
        with requests.get(url_call, stream=True, headers=self.headers, params=query_string) as br:
            br.raise_for_status()
            with open(self.file_name, 'wb') as bf:
                for chunk in br.iter_content(chunk_size=8192):
                    bf.write(chunk)

    def tz(self, tz=None):
        self.tz_set = tz

    def locale(self, locale=None):
        self.locale_set = locale

    def tag(self, tag=None):
        self.tag_set = tag

    def csv(self, csv=None):
        self.csv_set = csv

    def grows(self, rows=1):
        self.default_generator_rows = rows

    def drows(self, rows=10):
        self.default_dataset_rows = rows

    def get_generator_response_value(self):
        if self.default_generator_rows == 1:
            # Request a single value directly.
            self.generator_response_value = list(list(self.response_json.values())[0][0].values())[0]
        else:
            # Request for more values. Make response into a list and return
            self.generator_response_value = []
            for prime_key in self.response_json:
                for idx, val in enumerate(self.response_json[prime_key]):
                    for key, value in val.items():
                        self.generator_response_value.append(value)

    def get_dataset_response_value(self, response_type="list"):
        if (self.dataset_type.find("data/standard") >= 0) and (self.csv_set is None):
            # Purify result
            for standard_key in self.response_json:
                self.response_clean = self.response_json[standard_key]
        elif(self.csv_set is not None):
            self.response_clean = self.response_csv
        else:
            self.response_clean = self.response_json
        if response_type == "list":
            self.dataset_response_value = []
            if (self.csv_set is None):
                for rows in self.response_clean:
                    self.dataset_response_value.append(list(rows.values()))
            else:
                for line in self.response_clean.splitlines():
                    self.dataset_response_value.append(line.rstrip().split(','))
        elif response_type == "tuple":
            self.dataset_response_value = ()
            if (self.csv_set is None):
                for rows in self.response_clean:
                    self.dataset_response_value = self.dataset_response_value + tuple(list(rows.values()))
            else:
                for line in self.response_clean.splitlines():
                    self.dataset_response_value = self.dataset_response_value + tuple(line.rstrip().split(','))

    def print_dir_list(self, type_in="generators", only_cache=0):
        # Purify result only if we are getting from outside cache
        if (type_in == "generators" and self.generator_dict_cache == 0) or (type_in == "datasets" and self.dataset_dict_cache == 0):
            for standard_key in self.response_json:
                self.response_clean = self.response_json[standard_key]
                self.dict_cache[type_in] = self.response_clean
        else:
            # Dealing with an already cached request. Just load from cache
            self.response_clean = self.dict_cache[type_in]
        if type_in == "generators":
            if only_cache == 0:
                print("{:<20} {:<30}".format('Category:', 'Function:'))
                print("{:<20} {:<30}".format('===================', '============================='))
            for idx, val in enumerate(self.response_clean):
                for key, value in val.items():
                    if key == "GENERATOR_CATEGORY_NAME":
                        ws_cat = value
                    if key == "GENERATOR_WEBSERVICE_NAME":
                        ws_func = value
                if only_cache == 1:
                    self.generator_dict_cache = 1
                else:
                    print("{:<20} {:<30}".format(ws_cat, ws_func))
        elif type_in == "datasets":
            print("{:<10} {:<20} {:<30}".format('Type:', 'Category:', 'Dataset:'))
            print("{:<10} {:<20} {:<30}".format('=========', '===================', '============================='))
            for idx, val in enumerate(self.response_clean):
                for key, value in val.items():
                    if key == "DATASET_TYPE_NAME":
                        ws_type = value.split(' ')[0]
                    if key == "DATASET_CATEGORY_NAME":
                        if value == "Custom":
                            ws_cat = ""
                        else:
                            ws_cat = value
                    if key == "DATASET_WEBSERVICE_NAME":
                        ws_func = value
                if only_cache == 1:
                    print("{:<10} {:<20} {:<30}".format(ws_type, ws_cat, ws_func))
                    self.dataset_dict_cache = 1
                else:
                    print("{:<10} {:<20} {:<30}".format(ws_type, ws_cat, ws_func))


    def list_generators(self, only_cache=0):
        self.category = None
        self.dataset_type = "/"
        rest_path = "generator/"
        query_string = {}
        if self.generator_dict_cache == 0:
            # Only call if we have not cached already
            self.call_binubuo(rest_path, query_string)
        self.print_dir_list("generators", only_cache)

    def list_datasets(self):
        self.category = None
        self.dataset_type = "/"
        rest_path = "data/"
        query_string = {}
        if self.dataset_dict_cache == 0:
            # Only call if we have not cached already
            self.call_binubuo(rest_path, query_string)
        self.print_dir_list("datasets")

    def generate(self, category, function):
        # Incase called directly
        self.category = "/generator/" + category
        rest_path = "/" + function
        query_string = {"rows": self.default_generator_rows}
        self.call_binubuo(rest_path, query_string)
        if self.resp.ok:
            self.get_generator_response_value()
            return self.generator_response_value

    def dataset(self, dataset_name, dataset_type="custom", dataset_category=None):
        self.category = None
        if dataset_type == "custom":
            self.dataset_type = "/data/custom"
        elif dataset_type == "standard":
            self.dataset_type = "/data/standard/" + dataset_category
        rest_path = "/" + dataset_name
        query_string = {"rows": self.default_dataset_rows}
        self.call_binubuo(rest_path, query_string)
        if self.resp.ok:
            self.get_dataset_response_value()
            return self.dataset_response_value

    def dataset_to_file(self, dataset_name, file_name="same", dataset_type="custom", dataset_category=None):
        self.category = None
        if file_name == "same":
            if(self.csv_set is None):
                self.file_name = dataset_name + ".json"
            else:
                self.file_name = dataset_name + ".csv"
        else:
            self.file_name = file_name
        if dataset_type == "custom":
            self.dataset_type = "/data/custom"
        elif dataset_type == "standard":
            self.dataset_type = "/data/standard/" + dataset_category
        rest_path = "/" + dataset_name
        query_string = {"rows": self.default_dataset_rows}
        self.call_binubuo_to_file(rest_path, query_string)
