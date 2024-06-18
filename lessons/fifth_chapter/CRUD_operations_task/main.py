from fastapi import FastAPI, HTTPException
from databases import Database
from models.models import ToDoCreate, ToDoUpdate, ToDoReturn
from core.config import settings


app = FastAPI()

database = Database(settings.ASYNC_DB_URL)


# тут устанавливаем условия подключения к базе данных и отключения
@app.on_event("startup")
async def startup_database():
    await database.connect()


@app.on_event("shutdown")
async def shutdown_database():
    await database.disconnect()


@app.post("/create/", response_model=ToDoReturn)
async def create_todo(todo: ToDoCreate):
    query = ("INSERT INTO todo_table (title, description, completed) "
             "VALUES (:title, :description, :completed) RETURNING id")
    values = {
        "title": todo.title,
        "description": todo.description,
        "completed": False
    }
    try:
        todo_id = await database.execute(query=query, values=values)
        return ToDoReturn(**todo.model_dump(), id=todo_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create todo")


@app.get("/todo/{todo_id}", response_model=ToDoReturn)
async def get_todo(todo_id: int):
    query = "SELECT * FROM todo_table WHERE id = :todo_id"
    values = {"todo_id": todo_id}
    try:
        result = await database.fetch_one(query=query, values=values)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch todo from database")
    if result:
        return ToDoReturn(
            title=result["title"],
            description=result["description"],
            completed=result["completed"],
            id=result['id']
        )
    else:
        raise HTTPException(status_code=404, detail="Todo not found")


@app.put("/todo/{todo_id}", response_model=ToDoReturn)
async def update_todo(todo_id: int, todo: ToDoUpdate):
    query = ("UPDATE todo_table "
             "SET title = :title, description = :description, completed = :completed "
             "WHERE id = :todo_id")
    values = {
        "todo_id": todo_id,
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed
    }
    try:
        await database.execute(query=query, values=values)
        return ToDoReturn(**todo.model_dump(), id=todo_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to update todo in database")


@app.delete("/todo/{todo_id}", response_model=dict)
async def delete_todo(todo_id: int):
    query = "DELETE FROM todo_table WHERE id = :todo_id RETURNING id"
    values = {"todo_id": todo_id}
    try:
        deleted_rows = await database.execute(query=query, values=values)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to update todo in database")
    if deleted_rows:
        return {"message": "Todo deleted"}
    else:
        raise HTTPException(status_code=404, detail="Todo not found")
