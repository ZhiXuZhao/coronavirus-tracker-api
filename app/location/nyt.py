"""app.locations.nyt.py"""
from Commit1 import BaseInfo, Director, TimelinedLocation_Builder
from . import BuildTimeLinedLocation, TimelinedLocation, Director, BaseLocation, Locationinfo, CaseNumbers


class NYTLocation(TimelinedLocation):
    """
    A NYT (county) Timelinedlocation.
    """

    # pylint: disable=too-many-arguments,redefined-builtin
    def __init__(self, id, state, county, coordinates, last_updated, timelines):
        """ super().__init__(id, "US", state, coordinates, last_updated, timelines)

        self.state = state
        self.county = county """

        director = Director()
        base = BaseInfo(id=id,last_updated=last_updated)
        locationinfo = Locationinfo(country="US", province=state, coordinates=coordinates)
        builder = BuildTimeLinedLocation(baseinfo=base, geoinfo=locationinfo, timelines=timelines)
        director.set_builder(builder)
        nyt = director.build_location

    def serialize(self, timelines=False):  # pylint: disable=arguments-differ,unused-argument
        """
        Serializes the location into a dict.

        :returns: The serialized location.
        :rtype: dict
        """
        serialized = super().serialize(timelines)

        # Update with new fields.
        serialized.update(
            {"state": self.state, "county": self.county,}
        )

        # Return the serialized location.
        return serialized
