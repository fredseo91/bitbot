import os

path_to_file = os.path.join(os.path.dirname(__file__), 'tokens.txt')
equal_string = " = "

def get_tokens():

    token_list = ["access", "secret", "slack_token"]
    token_return = {}

    with open(path_to_file, 'r') as file:
        strings = file.readlines()

        for string in strings:

            for token in token_list:
                if token in string:
                    temp = token + equal_string
                    string = string.replace(temp, "")
                    token_return[token] = string
    return token_return


if __name__ == '__main__':
    print(get_tokens())
