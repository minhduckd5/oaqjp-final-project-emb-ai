import requests
import json


def emotion_detector(text_to_analyze):
    """
    Detect emotions in the given text using Watson NLP Emotion Predict function.

    Args:
        text_to_analyze (str): The text to analyze for emotions

    Returns:
        dict: Emotion scores and dominant emotion name
    """
    # URL for Watson NLP Emotion Predict function
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'

    # Headers required for the API request
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

    # Input JSON format with the text to analyze
    input_json = {"raw_document": {"text": text_to_analyze}}

    # Make POST request to Watson NLP API
    response = requests.post(url, headers=headers, json=input_json)

    # Handle error responses (e.g., blank input may return status code 400 or 200 with empty data)
    if response.status_code == 400:
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

    # Convert response text to dictionary for structured access
    response_dict = json.loads(response.text)

    # Check if emotionPredictions is empty or missing (blank input case)
    if not response_dict.get("emotionPredictions") or not response_dict.get("emotionPredictions")[0].get("emotion"):
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

    # Extract required emotion scores from the first prediction
    emotions = response_dict.get("emotionPredictions", [{}])[0].get("emotion", {})
    anger_score = emotions.get("anger", 0)
    disgust_score = emotions.get("disgust", 0)
    fear_score = emotions.get("fear", 0)
    joy_score = emotions.get("joy", 0)
    sadness_score = emotions.get("sadness", 0)

    # Determine the dominant emotion based on the highest score
    emotion_scores = {
        "anger": anger_score,
        "disgust": disgust_score,
        "fear": fear_score,
        "joy": joy_score,
        "sadness": sadness_score,
    }
    dominant_emotion = max(emotion_scores.items(), key=lambda item: item[1])[0]

    # Return formatted output with individual scores and dominant emotion
    return {
        "anger": anger_score,
        "disgust": disgust_score,
        "fear": fear_score,
        "joy": joy_score,
        "sadness": sadness_score,
        "dominant_emotion": dominant_emotion,
    }
