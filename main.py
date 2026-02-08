import os
import zipfile
import json
import time

print("""
██████╗ ███████╗██████╗ ██████╗  ██████╗  ██████╗██╗  ██╗
██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔════╝██║ ██╔╝
██████╔╝█████╗  ██║  ██║██████╔╝██║   ██║██║     █████╔╝ 
██╔══██╗██╔══╝  ██║  ██║██╔══██╗██║   ██║██║     ██╔═██╗ 
██████╔╝███████╗██████╔╝██║  ██║╚██████╔╝╚██████╗██║  ██╗
╚═════╝ ╚══════╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝

██████╗  █████╗  ██████╗██╗  ██╗
██╔══██╗██╔══██╗██╔════╝██║ ██╔╝
██████╔╝███████║██║     █████╔╝ 
██╔═══╝ ██╔══██║██║     ██╔═██╗ 
██║     ██║  ██║╚██████╗██║  ██╗
╚═╝     ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝

""")


BASE_DIR = os.getcwd()
WORLD_PATH = input('World file in the bedrock server : ')
while not os.path.exists(WORLD_PATH) :
    print('path doesnt exist')
    WORLD_PATH = input('World file in the bedrock server : ')
else:
    pass


def check_files(path):
    if not os.path.isdir(path):
        return []
    return [
        f for f in os.listdir(path)
        if os.path.isfile(os.path.join(path, f))
    ]


def check_mc(path):
    files = check_files(path)
    valid = []
    for f in files:
        if f.lower().endswith((".mcaddon", ".mcpack")):
            valid.append(f)
        else:
            print(f"{f} removed from the check list")
    return valid


def unzip_file(zip_filename, extract_dir):
    os.makedirs(extract_dir, exist_ok=True)
    with zipfile.ZipFile(zip_filename, "r") as z:
        z.extractall(extract_dir)


files = check_mc(BASE_DIR)
if not files:
    print("no valid .mcaddon or .mcpack files found")
    raise SystemExit

for i, f in enumerate(files):
    print(f"[{i}] {f}")

pick = int(input("\nPick a file index to add to server: "))
old_name = files[pick]
root, _ = os.path.splitext(old_name)
zip_name = f"{root}.zip"

if not os.path.exists(zip_name):
    os.rename(old_name, zip_name)

extract_dir = os.path.join(BASE_DIR, root)
unzip_file(zip_name, extract_dir)

unzip_folder = [
    d for d in os.listdir(extract_dir)
    if os.path.isdir(os.path.join(extract_dir, d))
]

for i, item in enumerate(unzip_folder):
    print(f"[{i}] {item}")


def add_pack(pack_dir, json_name):
    manifest = os.path.join(pack_dir, "manifest.json")
    if not os.path.exists(manifest):
        print(f"{pack_dir} has no manifest.json")
        return

    with open(manifest, "r", encoding="utf-8") as f:
        data = json.load(f)

    header = data.get("header", {})
    uuid = header.get("uuid")
    version = header.get("version", [])

    os.makedirs(WORLD_PATH, exist_ok=True)
    target = os.path.join(WORLD_PATH, json_name)

    if os.path.exists(target):
        try:
            with open(target, "r", encoding="utf-8") as f:
                packs = json.load(f)
        except json.JSONDecodeError:
            packs = []
    else:
        packs = []

    if not any(p.get("pack_id") == uuid for p in packs):
        packs.append({"pack_id": uuid, "version": version})

    with open(target, "w", encoding="utf-8") as f:
        json.dump(packs, f, indent=4)

    print(f"{json_name} updated successfully.")


pick = int(input("\nPick behavior pack index: "))
add_pack(os.path.join(extract_dir, unzip_folder[pick]), "world_behavior_packs.json")
time.sleep(1)
pick = int(input("\nPick resource pack index: "))
add_pack(os.path.join(extract_dir, unzip_folder[pick]), "world_resource_packs.json")
