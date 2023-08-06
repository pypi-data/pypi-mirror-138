# -*- coding: utf-8 -*-

import datetime
from dataclasses import dataclass


@dataclass
class FireMapTileStatusV1:
    id: str  # QTH locator string

    flng: float  # From longitude
    flat: float  # From latitude
    tlng: float  # To longitude
    tlat: float  # To latitude

    updated: datetime.datetime  # Date and time when status was updated
    drone_id: str  # Drone ID that sent the update

    people: int  # Number of people in the area
    people_updated: datetime.datetime  # Date and time when people was updated
