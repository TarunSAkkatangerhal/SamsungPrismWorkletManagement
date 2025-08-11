from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models.user import User
from app.models.worklet import Worklet
from app.schemas.worklet import WorkletCreate, WorkletOut, WorkletUpdate
from app.core.dependencies import get_current_user, require_admin_or_mentor

router = APIRouter()

# Public - Get all active worklets
@router.get("/", response_model=List[WorkletOut])
def get_worklets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    worklets = db.query(Worklet).filter(Worklet.is_active == True).offset(skip).limit(limit).all()
    return worklets

# Public - Get worklet by ID
@router.get("/{worklet_id}", response_model=WorkletOut)
def get_worklet(worklet_id: int, db: Session = Depends(get_db)):
    worklet = db.query(Worklet).filter(Worklet.id == worklet_id, Worklet.is_active == True).first()
    if not worklet:
        raise HTTPException(status_code=404, detail="Worklet not found")
    return worklet

# Admin/Mentor - Create worklet
@router.post("/", response_model=WorkletOut)
def create_worklet(
    worklet_data: WorkletCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_mentor)
):
    new_worklet = Worklet(**worklet_data.dict(), created_by=current_user.id)
    db.add(new_worklet)
    db.commit()
    db.refresh(new_worklet)
    return new_worklet

# Admin/Mentor - Update worklet
@router.put("/{worklet_id}", response_model=WorkletOut)
def update_worklet(
    worklet_id: int,
    worklet_data: WorkletUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_mentor)
):
    worklet = db.query(Worklet).filter(Worklet.id == worklet_id).first()
    if not worklet:
        raise HTTPException(status_code=404, detail="Worklet not found")
    
    # Allow updates only by creator or admin
    if worklet.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = worklet_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(worklet, field, value)
    
    db.commit()
    db.refresh(worklet)
    return worklet

# Admin/Mentor - Delete worklet (soft delete)
@router.delete("/{worklet_id}")
def delete_worklet(
    worklet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_mentor)
):
    worklet = db.query(Worklet).filter(Worklet.id == worklet_id).first()
    if not worklet:
        raise HTTPException(status_code=404, detail="Worklet not found")
    
    # Allow deletion only by creator or admin
    if worklet.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    worklet.is_active = False
    db.commit()
    return {"message": "Worklet deleted successfully"}

# Get worklets by category
@router.get("/category/{category}", response_model=List[WorkletOut])
def get_worklets_by_category(category: str, db: Session = Depends(get_db)):
    worklets = db.query(Worklet).filter(
        Worklet.category.ilike(f"%{category}%"),
        Worklet.is_active == True
    ).all()
    return worklets
