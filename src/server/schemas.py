from pydantic import BaseModel
from typing import List, Union

class UploadResponse(BaseModel):
    filename: str
    name: str
    date: str
    status: str
    rows: int
    line_count: Union[int, str]
    columns: List[str]

