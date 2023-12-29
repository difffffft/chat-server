import tiktoken


def num_tokens_from_string(base_model, string):
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(base_model)
    num_tokens = len(encoding.encode(string))
    return num_tokens
