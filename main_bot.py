# import required modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

import pyaudio
import wave
import wavio
import soundfile as sf
import sounddevice as sd
from pydub import AudioSegment

name = "Kailas_Walldoddi_MOFKRAH"
leave_meeting = False; 

opt = Options()
opt.add_argument('--disable-blink-features=AutomationControlled')
opt.add_argument('--start-maximized')
opt.add_experimental_option("prefs", {
	"profile.default_content_setting_values.media_stream_mic": 1,
	"profile.default_content_setting_values.media_stream_camera": 1,
	"profile.default_content_setting_values.geolocation": 0,
	"profile.default_content_setting_values.notifications": 1,
	"excludeSwitches": ["disable-popup-blocking"]
})
opt.add_argument("--disable-popup-blocking")
driver = webdriver.Chrome(options=opt)

def turnOffMicCam():
     # turn off Microphone
     time.sleep(2)
     driver.find_element(By.CSS_SELECTOR,'div.U26fgb.JRY2Pb.mUbCce.kpROve.yBiuPb.y1zVCf.M9Bg4d.HNeRed').click()
     driver.save_screenshot("screenshots/mic-off.png")
     print('mic off')
     time.sleep(5)
     
     # turn off camera
     driver.find_element(By.CSS_SELECTOR,'#yDmH0d > c-wiz > div > div > div:nth-child(29) > div.crqnQb > div > div.gAGjv > div.vgJExf > div > div > div.ZUpb4c > div.oORaUb.NONs6c > div > div.EhAUAc > div.GOH7Zb > div > div.U26fgb.JRY2Pb.mUbCce.kpROve.yBiuPb.y1zVCf.M9Bg4d.HNeRed').click()
     driver.save_screenshot("screenshots/camera-off.png")
     print('camera off')
     time.sleep(5)


def joinNow():
    # Join meet
    print("opened meet link")
    time.sleep(2)
    
    driver.find_element(By.CLASS_NAME, "qdOxv-fmcmS-wGMbrd").send_keys(name)
    time.sleep(2)
    
    
    try:
        # Try to find and click the "Join now" button
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Join now']"))).click()
        print("Entered meet successfully\n")
    except Exception as e:
        print("Meeting is not open, asking host to let in...")
        try:
            # Find and click the "Ask to join" button
            ask_to_join_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Ask to join']")))
            ask_to_join_button.click()
            driver.save_screenshot("screenshots/ask-to-join.png")
            print("Request to join sent, waiting for the host to let in...")
            time.sleep(2)
            # Wait until the "Asking to be let in..." element disappears, indicating that the bot has been admitted
            WebDriverWait(driver, 300).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div#c35.dHFSie")))
            print("Entered meet successfully after host approval\n")
        except Exception as e:
            print("Some error occurred, exiting the operation:", e)
            raise e

    time.sleep(2)



def record_audio(duration, output_filename):

    ###### audio recording using pyAudio 

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024

    audio = pyaudio.PyAudio()
    driver.save_screenshot("screenshots/joined.png")

    for i in range(audio.get_device_count()):
        print(f"Device {i}: {audio.get_device_info_by_index(i)['name']}")

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    
    print("Recording...")
    frames = []
    # global leave_meeting
    # while not leave_meeting:
    #     check_for_inactivity()
    #     data = stream.read(CHUNK)
    #     frames.append(data)

    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)
    driver.save_screenshot("screenshots/recording-done.png")
    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

# Check for inactivity (simple example: leave if only the bot is present)
def check_for_inactivity():
    global leave_meeting
    participants = len(driver.find_elements(By.CLASS_NAME, 'participant-tile'))
    print(f"Participants: {participants}")
    if participants <= 1:  # Assuming the bot itself is 1 participant
        leave_meeting = True
        print("Inactivity detected, leaving the meeting...")

    time.sleep(5)  # Check every 5 seconds

def leave_meeting_and_cleanup():
    # Leave the call
    driver.find_element(By.XPATH, '//*[@aria-label="Leave call"]').click()
    print("Left the meeting")
    time.sleep(3)  # Ensure the call ends

    # Close the browser
    driver.quit()
    print("Browser closed, operation complete.")


driver.get('https://meet.google.com/peb-vzug-qkq')
time.sleep(3)
driver.save_screenshot("screenshots/opening-link.png")

turnOffMicCam()
joinNow()

## wait untill the bot entered the meet

DURATION = 60 #second
record_audio(DURATION, 'meeting_audio.wav')
leave_meeting_and_cleanup()