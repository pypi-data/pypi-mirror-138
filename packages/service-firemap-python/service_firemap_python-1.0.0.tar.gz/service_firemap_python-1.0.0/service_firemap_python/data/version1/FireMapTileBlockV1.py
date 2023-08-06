# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Dict

from .FireMapTileStatusV1 import FireMapTileStatusV1


@dataclass
class FireMapTileBlockV1:
    id: str  # Rounder center lng_lat_zoom
    zoom: int  # Zoom level
    flng: float  # From longitude
    flat: float  # From latitude
    tlng: float  # To longitude
    tlat: float  # To latitude

    clear: Dict[str, FireMapTileStatusV1]  # Map with clear tiles
    smoke: Dict[str, FireMapTileStatusV1]  # Map with smoke tiles
    fire: Dict[str, FireMapTileStatusV1]  # Map with fire tiles
