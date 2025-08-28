from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .database import SessionLocal, engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()



@app.post("/tasks/", response_model=schemas.Task, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_new_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    
    return crud.create_task(db=db, task=task)

@app.get("/tasks/", response_model=List[schemas.Task], tags=["Tasks"])
def read_all_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks

@app.get("/tasks/{task_id}", response_model=schemas.Task, tags=["Tasks"])
def read_single_task(task_id: int, db: Session = Depends(get_db)):
  
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.put("/tasks/{task_id}", response_model=schemas.Task, tags=["Tasks"])
def update_existing_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
   
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task(db=db, db_task=db_task, task_update=task_update)

@app.delete("/tasks/{task_id}", response_model=schemas.Task, tags=["Tasks"])
def delete_existing_task(task_id: int, db: Session = Depends(get_db)):
 
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.delete_task(db=db, db_task=db_task)