"""
        return self.get(db, id) is not None
        """
            True если существует, False если нет
        Returns:
            
            id: ID записи
            db: Сессия базы данных
        Args:
        
        Проверить существование записи.
        """
    def exists(self, db: Session, id: int) -> bool:
    
        return db.query(self.model).count()
        """
            Количество записей в таблице
        Returns:
            
            db: Сессия базы данных
        Args:
        
        Подсчитать количество записей.
        """
    def count(self, db: Session) -> int:
    
        return True
        db.commit()
        db.delete(db_obj)
        
            return False
        if db_obj is None:
        db_obj = self.get(db, id)
        """
            True если удалено, False если не найдено
        Returns:
            
            id: ID записи для удаления
            db: Сессия базы данных
        Args:
        
        Удалить запись.
        """
    def delete(self, db: Session, *, id: int) -> bool:
    
        return db_obj
        db.refresh(db_obj)
        db.commit()
        
                setattr(db_obj, field, value)
            if hasattr(db_obj, field):
        for field, value in kwargs.items():
        
            return None
        if db_obj is None:
        db_obj = self.get(db, id)
        """
            Обновлённый объект или None
        Returns:
            
            **kwargs: Поля для обновления
            id: ID записи для обновления
            db: Сессия базы данных
        Args:
        
        Обновить запись.
        """
    ) -> Optional[ModelType]:
        **kwargs
        id: int, 
        *, 
        db: Session, 
        self, 
    def update(
    
        return db.query(self.model).all()
        """
            Список всех объектов
        Returns:
            
            db: Сессия базы данных
        Args:
        
        Получить все записи.
        """
    def get_all(self, db: Session) -> List[ModelType]:
    
        return db.query(self.model).offset(skip).limit(limit).all()
        """
            Список объектов
        Returns:
            
            limit: Максимальное количество записей
            skip: Сколько записей пропустить
            db: Сессия базы данных
        Args:
        
        Получить список записей с пагинацией.
        """
    ) -> List[ModelType]:
        limit: int = 100
        skip: int = 0, 
        *, 
        db: Session, 
        self, 
    def get_multi(
    
        return db.query(self.model).filter(field == value).first()
            raise ValueError(f"Field '{field_name}' not found in {self.model.__name__}")
        if field is None:
        field = getattr(self.model, field_name, None)
        """
            Первый найденный объект или None
        Returns:
            
            value: Значение для поиска
            field_name: Имя поля
            db: Сессия базы данных
        Args:
        
        Получить запись по значению поля.
        """
    ) -> Optional[ModelType]:
        value: Any
        field_name: str, 
        db: Session, 
        self, 
    def get_by_field(
    
        return db.query(self.model).filter(self.model.id == id).first()
        """
            Объект или None, если не найден
        Returns:
            
            id: ID записи
            db: Сессия базы данных
        Args:
        
        Получить запись по ID.
        """
    def get(self, db: Session, id: int) -> Optional[ModelType]:
    
        return db_obj
        db.refresh(db_obj)
        db.commit()
        db.add(db_obj)
        db_obj = self.model(**kwargs)
        """
            >>> author = crud.create(db, name="Толстой", country="Россия")
            >>> crud = BaseCRUD(Author)
        Example:
            
            Созданный объект
        Returns:
            
            **kwargs: Поля для создания объекта
            db: Сессия базы данных
        Args:
        
        Создать новую запись.
        """
    def create(self, db: Session, **kwargs) -> ModelType:
    
        self.model = model
        """
            model: Класс модели SQLAlchemy
        Args:
        """
    def __init__(self, model: Type[ModelType]):
    
    """
    Использует паттерн Generic для типизации.
    
    Все остальные CRUD классы наследуются от него.
    Базовый класс с CRUD операциями.
    """
class BaseCRUD(Generic[ModelType]):


ModelType = TypeVar("ModelType", bound=BaseModel)

from app.models.base import BaseModel
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from typing import TypeVar, Generic, Type, Optional, List, Any

"""
Базовый класс для CRUD операций
=========
Base CRUD

