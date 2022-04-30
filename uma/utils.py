# Copyright (c) 2022 - Jojo#7791
# Licensed under MIT

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any

__all__ = ["ChampInfo", "NodeInfo", "WarInfo"]


CHAMP_KEYS = (
    "name",
    "released",
    "class",
    "tier",
    "rank",
    "prestige",
    "hp",
    "attack",
    "crit_rate",
    "crit_dmge",
    "armor",
    "block_prof",
    "energy_resist",
    "physical_resist",
    "crit_resist",
    "sig_info",
    "abilities",
    "challenger_rating",
    "tags",
    "contact",
    "url_page",
    "img_portrait",
    "champid",
)


@dataclass(frozen=True)
class ChampInfo:
    name: str
    released: str
    _class: str
    tier: int
    rank: int
    prestige: int
    hp: int
    attack: int
    crit_rate: int
    crit_dmge: int
    armor: int
    block_prof: int
    energy_resist: int
    physical_resist: int
    crit_resist: int
    sig_info: List[str]
    abilities: Dict[str, Any]
    challenger_rating: int
    tags: List[str]
    contact: str
    url_page: str
    img_portrait: str  # NOTE this url doesn't seem to actually *point* to anything so it's pretty useless
    champid: str

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> ChampInfo:
        payload = {k: data[k] for k in CHAMP_KEYS}
        payload["_class"] = payload.pop("class")
        return cls(**payload)

NODE_KEYS = (
    "node_id", "node_name", "node_info",
)


@dataclass(frozen=True)
class NodeInfo:
    node_id: int
    node_name: str
    node_info: str

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> NodeInfo:
        return cls(
            node_id=data["node_id"],
            node_name=data["node_name"],
            node_info=data["node_info"],
        )


WAR_KEYS = (
    "tier",
    "nodes",
    "difficulty",
    "tier_multiplier",
    "tier_rank",
)


@dataclass(frozen=True)
class WarInfo:
    tier: int
    nodes: Dict[str, List[str]]
    difficulty: str
    tier_multiplier: str
    tier_rank: str

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> WarInfo:
        return cls(
            tier=data["tier"],
            nodes=data["nodes"],
            difficulty=data["difficulty"],
            tier_multiplier=data["tier_multiplier"],
            tier_rank=data["tier_rank"],
        )
