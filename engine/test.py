import struct
import time
import traceback
import pvporcupine
import pyaudio


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:

        #pre trained keywords
        porcupine = pvporcupine.create(keywords=["jarvis","alexa"])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        #loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            keyword=struct.unpack_from("h"*(porcupine.frame_length),keyword)

            #preprocessing keyword that comes from mic
            keyword_index=porcupine.process(keyword)

            #checking first keyword detector for not
            if keyword_index>=0:
                print("hotword detected")

                #pressing shortcut key ctrl+j
                import pyautogui as autogui
                autogui.keyDown("ctrl")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("ctrl")

            time.sleep(0.01)

    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()
        print("Error in hotword detection")
        traceback.print_exc()

hotword()