# -*- coding: utf-8 -*-
from typing import Optional

from aiohttp import ClientSession


async def fetch(query: str, intro: int, session: ClientSession) -> str:
    async with session.post(
        "https://yandex.ru/lab/api/yalm/text3",
        json={"query": query, "intro": intro, "filter": 1},
    ) as resp:
        r = await resp.json()
    return f"{r['query']}{r['text']}"


async def balaboba(
    query: str, *, intro: int = 0, session: Optional[ClientSession] = None
) -> str:
    """Отправка запроса Яндекс Балабобе.

    Args:
        query (str): Текст для Балабобы.
        intro (int, optional): Вариант стилизации.
            0 - Без стиля. По умолчанию.
            1 - Теории заговора.
            2 - ТВ-репортажи.
            3 - Тосты.
            4 - Пацанские цитаты.
            5 - Рекламные слоганы.
            6 - Короткие истории.
            7 - Подписи в Instagram.
            8 - Короче, Википедия.
            9 - Синопсисы фильмов.
            10 - Гороскоп.
            11 - Народные мудрости.
            18 - Новый Европейский Театр.
        session (Optional[ClientSession], optional): По умолчанию None.

    Returns:
        str: Ответ Балабобы.

    Examples:
        >>> response = await balaboba("Привет")

        >>> response = await balaboba("Привет", intro=11)

        >>> from aiohttp import ClientSession
        ... async with ClientSession() as session:
        ...     response = await balaboba("Привет", session=session)
    """
    if isinstance(session, ClientSession) and not session.closed:
        return await fetch(query, intro, session)
    async with ClientSession() as s:
        return await fetch(query, intro, s)
