from classes.chat_classes import AssistantMessage, UserMessage, UserInput

# Esta función construye el contenido de la conversacion entre el usuario
# y el asistente (texto e imagen) en el formato que el modelo de OpenAI espera.
def build_content(input: UserInput):
    obj = UserInput.model_validate(input)
    conversation = []

    for msg in obj.conversacion:

        if isinstance(msg, UserMessage):
            content = []

            if msg.text:
                content.append({
                    "type": "input_text",
                    "text": msg.text
                })

            if msg.image_url:
                content.append({
                    "type": "input_image",
                    "image_url": msg.image_url
                })

            conversation.append({
                "role": "user",
                "content": content
            })

        elif isinstance(msg, AssistantMessage):
            conversation.append({
                "role": "assistant",
                "content": msg.text
            })

    return conversation

def load_master_prompt():
    with open("master_prompt.txt", "r", encoding="utf-8") as file:
        return file.read()

