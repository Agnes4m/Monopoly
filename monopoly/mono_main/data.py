import json
from typing import Dict, List

from gsuid_core.data_store import get_res_path

from .utils import Player, AllData, Building


async def save_game(id: str, data: AllData):
    """保存游戏"""
    with open(
        get_res_path(['mono', f"{id}.json"]), mode="w", encoding="utf-8"
    ) as f:
        json.dump(data.dict(), f)
    return True


async def load_game(id: str):
    """读取游戏"""
    with open(
        get_res_path(['mono', f"{id}.json"]), mode="r", encoding="utf-8"
    ) as f:
        data = json.load(f)
        all_data = AllData(**data)
    return all_data


async def default_player(
    name: str, players: List[Dict[str, str]] = [], location_length: int = 20
):
    """初始化信息"""
    data = AllData(
        location_length,
        sence_buildings=[
            Building(name="起点", price=0, payment=0, location="起点"),
            Building(name="郑州", price=1000, payment=0, location="空地"),
            Building(name="长沙", price=1000, payment=0, location="空地"),
        ],
        players=[
            Player(name=players[0]),
        ],
    )
