from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import logging

app = FastAPI()

# Enable CORS
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


df = pd.read_csv('updated_drone_data.csv')
logging.basicConfig(level=logging.INFO)

current_index = 0


async def get_drone_data(index: int):
    if index < 0 or index >= len(df):
        return {"error": "Index out of bounds"}
    row = df.iloc[index].to_dict()
    logging.info(f"Sending data: {row}")
    return row


@app.get("/")
async def get_all_drone_data():
    data = df.to_dict(orient='records')
    return JSONResponse(data)


@app.get("/stream_data")
async def stream_drone_data():
    global current_index
    if current_index >= len(df):
        current_index = 0
    row_data = await get_drone_data(current_index)
    current_index += 1
    return JSONResponse(row_data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, debug=True)
