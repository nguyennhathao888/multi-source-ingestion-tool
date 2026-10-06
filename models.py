from pydantic import BaseModel, Field

class product(BaseModel):
    id: int
    title: str
    category: str
    price: float= Field(gt=0)
    rating: float=Field(ge=0,le=5)
    stock: int=Field(ge=0)



    
    
