from typing import List
import asyncio
import aiohttp
import re


class MatrixFetchError(Exception):
    """Исключение при ошибке загрузки матрицы."""
    pass


class MatrixHandler : 
  def __init__(self , url:str):
    if not url:
        raise ValueError("url не может быть пустым")
    self.url = url

  async def fetch_matrix(self) -> str :
    timeout = aiohttp.ClientTimeout(total=3)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(self.url) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientResponseError as e:
        raise MatrixFetchError(f"Ошибка сервера: {e.status}") from e
    except (aiohttp.ClientConnectionError, aiohttp.ServerTimeoutError) as e:
        raise MatrixFetchError(f"Сетевая ошибка: {e}") from e 
  
  async def parse_matrix(self , text_matrix:str) -> List[List[int]]:
    matrix = []
    for line in text_matrix.splitlines():
        line = line.strip()
        if not line or line.startswith('+'):
            continue
        # берём числа из строки
        numbers = re.findall(r'\d+', line)
        if numbers:
            matrix.append([int(n) for n in numbers])
    return matrix





  async def traversal_matrix(self , matrix: List[List[int]]) -> List[int] :
    if not matrix:
      return []
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        #левый столбец
        for i in range(top, bottom + 1):
            result.append(matrix[i][left])
        left += 1

        # нижняя строка
        for j in range(left, right + 1):
            result.append(matrix[bottom][j])
        bottom -= 1

        # правый столбец
        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][right])
            right -= 1

        # верхняя строка
        if top <= bottom:
            for j in range(right, left - 1, -1):
                result.append(matrix[top][j])
            top += 1

    return result
    
  


async def get_matrix(url:str) -> List[int] :
    matrix_obj = MatrixHandler(url)
    text = await matrix_obj.fetch_matrix()
    matrix = await matrix_obj.parse_matrix(text)
    return await matrix_obj.traversal_matrix(matrix)



async def main():
    SOURCE_URL = 'https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt'
    result = await get_matrix(SOURCE_URL)
    print("Получено:", result)
    

if __name__ == "__main__":
    asyncio.run(main())
  