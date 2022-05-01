# Copyright (c) 2022 - Jojo#7791
# Licensed under MIT

import asyncio
import aiohttp
from urllib.parse import quote as _uriquote

from .utils import ChampInfo, NodeInfo, WarInfo
from .exceptions import ChampionException, APIException, NodeException, WarException

from typing import Dict, Any


class Route:
    """The route for requesting data from the api"""

    BASE_URL = "https://api.rexians.tk/"

    def __init__(self, path: str, payload: Any = None, **kwargs):
        self.path = path
        url = self.BASE_URL + self.path
        if payload:
            # So, getting a node just requires `nodes/id` instead of `id=`
            # which is annoying lmfao
            url += str(payload)
        if kwargs:
            url += "&".join(f"{k}={_uriquote(v) if isinstance(v, str) else v}" for k, v in kwargs.items())
        self.url = url


class UMAClient:
    """An async Unofficial MCOC api wrapper"""

    def __init__(self, loop: asyncio.AbstractEventLoop = None):
        self.loop = loop or asyncio.get_event_loop()
        self.session = aiohttp.ClientSession()

    async def get_champ(self, champion: str, tier: int, rank: int) -> ChampInfo:
        """|coro|
        Get a champion from the api
        
        Parameters
        ----------
        champion :class:`str`
            The name of the champion
        tier :class:`int`
            The tier of the champion (1-6 stars)
        rank :class:`int`
            The rank of the champion (1-5)

        Returns
        -------
        :class:`ChampInfo`
            The info about the champion

        Raises
        ------
        ChampionException
            The champion was either not found or an issue with tier/rank
        APIException
            The is something wrong with the api
        """
        r = Route("champs/?", champ=champion, tier=tier, rank=rank)
        try:
            async with self.session.get(r.url) as re:
                if re.status == 500:
                    raise APIException
                elif re.status != 200:
                    raise ChampionException(data["details"])
                data = await re.json()
        except aiohttp.ClientError:
            raise ChampionException

        return ChampInfo.from_json(data)

    async def get_node(self, node: int) -> NodeInfo:
        """|coro|
        Get info for a node

        Parameters
        ----------
        node :class:`int`
            The id of the node

        Returns
        -------
        :class:`NodeInfo`
            The info about the node

        Raises
        ------
        NodeException
            There was something wrong with grabbing the node or the node id was wrong
        APIException
            There is something wrong with the api
        """
        r = Route("nodes/", node)
        try:
            async with self.session.get(r.url) as re:
                if re.status == 500:
                    raise APIException
                elif re.status != 200:
                    raise NodeException(data["details"])
                data = await re.json()
        except Exception as e:
            raise NodeException

        return NodeInfo.from_json(data)

    async def get_war(self, tier: int) -> WarInfo:
        """|coro|
        Get info about a war tier

        Parameters
        ----------
        tier :class:`int`
            The tier of the war
        
        Returns
        -------
        :class:`WarInfo`
            The info about the war

        Raises
        ------
        WarException
            There was something wrong with the tier
        APIException
            There is something wrong with the api
        """
        r = Route("war/", tier)
        try:
            async with self.session.get(r.url) as re:
                if re.status == 500:
                    raise APIException
                elif re.status != 200:
                    raise WarException(data["details"])
                data = await re.json()
        except Exception as e:
            raise WarException

        return WarInfo.from_json(data)

    async def close(self) -> None:
        """|coro|
        Closes the client

        This should always be ran before the process ends.
        """
        await self.session.close()
