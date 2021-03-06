from enum import Enum, unique, auto
from typing import Optional
from pydantic import BaseModel


class NewGoal(BaseModel):
    cat_id: Optional[int] = None
    goal_title: Optional[str] = None

    def complete(self) -> bool:
        return None not in (self.cat_id, self.goal_title)


@unique
class StateEnum(Enum):
    CREATE_CATEGORY_STATE = auto()
    CHOOSE_CATEGORY = auto()


class FSMData(BaseModel):
    state: StateEnum
    goal: NewGoal
    board_id: Optional[int] = None


FSM_STATES: dict[int, FSMData] = dict()
