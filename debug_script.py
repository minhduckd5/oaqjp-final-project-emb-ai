import inspect
from EmotionDetection import emotion_detector

print("Source code of emotion_detector:")
print(inspect.getsource(emotion_detector))
print("\nFile location:")
print(inspect.getfile(emotion_detector))
