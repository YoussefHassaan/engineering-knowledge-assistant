from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
import psycopg2
import datetime

app = FastAPI()

conn = psycopg2.connect(
    dbname="fastapi",
    user="postgres",
    password="2407",
    host="localhost"
)
cur = conn.cursor()

employees = []

class createEmployee(BaseModel):
    name: str
    email: str
    department: str
    salary: float

class employee(createEmployee):
    id: int

@app.get("/employees")
async def get_employees():
    cur.execute("SELECT * FROM employees")
    employees = cur.fetchall()
    employees = [dict(zip([column[0] for column in cur.description], row)) for row in employees]
    return employees

@app.get("/employees/{employee_id}")
async def get_employee(employee_id: int):
    cur.execute("SELECT * FROM employees WHERE id = %s", (employee_id,))
    employee = cur.fetchone()
    if employee:
        employee = dict(zip([column[0] for column in cur.description], employee))
        return employee
    raise HTTPException(status_code=404, detail="Employee not found")

@app.post("/employees")
async def create_employee(new_employee: createEmployee):
    cur.execute("INSERT INTO employees (name, email, department, salary) VALUES (%s, %s, %s, %s) RETURNING *", (new_employee.name, new_employee.email, new_employee.department, new_employee.salary))
    added_employee = cur.fetchone()
    added_employee = dict(zip([column[0] for column in cur.description], added_employee))
    conn.commit()
    return added_employee

@app.put("/employees/{employee_id}")
async def update_employee(employee_id: int, updated_employee: createEmployee):
    cur.execute("UPDATE employees SET name =  %s, email = %s, department = %s, salary = %s WHERE id = %s RETURNING *", (updated_employee.name, updated_employee.email, updated_employee.department, updated_employee.salary, employee_id))
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    updated_employee_data = cur.fetchone()
    updated_employee_data = dict(zip([column[0] for column in cur.description], updated_employee_data))
    conn.commit()

    return updated_employee_data

@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id: int):
    cur.execute("DELETE FROM employees WHERE id = %s RETURNING *", (employee_id,))
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    deleted_employee_data = cur.fetchone()
    deleted_employee_data = dict(zip([column[0] for column in cur.description], deleted_employee_data))
    conn.commit()
    return deleted_employee_data

