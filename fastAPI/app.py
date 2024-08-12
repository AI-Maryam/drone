from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import xml.etree.ElementTree as ET
import asyncio

app = FastAPI()

async def stream_xml_data():
    tree = ET.parse('droneradar_example.xml')  # Corrected file name
    root = tree.getroot()

    for robin in root.findall('Robin'):
        await asyncio.sleep(1)  # Wait for 1 second before sending the next item
        data = ET.tostring(robin, encoding='unicode')
        print(f"Sending data: {data}")
        yield data

@app.get("/stream-data")
async def stream_data():
    return StreamingResponse(stream_xml_data(), media_type='application/xml')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
