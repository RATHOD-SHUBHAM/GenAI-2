# Todo: Load the Libraries
import moviepy.editor as mp
import base64
from openai import OpenAI
import shutil
import cv2
import os

# Todo: Load the API
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# Todo: LLM calling.
client = OpenAI()

# Todo: Calling the vision model
def base64_vision(prompt):

  response = client.chat.completions.create(
      model = "gpt-4-turbo",
      messages=prompt,
      max_tokens = 300,
  )

  print(response.choices[0].message.content)


# Todo: Seperating video into individual frames.
def extract_frames(video_path, interval = 1):
  # Step 1:  Check if the 'Frames' directory exists, if not - then create it
  if os.path.exists('Frames'):
    # Delete all files in the Frames directory.
    for filename in os.listdir('Frames'):
      file_path = os.path.join('Frames', filename)

      try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
          os.unlike(file_path)
        elif os.path.isdir(file_path):
          shutil.rmtree(file_path)

      except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

  # Open the video file.
  video = cv2.VideoCapture(video_path)

  # Check if video opened successfully
  if not video.isOpened():
    print("Error opening video file")
    return

  # Get the frame rate of the video
  fps = video.get(cv2.CAP_PROP_FPS)

  # Calculate the frame number to skip
  frame_skip = int(fps * interval)

  frame_count = 0

  while True:
    # Read a frame
    success, frame = video.read()

    # If frame read successfully and its the correct interval
    if success and frame_count % frame_skip == 0:
      # Save the frame
      frame_filename = f'Frames/frame_{frame_count}.jpg'

      cv2.imwrite(frame_filename, frame)

      print(f'Saved {frame_filename}')

    if not success:
      break

    # Release the video capture object
    video.release()
    cv2.destroyAllWindows()


def convert_to_base64(image_path):
  with open(image_path, 'rb') as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

# Scrapping and transcribing the audio from the video
def whisper(audio):
  audio_file = open(audio, 'rb')

  transcript = client.audio.transcriptions.create(
      file = audio_file,
      model = 'whisper-1'
  )

  return transcript.text


def extract_audio(video_path):
  # load the video file
  video = mp.VideoFileClip(video_path)

  # extract the audio from the video
  audio = video.audio

  # Save the audio
  if not audio:
    transcript = "There is no audio for this video."
    print(transcript)
    return transcript
  else:
    audio.write_audiofile("video_audio.mp3")
    transcript = whisper("video_audio.mp3")
    print(f"Whisper video transcript: {transcript}")
    return transcript

# Running all the file
def video_GPT():
  frames_directory = "Frames"
  base64frames = []

  # check if the directory exists
  if not os.path.exists(frames_directory):
    os.makedirs(frames_directory)
    print(f"Created {frames_directory} Directory. ")
  else:
    # Clear all the files in the directory
    for filename in os.listdir(frames_directory):
      file_path = os.path.join(frames_directory, filename)

      if os.path.isfile(file_path):
        os.remove(file_path)

  video_path = 'input/test_1.mov'
  extract_frames(video_path, interval = 0.5)
  transcript = extract_audio(video_path)

  for filename in sorted(os.listdir(frames_directory)):
    file_path = os.path.join(frames_directory, filename)

    if os.path.isfile(file_path):
      encoded_image = convert_to_base64(file_path)
      base64frames.append(encoded_image)

  prompt = [
      {
          "role": "user",
          "content":[
              f"Explain what is happening in this sequence of frames, and do it concisely."
              f"Here is the transcript of the video audio in case that helps you:{transcript}",
              *map(lambda x: {"image": x, "resize": 480},
                   base64frames),
          ],
      },
  ]
  base64_vision(prompt)

if __name__ == '__main__':
    video_GPT()
