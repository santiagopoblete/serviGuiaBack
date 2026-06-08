from functions.chat_functions import build_content
from classes.chat_classes import UserInput, Message


def test_build_content_text_message():
    user_input = UserInput(
        conversacion=[
            Message(
                role="user",
                text="Necesito un plomero"
            )
        ]
    )

    result = build_content(user_input)

    assert result == [
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "Necesito un plomero"
                }
            ]
        }
    ]


def test_build_content_image_message():
    user_input = UserInput(
        conversacion=[
            Message(
                role="user",
                image_url="https://example.com/image.jpg"
            )
        ]
    )

    result = build_content(user_input)

    assert result[0]["role"] == "user"
    assert result[0]["content"][0]["type"] == "input_image"


def test_build_content_assistant_message():
    user_input = UserInput(
        conversacion=[
            Message(
                role="assistant",
                text="Hola"
            )
        ]
    )

    result = build_content(user_input)

    assert result == [
        {
            "role": "assistant",
            "content": "Hola"
        }
    ]