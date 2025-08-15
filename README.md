# 🦊 Python Wallet Manager

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Ethereum](https://img.shields.io/badge/network-Ethereum-%236C71C4)](https://ethereum.org/)
[![Security](https://img.shields.io/badge/encryption-AES--256-orange.svg)]()
[![Issues](https://img.shields.io/github/issues/74Thirsty/wallet.svg)](https://github.com/74Thirsty/wallet/issues)

A **robust, interactive CLI wallet manager** written in Python.  
Generate, import, export, delete, and back up wallets securely — with AES-256 encryption and no central server.  
Works out-of-the-box with the Ethereum network via a public RPC.

---

## ✨ Features

- 📦 **Create wallets** with address, private key, and 12-word mnemonic
- 🔐 **AES-256 encryption** for local wallet storage
- 📥 **Import wallets** from private key or mnemonic
- 📤 **Export wallets** to encrypted JSON
- 🗑 **Delete wallets** securely
- 💰 **Check ETH balances** via public Ethereum RPC
- 💾 **Backup & restore** entire wallet collection
- 🖥 **Interactive CLI** with menu navigation
- 🚫 **No KYC** — runs locally, no data leaves your machine

---

## 📦 Installation

```bash
git clone https://github.com/YourUser/wallet-manager.git
cd wallet-manager
pip install -r requirements.txt

