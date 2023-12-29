import tiktoken

from client import base_model

encoding = tiktoken.encoding_for_model(base_model)


def num_tokens_from_string(string):
    """Returns the number of tokens in a text string."""
    num_tokens = len(encoding.encode(string))
    return num_tokens
