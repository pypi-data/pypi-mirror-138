# -*- coding: utf-8 -*-
from typing import Optional, List

import pymongo
from bson import Decimal128
from pip_services3_commons.data import FilterParams, PagingParams, DataPage
from pip_services3_mongodb.persistence import IdentifiableMongoDbPersistence

from .IFireMapPersistence import IFireMapPersistence
from ..data.version1.FireMapTileBlockV1 import FireMapTileBlockV1


class FireMapMongoDbPersistence(IdentifiableMongoDbPersistence, IFireMapPersistence):

    def __init__(self):
        super().__init__('firemap')
        self._max_page_size = 1000

    def __compose_filter(self, filter: FilterParams):
        filter = filter or FilterParams()
        criteria = []

        flng = filter.get_as_nullable_float('flng')
        flat = filter.get_as_nullable_float('flat')
        tlng = filter.get_as_nullable_float('tlng')
        tlat = filter.get_as_nullable_float('tlat')

        zoom = filter.get_as_nullable_integer('zoom')

        coordinates = filter.get_as_nullable_string('coordinates')

        if isinstance(coordinates, str):
            coordinates = coordinates.split(',')
        if not isinstance(coordinates, list):
            coordinates = None

        flng2 = None
        tlng2 = None

        # round to the next tile for current zoom
        if all([flng, flat, tlng, tlat]):
            # if coordinates is left top and right bottom corners
            if flat > tlat:
                flat, tlat = tlat, flat

            # if coordinates pass through the last meridian
            if flng > tlng:
                flng2 = -180
                tlng2 = tlng
                tlng = 180

        # get blocks for coordinates
        if coordinates:
            for location in coordinates:
                lat, long = location.split(';')
                lat, long = float(lat), float(long)
                criteria.extend([{'$and': [{'flng': {'$lte': long}}, {'tlng': {'$gte': long}},
                                           {'flat': {'$gte': lat}}, {'tlat': {'$lte': lat}}]}])

            criteria = [{'$or': criteria}]

        if flng and tlng:
            criteria.extend([{'flng': {'$gte': flng, '$lte': tlng}}, {'tlng': {'$gte': flng, '$lte': tlng}}])

            if flng2 and tlng2:
                criteria.extend([{'flng': {'$gte': flng2, '$lte': tlng2}}, {'tlng': {'$gte': flng2, '$lte': tlng2}}])
                criteria = [{'$or': criteria}]

        if flat and tlat:
            criteria.extend([{'flat': {'$gte': flat, '$lte': tlat}}, {'tlat': {'$gte': flat, '$lte': tlat}}])
        if zoom:
            criteria.append({'zoom': zoom})
        return None if len(criteria) < 1 else {'$and': criteria}

    def get_tile_blocks_by_filter(self, correlation_id: Optional[str], filter: FilterParams,
                                  paging: PagingParams) -> DataPage:
        # get blocks in passed coordinates
        page = self.get_page_by_filter(correlation_id, self.__compose_filter(filter), paging, None, None)

        return page

    def update_tile_blocks(self, correlation_id: Optional[str], updates: List[FireMapTileBlockV1]):
        if updates is None:
            return

        operations = []

        for update in updates:
            update_item = self._convert_from_public(update)
            operation = pymongo.operations.UpdateOne({'_id': update_item['_id']}, {'$set': update_item}, upsert=True)
            operations.append(operation)

        result = self._collection.bulk_write(operations)

        if len(result.bulk_api_result['writeErrors']) == 0 and len(result.bulk_api_result['writeConcernErrors']) == 0:
            self._logger.trace(correlation_id, "Updated %s firemap blocks %s", self._collection_name, len(operations))

    def _convert_from_public(self, value: FireMapTileBlockV1) -> dict:
        decimal_keys = ['flng', 'flat', 'tlng', 'tlat']

        converted = super()._convert_from_public(value)

        for id in value.clear.keys():
            clear_tile = super()._convert_from_public(value.clear[id])
            smoke_tile = super()._convert_from_public(value.smoke[id])
            fire_tile = super()._convert_from_public(value.fire[id])

            # convert coordinates to mongo decimals
            for key in decimal_keys:
                clear_tile[key] = Decimal128(str(clear_tile[key]))
                smoke_tile[key] = Decimal128(str(smoke_tile[key]))
                fire_tile[key] = Decimal128(str(fire_tile[key]))

            converted['clear'][id] = clear_tile
            converted['smoke'][id] = smoke_tile
            converted['fire'][id] = fire_tile

        for key in decimal_keys:
            converted[key] = Decimal128(str(converted[key]))

        return converted

    def _convert_to_public(self, value: dict) -> FireMapTileBlockV1:
        decimal_keys = ['flng', 'flat', 'tlng', 'tlat']

        for key in decimal_keys:
            value[key] = float(str(value[key]))

        converted = super()._convert_to_public(value)

        for id in value['clear'].keys():

            # convert coordinates from mongo decimals
            for key in decimal_keys:
                value['clear'][id][key] = float(str(value['clear'][id][key]))
                value['smoke'][id][key] = float(str(value['smoke'][id][key]))
                value['fire'][id][key] = float(str(value['fire'][id][key]))

            converted.clear[id] = super()._convert_to_public(value['clear'][id])
            converted.smoke[id] = super()._convert_to_public(value['smoke'][id])
            converted.fire[id] = super()._convert_to_public(value['fire'][id])

        return converted
