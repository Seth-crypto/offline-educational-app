# content/database.py
import os

# This dictionary holds all the content.
# 'image' keys are filenames found in assets/images/
TOPICS = {
    "history": {
        "title": "World History",
        "intro": "Explore the annals of human civilization.",
        "content": [
            {
                "title": "The Ancient Egyptians",
                "text": "Ancient Egypt was a civilization of ancient North Africa, concentrated along the lower reaches of the Nile River, situated in the place that is now the country Egypt. It is one of the six historic civilizations to arise independently.",
                "image": "egypt.jpg" 
            },
            {
                "title": "The Industrial Revolution",
                "text": "The Industrial Revolution was the transition to new manufacturing processes in Great Britain, continental Europe, and the United States, in the period from about 1760 to sometime between 1820 and 1840.",
                "image": "industrial.jpg"
            }
        ],
        "quiz": [
            {
                "question": "Which civilization built the Pyramids?",
                "options": ["Romans", "Greeks", "Egyptians", "Mayans"],
                "answer": "Egyptians"
            },
            {
                "question": "In which century did the Industrial Revolution begin?",
                "options": ["18th Century", "20th Century", "15th Century", "10th Century"],
                "answer": "18th Century"
            }
        ]
    },
    "science": {
        "title": "General Science",
        "intro": "Discover the laws of nature and the universe.",
        "content": [
            {
                "title": "The Solar System",
                "text": "The Solar System is the gravitationally bound system of the Sun and the objects that orbit it, either directly or indirectly.",
                "image": "space.jpg"
            },
            {
                "title": "Photosynthesis",
                "text": "Photosynthesis is the process used by plants, algae and certain bacteria to harness energy from sunlight and turn it into chemical energy.",
                "image": "plant.jpg"
            }
        ],
        "quiz": [
            {
                "question": "What is the center of our Solar System?",
                "options": ["Earth", "Moon", "Sun", "Mars"],
                "answer": "Sun"
            }
        ]
    }
}
