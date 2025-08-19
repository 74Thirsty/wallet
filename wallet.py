#!/usr/bin/env python3
import os
import sys
import json
import getpass
import secrets
from pathlib import Path
from hashlib import pbkdf2_hmac

from eth_account import Account
from mnemonic import Mnemonic
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from web3 import Web3

try:
    import qrcode
except ImportError:
    qrcode = None

# === CONFIG ===
DATA_FILE = Path("wallets.enc")
DEFAULT_RPC = "https://ethereum.publicnode.com"
Account.enable_unaudited_hdwallet_features()


# === Encryption Utils ===
def derive_key(password: str, salt: bytes) -> bytes:
    return pbkdf2_hmac("sha256", password.encode(), salt, 200000, dklen=32)


def encrypt_data(password: str, data: dict) -> bytes:
    salt = secrets.token_bytes(16)
    aesgcm = AESGCM(derive_key(password, salt))
    nonce = secrets.token_bytes(12)
    ct = aesgcm.encrypt(nonce, json.dumps(data).encode(), None)
    return salt + nonce + ct


def decrypt_data(password: str, blob: bytes) -> dict:
    salt, nonce, ct = blob[:16], blob[16:28], blob[28:]
    aesgcm = AESGCM(derive_key(password, salt))
    data = aesgcm.decrypt(nonce, ct, None)
    return json.loads(data.decode())


# === Wallet File Management ===
def load_wallets(password: str) -> dict:
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "rb") as f:
        blob = f.read()
    try:
        return decrypt_data(password, blob)
    except Exception:
        print("❌ Incorrect password or corrupted file.")
        return {}


def save_wallets(password: str, wallets: dict):
    blob = encrypt_data(password, wallets)
    with open(DATA_FILE, "wb") as f:
        f.write(blob)


# === Wallet Generation ===
def generate_wallet(derivation_path="m/44'/60'/0'/0/0", chain="eth"):
    mnemo = Mnemonic("english")
    mnemonic = mnemo.generate(strength=128)
    acct = Account.from_mnemonic(mnemonic, account_path=derivation_path)
    return acct, mnemonic, derivation_path, chain


def create_wallet(wallets: dict):
    dp = input("Derivation path [default m/44'/60'/0'/0/0]: ").strip() or "m/44'/60'/0'/0/0"
    chain = input("Chain tag (eth, polygon, bsc, etc): ").strip() or "eth"
    acct, mnemonic, dp, chain = generate_wallet(dp, chain)
    wallets[acct.address] = {
        "private_key": acct.key.hex(),
        "mnemonic": mnemonic,
        "derivation_path": dp,
        "chain": chain,
    }
    print(f"✅ Created wallet {acct.address} ({chain})")
    return wallets


def create_batch_wallets(wallets: dict):
    try:
        count = int(input("How many wallets to create? ").strip())
        if count <= 0:
            print("❌ Invalid count.")
            return wallets
    except ValueError:
        print("❌ Please enter a number.")
        return wallets

    dp = input("Derivation path [default m/44'/60'/0'/0/0]: ").strip() or "m/44'/60'/0'/0/0"
    chain = input("Chain tag (eth, polygon, bsc, etc): ").strip() or "eth"

    for i in range(count):
        acct, mnemonic, dp, chain = generate_wallet(dp, chain)
        wallets[acct.address] = {
            "private_key": acct.key.hex(),
            "mnemonic": mnemonic,
            "derivation_path": dp,
            "chain": chain,
        }
        print(f"✅ [{i+1}/{count}] Created {acct.address} ({chain})")

    print(f"🎉 Batch creation complete. {count} wallets added.")
    return wallets


def list_wallets(wallets: dict):
    if not wallets:
        print("⚠️ No wallets stored.")
        return
    for i, (addr, meta) in enumerate(wallets.items(), 1):
        print(f"{i}. {addr} ({meta.get('chain','eth')}) dp={meta.get('derivation_path')}")


def delete_wallet(wallets: dict):
    addr = input("Enter address to delete: ").strip()
    if addr in wallets:
        del wallets[addr]
        print("🗑 Deleted.")
    else:
        print("❌ Address not found.")
    return wallets


def import_wallet(wallets: dict):
    choice = input("Import from (1) Private Key, (2) Mnemonic: ")
    chain = input("Chain tag (eth, polygon, etc): ").strip() or "eth"
    if choice == "1":
        pk = input("Private key (0x...): ").strip()
        acct = Account.from_key(pk)
        wallets[acct.address] = {
            "private_key": pk,
            "mnemonic": None,
            "chain": chain,
        }
        print(f"✅ Imported {acct.address}")
    elif choice == "2":
        mnemonic = input("Mnemonic: ").strip()
        dp = input("Derivation path [default m/44'/60'/0'/0/0]: ").strip() or "m/44'/60'/0'/0/0"
        acct = Account.from_mnemonic(mnemonic, account_path=dp)
        wallets[acct.address] = {
            "private_key": acct.key.hex(),
            "mnemonic": mnemonic,
            "derivation_path": dp,
            "chain": chain,
        }
        print(f"✅ Imported {acct.address}")
    return wallets


