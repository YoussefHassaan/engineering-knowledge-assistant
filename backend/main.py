from fastapi import FastAPI , HTTPException
from pydantic import BaseModel

app = FastAPI()

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
    return  employees

@app.get("/employees/{employee_id}")
async def get_employee(employee_id: int):
    for employee in employees:
        if employee.id == employee_id:
            return employee
    raise HTTPException(status_code=404, detail="Employee not found")

@app.post("/employees")
async def create_employee(new_employee: createEmployee):
    new_id = len(employees) + 1
    new_employee = employee(id=new_id, **new_employee.model_dump())
    employees.append(new_employee)
    return new_employee

@app.put("/employees/{employee_id}")
async def update_employee(employee_id: int, updated_employee: createEmployee):
    for index,emp in enumerate(employees):
        if emp.id == employee_id:
            employees[index] = employee(id=employee_id, **updated_employee.model_dump())
            return employees[index]
    raise HTTPException(status_code=404, detail="Employee not found")

@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id: int):
    for index, emp in enumerate(employees):
        if emp.id == employee_id:
            del employees[index]
            return {"detail": "Employee deleted"}
    raise HTTPException(status_code=404, detail="Employee not found")

