import tkinter as tk
from tkinter import messagebox
import secrets
import string
import base64
import re

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


# =========================
# TraX19 Security Portal
# Hydrotik Team Project
# =========================

APP_NAME = "TraX19 Security Portal"

PBKDF2_ITERATIONS = 390000
SALT_SIZE = 16

# Main colors
BG_COLOR = "#020617"
CARD_COLOR = "#0f172a"
INPUT_COLOR = "#020617"
TEXT_COLOR = "#e5e7eb"
MUTED_COLOR = "#94a3b8"
CYAN_COLOR = "#38bdf8"
PRIMARY_COLOR = "#2b7a78"
BLUE_COLOR = "#2563eb"
DANGER_COLOR = "#ef4444"
LIGHT_BUTTON = "#e5e7eb"
DARK_BUTTON = "#374151"

# Fonts used in the interface
FONT_TITLE = ("Arial", 22, "bold")
FONT_SUBTITLE = ("Arial", 11)
FONT_CARD_TITLE = ("Arial", 15, "bold")
FONT_LABEL = ("Arial", 11, "bold")
FONT_NORMAL = ("Arial", 11)
FONT_BUTTON = ("Arial", 11, "bold")
FONT_SMALL = ("Arial", 9)
FONT_FOOTER = ("Arial", 8)


# =========================
# Encryption Functions
# =========================

