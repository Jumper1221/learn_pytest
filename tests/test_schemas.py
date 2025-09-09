# tests/test_schemas.py
import pytest
from pydantic import ValidationError
from schemas import ItemCreate

def test_item_create_success():
    """Тест успешного создания схемы ItemCreate."""
    item = ItemCreate(name="Valid Name", description="Valid description")
    assert item.name == "Valid Name"
    assert item.description == "Valid description"

def test_item_create_cursed_name_fails():
    """Тест провала валидации, если имя содержит 'Cursed'."""
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(name="A Cursed Sword", description="Very shiny")
    
    # Проверяем, что в сообщении об ошибке есть нужный текст
    assert "Item name cannot be 'Cursed'" in str(exc_info.value)

def test_item_create_same_name_and_description_fails():
    """Тест провала валидации, если имя и описание совпадают."""
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(name="Repetitive", description="Repetitive")
    
    assert "Name and description cannot be the same" in str(exc_info.value)

def test_item_create_no_description_success():
    """Тест успешного создания, когда описание отсутствует."""
    item = ItemCreate(name="Just a name")
    assert item.name == "Just a name"
    assert item.description is None