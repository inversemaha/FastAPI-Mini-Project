"""
Schema registry for handling forward references in a scalable way.
This pattern is used by major FastAPI applications in production.
"""
from typing import Dict, Type
from pydantic import BaseModel


class SchemaRegistry:
    """Centralized registry for Pydantic models with forward references."""
    
    _models: Dict[str, Type[BaseModel]] = {}
    _rebuilt: bool = False
    
    @classmethod
    def register(cls, model_class: Type[BaseModel]) -> Type[BaseModel]:
        """Register a model class that may have forward references."""
        cls._models[model_class.__name__] = model_class
        return model_class
    
    @classmethod
    def rebuild_all(cls) -> None:
        """Rebuild all registered models to resolve forward references."""
        if cls._rebuilt:
            return
            
        # Import all schema modules to ensure all models are available
        from app.schemas import author, book, genre, borrow_record
        
        # Rebuild all models that have forward references
        for model_class in cls._models.values():
            try:
                model_class.model_rebuild()
            except Exception as e:
                print(f"Warning: Could not rebuild {model_class.__name__}: {e}")
        
        cls._rebuilt = True
    
    @classmethod
    def get_model(cls, name: str) -> Type[BaseModel]:
        """Get a registered model by name."""
        return cls._models.get(name)


# Convenience decorator
def register_schema(cls: Type[BaseModel]) -> Type[BaseModel]:
    """Decorator to register schemas with forward references."""
    return SchemaRegistry.register(cls)