import tiktoken

tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")

print(tokenizer.encode_batch(["Hello, world!", "Whats up?"]))
