import edge_tts

async def generate_audio(text,outputFilename):
    communicate = edge_tts.Communicate(text,"ta-IN-ValluvarNeural")
    await communicate.save(outputFilename)





