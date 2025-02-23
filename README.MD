# Hacking Toolkit

## 📌 Description
This project is a collection of utilities for security testing and fuzzing. Currently, it includes a file and directory fuzzer that searches for existing files on a target website based on a given list and extensions. The project will be expanded with additional security tools in the future.

## 📁 Project Structure
```md
Hacking/
│── fazzer/                # Directory containing the fuzzing utility
│   ├── fazzer_directory.py  # Main fuzzing script
│   ├── file.txt            # File storing found directories
│   ├── wordlist.txt        # File containing the wordlist for fuzzing
```

## 🚀 Installation & Usage

### 1️⃣ Install Dependencies
Before running the fuzzer, install the required libraries (e.g., requests):
```bash

pip install -r requirements.txt
```
### 2️⃣ Configure Settings
Modify `application.properties` to set logging level and the number of threads for fuzzing:
```
[Settings]
log_level = INFO
max_workers = 10
```

### 3️⃣ Run the Fuzzer
Run the fuzzer using:
```bash

python fazzer/fazzer_directory.py
```

Then enter:
The target website URL (without a trailing /)
A list of file extensions separated by commas (e.g., .txt,.php)
Results are saved in `fazzer/file.txt.`

## 🛠️ Configuration
- Modify the wordlist by changing the file name or editing `wordlist.txt`.
- Change the results file by specifying a custom output file during execution.
- Adjust settings in `application.properties` for logging level and concurrency.

Logs are saved in `fuzzer.log`.

## 🔥 Future Features



## 📜 License
This project is for educational purposes only. The author is not responsible for any unauthorized use.

