import json
import os


class DistrictNotFoundException(Exception):
    """
    Exception to be raised if correct district is not provided by user
    """
    pass


class DistrictNotProvidedException(Exception):
    """
    Exception to be raised if  district is not provided by user
    """
    # pass


class MunicipalitiesNotException(Exception):
    """
    Exception to be raised if  municipalities is not correct
    """
    # pass


class NepalMunicipality:
    def __init__(self, district_name=None):
        self.municipality_name = None
        self._all_data = []
        self._district_name = district_name
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        json_data_path = os.path.join(BASE_DIR, 'data', 'data.json')
        f = open(json_data_path, 'r')
        self._data = json.loads(f.read())
        self._district = []

    def all_districts(self):
        """
        Use this method to get a list of all districts of nepal
        """
        for items in self._data:
            for item in items.keys():
                self._district.append(item)
        return self._district

    def all_municipalities(self):
        """
        Use this to get list of all municipalities of specific district
        provided from class instance if district is none You will get None as return Value
        """
        if self._district_name is not None:
            for items in self._data:
                if self._district_name in self.all_districts():
                    if items.get(self._district_name) is not None:
                        return items.get(self._district_name)
                else:
                    raise DistrictNotFoundException('District not found for following text, please check '
                                                    'district spelling.')
        raise DistrictNotProvidedException('District not provided please provide district name.')

    def all_data_info(self, municipality_name):
        """
        Use this to get list of all municipalities of specific district
        provided from class instance if district is none You will get None as return Value
        """
        self.municipality_name = municipality_name
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        json_data_path = os.path.join(BASE_DIR,  'data/all_nepali_municipalities.json')
        f = open(json_data_path, 'r')
        self._data = json.loads(f.read())
        self._all_data = []
        for item in self._data:
            if item['name'] == self.municipality_name:
                self._all_data.append(item)
        if len(self._all_data) == 0:
            raise MunicipalitiesNotException("No matching info for provided municipalities try changing spelling or "
                                             "try another name.")
        else:
            return self._all_data


