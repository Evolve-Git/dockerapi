from fastapi import Form, FastAPI, Depends, HTTPException, Body
from typing import Optional, List
from models import ContainerResponse, ContainerCreate
from db import get_db_connection
from auth import create_access_token, verify_password, get_current_user

app = FastAPI(
    title="Container Tracker API",
    version="1.0",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

@app.get("/api/containers", response_model=List[ContainerResponse])
def search_containers(
    q: Optional[str] = None,
    current_user: str = Depends(get_current_user)
):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            if q:
                query = "SELECT id, container_number, cost FROM containers WHERE container_number LIKE %s"
                cursor.execute(query, (f"%{q}%",))
            else:
                query = "SELECT id, container_number, cost FROM containers LIMIT 50"
                cursor.execute(query)
            results = cursor.fetchall()
            return results
    finally:
        connection.close()

@app.get("/api/containers/by-cost", response_model=List[ContainerResponse])
def search_by_cost(
    cost: Optional[float] = None,
    min: Optional[float] = None,
    max: Optional[float] = None,
    current_user: str = Depends(get_current_user)
):
    if not any([cost, min, max]):
        raise HTTPException(status_code=400, detail="At least one parameter (cost, min, max) is required")

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            if cost is not None:
                query = "SELECT id, container_number, cost FROM containers WHERE cost = %s"
                cursor.execute(query, (cost,))
            else:
                conditions = []
                params = []
                if min is not None:
                    conditions.append("cost >= %s")
                    params.append(min)
                if max is not None:
                    conditions.append("cost <= %s")
                    params.append(max)
                where_clause = " AND ".join(conditions)
                query = f"SELECT id, container_number, cost FROM containers WHERE {where_clause}"
                cursor.execute(query, params)
            results = cursor.fetchall()
            return results
    finally:
        connection.close()

@app.post("/api/containers", response_model=ContainerResponse, status_code=201)
def create_container(
    container: ContainerCreate,
    current_user: str = Depends(get_current_user)
):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM containers WHERE container_number = %s", (container.container_number,))
            if cursor.fetchone():
                raise HTTPException(status_code=409, detail="Container number already exists")

            query = "INSERT INTO containers (container_number, cost) VALUES (%s, %s)"
            cursor.execute(query, (container.container_number, round(container.cost, 2)))
            connection.commit()

            cursor.execute("SELECT id, container_number, cost FROM containers WHERE container_number = %s", (container.container_number,))
            new_container = cursor.fetchone()
            return new_container
    except Exception as e:
        connection.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        connection.close()

@app.post("/token", include_in_schema=False)
def login_for_access_token(
    username: str = Form(...),
    password: str = Form(...),
    # client_id: str = Form(None),
    # client_secret: str = Form(None),
    grant_type: str = Form(...)
):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT username, password_hash FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            if not user:
                raise HTTPException(status_code=400, detail="Incorrect username or password")
            if not verify_password(password, user["password_hash"]):
                raise HTTPException(status_code=400, detail="Incorrect username or password")

            token = create_access_token(data={"sub": user["username"]})
            return {
                "access_token": token,
                "token_type": "bearer",
                "expires_in": 3600
            }
    finally:
        connection.close()