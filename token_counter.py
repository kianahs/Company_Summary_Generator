import tiktoken


def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:

        print(
            f"Warning: No tokenizer found for model '{model}', using cl100k_base as fallback.")
        encoding = tiktoken.get_encoding("cl100k_base")

    return len(encoding.encode(text))


if __name__ == "__main__":

    res = count_tokens(text="This is a token counting test",
                       model="gpt-3.5-turbo")
    print(res)
