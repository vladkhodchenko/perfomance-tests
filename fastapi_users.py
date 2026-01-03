from fastapi import FastAPI, Query, Path,  Body, APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr, RootModel


app = FastAPI()


users_router = APIRouter(
    prefix = "/api/v1/users",
    tags = ["users-service"]
)

class UserIn(BaseModel):
    email: EmailStr
    username: str


class UserOut(UserIn):
    id: int


class UsersStore(RootModel):
    root: list[UserOut]

    def find(self, user_id: int) -> UserOut | None:
        return next(filter(lambda user: user.id == user_id, self.root), None)

    def create(self, user_in: UserIn) -> UserOut:
        user = UserOut(id=len(self.root)+1, **user_in.model_dump())
        self.root.append(user)
        return user

    def update(self, user_id: int, user_in: UserIn) -> UserOut:
        """
        Обновляет существующего пользователя по ID.
        """
        # Находим индекс существующей записи
        index = next(index for index, user in enumerate(self.root) if user.id == user_id)
        # Создаём новый объект с тем же ID и обновлёнными полями
        updated = UserOut(id=user_id, **user_in.model_dump())
        # Заменяем в списке
        self.root[index] = updated
        return updated

    def delete(self, user_id: int) -> None:
        """
        Удаляет пользователя по ID, фильтруя список.
        """
        self.root = [user for user in self.root if user.id != user_id]



store = UsersStore(root=[])

@users_router.get("/{user_id}", response_model=UserOut)
async def get_user():
    """
    GET /api/v1/users/{user_id}
    Возвращает пользователя по ID или 404, если не найден.
    """
    if not (user := store.find(user_id)):
        raise HTTPException(
            detail=f"User with id {user_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

    return user


@users_router.get("", response_model=list[UserOut])
async def get_users():
    """
    GET /api/v1/users
    Возвращает список всех пользователей.
    """
    return store.root


@users_router.post("", response_model=UserOut)
async def create_user(user: UserIn):
    """
    POST /api/v1/users
    Создаёт нового пользователя и возвращает его данные с ID.
    """
    return store.create(user)


@users_router.post("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user: UserIn):
    """
    PUT /api/v1/users/{user_id}
    Обновляет данные пользователя по ID или возвращает 404, если не существует.
    """
    if not store.find(user_id):
        raise HTTPException(
            detail=f"User with id {user_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

    return store.update(user_id, user)


@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    """
    DELETE /api/v1/users/{user_id}
    Удаляет пользователя по ID или возвращает 404, если не существует.
    """
    if not store.find(user_id):
        raise HTTPException(
            detail=f"User with id {user_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

    store.delete(user_id)
    # При status_code=204 тело ответа пустое


app.include_router(users_router)
