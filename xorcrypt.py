import base64
import sys
import os
import time
import argparse

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.text import Text
    from rich.table import Table
    from rich.theme import Theme
    from rich.align import Align
except ImportError:
    print("This tool requires the 'rich' library for its UI.")
    print("Please install it using: pip install rich")
    sys.exit(1)

custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "danger": "bold red",
    "success": "bold green"
})
console = Console(theme=custom_theme)


def gradient_text(text_str, start_color=(211, 0, 255), end_color=(0, 212, 255)):
    """for gradient"""
    text = Text()
    length = len(text_str)
    for i, char in enumerate(text_str):
        if length > 1:
            ratio = i / (length - 1)
        else:
            ratio = 0
        r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
        text.append(char, style=f"rgb({r},{g},{b})")
    return text


BANNER_LINES = r"""
██╗  ██╗ ██████╗ ██████╗  ██████╗██████╗ ██╗   ██╗██████╗ ████████╗
╚██╗██╔╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝
 ╚███╔╝ ██║   ██║██████╔╝██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   
 ██╔██╗ ██║   ██║██╔══██╗██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   
██╔╝ ██╗╚██████╔╝██║  ██║╚██████╗██║  ██║   ██║   ██║        ██║   
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝   
                                                                   
""".strip("\n")

SUB_LINE = "XOR + Base64 Encrypt / Decrypt  ·  by d0s3c"

def print_banner():
    console.clear()
    console.print()
    
    banner_text = Text()
    for line in BANNER_LINES.splitlines():
        banner_text.append(gradient_text(line))
        banner_text.append("\n")
    
    console.print(Align.center(banner_text))
    console.print(Align.center(f"[bold cyan]{SUB_LINE}[/]"))
    console.print(Align.center(Text("──────────────────────────────────────────────────", style="dim")))
    console.print()



def xor_bytes(data: bytes, key: str) -> bytes:
    key_bytes = key.encode()
    if not key_bytes:
        raise ValueError("Key must not be empty.")
    return bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data)])

def encrypt(plaintext: str, key: str) -> str:
    """UTF-8 plaintext  ➡  XOR  ➡  Base64  ➡  ASCII string"""
    xored = xor_bytes(plaintext.encode(), key)
    return base64.b64encode(xored).decode()

def decrypt(encoded: str, key: str) -> str:
    """Base64 string  ➡  XOR  ➡  UTF-8 plaintext"""
    try:
        decoded = base64.b64decode(encoded)
    except Exception:
        raise ValueError("Invalid Base64 input.")
    result = xor_bytes(decoded, key)
    return result.decode(errors="replace")

def encrypt_hex(plaintext: str, key: str) -> str:
    """UTF-8 plaintext  ➡  XOR  ➡  Base64  ➡  Hex string"""
    b64 = encrypt(plaintext, key)
    return b64.encode().hex()

def decrypt_hex(hex_str: str, key: str) -> str:
    """Hex string  ➡  Base64  ➡  XOR  ➡  UTF-8 plaintext"""
    try:
        b64 = bytes.fromhex(hex_str.strip()).decode()
    except Exception:
        raise ValueError("Invalid Hex input.")
    return decrypt(b64, key)



def section(title):
    console.print()
    console.print(Align.center(f"[bold magenta]─── {title} ───[/]"))
    console.print()

def result_box(title, content):
    console.print()
    panel = Panel(
        f"[bold white]{content}[/]", 
        title=f"[success]{title}[/]", 
        border_style="green",
        expand=False,
        padding=(1, 4)
    )
    console.print(Align.center(panel))
    console.print()

