from typing import List

import aiohttp


class MatrixFetchError(Exception):
    """Исключение при ошибке загрузки матрицы."""
    pass


class MatrixHandler : 
  def __init__(self , url:str):
    if url == None :
     print("ошибка")

  async def fetch_matrix(url : str) :
    pass
  
  async def parse_matrix(matrix:str) :
    pass

  async def traversal_matrix(matrix: List[List[int]]) -> List[int] :
    pass
    
  


async def get_matrix(url:str) -> List[int] :
    
    pass
  