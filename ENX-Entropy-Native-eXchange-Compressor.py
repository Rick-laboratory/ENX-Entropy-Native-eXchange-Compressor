# 🔥 ENX Bare Compressor – Full Pipeline for 100,000 Digits
# Compresses a massive number into a raw binary file, decompresses it, and saves the result to a .txt file.
# ✅ Zero metadata, zero padding issues, full roundtrip safe.

import os
import sys
import random
import time

# === CONFIG ===
sys.set_int_max_str_digits(1000000)  # Allow huge numbers
DIGITS = 1000_000
FILE_PATH_BIN = "compressed_enx_100k_raw.bin"
FILE_PATH_TXT = "decoded_enx_100k_number.txt"

# === CORE FUNCTIONS ===

def generate_large_number(num_digits):
    return int(''.join(str(random.randint(0, 9)) for _ in range(num_digits)) )  # Appended '1' for stability

def compress_number_to_bytes(number):
    return number.to_bytes((number.bit_length() + 7) // 8, 'big')

def decompress_bytes_to_number(byte_data):
    return int.from_bytes(byte_data, 'big')

def stream_encode_large_number(digit_source, chunk_size=10_000_000, output_path="ENX_streamed_output.bin"):
    """
    Stream-kompatibler ENX-Encoder für extrem große Zahlen.
    - Verarbeitet den Eingabetext in definierten Ziffern-Chunks
    - Wandelt jeden Chunk in ein kompaktes Byteformat um (int.to_bytes)
    - Schreibt direkt in eine Binärdatei, ohne alles im RAM zu halten
    """
    with open(output_path, "wb") as out_file:
        for i in range(0, len(digit_source), chunk_size):
            chunk = digit_source[i:i + chunk_size]
            number = int(chunk)
            chunk_bytes = number.to_bytes((number.bit_length() + 7) // 8, 'big')
            out_file.write(chunk_bytes)
    print(f"✅ Komprimiert: {output_path}")



# === COMPRESSION PIPELINE ===

# Step 1: Generate number
original_number = generate_large_number(DIGITS)
original_digit_length = len(str(original_number))

# Step 2: Compress to raw bytes
start_compress = time.time()
compressed_bytes = compress_number_to_bytes(original_number)
compress_time = time.time() - start_compress

# Step 3: Save compressed data
with open(FILE_PATH_BIN, "wb") as f:
    f.write(compressed_bytes)

# === DECOMPRESSION PIPELINE ===

# Step 4: Load and decompress
with open(FILE_PATH_BIN, "rb") as f:
    loaded_bytes = f.read()

start_decompress = time.time()
decompressed_number = decompress_bytes_to_number(loaded_bytes)
decompress_time = time.time() - start_decompress

# Step 5: Save decompressed number to text file
with open(FILE_PATH_TXT, "w") as f:
    f.write(str(decompressed_number))

# Step 6: Verify final roundtrip by reading decoded text file
with open(FILE_PATH_TXT, "r") as f:
    decoded_text = f.read().strip()
    final_number = int(decoded_text)

# === VALIDATION ===

roundtrip_ok = final_number == original_number
file_size = os.path.getsize(FILE_PATH_BIN)
bytes_saved = original_digit_length - len(compressed_bytes)
savings_percent = round(100 * bytes_saved / original_digit_length, 2)

# === OUTPUT ===

print("\n=== ENX Bare Compression Report ===")
print(f"Original digits: {original_digit_length}")
print(f"Binary file size: {file_size} bytes")
print(f"Bytes saved: {bytes_saved} ({savings_percent}%)")
print(f"✅ Roundtrip check: {roundtrip_ok}")
print(f"⚡ Compression time: {compress_time:.6f} s")
print(f"⚡ Decompression time: {decompress_time:.6f} s")
print(f"📄 Binary file: {FILE_PATH_BIN}")
print(f"📄 Decoded file: {FILE_PATH_TXT}")
#Copyright 23.04.2025 Rick Armbruster