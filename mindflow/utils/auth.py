import os

OPENAI_API_KEY_LINK = "https://platform.openai.com/account/api-keys"

def get_key_file_path():
    if os.name == 'nt':  # Check if the OS is Windows
        config_dir = os.getenv('APPDATA')
    else:
        config_dir = os.path.join(os.path.expanduser('~'), '.config')
    mindflow_dir = os.path.join(config_dir, 'mindflow')
    return os.path.join(mindflow_dir, 'api_key.txt')

def write_key_to_file(key):
    key_file_path = get_key_file_path()
    if not os.path.exists(os.path.dirname(key_file_path)):
        os.makedirs(os.path.dirname(key_file_path))
    with open(key_file_path, 'w') as f:
        f.write(key)

def api_key_file_exists():
    key_file_path = get_key_file_path()
    return os.path.exists(key_file_path)

def get_api_key():
    if not api_key_file_exists():
        raise ValueError(f"OpenAI API Key not found. Please run `mf login` and paste in your openAI API key. You can find it here: {OPENAI_API_KEY_LINK}")

    key_file_path = get_key_file_path()
    if not os.path.exists(key_file_path):
        raise FileNotFoundError(f"{key_file_path} not found. Make sure you have saved your API key by calling write_key_to_file function.")
    with open(key_file_path, 'r') as f:
        api_key = f.read().strip()
    return api_key
