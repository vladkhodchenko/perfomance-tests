from fastapi import FastAPI, Query, Path,  Body, APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
import uvicorn


app = FastAPI(title="basics")


router = APIRouter(
    prefix="/api/v1",             # общий префикс для всех путей в этом роутере
    tags=["Basics"]               # в Swagger UI группа будет помечена тегом "Basics"
)

class User(BaseModel):
    username: str  # логин пользователя
    email: str     # email пользователя
    age: int       # возраст пользователя


class UserResponse(BaseModel):
    username: str
    email: str
    message: str


def validate_min_age(min_age: int = 18):
    def checker(user: User):
        if user.age < min_age:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User must be at least {min_age} years old"
            )
        return user

    return checker

@router.get(  # Вместо app используем router
    "/basics/{item_id}",
    summary="Получить базовую информацию по item_id"
)

async def get_basics(
    name: str = Query(                      # query-параметр name
        default="Alise",
        description="Имя пользователя"
    ),
    item_id: int = Path(                    # path-параметр item_id
        ...,                                # обязательный (без default)
        description="Идентификатор элемента"
    )
):
    # возвращаем сообщение с именем и номером элемента
    return {
        "message": f"Hello, {name}!",
        "description": f"Item number {item_id}"
    }


@router.post(  # Вместо app используем router
    "/basics/users",
    response_model=UserResponse,
    summary="Создать нового пользователя"
)
async def create_user(
    user: User = Body(..., description="Данные нового пользователя")
):
    # FastAPI автоматически:
    # 1) распарсит JSON из тела запроса
    # 2) провалидирует его по полям модели User
    return UserResponse(
        username=user.username,
        email=user.email,
        message="User created successfully!"
    )


@router.post("/basics/register", summary="Регистрация пользователя с проверкой возраста")
async def register_user(
        user: User = Depends(validate_min_age(min_age=21))  # внедряем зависимость
):
    return {
        "message": f"User {user.username} registered successfully",
        "email": user.email,
        "age": user.age
    }


app.include_router(router)


if __name__ == "__main__":

    uvicorn.run(
        "fastapi_basics:app",  # "<module_name>:<app_instance>"
        host="127.0.0.1",  # адрес, на котором слушаем входящие подключения
        port=8000,  # порт
        reload=True,  # перезагрузка при изменении файлов
        log_level="info"  # уровень логирования
    )