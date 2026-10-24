"""
tools/extract_android_apk.py
Streams the compressed byte range for templates/android_debug.apk directly from GitHub
and writes the decompressed android_debug.apk (121.37 MB) into Godot's export_templates directory.
"""
import os
import subprocess
import sys
import zlib

URL = "https://github.com/godotengine/godot/releases/download/4.7.2-stable/Godot_v4.7.2-stable_export_templates.tpz"
START = 85
END = 125834960
EXPECTED_UNCOMPRESSED = 127263590 # 121.37 MB

dest_dir = os.path.expanduser(r"~\AppData\Roaming\Godot\export_templates\4.7.2.stable")
os.makedirs(dest_dir, exist_ok=True)
dest_path = os.path.join(dest_dir, "android_debug.apk")

# Also write version.txt
version_path = os.path.join(dest_dir, "version.txt")
with open(version_path, "w") as f:
    f.write("4.7.2.stable\n")

print(f"Streaming and decompressing android_debug.apk ({END - START + 1} bytes compressed) to:")
print(f"-> {dest_path}")

cmd = [
    "curl.exe", "-sL",
    "-r", f"{START}-{END}",
    URL
]

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
decompressor = zlib.decompressobj(-15)

total_in = 0
total_out = 0

with open(dest_path, "wb") as out_f:
    while True:
        chunk = proc.stdout.read(1024 * 1024)
        if not chunk:
            break
        total_in += len(chunk)
        decomp = decompressor.decompress(chunk)
        if decomp:
            out_f.write(decomp)
            total_out += len(decomp)
        print(f"Downloaded: {total_in / (1024*1024):.1f} MB | Extracted: {total_out / (1024*1024):.1f} MB", end="\r", flush=True)

    rem = decompressor.flush()
    if rem:
        out_f.write(rem)
        total_out += len(rem)

proc.wait()
print(f"\nCompleted! android_debug.apk size: {os.path.getsize(dest_path)} bytes ({total_out / (1024*1024):.2f} MB)")
