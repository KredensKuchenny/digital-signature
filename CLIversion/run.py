import sys
import shutil
import argparse
from source.signatureEngine.sign_encryptor import *
from source.signatureEngine.sign_dencryptor import *
from source.rsaGenerator.rsa_generator import *

# Change recursion limit to 10k
sys.setrecursionlimit(10000)

# Create argparse object
parser = argparse.ArgumentParser(
    description="Create your own digital signature! In rsaGenerate mode you must give [--size] (key size in bytes), [--private_rsa_path_name_file] (place and filename with .pem extension where you want to store private key) and [--public_rsa_path_name_file] (place and filename with .pem extension where you want to store private key). In createSignature mode you must give [--file_location_and_name] (path with filename which you want to signature), [--private_rsa_path_name_file] (private key place and file name with .pem extension), [--signature_file_location] (place and filename of signature) and [--signatured_file_location] (place where you want store copy of signatured file). In checkSignature mode you must give [--file_location_and_name] (path with filename of recived file), [--signature_file_location] (path and filename with signature), [--public_rsa_path_name_file] (path and filename of public RSA key in .pem format"
)

# Create usable arguments
parser.add_argument(
    "-a", "--action", help="rsaGenerate, createSignature, checkSignature", type=str
)

parser.add_argument(
    "-s",
    "--size",
    help="Give RSA key size in bits, default is 2048",
    type=int,
    default=2048,
)

parser.add_argument(
    "-fpriv",
    "--private_rsa_path_name_file",
    help="Give path and file name. File extension must be .pem, default is privateKeyRSA/private_key.pem",
    type=str,
    default="privateKeyRSA/private_key.pem",
)

parser.add_argument(
    "-fpub",
    "--public_rsa_path_name_file",
    help="Give path and file name. File extension must be .pem, default is sendFilesToB/public_key.pem",
    type=str,
    default="sendFilesToB/public_key.pem",
)

parser.add_argument(
    "-f",
    "--file_location_and_name",
    help="Give file path and name, default is exampleMessages/secretMessage.png",
    type=str,
    default="exampleMessages/secretMessage.png",
)

parser.add_argument(
    "-fb",
    "--signatured_file_location",
    help="Give file path or file path and name where you want to copy signatured file, default is sendFilesToB",
    type=str,
    default="sendFilesToB",
)

parser.add_argument(
    "-fs",
    "--signature_file_location",
    help="Give location of signature, default is sendFilesToB/sha256_sign.txt",
    type=str,
    default="sendFilesToB/sha256_sign.txt",
)

# Get intercepted arguments
args = parser.parse_args()

# Choose functionality
if args.action == "rsaGenerate":
    # Creating RSA keys
    publicKey, privateKey = rsa_generator(args.size, audio_trng())

    # Creating PEM form and save private key to file
    pem_private_key = pem_rsa_private_key(privateKey)
    with open(args.private_rsa_path_name_file, "wb") as pem_file:
        pem_file.write(pem_private_key)

    # Creating PEM form and save public key to file
    pem_public_key = pem_rsa_public_key(publicKey)
    with open(args.public_rsa_path_name_file, "wb") as pem_public_file:
        pem_public_file.write(pem_public_key)

elif args.action == "createSignature":
    # Create signature
    sign_encryptor(
        args.file_location_and_name,
        args.private_rsa_path_name_file,
        args.signature_file_location,
    )

    # Copy the signed file to sendFilesToB directory
    shutil.copy2(args.file_location_and_name, args.signatured_file_location)

# Example usage: python run.py -a checkSignature -f recivedFilesFromA/secretMessage.png -fs recivedFilesFromA/sha256_sign.txt -fpub recivedFilesFromA/public_key.pem
elif args.action == "checkSignature":
    # Check signature
    getInfo = sign_dencryptor(
        args.file_location_and_name,
        args.signature_file_location,
        args.public_rsa_path_name_file,
    )

    # Show information
    print(getInfo)
else:
    print("Use [-h] option to show avaliable options!")
