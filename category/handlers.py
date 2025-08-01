from models.category import Category
from core.database import SessionLocal

def create_category(name: str):
    session = SessionLocal()
    try:
        category = Category(name=name)
        session.add(category)
        session.commit()
        session.refresh(category)
        return category
    except:
        session.rollback()
        raise
    finally:
        session.close()

def get_all_categories():
    session = SessionLocal()
    try:
        return session.query(Category).all()
    finally:
        session.close()

def get_category_by_id(category_id: int):
    session = SessionLocal()
    try:
        return session.query(Category).filter_by(id=category_id).first()
    finally:
        session.close()

def update_category(category_id: int, name: str):
    session = SessionLocal()
    try:
        category = session.query(Category).get(category_id)
        if not category:
            return None
        category.name = name
        session.commit()
        return category
    except:
        session.rollback()
        raise
    finally:
        session.close()

def delete_category(category_id: int):
    session = SessionLocal()
    try:
        category = session.query(Category).get(category_id)
        if not category:
            return None
        session.delete(category)
        session.commit()
        return True
    except:
        session.rollback()
        raise
    finally:
        session.close()