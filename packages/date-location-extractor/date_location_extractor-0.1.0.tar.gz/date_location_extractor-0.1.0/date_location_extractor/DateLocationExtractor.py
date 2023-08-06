from datetime import datetime
from dateutil import parser
from geotext import GeoText

import os
import datefinder
import ast


class DateLocationExtractor:
    RANKING_WEIGHT_HAS_DATE = 0.3
    RANKING_WEIGHT_HAS_DAY = 0.2
    RANKING_WEIGHT_HAS_COUNTRY = 0.3
    RANKING_WEIGHT_HAS_CITY = 0.2
    loaded_file = None
    normalized_data = []
    today = datetime.today()

    def __init__(self):
        pass

    def load_json_file(self, file_location):
        self.loaded_file = file_location

    def get_date_location_from_json_file(self, file, use_simple_parser=False):
        self.loaded_file = file
        if not os.path.isfile(self.loaded_file):
            raise FileNotFoundError("JSON File not Found")

        with open(self.loaded_file, 'r') as f:
            data = ast.literal_eval(f.read())
            if use_simple_parser:
                self.normalized_data = self.get_date_location_from_list_with_parser(data)
            else:
                self.normalized_data = self.get_date_location_from_list(data)
        return self.normalized_data

    def get_date_location_from_list(self, string_list):
        if not isinstance(string_list, list):
            raise TypeError("string_list should be a list")

        output_list = []
        for current_string in string_list:
            if not isinstance(current_string, str):
                raise TypeError("every element of string_list should be a string")
            output_list.append(self.__get_date_location_from_string(current_string))
        return output_list

    def get_date_location_from_list_with_parser(self, string_list):
        output_list = []
        for current_string in string_list:
            found_date = self.__parse_split_strings(current_string, ',')
            found_date = self.__parse_split_strings(current_string, ' ') \
                if not found_date else found_date
            if found_date:
                address = current_string.replace(found_date[1], '').strip(", ")
                normalized_address = self.get_location_from_string(address)
                date_iso = found_date[0].strftime("%Y-%m-%d")
                ranking = self.__get_ranking(normalized_address, date_iso)
                output_list.append({"address": address, "date_iso": date_iso, "ranking": ranking,
                                    "normalized_address": normalized_address})
            else:
                normalized_address = self.get_location_from_string(current_string)
                ranking = self.__get_ranking(normalized_address)
                output_list.append({"address": current_string, "date_iso": "", "ranking": ranking,
                                    "normalized_address": normalized_address})

        return output_list

    def get_location_from_string(self, current_string):
        geo_text_instance = GeoText(current_string)
        first_country = geo_text_instance.country_mentions.popitem(last=False)[
            0] if geo_text_instance.country_mentions else ""
        first_city = geo_text_instance.cities[0] if geo_text_instance.cities else ""
        return {"City": first_city, "Country": first_country}

    def __get_ranking(self, normalized_address, date=None):
        current_ranking = 0
        if normalized_address.get('City'):
            current_ranking = current_ranking + self.RANKING_WEIGHT_HAS_CITY
        if normalized_address.get('Country'):
            current_ranking = current_ranking + self.RANKING_WEIGHT_HAS_COUNTRY
        if date:
            current_ranking = current_ranking + self.RANKING_WEIGHT_HAS_DATE
            day = datetime.strptime(date, '%Y-%m-%d').day
            today = self.today.day
            if day != today:
                current_ranking = current_ranking + self.RANKING_WEIGHT_HAS_DAY
        return current_ranking

    def __get_date_location_from_string(self, current_string):
        matches = datefinder.find_dates(text=current_string, source=True)
        # TODO: try to analyze multiple possible matches and choose the best one instead of the first one
        for match in matches:
            original_date_datetime = match[0]
            original_date_string = match[1]
            location = current_string.replace(original_date_string, '')
            normalized_address = self.get_location_from_string(location)
            ranking = self.__get_ranking(normalized_address, original_date_datetime.strftime("%Y-%m-%d"))
            return {
                "address": location.strip(', '),
                "date_iso": original_date_datetime.strftime("%Y-%m-%d"),
                "ranking": ranking,
                "normalized_address": normalized_address
            }
        normalized_address = self.get_location_from_string(current_string)
        ranking = self.__get_ranking(normalized_address)
        return {
            "address": current_string.strip(', '),
            "date_iso": "",
            "ranking": ranking,
            "normalized_address": normalized_address}

    def __parse_split_strings(self, full_string, character_delimiter=','):
        if not full_string:
            return False
        found_date = False
        for string_part in full_string.split(character_delimiter):
            try:
                found_date = (parser.parse(string_part), string_part)
            except:
                pass
        return found_date