def show_menu():
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Key", style="bold cyan", justify="right")
    table.add_column("Name", style="bold white")
    table.add_column("Description", style="dim")

    opts = [
        ("1", "Decrypt",              "Base64 + XOR            →  plaintext"),
        ("2", "Encrypt",              "Plaintext               →  XOR + Base64"),
        ("3", "Encrypt (Hex)",        "Plaintext               →  XOR + Base64 + Hex"),
        ("4", "Decrypt (Hex)",        "Hex + Base64 + XOR      →  plaintext"),
        ("5", "Decrypt from file",    "Read encoded text from a file"),
        ("6", "Encrypt to file",      "Write Base64 output to a file"),
        ("0", "Exit",                 "Quit"),
    ]
    
    for num, name, desc in opts:
        table.add_row(f"[{num}]", name, desc)

    menu_panel = Panel(table, title="[bold cyan]Main Menu[/]", expand=False, border_style="dim")
    console.print(Align.center(menu_panel))



def handle_decrypt():
    section("Decrypt  ·  Base64 + XOR")
    encoded = Prompt.ask("      [info]Enter Base64-encoded string[/]")
    if not encoded:
        console.print("      [warning]  No input provided.[/]")
        return
    key = Prompt.ask("      [info]Enter XOR key[/]")
    if not key:
        console.print("      [warning]  No key provided.[/]")
        return
    try:
        plain = decrypt(encoded, key)
        result_box("Decrypted Output", plain)
    except Exception as e:
        console.print(f"      [danger]  Error: {e}[/]")

def handle_encrypt():
    section("Encrypt  ·  XOR + Base64")
    plain = Prompt.ask("      [info]Enter plaintext to encrypt[/]")
    if not plain:
        console.print("      [warning]  No input provided.[/]")
        return
    key = Prompt.ask("      [info]Enter XOR key[/]")
    if not key:
        console.print("      [warning]  No key provided.[/]")
        return
    try:
        encoded = encrypt(plain, key)
        result_box("Encrypted Output (Base64)", encoded)
    except Exception as e:
        console.print(f"      [danger]  Error: {e}[/]")

def handle_encrypt_hex():
    section("Encrypt  ·  XOR + Base64 + Hex")
    plain = Prompt.ask("      [info]Enter plaintext to encrypt[/]")
    if not plain:
        console.print("      [warning]  No input provided.[/]")
        return
    key = Prompt.ask("      [info]Enter XOR key[/]")
    if not key:
        console.print("      [warning]  No key provided.[/]")
        return
    try:
        hex_out = encrypt_hex(plain, key)
        result_box("Encrypted Output (Hex)", hex_out)
    except Exception as e:
        console.print(f"      [danger]  Error: {e}[/]")

def handle_decrypt_hex():
    section("Decrypt  ·  Hex + Base64 + XOR")
    hex_str = Prompt.ask("      [info]Enter Hex-encoded string[/]")
    if not hex_str:
        console.print("      [warning]  No input provided.[/]")
        return
    key = Prompt.ask("      [info]Enter XOR key[/]")
    if not key:
        console.print("      [warning]  No key provided.[/]")
        return
    try:
        plain = decrypt_hex(hex_str, key)
        result_box("Decrypted Output", plain)
    except Exception as e:
        console.print(f"      [danger]  Error: {e}[/]")

def handle_decrypt_file():
    section("Decrypt from File")
    path = Prompt.ask("      [info]Enter file path[/]")
    if not path or not os.path.isfile(path):
        console.print("      [warning]  File not found.[/]")
        return
    key = Prompt.ask("      [info]Enter XOR key[/]")
    if not key:
        console.print("      [warning]  No key provided.[/]")
        return
    try:
        with open(path, "r") as f:
            encoded = f.read().strip()
        plain = decrypt(encoded, key)
        result_box(f"Decrypted Output ({os.path.basename(path)})", plain)
        
        if Confirm.ask("      [info]Save plaintext to file?[/]"):
            out_path = path + ".decrypted.txt"
            with open(out_path, "w") as f:
                f.write(plain)
            console.print(f"      [success]  Saved to {out_path}[/]")
    except Exception as e:
        console.print(f"      [danger]  Error: {e}[/]")

