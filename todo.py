from fastapi import APIRouter
from typing import Dict, List
from pydantic import BaseModel

# todo_list 리스트 객체
todo_list: List[Dict] = []

# APIRouter 클래스 생성
router = APIRouter()


# POST 방식 - todo_list에 새로운 항목 추가
@router.post("/add_todo", response_model=Dict)
async def add_todo(todo_item: Dict) -> Dict:
    """
    todo_list에 새로운 항목을 추가합니다.
    
    Args:
        todo_item: 추가할 todo 항목 (Dict 타입)
    
    Returns:
        Dict: 추가된 todo 항목과 상태 정보
    """
    todo_list.append(todo_item)
    return {
        "status": "success",
        "message": "Todo item added successfully",
        "item": todo_item,
        "total_items": len(todo_list)
    }


# GET 방식 - todo_list 가져오기
@router.get("/retrieve_todo", response_model=Dict)
async def retrieve_todo() -> Dict:
    """
    todo_list를 가져옵니다.
    
    Returns:
        Dict: todo_list와 상태 정보
    """
    return {
        "status": "success",
        "todo_list": todo_list,
        "total_items": len(todo_list)
    }

