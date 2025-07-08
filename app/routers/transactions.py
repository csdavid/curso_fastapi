from fastapi import APIRouter, HTTPException, Query, status
from models import Transaction, TransactionCreate, Customer
from sqlmodel import SQLModel, Field, Relationship
from db import SessionDep
from sqlmodel import select

router = APIRouter(tags=["transactions"])


@router.post("/transactions", status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction_data: TransactionCreate, session: SessionDep):
    transaction_data_dict = transaction_data.model_dump()
    print(transaction_data_dict)
    customer = session.get(Customer, transaction_data_dict.get("customer_id"))
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )

    transaction_db = Transaction.model_validate(transaction_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)

    return transaction_db


@router.get("/transactions")
async def list_transactions(
    session: SessionDep,
    skip: int = Query(0, description="Number of transactions to skip"),
    limit: int = Query(10, description="Number of transactions to return"),
):
    query = select(Transaction).offset(skip).limit(limit)
    transactions = session.exec(query).all()
    return transactions
