import os

def write_openai_api_key_to_file(key):
    if os.name == 'nt':  # Check if the OS is Windows
        config_dir = os.getenv('APPDATA')
    else:
        config_dir = os.path.join(os.path.expanduser('~'), '.config')
    mindflow_dir = os.path.join(config_dir, 'mindflow')
    if not os.path.exists(mindflow_dir):
        os.makedirs(mindflow_dir)
    key_file = os.path.join(mindflow_dir, 'api_key.txt')
    with open(key_file, 'w') as f:
        f.write(key)
    print("Wrote API key to", key_file)