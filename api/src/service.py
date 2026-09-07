import math

from fastapi import HTTPException
from fastapi.responses import HTMLResponse

from src.routers import lid


async def get_home_page() -> HTMLResponse:
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Главная страница</title>
        <style>
            body { font-family: sans-serif; padding: 2rem; background-color: #f4f4f9; }
            .container { max-width: 800px; margin: 0 auto; background: white;
            padding: 2rem; border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Привет из FastAPI!</h1>
            <p>Это простая HTML-страница, отданная через APIRouter.</p>
            <a href="/api/v1/docs">Перейти к Swagger UI (/api/v1/docs)</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


async def get_leaders_page(page: int = 1, size: int = 10) -> HTMLResponse:

    sorted_lid = sorted(lid, key=lambda x: x.score, reverse=True)

    offset = (page - 1) * size
    total_pages = math.ceil(len(sorted_lid) / size) if sorted_lid else 0

    if total_pages > 0 and page > total_pages:
        raise HTTPException(404, detail="Страница не найдена")

    leaders = sorted_lid[offset:offset + size]

    rows_html = ""
    for idx, lider in enumerate(leaders, start=offset + 1):
        rows_html += f"""
        <tr>
            <td>{idx}</td>
            <td>{lider.name}</td>
            <td>{lider.score}</td>
        </tr>
        """

    pagination_html = ""
    if page > 1:
        pagination_html += f'<a href="/leaders?page={page-1}&size={size}">← Назад</a> '
    for p in range(1, total_pages + 1):
        if p == page:
            pagination_html += f'<span style="font-weight:bold;">{p}</span> '
        else:
            pagination_html += f'<a href="/leaders?page={p}&size={size}">{p}</a> '
    if page < total_pages:
        pagination_html += f'<a href="/leaders?page={page+1}&size={size}">Вперёд →</a>'

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Таблица лидеров</title>
        <style>
            body {{ font-family: sans-serif; padding: 2rem; background-color: #f4f4f9; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 2rem; border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 1rem; }}
            th, td {{ padding: 0.5rem; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #f2f2f2; }}
            .pagination a {{ margin-right: 5px; text-decoration: none; }}
            .pagination a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Таблица лидеров</h1>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Имя</th>
                        <th>Очки</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
            <div class="pagination">
                {pagination_html}
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
