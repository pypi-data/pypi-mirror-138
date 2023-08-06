# -*- coding: utf-8 -*-
import datetime
from copy import deepcopy

from pip_services3_commons.data import FilterParams

from service_firemap_python.data.version1 import FireMapTileStatusV1
from service_firemap_python.data.version1.FireMapTileBlockV1 import FireMapTileBlockV1
from service_firemap_python.persistence.IFireMapPersistence import IFireMapPersistence

tile1 = FireMapTileStatusV1(
    id='DO00FF00AA',
    flng=-120,
    flat=51,
    tlng=-118,
    tlat=50,

    updated=datetime.datetime.now(),
    drone_id='drone 1',
    people=5,
    people_updated=datetime.datetime.now()
)

BLOCK1 = FireMapTileBlockV1(
    id='DO00AA00AA',
    zoom=3,
    flat=51,
    flng=-120,
    tlat=50,
    tlng=-118,
    clear={tile1.id: deepcopy(tile1)},
    smoke={tile1.id: deepcopy(tile1)},
    fire={tile1.id: deepcopy(tile1)},
)

tile2 = FireMapTileStatusV1(
    id='DO05RR00AA',
    flng=-120,
    flat=56,
    tlng=-118,
    tlat=55,

    updated=datetime.datetime.now(),
    drone_id='drone 2',
    people=10,
    people_updated=datetime.datetime.now()
)
BLOCK2 = FireMapTileBlockV1(
    id='DO05AA00AA',
    zoom=3,
    flat=56,
    flng=-120,
    tlat=55,
    tlng=-118,
    clear={tile2.id: deepcopy(tile2)},
    smoke={tile2.id: deepcopy(tile2)},
    fire={tile2.id: deepcopy(tile2)},
)


class FireMapPersistenceFixture:
    _persistence: IFireMapPersistence

    def __init__(self, persistence: IFireMapPersistence):
        assert persistence is not None
        self._persistence = persistence

    def test_get_and_update_fire_maps(self):
        # create blocks
        self._persistence.update_tile_blocks(None, [BLOCK1, BLOCK2])

        page = self._persistence.get_tile_blocks_by_filter(None, None, None)

        assert len(page.data) == 2

        block1: FireMapTileBlockV1 = page.data[0]
        block2: FireMapTileBlockV1 = page.data[1]

        assert BLOCK1.id == block1.id
        assert BLOCK1.zoom == block1.zoom
        assert BLOCK1.flat == block1.flat
        assert BLOCK1.flng == block1.flng
        assert BLOCK1.tlat == block1.tlat
        assert BLOCK1.tlng == block1.tlng
        assert len(BLOCK1.clear) == len(block1.clear)

        assert BLOCK2.id == block2.id
        assert BLOCK2.zoom == block2.zoom
        assert BLOCK2.flat == block2.flat
        assert BLOCK2.flng == block2.flng
        assert BLOCK2.tlat == block2.tlat
        assert BLOCK2.tlng == block2.tlng
        assert len(BLOCK2.clear) == len(block2.clear)

        block2.zoom = 2
        block2.clear['DO05RR00AA'].people = 30

        # update blocks
        self._persistence.update_tile_blocks(None, [block2])

        # get with filters
        page = self._persistence.get_tile_blocks_by_filter(None, FilterParams.from_tuples('zoom', 2), None)

        assert len(page.data) == 1

        block2 = page.data[0]

        assert BLOCK2.id == block2.id
        assert block2.zoom == 2
        assert BLOCK2.flat == block2.flat
        assert BLOCK2.flng == block2.flng
        assert BLOCK2.tlat == block2.tlat
        assert BLOCK2.tlng == block2.tlng
        assert block2.clear['DO05RR00AA'].people == 30
