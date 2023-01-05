from functools import reduce
import json
from typing import Dict, Tuple, TypeVar, cast

from projectl_old import VisibleState

T = TypeVar("T")


def merge_tuple_tuple_in_dict(
    accumulator: Dict[T, Dict[T, T]],
    item: Tuple[Tuple[T, T], T],
) -> Dict[T, Dict[T, T]]:
    ((k1, k2), value) = item
    return {
        **accumulator,
        k1: {**(accumulator.get(k1) or {}), k2: value},
    }


def json_of_game_state(game_state: VisibleState) -> str:
    return json.dumps(
        {
            **game_state,
            "players_pieces": reduce(
                merge_tuple_tuple_in_dict,
                game_state["players_pieces"].items(),
                cast(Dict[int, Dict[int, int]], {}),
            ),
        }
    )
