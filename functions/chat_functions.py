from classes.chat_classes import UserInput

# Esta función construye el contenido de la conversacion entre el usuario
# y el asistente (texto e imagen) en el formato que el modelo de OpenAI espera.
def build_content(input: UserInput):
    conversation = []

    for i in range(len(input.conversacion)):
        inp = input.conversacion[i]
        cont = []

        if inp.role == "user":
            if inp.text:
                cont.append({
                    "type": "input_text",
                    "text": inp.text
                })

            if inp.image_url:
                cont.append({
                    "type": "input_image",
                    "image_url": inp.image_url
                })

            message_content = {
                "role": inp.role,
                "content": cont
            }

        elif inp.role == "assistant":
            message_content = {
                "role": inp.role,
                "content": inp.text
            }

        if not cont:
            raise ValueError("Debes proporcionar al menos un texto o una imagen.")

        conversation.append(message_content)

    return conversation

def load_master_prompt():
    with open("master_prompt.txt", "r", encoding="utf-8") as file:
        return file.read()

