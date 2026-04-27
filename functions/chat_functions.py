from classes.chat_classes import UserInput

# Esta función construye el contenido de la entrada del usuario (texto e imagen)
# en el formato que el modelo de OpenAI espera.
def build_content(input: UserInput):
    content = []

    if input.text:
        content.append({
            "type": "input_text",
            "text": input.text
        })

    if input.image_url:
        content.append({
            "type": "input_image",
            "image_url": input.image_url
        })

    if not content:
        raise ValueError("Debes proporcionar al menos un texto o una imagen.")

    return content

def load_master_prompt():
    with open("master_prompt.txt", "r", encoding="utf-8") as file:
        return file.read()

