from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA


def sign_dencryptor(file_location, sha256_sign_location, public_key_location):
    # Open and read file
    with open(file_location, "rb") as f:
        file = f.read()

    # Calculate SHA256
    digest = SHA256.new()
    digest.update(file)

    # Get recived siganture
    with open(sha256_sign_location) as f:
        sig = f.read()

    # Convert signature
    sig = bytes.fromhex(sig)

    # Import public RSA key
    with open(public_key_location) as f:
        public_key = RSA.importKey(f.read())

    # Verify received signature and file
    verifier = PKCS1_v1_5.new(public_key)
    verified = verifier.verify(digest, sig)

    # Inform about the correctness of the data
    if verified:
        return "Ok: Message verified"
    else:
        return "Error: Message modified"
