from classes import UserInput

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
        raise ValueError("Debes proporcionar al menos una pregunta o una imagen.")

    return content

