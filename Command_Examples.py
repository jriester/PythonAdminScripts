import textwrap

from Helper_Functions import *

user_configs = None


def init():
    """
    Initializes the user_configs variable.
    """
    global user_configs
    user_configs = load_config()

    # Set the environment variables for Confluent Platform
    os.environ['CONFLUENT_HOME'] = user_configs.get("File", "confluent_home")
    os.environ['PATH'] += os.pathsep + os.path.join(os.environ['CONFLUENT_HOME'], 'bin')


def prompt_with_validation(prompt_message, valid_responses=['yes', 'no']):
    """
    Prompts the user with a message and validates the response.

    Args:
        prompt_message: The prompt message.
        valid_responses: The valid responses.

    Returns:
        The response.
    """
    prompt_message += f" ({', '.join(valid_responses)}): "
    lower_responses = [response.lower() for response in valid_responses]  # convert valid responses to lowercase
    while True:
        response = input(prompt_message).lower()
        if response in lower_responses:
            return response
        else:
            print(f"Invalid response. Valid responses are: {', '.join(valid_responses)}")
            prompt_message = f"{prompt_message[:-3]} ({', '.join(valid_responses)}): "


# Print and execute the appropriate command
def print_and_run(command):
    """
    Prints and runs the command.

    Args:
        command: The command.
    """
    print(f"Command to use: \n {command}")
    # subprocess.run(command, shell=True, check=True)


def check_defaults(config, keys):
    """
    Checks if the keys have default values.

    Args:
        config: The configuration.
        keys: The keys to check.

    Returns:
        The keys with default values.
    """
    defaults = []
    for key in keys:
        section, option = key.split('.')
        value = config.get(section, option)
        if value.startswith('<') and value.endswith('>'):
            defaults.append(key)
    return defaults


def generate_curl_command():
    """
    Generates the CURL command.

    Returns:
        The CURL command.
    """
    # Get values from config file
    broker_api_key = user_configs.get('Cluster_Connection', 'broker_api_key')
    broker_api_secret = user_configs.get('Cluster_Connection', 'broker_api_secret')
    schemaregistry_api_key = user_configs.get('Cluster_Connection', 'schemaregistry_api_key')
    schemaregistry_api_secret = user_configs.get('Cluster_Connection', 'schemaregistry_api_secret')
    value_schema = user_configs.get('Cluster_Connection', 'value_schema')
    data_to_write = user_configs.get('Cluster_Connection', 'data_to_write')
    topic_name = user_configs.get('Cluster_Connection', 'topic_name')
    bootstrap_server = user_configs.get('Cluster_Connection', 'bootstrap_server')
    bootstrap_port = user_configs.get('Cluster_Connection', 'bootstrap_port')

    # Prompt user for security protocol
    valid_protocols = ['PLAINTEXT', 'SSL', 'SASL_PLAINTEXT', 'SASL_SSL']
    protocol = prompt_with_validation("Enter the security protocol required on the Kafka broker", valid_protocols)

    message_content = data_to_write
    # Prompt user for message content
    if message_content == '':
        message_content = input("Enter the content of the message to post: ")

    # Generate CURL command
    curl_command = f"curl -X POST -H 'Content-Type: application/vnd.kafka.json.v2+json' -H 'Accept: application/vnd.kafka.v2+json' --data '{{\"records\":[{{\"value\":\"{message_content}\"}}]}}' '{'https' if protocol == 'SSL' else 'http'}://{bootstrap_server}:{bootstrap_port}/topics/{topic_name}'"

    # Add security protocol to CURL command
    if protocol != 'PLAINTEXT':
        curl_command += f" --broker-list '{bootstrap_server}:{bootstrap_port}' --producer.config client-{protocol.lower()}.properties"

    # Add authentication to CURL command
    if protocol == 'SASL_PLAINTEXT' or protocol == 'SASL_SSL':
        curl_command += f" -u '{broker_api_key}:{broker_api_secret}' --property schema.registry.basic.auth.user.info='{schemaregistry_api_key}:{schemaregistry_api_secret}'"

    # Add value schema to CURL command
    if value_schema != '':
        curl_command += f" --property value.schema='{value_schema}'"

    # Add message content to CURL command
    if data_to_write != '':
        curl_command = curl_command.replace(f"'{{'records':[{{'value':'{message_content}'}}]}}'", f"'{data_to_write}'")

    # Need Schema CURL commands
    # curl -X GET http://localhost:8081/subjects/Kafka-value/versions

    # Wrap CURL command at 80 characters
    wrapped_command = textwrap.wrap(curl_command, width=80)
    wrapped_command = " \\\n    ".join(wrapped_command)
    # Print CURL command
    # print(f"CURL command:\n {curl_command}")
    return wrapped_command


# Need option to reach Schema and data from file

init()

valid_responses = ['curl', 'cli', 'console']
output = prompt_with_validation("Which output do you want to see?", valid_responses)
if output == 'curl':
    # print('Sample CURL commands for Confluent Cloud:')
    # TODO this needs work to test, I think this needs to be base64

    keys = ['Cluster_Connection.broker_api_key', 'Cluster_Connection.value_schema', 'Cluster_Connection.data_to_write',
            'Cluster_Connection.bootstrap_server', 'Cluster_Connection.bootstrap_port']
    defaults = check_defaults(user_configs, keys)
    if defaults:
        print("Do something if all default values")

    command = generate_curl_command()

    print(command)