def export_wallet(wallets: dict):
    addr = input("Address to export: ").strip()
    if addr not in wallets:
        print("❌ Address not found.")
        return
    fname = addr.replace("0x", "") + ".json"
    with open(fname, "w") as f:
        json.dump(wallets[addr], f, indent=2)
    print(f"📤 Exported to {fname}")
    if qrcode:
        img = qrcode.make(addr)
        qrname = addr.replace("0x", "") + ".png"
        img.save(qrname)
        print(f"📷 QR saved to {qrname}")


def check_balance(wallets: dict):
    addr = input("Address to check balance: ").strip()
    rpc = input("RPC URL [default ETH]: ").strip() or DEFAULT_RPC
    w3 = Web3(Web3.HTTPProvider(rpc))
    if addr not in wallets:
        print("❌ Address not found.")
        return
    try:
        balance = w3.eth.get_balance(addr)
        print(f"💰 {addr} Balance: {w3.from_wei(balance, 'ether')} ETH")
    except Exception as e:
        print(f"❌ RPC error: {e}")


def backup_all(wallets: dict):
    fname = "wallets_backup.json"
    with open(fname, "w") as f:
        json.dump(wallets, f, indent=2)
    print(f"📦 Backup saved to {fname}")


def restore_backup(wallets: dict):
    fname = input("Backup file path: ").strip()
    if not os.path.isfile(fname):
        print("❌ File not found or is a directory.")
        return wallets
    try:
        with open(fname, "r") as f:
            data = json.load(f)
        wallets.update(data)
        print("♻️ Backup restored.")
    except Exception as e:
        print(f"❌ Failed to restore backup: {e}")
    return wallets


def export_manifest(wallets: dict):
    fname = "wallet_manifest.yaml"
    try:
        import yaml
    except ImportError:
        print("⚠️ PyYAML not installed, falling back to JSON.")
        fname = "wallet_manifest.json"
        with open(fname, "w") as f:
            json.dump(wallets, f, indent=2)
    else:
        with open(fname, "w") as f:
            yaml.dump(wallets, f, sort_keys=False)
    print(f"📒 Manifest written to {fname}")


def create_vanity_wallet(wallets: dict):
    prefix = input("Enter hex prefix (without 0x): ").lower().strip()
    print("⚠️ WARNING: Vanity generation is slow as hell. Longer prefixes may take HOURS.")
    tries = 0
    while True:
        acct = Account.create()
        addr = acct.address.lower()
        tries += 1
        if addr[2:].startswith(prefix):
            print(f"✅ Vanity wallet found after {tries} tries: {acct.address}")
            wallets[acct.address] = {
                "private_key": acct.key.hex(),
                "mnemonic": None,
                "derivation_path": None,
                "chain": "eth",
            }
            return wallets
        if tries % 10000 == 0:
            print(f"...still searching, {tries} attempts so far")


# === Main Menu ===
def main():
    print("=== Python Wallet Maker Pro ===")
    password = getpass.getpass("Master password: ")
    wallets = load_wallets(password)

    while True:
        print("\nMenu:")
        print("1. Create Wallet")
        print("2. List Wallets")
        print("3. Import Wallet")
        print("4. Export Wallet (JSON + QR)")
        print("5. Delete Wallet")
        print("6. Check Balance")
        print("7. Backup All")
        print("8. Restore From Backup")
        print("9. Export Manifest (YAML/JSON)")
        print("10. Create Vanity Wallet")
        print("11. Create Batch Wallets")
        print("0. Exit")

        choice = input("> ").strip()
        if choice == "1":
            wallets = create_wallet(wallets)
        elif choice == "2":
            list_wallets(wallets)
        elif choice == "3":
            wallets = import_wallet(wallets)
        elif choice == "4":
            export_wallet(wallets)
        elif choice == "5":
            wallets = delete_wallet(wallets)
        elif choice == "6":
            check_balance(wallets)
        elif choice == "7":
            backup_all(wallets)
        elif choice == "8":
            wallets = restore_backup(wallets)
        elif choice == "9":
            export_manifest(wallets)
        elif choice == "10":
            wallets = create_vanity_wallet(wallets)
        elif choice == "11":
            wallets = create_batch_wallets(wallets)
        elif choice == "0":
            save_wallets(password, wallets)
            print("💾 Changes saved. Goodbye.")
            sys.exit()
        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted.")
