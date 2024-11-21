import tiktoken
import emoji
import random


def text_to_tokens(text, max_per_row=10):
    ids = enc.encode(text)
    unique_tokens = set(ids)
    # map all tokens we see to a unique emoji
    id_to_emoji = {id: emoji for emoji, id in zip(emojis, unique_tokens)}
    # do the translatation
    lines = []
    for i in range(0, len(ids), max_per_row):
        lines.append(''.join([id_to_emoji[id] for id in ids[i:i+max_per_row]]))
    out = '\n'.join(lines)
    return out


if __name__ == "__main__":
    enc = tiktoken.encoding_for_model("gpt-4o")
    print(enc.n_vocab) # number of tokens in total

    emojis = list(emoji.EMOJI_DATA.keys())
    random.seed(15)
    random.shuffle(emojis)
    print(len(emoji.EMOJI_DATA))

    
    text = """Strawberry里有几个r?"""
    print(text_to_tokens(text, max_per_row=20))
    print(enc.encode(text))
    