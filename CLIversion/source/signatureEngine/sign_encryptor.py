from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA


def sign_encryptor(file_location, private_key_location, signature_file_location):
    # Open and read file
    with open(file_location, "rb") as f:
        file = f.read()

    # Import private RSA key
    with open(private_key_location, "r") as myfile:
        private_key = RSA.importKey(myfile.read())

    # Calculate SHA256
    digest = SHA256.new()
    digest.update(file)

    # Create siganture using private key
    signer = PKCS1_v1_5.new(private_key)
    sig = signer.sign(digest)

    # Save siganture to file
    with open(signature_file_location, "w") as file:
        file.write(sig.hex())
