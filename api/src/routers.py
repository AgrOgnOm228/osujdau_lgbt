from fastapi import APIRouter, HTTPException

import src.utils as utils
from src.schemes import Lider

router = APIRouter()

lid: list[Lider] = utils.create_fake_lid()


@router.get('/list')
async def get_liders_list(limit: int = 10, offset: int = 0) -> list[Lider]:
    if offset < 0 or limit < 1:
        raise HTTPException(400, detail="Некорректные параметры пагинации")
    return lid[offset:offset + limit]



@router.get('/{liders_board}')
async def get_lider(liders_board: int) -> Lider:
    try:
        o = lid[liders_board]
        return o
    except IndexError as err:
        raise HTTPException(404,detail='Не правильно указан индекс') from err


@router.post('/')
async def create(
    body: Lider
) -> list[Lider]:
    lid.append(body)
    return lid



# Нужен список(dict) в котором будут храниться данные об одной записи(об одном рекорде).
# При выдаче данных через list нужно сделать так называемую ПАГИНАЦИЮ.
# Пагинация - функция которая обрезает выдачу до определнного момента
# т.е. - есть 10 котят - ты их сортируешь по росту(предположим) и нужно взять 4 за исключением 2-х самых маленьких
# Остается 4 котят

# [,44,55,66,77,88,100,101] -> [44,55,66,77] - limit = 4 - offset = 2