def handle_encrypt_file():
    section("Encrypt to File")
    path = Prompt.ask("      [info]Enter file path[/]")
    if not path or not os.path.isfile(path):
        console.print("      [warning]  File not found.[/]")
        return
    key = Prompt.ask("      [info]Enter XOR key[/]")
    if not key:
        console.print("      [warning]  No key provided.[/]")
        return
    try:
        with open(path, "r", errors="replace") as f:
            plain = f.read()
        encoded = encrypt(plain, key)
        out_path = path + ".b64xor"
        with open(out_path, "w") as f:
            f.write(encoded)
        result_box("Encrypted Output Written To", out_path)
        console.print(f"      [success]✓  Done — {len(encoded)} chars written.[/]")
    except Exception as e:
        console.print(f"      [danger]✗  Error: {e}[/]")



def cli_mode():
    parser = argparse.ArgumentParser(
        description="XOR + Base64 (+ optional Hex) encrypt/decrypt tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  xorcrypt -d 'SGVsbG8=' -k mykey\n"
               "  xorcrypt -e 'Hello World' -k mykey\n"
               "  xorcrypt -e 'Hello World' -k mykey --hex\n"
               "  xorcrypt -d 'a1b2c3...' -k mykey --hex\n"
               "  xorcrypt -df input.b64 -k mykey\n"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d",  "--decrypt",      metavar="STR",  help="Decrypt a Base64 (or Hex) string")
    group.add_argument("-e",  "--encrypt",      metavar="TEXT", help="Encrypt a plaintext string")
    group.add_argument("-df", "--decrypt-file", metavar="FILE", help="Decrypt from file")
    group.add_argument("-ef", "--encrypt-file", metavar="FILE", help="Encrypt file contents")
    parser.add_argument("-k",    "--key",    required=True, metavar="KEY",  help="XOR key")
    parser.add_argument("--hex", action="store_true",                       help="Use XOR + Base64 + Hex mode")
    parser.add_argument("-o",    "--output",               metavar="FILE",  help="Write output to file")
    args = parser.parse_args()

    try:
        if args.decrypt:
            out = decrypt_hex(args.decrypt, args.key) if args.hex else decrypt(args.decrypt, args.key)
        elif args.encrypt:
            out = encrypt_hex(args.encrypt, args.key) if args.hex else encrypt(args.encrypt, args.key)
        elif args.decrypt_file:
            with open(args.decrypt_file) as f:
                raw = f.read().strip()
            out = decrypt_hex(raw, args.key) if args.hex else decrypt(raw, args.key)
        elif args.encrypt_file:
            with open(args.encrypt_file, errors="replace") as f:
                raw = f.read()
            out = encrypt_hex(raw, args.key) if args.hex else encrypt(raw, args.key)

        if args.output:
            with open(args.output, "w") as f:
                f.write(out)
            console.print(f"[success] Output written to {args.output}[/]")
        else:
            print(out)
    except Exception as e:
        console.print(f"[danger] {e}[/]", style="bold red")
        sys.exit(1)



def main():
    if len(sys.argv) > 1:
        cli_mode()
        return

    print_banner()

    HANDLERS = {
        "1": handle_decrypt,
        "2": handle_encrypt,
        "3": handle_encrypt_hex,
        "4": handle_decrypt_hex,
        "5": handle_decrypt_file,
        "6": handle_encrypt_file,
    }

    while True:
        show_menu()
        console.print()
        prompt_text = Align.center("[info]Select option[/]")
        console.print(prompt_text)
        choice = Prompt.ask("      [dim]›[/]")

        if choice == "0":
            console.print(Align.center("\n[warning]Goodbye.[/]\n"))
            sys.exit(0)

        handler = HANDLERS.get(choice)
        if handler:
            handler()
            console.print()
            console.print(Align.center("[dim]Press Enter to continue...[/]"))
            Prompt.ask("")
            print_banner()
        else:
            console.print(Align.center(f"[warning]  Unknown option: '{choice}'[/]"))
            time.sleep(0.8)
            print_banner()

if __name__ == "__main__":
    main()
