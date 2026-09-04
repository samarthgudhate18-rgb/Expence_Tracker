from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Backend.database import get_connection, create_table


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Expense(BaseModel):
    title: str
    amount: float
    category: str


create_table()


@app.get("/")
def home():
    return {"message": "Expense Tracker API is working!"}


@app.get("/expenses")
def get_expenses():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM expenses")

    expenses = cursor.fetchall()

    connection.close()

    return expenses


@app.post("/expenses")
def add_expense(expense: Expense):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO expenses (title, amount, category)
        VALUES (?, ?, ?)
        """,
        (expense.title, expense.amount, expense.category)
    )

    connection.commit()

    new_id = cursor.lastrowid

    connection.close()

    return {
        "id": new_id,
        "title": expense.title,
        "amount": expense.amount,
        "category": expense.category
    }

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    connection.commit()

    connection.close()

    return {"message": "Expense deleted successfully"}

@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, expense: Expense):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE expenses
        SET title = ?, amount = ?, category = ?
        WHERE id = ?
        """,
        (expense.title, expense.amount, expense.category, expense_id)
    )

    connection.commit()

    connection.close()

    return {
        "message": "Expense updated successfully",
        "id": expense_id,
        "title": expense.title,
        "amount": expense.amount,
        "category": expense.category
    }