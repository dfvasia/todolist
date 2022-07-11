from enum import Enum, unique, auto
from typing import Optional
from datetime import date
from pydantic import BaseModel


class NewGoal(BaseModel):
    cat_id: Optional[int] = None
    goal_title: Optional[str] = None
    due_date: Optional[date] = None  # datetime.now()

    def complete(self) -> bool:
        return None not in (self.cat_id, self.goal_title, self.due_date)


@unique
class StateEnum(Enum):
    CREATE_CATEGORY_STATE = 1
    CHOOSE_CATEGORY = 2


class FSMData(BaseModel):
    state: StateEnum
    goal: NewGoal
    board_id: Optional[int] = None


FSM_STATES: dict[int, FSMData] = dict()
