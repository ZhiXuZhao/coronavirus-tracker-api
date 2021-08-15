"""app.location"""
from ..coordinates import Coordinates
from ..utils import countries
from ..utils.populations import country_population

#parts

# put confirmed cases, deaths cases, recovered cases into one class
# Inseated of using confirmed cases, deaths cases, recovered cases as attributes, we can use CaseNumbers class instance as attribute
class CaseNumbers:
    def __init__(self, confirmed = 0, deaths = 0, recovered = 0):
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered


#put all location information into one class
#CaseNumbers, Locationinfo, coordinates and Location forms one aggregate
class Locationinfo:
    def __init__(self, country, province, coordinates):
        #self.id = id
        self.country = country.strip()
        self.province = province.strip()
        self.coordinates = coordinates
        #get countrycode and population so no extra methods are needed
        self.country_code = (countries.country_code(self.locationinfo.country) or countries.DEFAULT_COUNTRY_CODE).upper()
        self.population = country_population(self.country_code)

#timelines is a parts as well
class timeline:
    timeline = None


# Base info every location has, id, last_updated and serialize
class BaseLocation:
    def __init__(self, id, last_updated):
        self.id = id
        self.last_updated = last_updated

    def serialize(self):
        """
        Serializes the location into a dict.
        :returns: The serialized location.
        :rtype: dict
        """
        return {
            # General info.
            "id": self.locationinfo.id,
            "country": self.locationinfo.country,
            "country_code": self.country_code,
            "country_population": self.country_population,
            "province": self.locationinfo.province,
            # Coordinates.
            "coordinates": self.locationinfo.coordinates.serialize(),
            # Last updated.
            "last_updated": self.last_updated,
            # Latest data (statistics).
            "latest": {
                "confirmed": self.casenumbers.confirmed,
                "deaths": self.casenumbers.deaths,
                "recovered": self.casenumbers.recovered,
            },
        }
        
    
# The origional code has Location and Timelined location
# Timelined location is a subclass(similar) of Location
# Apply builder pattern here so only one constructor will be called
# It would be more useful if we have more Location class variation here
# For example, if some location class only requires cases and some location classes only require info
from abc import abstractmethod

class Builder:
    # Builder class, used to create different parts of Location
    # A location has info, casenumbers and timelines(if needed)
    def baseinfo_builder(self) -> None:
        pass
    def casenumber_builder(self) -> None:
        pass
    def loaction_info_builder(self) -> None:
        pass
    def timeline_builder(self) -> None:
        pass

#whole product 1 Location
class Location:
    def __init__(self):
        self.casenumbers = None
        self.baseinfo = None
        self.locationinfo = None

    def build_casenumber(self, casenumber):
        self.casenumbers = casenumber

    def build_baseinfo(self, baseinfo):
        self.baseinfo = baseinfo

    def build_loaction_info(self, locationinfo):
        self.locationinfo = locationinfo

#whole product 2 Timelined Location
class TimelinedLocation:
    def __init__(self):
        self.casenumbers = None
        self.baseinfo = None
        self.locationinfo = None
        self.timelines = None

    def build_casenumber(self, casenumber):
        self.casenumbers = casenumber

    def build_baseinfo(self, baseinfo):
        self.baseinfo = baseinfo

    def build_loaction_infor(self, locationinfo):
        self.locationinfo = locationinfo

    def build_timeline(self, timelines):
        self.timelines = timelines
        

class BuildLocation(Builder):
    def __init__(self) -> None:
        self.reset()
    
    def reset(self) -> None:
        self._location = Location()

    @property
    def location(self) -> Location:
         location = self._location
         self.reset()
         return location  

    def casenumber_builder(self) -> None:
        self._location.build_casenumber

    def baseinfo_builder(self) -> None:
        self._location.build_baseinfo

    def loaction_info_builder(self) -> None:
        self._location.build_loaction_info

