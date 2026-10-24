"""
tools/fetch_android_template.py
Extracts the official Godot 4.7.2 Android export templates (android_debug.apk, android_release.apk, version.txt)
from GitHub releases using HTTP Range requests without needing to download the entire 1.28 GB archive.
"""
import os
import struct
import sys
import urllib.request
import zlib

URL = "https://github.com/godotengine/godot/releases/download/4.7.2-stable/Godot_v4.7.2-stable_export_templates.tpz"

print("1. Resolving final URL and Content-Length...")
req = urllib.request.Request(URL, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    final_url = resp.geturl()
    total_size = int(resp.headers.get("Content-Length"))

print(f"   Resolved: {final_url[:60]}... ({total_size / (1024*1024):.1f} MB)")

print("2. Fetching End of Central Directory (EOCD)...")
tail_req = urllib.request.Request(final_url, headers={
    "Range": f"bytes={total_size - 65536}-{total_size - 1}",
    "User-Agent": "Mozilla/5.0"
})
with urllib.request.urlopen(tail_req) as r:
    tail_data = r.read()

eocd_idx = tail_data.rfind(b"\x50\x4b\x05\x06")
if eocd_idx == -1:
    print("Error: Could not find EOCD signature!")
    sys.exit(1)

disk_num, cd_disk, disk_entries, total_entries, cd_size, cd_offset = struct.unpack("<HHHHII", tail_data[eocd_idx+4:eocd_idx+20])
print(f"   Entries: {total_entries}, CD offset: {cd_offset}, CD size: {cd_size / (1024*1024):.2f} MB")

print("3. Fetching Central Directory...")
cd_req = urllib.request.Request(final_url, headers={
    "Range": f"bytes={cd_offset}-{cd_offset + cd_size - 1}",
    "User-Agent": "Mozilla/5.0"
})
with urllib.request.urlopen(cd_req) as r:
    cd_data = r.read()

entries = []
pos = 0
fmt = "<IHHHHHHIIIHHHHHII"
while pos < len(cd_data):
    if cd_data[pos:pos+4] != b"\x50\x4b\x01\x02":
        break
    header = cd_data[pos:pos+46]
    sig, ver_made, ver_needed, flags, comp_method, mtime, mdate, crc, comp_size, uncomp_size, name_len, extra_len, comment_len, disk_num, int_attr, ext_attr, local_offset = struct.unpack(fmt, header)
    name = cd_data[pos+46:pos+46+name_len].decode("utf-8", errors="replace")
    entries.append({
        "name": name,
        "method": comp_method,
        "comp_size": comp_size,
        "uncomp_size": uncomp_size,
        "local_offset": local_offset,
        "crc": crc
    })
    pos += 46 + name_len + extra_len + comment_len

print(f"   Parsed {len(entries)} entries.")

dest_dir = os.path.expanduser(r"~\AppData\Roaming\Godot\export_templates\4.7.2.stable")
os.makedirs(dest_dir, exist_ok=True)

targets = ["templates/android_debug.apk", "templates/android_release.apk", "templates/version.txt"]
found = [e for e in entries if e["name"] in targets]

for e in found:
    target_name = os.path.basename(e["name"])
    dest_path = os.path.join(dest_dir, target_name)
    print(f"\n4. Downloading {target_name} ({e['comp_size']/(1024*1024):.1f} MB compressed -> {e['uncomp_size']/(1024*1024):.1f} MB)...")

    # Read local header to get precise data offset
    h_req = urllib.request.Request(final_url, headers={
        "Range": f"bytes={e['local_offset']}-{e['local_offset']+29}",
        "User-Agent": "Mozilla/5.0"
    })
    with urllib.request.urlopen(h_req) as r:
        loc_h = r.read()

    l_sig, l_ver, l_flags, l_method, l_mtime, l_mdate, l_crc, l_csize, l_usize, l_nlen, l_elen = struct.unpack("<IHHHHHIIIHH", loc_h)
    data_start = e['local_offset'] + 30 + l_nlen + l_elen
    data_end = data_start + e['comp_size'] - 1

    stream_req = urllib.request.Request(final_url, headers={
        "Range": f"bytes={data_start}-{data_end}",
        "User-Agent": "Mozilla/5.0"
    })
    
    with urllib.request.urlopen(stream_req) as s_resp, open(dest_path, "wb") as out_f:
        if e["method"] == 0: # Stored
            while True:
                b = s_resp.read(1024*1024)
                if not b: break
                out_f.write(b)
        elif e["method"] == 8: # Deflated
            d = zlib.decompressobj(-15)
            downloaded = 0
            while True:
                b = s_resp.read(1024*1024)
                if not b: break
                downloaded += len(b)
                decomp = d.decompress(b)
                if decomp: out_f.write(decomp)
                print(f"   Downloaded: {downloaded/(1024*1024):.1f} MB / {e['comp_size']/(1024*1024):.1f} MB", end="\r", flush=True)
            rem = d.flush()
            if rem: out_f.write(rem)
            print()

    final_bytes = os.path.getsize(dest_path)
    print(f"   Extracted {target_name}: {final_bytes / (1024*1024):.2f} MB")

print("\n=== GODOT 4.7.2 ANDROID TEMPLATES INSTALLED SUCCESSFULLY ===")
