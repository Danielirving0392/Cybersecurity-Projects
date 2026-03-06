import hashlib

# Database of known malware file hashes (mix of MD5, SHA1, and SHA256)
# These are used to identify malicious files by comparing their hash fingerprints
Malware_Database = [
    "2546dcffc5ad854d4ddc64fbf056871cd5a00f2471cb7a5bfd4ac23b6e9eedad",   # SHA256
    "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f",    # SHA256
    "3395856ce81f2b7382dee72602f798b642f14140",                             # SHA1
    "44d88612fea8a8f36de82e1278abb02f",                                     # MD5
    "6ce6f415d8475545be5ba114f208b0ff",                                     # MD5
    "73d6b0ca9c5554fd2b37ff8af6b51812f3af49962cebd6e042d0883a45794ddb8a53724275d26f3e18cebf1cd1d67740acc920aba16965038c0cc75b87030fbe",  # SHA512
    "765dceb9a8c8ff4318e3ccaf7dbb9b05c0a53a819d24a50714aebe6c",            # SHA224
    "b31bb2cf25d7e654c694ffb85b426d164a210ead66affc3b004702be",            # SHA224
    "b42ec8b47deb2dc75edebd01132d63f8e8d4cd08e5d26d8bd366bdc5",            # SHA224
    "bec1b52d350d721c7e22a6d4bb0a92909893a3ae",                             # SHA1
    "cc805d5fab1fd71a4ab352a9c533e65fb2d5b885518f4e565e68847223b8e6b85cb48f3afad842726d99239c9e36505c64b0dc9a061d9e507d833277ada336ab",  # SHA512
    "d27265074c9eac2e2122ed69294dbc4d7cce9141",                             # SHA1
    "d9305862fe0bf552718d19db43075d88cffd768974627db60fa1a90a8d45563e035a6449663b8f66aac53791d77f37dbb5035159aa08e69fc473972022f80010",  # SHA512
    "e1105070ba828007508566e28a2b8d4c65d192e9eaf3b7868382b7cae747b397",    # SHA256
    "e4968ef99266df7c9a1f0637d2389dab",                                     # MD5
]


def File_hasher(file_path):
    """Reads a file in binary mode and returns its MD5 hash as a hex string."""
    # Open the file in binary mode to ensure accurate hashing across all file types
    with open(file_path, 'rb') as f:
        content = f.read()
    # Compute and return the MD5 hash of the file's contents
    return hashlib.md5(content).hexdigest()


def scanner(file_path):
    """Scans a file by hashing it and checking against the malware database."""
    # Generate the MD5 hash of the target file
    Hash = File_hasher(file_path)
    print(f"md5 : {Hash}")

    # Compare the file's hash against known malware signatures
    if Hash in Malware_Database:
        print(f"{file_path} is Malicious")
    else:
        print(f"{file_path} is not malicious")


def main():
    # Target file to be scanned
    File = "Test.txt"
    scanner(File)


# Entry point — only runs when the script is executed directly, not when imported
if __name__ == "__main__":
    main()