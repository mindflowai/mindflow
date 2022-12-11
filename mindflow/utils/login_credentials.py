import os
import configparser

def get_login_credentials(create_new = False) -> dict:
    # Get the directory containing the package
    package_dir = os.path.dirname(__file__)

    # Create the configuration file path
    config_file = os.path.join(package_dir, "config.ini")

    # Check if the configuration file exists
    if os.path.exists(config_file) and not create_new:
        # Read the configuration from the file
        config = configparser.ConfigParser()
        config.read(config_file)
    else:
        # Prompt the user for the configuration values
        print("Please specify either your email and password or your session token.")
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        session_token = input("Enter your session token: ")

        # Create the config parser
        config = configparser.ConfigParser()

        # Set the configuration values
        config["DEFAULT"] = {
            "email": email,
            "password": password,
            "session_token": session_token,
        }

        # Save the configuration to the file
        with open(config_file, "w") as f:
            config.write(f)
    
    return dict(config["DEFAULT"])
