from pydantic import BaseModel


class SQLPair(BaseModel):
    question: str
    sql_query: str
