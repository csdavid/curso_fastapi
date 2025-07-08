from fastapi import APIRouter, status
from models import Plan
from db import SessionDep
from sqlmodel import select

router = APIRouter(tags=["plans"])


@router.post("/plans", status_code=status.HTTP_201_CREATED, response_model=Plan)
async def create_plan(plan_dat: Plan, session: SessionDep):
    plan = Plan.model_validate(plan_dat.model_dump())
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan


@router.get("/plans", response_model=list[Plan])
async def list_plans(session: SessionDep):
    plans = session.exec(select(Plan)).all()
    return plans
