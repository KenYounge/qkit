""" The alleged RC4 encryption method in plain Python 3 and no dependencies. """

def encrypt(text, keyphrase):

    assert len(keyphrase) > 8, 'INVALID ENCRYPTION KEY: Provide a passphrase of at least 8 characters.'

    msg_chars = sorted(list({c for c in text}))

    # Detect incoming encrypted text when it is all zeros and ones (do not use to encrypt messages of just zeros ones).
    reverse = bool(msg_chars == ['0', '1'])
    if reverse:
        num_message = [int(text[i:i + 8], 2) for i in range(0, len(text), 8)]
    else:
        num_message = [ord(c) for c in text]

    j = 0
    box = [i for i in range(256)]
    for i in range(256):
        j = (j + box[i] + ord(keyphrase[i % len(keyphrase)])) % 256
        box[i], box[j] = box[j], box[i]
    j = 0
    i = 0
    stream = []
    for _ in text:
        j = (j + 1) % 256
        i = (i + box[j]) % 256
        box[j], box[i] = box[i], box[j]
        addon = (box[i] + box[j]) % 256
        stream.append(box[addon])

    if reverse:
        out = ''.join(chr(i ^ j) for i, j in zip(num_message, stream))
    else:
        out = ''.join(['{:08b}'.format(i ^ j) for i, j in zip(num_message, stream)])

    return out

