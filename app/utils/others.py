""" 
async def fake_video_streamer():
    for i in range(1, 11):
        await anyio.sleep(2)
        yield f"Data point {i}\n"
        #await asyncio.sleep(1)  # Simulate some asynchronous work

def fake_data_streamer():
    for i in range(10):
        yield b'some fake data\n\n'
        time.sleep(1.0)
        

@router.get("/stream-data")
async def stream_data():
    return StreamingResponse(fake_video_streamer(), media_type='text/event-stream') """