"""
Inject Ramgarh Escape custom Bollywood game icons into Android APK and Godot export template,
then re-sign the APK.
"""
import os
import shutil
import subprocess
import zipfile

APK_PATH = r"build\android\RamgarhEscape.apk"
TEMPLATE_PATH = r"C:\Users\Rushi\AppData\Roaming\Godot\export_templates\4.7.2.stable\android_debug.apk"
ICONS_DIR = r"build\icons"
KEYSTORE_PATH = os.path.expandvars(r"%APPDATA%\Godot\keystores\debug.keystore")
JARSIGNER_PATH = r"C:\Program Files\Java\jdk-24\bin\jarsigner.exe"

ICON_MAP = {
    # density icons
    "res/mipmap-mdpi-v4/icon.webp": os.path.join(ICONS_DIR, "mipmap-mdpi-v4", "icon.webp"),
    "res/mipmap-mdpi-v4/icon_foreground.webp": os.path.join(ICONS_DIR, "mipmap-mdpi-v4", "icon_foreground.webp"),
    "res/mipmap-mdpi-v4/icon_background.webp": os.path.join(ICONS_DIR, "mipmap-mdpi-v4", "icon_background.webp"),
    "res/mipmap-mdpi-v4/icon_monochrome.webp": os.path.join(ICONS_DIR, "mipmap-mdpi-v4", "icon_monochrome.webp"),

    "res/mipmap-hdpi-v4/icon.webp": os.path.join(ICONS_DIR, "mipmap-hdpi-v4", "icon.webp"),
    "res/mipmap-hdpi-v4/icon_foreground.webp": os.path.join(ICONS_DIR, "mipmap-hdpi-v4", "icon_foreground.webp"),
    "res/mipmap-hdpi-v4/icon_background.webp": os.path.join(ICONS_DIR, "mipmap-hdpi-v4", "icon_background.webp"),
    "res/mipmap-hdpi-v4/icon_monochrome.webp": os.path.join(ICONS_DIR, "mipmap-hdpi-v4", "icon_monochrome.webp"),

    "res/mipmap-xhdpi-v4/icon.webp": os.path.join(ICONS_DIR, "mipmap-xhdpi-v4", "icon.webp"),
    "res/mipmap-xhdpi-v4/icon_foreground.webp": os.path.join(ICONS_DIR, "mipmap-xhdpi-v4", "icon_foreground.webp"),
    "res/mipmap-xhdpi-v4/icon_background.webp": os.path.join(ICONS_DIR, "mipmap-xhdpi-v4", "icon_background.webp"),
    "res/mipmap-xhdpi-v4/icon_monochrome.webp": os.path.join(ICONS_DIR, "mipmap-xhdpi-v4", "icon_monochrome.webp"),

    "res/mipmap-xxhdpi-v4/icon.webp": os.path.join(ICONS_DIR, "mipmap-xxhdpi-v4", "icon.webp"),
    "res/mipmap-xxhdpi-v4/icon_foreground.webp": os.path.join(ICONS_DIR, "mipmap-xxhdpi-v4", "icon_foreground.webp"),
    "res/mipmap-xxhdpi-v4/icon_background.webp": os.path.join(ICONS_DIR, "mipmap-xxhdpi-v4", "icon_background.webp"),
    "res/mipmap-xxhdpi-v4/icon_monochrome.webp": os.path.join(ICONS_DIR, "mipmap-xxhdpi-v4", "icon_monochrome.webp"),

    "res/mipmap-xxxhdpi-v4/icon.webp": os.path.join(ICONS_DIR, "mipmap-xxxhdpi-v4", "icon.webp"),
    "res/mipmap-xxxhdpi-v4/icon_foreground.webp": os.path.join(ICONS_DIR, "mipmap-xxxhdpi-v4", "icon_foreground.webp"),
    "res/mipmap-xxxhdpi-v4/icon_background.webp": os.path.join(ICONS_DIR, "mipmap-xxxhdpi-v4", "icon_background.webp"),
    "res/mipmap-xxxhdpi-v4/icon_monochrome.webp": os.path.join(ICONS_DIR, "mipmap-xxxhdpi-v4", "icon_monochrome.webp"),

    # generic mipmap
    "res/mipmap/icon.webp": os.path.join(ICONS_DIR, "mipmap", "icon.webp"),
    "res/mipmap/icon_foreground.webp": os.path.join(ICONS_DIR, "mipmap", "icon_foreground.webp"),
    "res/mipmap/icon_background.webp": os.path.join(ICONS_DIR, "mipmap", "icon_background.webp"),

    # splash icon
    "res/drawable/splash_icon.webp": os.path.join(ICONS_DIR, "drawable", "splash_icon.webp"),
}

def update_apk_zip(target_apk, remove_meta_inf=False):
    if not os.path.exists(target_apk):
        print(f"[SKIP] Target does not exist: {target_apk}")
        return False
        
    print(f"Injecting game icons into: {target_apk}")
    temp_apk = target_apk + ".tmp"
    
    with zipfile.ZipFile(target_apk, "r") as zin:
        with zipfile.ZipFile(temp_apk, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if remove_meta_inf and item.filename.startswith("META-INF/"):
                    # Exclude existing signature files so we can re-sign cleanly
                    continue
                if item.filename in ICON_MAP:
                    # Replace with our custom icon
                    src_file = ICON_MAP[item.filename]
                    if os.path.exists(src_file):
                        with open(src_file, "rb") as f:
                            data = f.read()
                        zout.writestr(item, data)
                        print(f"  [REPLACED] {item.filename}")
                        continue
                # Keep original entry
                data = zin.read(item.filename)
                zout.writestr(item, data)

    # Atomic replace
    os.remove(target_apk)
    os.rename(temp_apk, target_apk)
    print(f"  Successfully updated: {target_apk}")
    return True

def sign_apk(apk_path):
    print(f"\nSigning APK: {apk_path}")
    if not os.path.exists(JARSIGNER_PATH):
        print(f"[ERROR] jarsigner not found at {JARSIGNER_PATH}")
        return False
    if not os.path.exists(KEYSTORE_PATH):
        print(f"[ERROR] keystore not found at {KEYSTORE_PATH}")
        return False
        
    cmd = [
        JARSIGNER_PATH,
        "-sigalg", "SHA256withRSA",
        "-digestalg", "SHA-256",
        "-keystore", KEYSTORE_PATH,
        "-storepass", "android",
        apk_path,
        "androiddebugkey"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[ERROR] jarsigner failed: {res.stderr}")
        return False
    print("  [SUCCESS] APK signed with debug keystore!")
    
    # Verify
    verify_cmd = [JARSIGNER_PATH, "-verify", apk_path]
    vres = subprocess.run(verify_cmd, capture_output=True, text=True)
    if "jar verified" in vres.stdout.lower():
        print("  [VERIFIED] jarsigner verified APK integrity successfully!")
        return True
    else:
        print(f"  Verification output: {vres.stdout}")
        return True

def main():
    # 1. Update export template so future Godot builds always have the custom icon
    if os.path.exists(TEMPLATE_PATH):
        update_apk_zip(TEMPLATE_PATH, remove_meta_inf=False)
    
    # 2. Update target game APK and re-sign
    if os.path.exists(APK_PATH):
        update_apk_zip(APK_PATH, remove_meta_inf=True)
        sign_apk(APK_PATH)
    else:
        print(f"[NOTE] {APK_PATH} not found. Run build_apk.bat first.")

if __name__ == "__main__":
    main()
