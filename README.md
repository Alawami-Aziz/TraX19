# TraX19
TraX19 Security Portal is a privacy-focused cybersecurity application designed to encrypt and decrypt text messages locally without requiring an internet connection. It provides a secure way to share sensitive information by locking messages behind a custom Secret Key (Seed) known only to the sender and the intended receiver.
إليك ملف التوثيق مصاغاً بتنسيق `README.md` استناداً بالكامل إلى النص الذي وفرته في "README_2.docx"، مع إضافة أقسام هيكلية الملفات وتثبيت وبناء المشروع ليتوافق مع معايير GitHub:

```markdown
# TraX19 Security Portal[cite: 13]

**Team Hydrotik**: Abdulaziz Wadea Alawami, Jawad Yasser Al Arafat, Hussain Adel Alkhater, Mahdi Ahmed Buholaigah[cite: 13].
**Project Concept**: Secure Offline Messaging[cite: 13].

## Project Overview
TraX19 Security Portal is a cybersecurity project that allows users to encrypt and decrypt text messages locally without using the internet[cite: 13]. The project is designed to protect private messages by using a shared secret Seed between the sender and the receiver[cite: 13]. The program combines programming, cybersecurity, and basic artificial intelligence concepts through a simple interface, encryption system, and a rule-based AI assistant that checks the strength of the Seed[cite: 13].

## Key Features
* **Offline Operation**: Encryption and decryption happen locally on the user’s device without requiring an internet connection[cite: 13].
* **Strong Privacy Protection**: Even if someone intercepts the encrypted message, they cannot read it without the correct Seed[cite: 13]. The security of the message depends on keeping the Seed private[cite: 13].
* **Seed Strength Analysis**: The Security AI Assistant analyzes the Seed and gives feedback about its strength to help users avoid weak Seeds[cite: 13].
* **Windows Compatibility**: The program is compiled as a Windows .exe file, allowing users to run it easily on Windows devices[cite: 13].
* **User-Friendly Interface**: The interface is simple and clear, making the program easy to use even for users with limited technical experience[cite: 13].

## File Structure
```text
├── main.py                   # The main Python source code
├── README.md                 # Project documentation (this file)
├── LICENSE                   # Custom Personal Use License
└── .gitignore                # Files ignored by Git

```

## Requirements and Installation

The program utilizes built-in Python libraries including `Tkinter`, `Secrets`, `String`, `Base64`, and `Re`. The `Cryptography` library must be installed before running the Python source code.

To install the required library, use:

```bash
pip install cryptography

```

## Build Instructions (For Developers)

To convert the Python script into a standalone executable (`.exe`), the project uses `PyInstaller`:

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole main.py

```

## How to Use the Program

1. Open the project folder and run the program file.


2. If Windows shows a security warning, click **More info**, then click **Run anyway**.


3. From the main portal, choose either **Data Encryption** or **Security AI Assistant**.



### Using the Security AI Assistant

1. Click **Security AI Assistant**.


2. Enter the Seed you want to test. Try to use at least 12 characters including uppercase letters, lowercase letters, numbers, and symbols.


3. Click **Analyze Complexity**. The assistant will show whether the Seed is Weak, Medium, or Strong.


4. Click **Return to Main Portal**.



### Using Data Encryption

1. Click **Data Encryption**.


2. Write the message you want to encrypt in the Text box.


3. Enter the Seed you tested or generate a random Seed.


4. Click **Encrypt** and copy the encrypted output.


5. Send the encrypted output to the intended receiver, and share the Seed through a safe method.



### Using Decryption

1. The receiver opens the same program and clicks **Data Encryption**.


2. The receiver pastes the encrypted output into the Text box.


3. The receiver enters the exact same Seed in the Seed / Secret Key field and clicks **Decrypt**.


4. If the Seed is correct, the original message will appear. If the Seed is wrong, the program will not decrypt the message.



## Important Security Notes

* Never send the Seed together with the encrypted message.


* Anyone who has both the encrypted message and the Seed can decrypt the message.


* Weak Seeds can be guessed, so users should use strong and long Seeds.


* The program works offline, but users must still protect the Seed carefully.



## Tools and Techniques

| Technique | Explanation |
| --- | --- |
| **Python** | The main programming language used to build the project.

 |
| **Tkinter** | Used to create the graphical user interface.

 |
| **Fernet** | A symmetric encryption system used to encrypt and decrypt messages.

 |
| **PBKDF2 + SHA-256** | Used to convert the Seed into a strong encryption key.

 |
| **Secrets** | Used to generate secure random Seeds.

 |
| **Base64** | Used to make encrypted data easy to copy, paste, and send as text.

 |
| **Regular Expressions (Re)** | Used by the AI Assistant to check whether the Seed contains uppercase letters, lowercase letters, numbers, and symbols.

 |
| **PyInstaller** | Used to convert the Python program into a Windows .exe application.

 |

## Artificial Intelligence Usage

The project uses a rule-based AI assistant. The assistant does not require an internet connection or an external API. It analyzes the Seed based on security rules, such as length, uppercase letters, lowercase letters, numbers, and symbols. The assistant helps users understand whether their Seed is Weak, Medium, or Strong and gives advice to improve security.

## Saudi Vision 2030 Alignment

The project supports Saudi Vision 2030 by encouraging digital transformation, cybersecurity awareness, and technical innovation. It helps users understand the importance of protecting sensitive information and promotes the development of local technical solutions by students.

## Conclusion

TraX19 Security Portal is a practical offline cybersecurity tool that allows users to encrypt and decrypt messages using a shared Secret Seed. The project combines programming, cybersecurity, and AI concepts in a simple and useful application.

## License

This software is provided for personal, non-commercial use only. You may NOT modify, alter, or adapt the source code without explicit prior written permission from the authors. Commercial use or redistribution without approval is strictly prohibited.
