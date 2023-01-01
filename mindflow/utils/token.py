
import os
import getpass

def set_token(token): 
    """
    This function is used to set the token for the user.
    """
    if token is None:
        token = getpass.getpass("Authorization Key: ")
        
    with open(os.path.join(os.path.expanduser("~"), ".mindflow"), "w") as f:
        f.write(token)
        f.close()
    
    print("Token set successfully.")

def get_token():
    """
    This function is used to get the token for the user.
    """
    with open(os.path.join(os.path.expanduser("~"), ".mindflow"), "r") as f:
        token = f.read()
        f.close()
    return token
    