# 🦊 Python Wallet Manager
![GADGET SAAVY banner](https://raw.githubusercontent.com/74Thirsty/74Thirsty/main/assets/banner.svg)

## 🔧 Technologies & Tools

[![Cyfrin](https://img.shields.io/badge/Cyfrin-Audit%20Ready-005030?logo=shield&labelColor=F47321)](https://www.cyfrin.io/)
[![FlashBots](https://img.shields.io/pypi/v/finta?label=Finta&logo=python&logoColor=2774AE&labelColor=FFD100)](https://www.flashbots.net/)
[![Python](https://img.shields.io/badge/Python-3.11-003057?logo=python&labelColor=B3A369)](https://www.python.org/)
[![Solidity](https://img.shields.io/badge/Solidity-0.8.20-7BAFD4?logo=ethereum&labelColor=4B9CD3)](https://docs.soliditylang.org)
[![pYcHARM](https://img.shields.io/badge/Built%20with-PyCharm-782F40?logo=pycharm&logoColor=CEB888)](https://www.jetbrains.com/pycharm/)
[![Issues](https://img.shields.io/github/issues/74Thirsty/wallet.svg?color=hotpink&labelColor=brightgreen)](https://github.com/74Thirsty/wallet/issues)
[![Lead Dev](https://img.shields.io/badge/C.Hirschauer-Lead%20Developer-041E42?logo=parrotsecurity&labelColor=C5B783)](https://christopherhirschauer.bio)
[![Security](https://img.shields.io/badge/encryption-AES--256-orange.svg?color=13B5EA&labelColor=9EA2A2)]()

> <p><strong>Christopher Hirschauer</strong><br>
> Builder @ the bleeding edge of MEV, automation, and high-speed arbitrage.<br>
<em>Updated: August 2025</em></p>

A **robust, interactive CLI wallet manager** written in Python.  
Generate, import, export, delete, and back up wallets securely — with AES-256 encryption and no central server.  
Supports Ethereum and any EVM-compatible network via public or custom RPC.

---

## ✨ Features

- 📦 **Create wallets** with address, private key, and 12-word mnemonic
- 🧑‍🤝‍🧑 **Batch wallet creation** (generate multiple at once)
- 🔐 **AES-256 encryption** for secure local wallet storage
- 📥 **Import wallets** from private key or mnemonic
- 📤 **Export wallets** to JSON + QR code (optional)
- 🗑 **Delete wallets** securely from storage
- 💰 **Check balances** using Ethereum or custom RPC URLs
- 💾 **Backup & restore** entire wallet collection
- 📒 **Export manifest** (YAML or JSON)
- 🧾 **Export recovery sheet** (mnemonic + derivation path) in plaintext or encrypted form
- 🦄 **Vanity wallet generation** (search for custom hex prefixes)
- 🖥 **Interactive CLI** with menu navigation
- 🚫 **No KYC** — runs locally, no data leaves your machine

---

## 📦 Installation

```
git clone https://github.com/74Thirsty/wallet-manager.git
cd wallet-manager
pip install -r requirements.txt
```

🚀 Usage
Run the CLI:
```
python wallet_manager.py
```

You’ll be prompted to set a master password.
All wallets are stored in a single encrypted file: wallets.enc.

⚠️ Security Notes

🔑 Always back up your mnemonic + derivation path using the recovery sheet feature.<br>
🛡 Forgetting your master password = unrecoverable funds.>br>
🏴 Vanity wallet generation is computationally expensive — longer prefixes can take hours.<br>
💻 No telemetry, no cloud storage — your keys, your machine.
