from typing import List

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
  
  async def parse_matrix(self , text_matrix:str) :
    matrix = []
    for line in text_matrix.splitlines():
        line = line.strip()
        if not line or line.startswith('+'):
            continue
        # берём числа из строки
        numbers = re.findall(r'\d+', line)
        if numbers:
            for n in numbers :
              matrix.append([int(n)])
    return matrix

  async def traversal_matrix(self , matrix: List[List[int]]) -> List[int] :
    pass
    
  


async def get_matrix(url:str) -> List[int] :
    
    pass
  