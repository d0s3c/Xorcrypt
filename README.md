<img width="1181" height="623" alt="image" src="https://github.com/user-attachments/assets/79b0ddf9-414d-4331-bec0-f16110fdff48" />

# 🔑 Xorcrypt

## XOR + Base64 Encrypt / Decrypt CLI Tool
## Built with a rich interactive UI and command-line support.

# Features 

- 🔐 XOR + Base64 encoding/decoding
- 🔢 Optional Hex encoding layer
- 📂 File encryption & decryption support

# 📦 Installation

```
git clone https://github.com/d0s3c/xorcrypt.git
cd xorcrypt
pip install -r requirements.txt
```
## Or manually download
```
pip install rich
```

# then simply run:
```
python xorcrypt.py
```

# or run with CLI 

## 🔓 Decrypt Base64
```
python xorcrypt.py -d "SGVsbG8=" -k mykey
```
## 🔐 Encrypt Text
```
python xorcrypt.py -e "Hello World" -k mykey
```
## 🔢 Encrypt with Hex
```
python xorcrypt.py -e "Hello World" -k mykey --hex
```
## 🔓 Decrypt Hex
```
python xorcrypt.py -d "613162326333..." -k mykey --hex
```
## 📂 Decrypt from File
```
python xorcrypt.py -df input.b64 -k mykey
```
## 📂 Encrypt File
```
python xorcrypt.py -ef secret.txt -k mykey
```
## 💾 Save Output to File
```
python xorcrypt.py -e "Hello" -k mykey -o output.txt
```