class BuildTimeLinedLocation(Builder):
    def __init__(self) -> None:
        self.reset()
    
    def reset(self) -> None:
        self.timelined_location = TimelinedLocation()

    @property
    def Timelinedlocation(self) -> TimelinedLocation:
         timelined_location = self._timelined_location
         self.reset()
         return timelined_location  

    def casenumber_builder(self) -> None:
        self.timelined_location.build_casenumber

    def baseinfo_builder(self) -> None:
        self.timelined_location.build_baseinfo

    def loaction_info_builder(self) -> None:
        self.timelined_location.build_loaction_infor

    def timeline_builder(self) -> None:
        self.timelined_location.build_timeline

class Director:
    def __init__(self) -> None:
        self._builder = None

    def set_builder(self, builder: Builder) -> None:
        self._builder = builder

    def buildLoaction(self) -> None:
        self._builder.baseinfo_builder()
        self._builder.casenumber_builder()
        self._builder.loaction_info_builder()

    def buildTimelinedLocation(self) -> None:
        self._builder.loaction_info_builder()
        self._builder.baseinfo_builder()
        self._builder.casenumber_builder()
        self._builder.timeline_builder()



# pylint: disable=redefined-builtin,invalid-name
# class Location:  # pylint: disable=too-many-instance-attributes
#     """
#     A location in the world affected by the coronavirus.
#     """

#     def __init__(
#         self, id, country, province, coordinates, last_updated, confirmed, deaths, recovered,
#     ):  # pylint: disable=too-many-arguments
#         # General info.
#         self.id = id
#         self.country = country.strip()
#         self.province = province.strip()
#         self.coordinates = coordinates

#         # Last update.
#         self.last_updated = last_updated

#         # Statistics.
#         self.confirmed = confirmed
#         self.deaths = deaths
#         self.recovered = recovered

#     @property
#     def country_code(self):
#         """
#         Gets the alpha-2 code represention of the country. Returns 'XX' if none is found.

#         :returns: The country code.
#         :rtype: str
#         """
#         return (countries.country_code(self.country) or countries.DEFAULT_COUNTRY_CODE).upper()

#     @property
#     def country_population(self):
#         """
#         Gets the population of this location.

#         :returns: The population.
#         :rtype: int
#         """
#         return country_population(self.country_code)

#     def serialize(self):
#         """
#         Serializes the location into a dict.

#         :returns: The serialized location.
#         :rtype: dict
#         """
#         return {
#             # General info.
#             "id": self.id,
#             "country": self.country,
#             "country_code": self.country_code,
#             "country_population": self.country_population,
#             "province": self.province,
#             # Coordinates.
#             "coordinates": self.coordinates.serialize(),
#             # Last updated.
#             "last_updated": self.last_updated,
#             # Latest data (statistics).
#             "latest": {
#                 "confirmed": self.confirmed,
#                 "deaths": self.deaths,
#                 "recovered": self.recovered,
#             },
#         }


# class TimelinedLocation(Location):
#     """
#     A location with timelines.
#     """

#     # pylint: disable=too-many-arguments
#     def __init__(self, id, country, province, coordinates, last_updated, timelines):
#         super().__init__(
#             # General info.
#             id,
#             country,
#             province,
#             coordinates,
#             last_updated,
#             # Statistics (retrieve latest from timelines).
#             confirmed=timelines.get("confirmed").latest or 0,
#             deaths=timelines.get("deaths").latest or 0,
#             recovered=timelines.get("recovered").latest or 0,
#         )

#         # Set timelines.
#         self.timelines = timelines

#     # pylint: disable=arguments-differ
#     def serialize(self, timelines=False):
#         """
#         Serializes the location into a dict.

#         :param timelines: Whether to include the timelines.
#         :returns: The serialized location.
#         :rtype: dict
#         """
#         serialized = super().serialize()

#         # Whether to include the timelines or not.
#         if timelines:
#             serialized.update(
#                 {
#                     "timelines": {
#                         # Serialize all the timelines.
#                         key: value.serialize()
#                         for (key, value) in self.timelines.items()
#                     }
#                 }
#             )

#         # Return the serialized location.
#         return serialized