def makeKey(seed: str, salt: bytes) -> bytes:
    """
    Convert the seed into a valid Fernet key.
    Same seed and same salt will always give the same key.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(seed.encode("utf-8")))
    return key


def lock_msg(plain_text: str, seed: str) -> str:
    """
    Encrypt the normal message.
    The salt is added with the encrypted token because it is needed later.
    """
    salt = secrets.token_bytes(SALT_SIZE)
    key = makeKey(seed, salt)

    fernet = Fernet(key)
    token = fernet.encrypt(plain_text.encode("utf-8"))

    # We keep salt with token, but the seed must stay secret
    final_text = base64.urlsafe_b64encode(salt + token).decode("utf-8")
    return final_text


def openMsg(encText: str, seed: str) -> str:
    """
    Decrypt the encrypted message using the same seed.
    If seed is different, Fernet will reject the token.
    """
    try:
        encData = base64.urlsafe_b64decode(encText.encode("utf-8"))

        salt = encData[:SALT_SIZE]
        token = encData[SALT_SIZE:]

        key = makeKey(seed, salt)
        fernet = Fernet(key)

        plainText = fernet.decrypt(token).decode("utf-8")
        return plainText

    except (InvalidToken, ValueError, Exception):
        raise ValueError(
            "Decryption failed. Make sure the encrypted text is correct and the Seed matches exactly."
        )


def genSeed(length: int = 32) -> str:
    """
    Generate random strong seed.
    secrets is used here because random is not good for security.
    """
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{};:,.?/"
    seedTxt = ""

    for i in range(length):
        seedTxt += secrets.choice(chars)

    return seedTxt


# =========================
# AI Assistant Functions
# =========================

def seed_check(seed: str) -> str:
    """
    Check seed strength using simple rules.
    This is not a real AI model, but it works like a small assistant.
    """
    length_ok = len(seed) >= 12
    has_lower = bool(re.search(r"[a-z]", seed))
    has_upper = bool(re.search(r"[A-Z]", seed))
    has_number = bool(re.search(r"[0-9]", seed))
    has_symbol = bool(re.search(r"[^a-zA-Z0-9]", seed))

    score = sum([length_ok, has_lower, has_upper, has_number, has_symbol])

    if score <= 2:
        return "Weak Seed"
    elif score == 3 or score == 4:
        return "Medium Seed"
    else:
        return "Strong Seed"


def seedAdvice(seed: str) -> str:
    """
    Give advice depending on the seed strength.
    """
    strength = seed_check(seed)

    if strength == "Weak Seed":
        return "Your Seed is weak. Use at least 12 characters with uppercase letters, lowercase letters, numbers, and symbols."
    elif strength == "Medium Seed":
        return "Your Seed is acceptable, but it can be stronger. Add more length and symbols."
    else:
        return "Your Seed is strong. Keep it private and never share it with the encrypted message."


# =========================
# UI Helpers
# =========================

def wipe():
    for widget in root.winfo_children():
        widget.destroy()


def backBtn(command):
    back_button = tk.Button(
        root,
        text="← Back",
        command=command,
        bg=LIGHT_BUTTON,
        fg="#111827",
        font=FONT_SMALL,
        bd=0,
        width=10
    )
    back_button.place(x=12, y=12)


# =========================
# Home Page
# =========================

def homeScreen():
    wipe()

    container = tk.Frame(root, bg=BG_COLOR)
    container.pack(expand=True, fill="both")

    title = tk.Label(
        container,
        text="TraX19 Cryptographic System",
        font=FONT_TITLE,
        bg=BG_COLOR,
        fg=CYAN_COLOR
    )
    title.pack(pady=(70, 8))

    subtitle = tk.Label(
        container,
        text="Official Security Portal | Developed by Hydrotik Team",
        font=FONT_SUBTITLE,
        bg=BG_COLOR,
        fg=MUTED_COLOR
    )
    subtitle.pack(pady=(0, 45))

    menu_frame = tk.Frame(container, bg=BG_COLOR)
    menu_frame.pack()

    # First card: encryption page
    enc_card = tk.Frame(
        menu_frame,
        bg=CARD_COLOR,
        width=260,
        height=190,
        padx=20,
        pady=20
    )
    enc_card.pack(side="left", padx=20)
    enc_card.pack_propagate(False)

    enc_icon = tk.Label(
        enc_card,
        text="🔒",
        font=("Arial", 34),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    )
    enc_icon.pack(pady=(5, 8))

    enc_title = tk.Label(
        enc_card,
        text="Data Encryption",
        font=FONT_CARD_TITLE,
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    )
    enc_title.pack()

    enc_desc = tk.Label(
        enc_card,
        text="Launch the standalone cryptographic module",
        font=FONT_NORMAL,
        bg=CARD_COLOR,
        fg=MUTED_COLOR,
        wraplength=210,
        justify="center"
    )
    enc_desc.pack(pady=10)

    for widget in [enc_card, enc_icon, enc_title, enc_desc]:
        widget.bind("<Button-1>", lambda e: cryptoPage())
        widget.bind("<Enter>", lambda e, w=enc_card: w.config(bg="#172554"))
        widget.bind("<Leave>", lambda e, w=enc_card: w.config(bg=CARD_COLOR))

    # Second card: seed assistant
    ai_card = tk.Frame(
        menu_frame,
        bg=CARD_COLOR,
        width=260,
        height=190,
        padx=20,
        pady=20
    )
    ai_card.pack(side="left", padx=20)
    ai_card.pack_propagate(False)

    ai_icon = tk.Label(
        ai_card,
        text="🤖",
        font=("Arial", 34),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    )
    ai_icon.pack(pady=(5, 8))

    ai_title = tk.Label(
        ai_card,
        text="Security AI Assistant",
        font=FONT_CARD_TITLE,
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    )
    ai_title.pack()

    ai_desc = tk.Label(
        ai_card,
        text="Verify seed complexity and security standards",
        font=FONT_NORMAL,
        bg=CARD_COLOR,
        fg=MUTED_COLOR,
        wraplength=210,
        justify="center"
    )
    ai_desc.pack(pady=10)

    for widget in [ai_card, ai_icon, ai_title, ai_desc]:
        widget.bind("<Button-1>", lambda e: aiHelp())
        widget.bind("<Enter>", lambda e, w=ai_card: w.config(bg="#172554"))
        widget.bind("<Leave>", lambda e, w=ai_card: w.config(bg=CARD_COLOR))

    footer = tk.Label(
        container,
        text="Team: Hydrotik",
        font=FONT_FOOTER,
        bg=BG_COLOR,
        fg=MUTED_COLOR
    )
    footer.pack(side="bottom", pady=16)


# =========================
# Encryption Page
# =========================

def cryptoPage():
    wipe()
    backBtn(homeScreen)

    main_card = tk.Frame(root, bg=CARD_COLOR, padx=22, pady=18)
    main_card.pack(expand=True, fill="both", padx=24, pady=(44, 12))

    title_label = tk.Label(
        main_card,
        text="Data Encryption",
        font=FONT_TITLE,
        bg=CARD_COLOR,
        fg=CYAN_COLOR
    )
    title_label.pack(pady=(0, 4))

    subtitle_label = tk.Label(
        main_card,
        text="Secure offline messaging using Seed based encryption",
        font=FONT_SMALL,
        bg=CARD_COLOR,
        fg=MUTED_COLOR
    )
    subtitle_label.pack(pady=(0, 8))

    note_label = tk.Label(
        main_card,
        text="Note: The message is processed locally on this device.",
        font=FONT_SMALL,
        bg=CARD_COLOR,
        fg=DANGER_COLOR
    )
    note_label.pack(pady=(0, 12))

    input_label = tk.Label(
        main_card,
        text="Text:",
        font=FONT_LABEL,
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        anchor="w"
    )
    input_label.pack(fill="x")

    msgText_box = tk.Text(
        main_card,
        height=6,
        width=64,
        font=FONT_NORMAL,
        wrap="word",
        bd=1,
        relief="solid",
        bg=INPUT_COLOR,
        fg=TEXT_COLOR,
        insertbackground=TEXT_COLOR
    )
    msgText_box.pack(pady=(5, 12))

    seed_label = tk.Label(
        main_card,
        text="Seed / Secret Key:",
        font=FONT_LABEL,
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        anchor="w"
    )
    seed_label.pack(fill="x")

    seed_frame = tk.Frame(main_card, bg=CARD_COLOR)
    seed_frame.pack(fill="x", pady=(5, 12))

    seed_entry = tk.Entry(
        seed_frame,
        font=FONT_NORMAL,
        bd=1,
        relief="solid",
        show="*",
        bg=INPUT_COLOR,
        fg=TEXT_COLOR,
        insertbackground=TEXT_COLOR
    )
    seed_entry.pack(side="left", fill="x", expand=True, ipady=5)

    seed_visible = tk.BooleanVar(value=False)

    def toggleSeed():
        if seed_visible.get():
            seed_entry.config(show="*")
            seed_visible.set(False)
            show_seed_button.config(text="Show")
        else:
            seed_entry.config(show="")
            seed_visible.set(True)
            show_seed_button.config(text="Hide")

    show_seed_button = tk.Button(
        seed_frame,
        text="Show",
        command=toggleSeed,
        bg=LIGHT_BUTTON,
        fg="#111827",
        font=FONT_SMALL,
        bd=0,
        width=8
    )
    show_seed_button.pack(side="left", padx=(8, 0), ipady=4)

    assistant_message = tk.Label(
        main_card,
        text="AI Assistant: Use a strong Seed and never send it with the encrypted message.",
        font=FONT_SMALL,
        bg=CARD_COLOR,
        fg=MUTED_COLOR,
        wraplength=540,
        justify="center"
    )

    def on_genSeed():
        newSeed = genSeed()

        seed_entry.delete(0, tk.END)
        seed_entry.insert(0, newSeed)

        assistant_message.config(text="AI Assistant: " + seedAdvice(newSeed), fg=CYAN_COLOR)

        messagebox.showinfo(
            "Done",
            "A strong random Seed has been generated. Keep it secret and do not send it with the encrypted text."
        )

    genSeed_button = tk.Button(
        main_card,
        text="Generate Random Seed",
        command=on_genSeed,
        bg=DARK_BUTTON,
        fg=TEXT_COLOR,
        font=FONT_BUTTON,
        bd=0,
        width=24
    )
    genSeed_button.pack(pady=(0, 12), ipady=7)

    assistant_message.pack(pady=(0, 10))

    def update_seedAdvice(event=None):
        seedTxt = seed_entry.get().strip()

        if seedTxt == "":
            assistant_message.config(
                text="AI Assistant: Enter or generate a Seed to check its strength.",
                fg=MUTED_COLOR
            )
            return

        strength = seed_check(seedTxt)

        if strength == "Weak Seed":
            color = DANGER_COLOR
        else:
            color = CYAN_COLOR

        assistant_message.config(
            text="AI Assistant: " + seedAdvice(seedTxt),
            fg=color
        )

    seed_entry.bind("<KeyRelease>", update_seedAdvice)

    button_frame = tk.Frame(main_card, bg=CARD_COLOR)
    button_frame.pack(pady=(0, 12))

    output_label = tk.Label(
        main_card,
        text="Output:",
        font=FONT_LABEL,
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        anchor="w"
    )
    output_label.pack(fill="x")

    outTxt_box = tk.Text(
        main_card,
        height=6,
        width=64,
        font=FONT_NORMAL,
        wrap="word",
        bd=1,
        relief="solid",
        state="disabled",
        bg=INPUT_COLOR,
        fg=TEXT_COLOR,
        insertbackground=TEXT_COLOR
    )
    outTxt_box.pack(pady=(5, 10))

    def get_input_and_seed():
        text = msgText_box.get("1.0", tk.END).strip()
        seed = seed_entry.get().strip()

        if text == "":
            messagebox.showwarning("Warning", "Please enter text first.")
            return None, None

        if seed == "":
            messagebox.showwarning("Warning", "Please enter a Seed or generate a random one.")
            return None, None

        return text, seed

    def set_output(text):
        outTxt_box.config(state="normal")
        outTxt_box.delete("1.0", tk.END)
        outTxt_box.insert(tk.END, text)
        outTxt_box.config(state="disabled")

    def on_encrypt():
        text, seed = get_input_and_seed()

        if text is None:
            return

        try:
            encrypted = lock_msg(text, seed)
            set_output(encrypted)

            assistant_message.config(
                text="AI Assistant: Text encrypted successfully. Share only the encrypted output, not the Seed.",
                fg=CYAN_COLOR
            )

        except Exception as e:
            messagebox.showerror("Error", "An error occurred during encryption:\n" + str(e))

    def on_decrypt():
        text, seed = get_input_and_seed()

        if text is None:
            return

        try:
            decrypted = openMsg(text, seed)
            set_output(decrypted)

            assistant_message.config(
                text="AI Assistant: Decryption completed successfully.",
                fg=CYAN_COLOR
            )

        except ValueError as e:
            messagebox.showerror("Decryption Failed", str(e))

            assistant_message.config(
                text="AI Assistant: Decryption failed. The Seed may be incorrect or the encrypted text may be damaged.",
                fg=DANGER_COLOR
            )

    encrypt_button = tk.Button(
        button_frame,
        text="Encrypt",
        command=on_encrypt,
        bg=PRIMARY_COLOR,
        fg=TEXT_COLOR,
        font=FONT_BUTTON,
        bd=0,
        width=16
    )
    encrypt_button.pack(side="left", padx=8, ipady=8)

    decrypt_button = tk.Button(
        button_frame,
        text="Decrypt",
        command=on_decrypt,
        bg=BLUE_COLOR,
        fg=TEXT_COLOR,
        font=FONT_BUTTON,
        bd=0,
        width=16
    )
    decrypt_button.pack(side="left", padx=8, ipady=8)

    utility_frame = tk.Frame(main_card, bg=CARD_COLOR)
    utility_frame.pack(pady=(0, 4))

    def copy_output():
        output = outTxt_box.get("1.0", tk.END).strip()

        if output == "":
            messagebox.showwarning("Warning", "There is no output to copy.")
            return

        root.clipboard_clear()
        root.clipboard_append(output)

        messagebox.showinfo("Done", "Output copied successfully.")

    def clear_all():
        msgText_box.delete("1.0", tk.END)
        seed_entry.delete(0, tk.END)
        set_output("")

        assistant_message.config(
            text="AI Assistant: Use a strong Seed and never send it with the encrypted message.",
            fg=MUTED_COLOR
        )

    copy_button = tk.Button(
        utility_frame,
        text="Copy Output",
        command=copy_output,
        bg=LIGHT_BUTTON,
        fg="#111827",
        font=FONT_SMALL,
        bd=0,
        width=14
    )
    copy_button.pack(side="left", padx=6, ipady=5)

    clear_button = tk.Button(
        utility_frame,
        text="Clear All",
        command=clear_all,
        bg="#fee2e2",
        fg=DANGER_COLOR,
        font=FONT_SMALL,
        bd=0,
        width=14
    )
    clear_button.pack(side="left", padx=6, ipady=5)

    warning_label = tk.Label(
        main_card,
        text="Security note: Never send the Seed with the encrypted message. Anyone who has both the encrypted text and the Seed can read the message.",
        font=FONT_SMALL,
        bg=CARD_COLOR,
        fg=DANGER_COLOR,
        wraplength=540,
        justify="center"
    )
    warning_label.pack(pady=(8, 0))


# =========================
# AI Assistant Page
# =========================

def aiHelp():
    wipe()
    backBtn(homeScreen)

    container = tk.Frame(root, bg=BG_COLOR)
    container.pack(expand=True, fill="both")

    title = tk.Label(
        container,
        text="Security AI Assistant 🤖",
        font=FONT_TITLE,
        bg=BG_COLOR,
        fg=CYAN_COLOR
    )
    title.pack(pady=(50, 25))

    chat_section = tk.Frame(
        container,
        bg=CARD_COLOR,
        padx=25,
        pady=22
    )
    chat_section.pack(pady=10)

    welcome_text = tk.Label(
        chat_section,
        text="Welcome. I am the TraX19 automated advisor. Please input your cryptographic seed for complexity analysis.",
        font=FONT_NORMAL,
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        wraplength=560,
        justify="center"
    )
    welcome_text.pack(pady=(0, 18))

    seed_entry = tk.Entry(
        chat_section,
        width=45,
        font=FONT_NORMAL,
        bg=INPUT_COLOR,
        fg=TEXT_COLOR,
        insertbackground=TEXT_COLOR,
        relief="solid"
    )
    seed_entry.pack(pady=8, ipady=6)

    result_label = tk.Label(
        chat_section,
        text="",
        font=FONT_CARD_TITLE,
        bg=CARD_COLOR,
        fg=CYAN_COLOR
    )
    result_label.pack(pady=(14, 0))

    advice_label = tk.Label(
        chat_section,
        text="",
        font=FONT_SMALL,
        bg=CARD_COLOR,
        fg=MUTED_COLOR,
        wraplength=540,
        justify="center"
    )
    advice_label.pack(pady=(8, 0))

    def analyze_button_action():
        seedTxt = seed_entry.get().strip()

        if seedTxt == "":
            messagebox.showwarning("Warning", "Please enter secret seed first.")
            return

        strength = seed_check(seedTxt)
        advice = seedAdvice(seedTxt)

        if strength == "Weak Seed":
            color = DANGER_COLOR
        else:
            color = CYAN_COLOR

        result_label.config(text="Analysis Result: " + strength, fg=color)
        advice_label.config(text=advice, fg=color)

    analyze_button = tk.Button(
        chat_section,
        text="Analyze Complexity",
        command=analyze_button_action,
        bg=BLUE_COLOR,
        fg=TEXT_COLOR,
        font=FONT_CARD_TITLE,
        relief="flat",
        width=22
    )
    analyze_button.pack(pady=10, ipady=6)

    info_grid = tk.Frame(container, bg=BG_COLOR)
    info_grid.pack(pady=25)

    info_data = [
        (
            "What is a Seed?",
            "A secret string used to derive the cryptographic key."
        ),
        (
            "Offline Operation",
            "The message is encrypted and decrypted locally on your device."
        ),
        (
            "Risk Mitigation",
            "Never share your seed through insecure communication channels."
        )
    ]

    for title_text, desc_text in info_data:
        info_box = tk.Frame(
            info_grid,
            bg=CARD_COLOR,
            width=210,
            height=120,
            padx=15,
            pady=15
        )
        info_box.pack(side="left", padx=10)
        info_box.pack_propagate(False)

        box_title = tk.Label(
            info_box,
            text=title_text,
            font=FONT_CARD_TITLE,
            bg=CARD_COLOR,
            fg=CYAN_COLOR
        )
        box_title.pack(pady=(0, 8))

        box_desc = tk.Label(
            info_box,
            text=desc_text,
            font=FONT_SMALL,
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            wraplength=170,
            justify="center"
        )
        box_desc.pack()

    # Simple return button, easier for user than only the small back button
    back_button = tk.Button(
        container,
        text="← Return to Main Portal",
        command=homeScreen,
        bg=BG_COLOR,
        fg=CYAN_COLOR,
        font=FONT_NORMAL,
        relief="flat"
    )
    back_button.pack(pady=12)


# =========================
# Run App
# =========================

root = tk.Tk()
root.title(APP_NAME)
root.geometry("760x680")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

homeScreen()
root.mainloop()