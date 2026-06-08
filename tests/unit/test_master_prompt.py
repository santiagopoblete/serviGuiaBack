from functions.chat_functions import load_master_prompt


def test_master_prompt_loads():

    prompt = load_master_prompt()

    assert isinstance(prompt, str)
    assert len(prompt) > 0