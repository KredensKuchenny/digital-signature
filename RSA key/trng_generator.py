import wave
import struct
import numpy as np


def audio_trng(N=256000, L=8):
    def swap_bits(num):
        # Swap the 32 most significant bits with the 32 least significant bits
        msb = num >> 32
        lsb = num & ((1 << 32) - 1)
        swapped_num = (lsb << 32) | msb
        # Perform XOR operation to increase randomness
        result = swapped_num ^ num

        return result

    # Open the wave file and read the binary data
    w = wave.open("sound-samples/test.wav", "rb")
    if w is None:
        print("Error: Unable to open file")
        exit()

    nframes = w.getnframes()

    # Read the audio data as a string of bytes
    audio_data = w.readframes(nframes)

    # Convert the audio data to a numpy array
    audio_data = np.frombuffer(audio_data, dtype=np.uint16)

    w.close()

    gamma = 2
    epsilon = 0.1
    alpha = 1
    n = int(N / 256 * 8)

    A = []
    for byte in audio_data:
        A.append(byte)

    # Check if audio file is long enough
    if len(A) < n:
        raise ValueError("Error: Audio file is too short")

    r = []
    mask = 0b00000111
    for v in A:
        r.append(v & mask)

    x = [
        [0.141592, 0.653589, 0.793238, 0.462643, 0.383279, 0.502884, 0.197169, 0.399375]
    ]
    c = 0

    def fT(x, alpha):
        if 0 <= x < 0.5:
            return alpha * x
        elif 0.5 <= x <= 1:
            return alpha * (1 - x)
        else:
            raise ValueError("x must be in range of [0, 1]")

    z = [0, 0, 0, 0, 0, 0, 0, 0]
    O = []
    y = 0

    while len(O) <= N:
        for i in range(L):
            t = len(x) - 1
            x[t][i] = ((0.071428571 * r[y]) + x[t][i]) * 0.666666667
            c += 1
        for t in range(gamma):
            for i in range(L):
                try:
                    x[t + 1][i] = (
                        (1 - epsilon) * fT(x[t][i], alpha)
                        + epsilon / 2 * (fT(x[t][(i + 1) % L], alpha))
                        + fT(x[t][(i - 1) % L], alpha)
                    )
                except:
                    x.append([0, 0, 0, 0, 0, 0, 0, 0])
                    x[t + 1][i] = (
                        (1 - epsilon) * fT(x[t][i], alpha)
                        + epsilon / 2 * (fT(x[t][(i + 1) % L], alpha))
                        + fT(x[t][(i - 1) % L], alpha)
                    )
        for i in range(L):
            word = struct.pack("d", x[2][i])
            # Converting a byte string to a uint64 value
            int_value = int.from_bytes(word, byteorder="big", signed=False)
            z[i] = int_value
            x[0][i] = x[2][i]
        for i in range(int(L / 2)):
            z[i] = int(z[i]) ^ swap_bits(int(z[i + int(L / 2)]))
        O.append(z[0] + z[1] * 256 + z[2] * pow(2, 16) + z[3] * pow(2, 24))
        y += 1

    # Downloading 8 bits from each output sample
    bytes_form_O = []
    for j in range(len(O) - 1):
        for i in range(0, 256, 8):
            bajt = (O[j] >> (256 - (i + 8))) & 0xFF
            if bajt != 0:
                bytes_form_O.append(bajt)

    return bytes_form_O
