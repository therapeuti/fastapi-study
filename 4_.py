from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

class Item(BaseModel):
    name: str
    price: float
    description: str | None = None
    

app = FastAPI(debug=True)

@app.post('/items')
def create_item(item: Item):
    return item

if __name__=='__main__':
    uvicorn.run('4_.py:app', reload=True)