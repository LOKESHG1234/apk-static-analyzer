# APK Static Analyzer

APK Static Analyzer is a Python-based tool that performs static analysis on Android APK files. This tool uses **JADX** for decompiling APKs, extracting essential app details from the AndroidManifest, scanning the code for suspicious strings, and generating a structured report. It’s a command-line tool designed for quick security and information analysis of Android applications.

---

## 🚀 Features

- **APK Decompiling**: Decompiles APK files into source code using **JADX**.
- **Manifest Extraction**: Extracts crucial details like **package name**, **permissions**, etc., from the `AndroidManifest.xml`.
- **Permissions Check**: Lists Android app permissions to help identify security risks.
- **Suspicious Code Identification**: Scans for suspicious strings in the decompiled code (e.g., `password`, `key`, `token`, etc.).
- **Error Handling**: If the APK fails to decompile, the tool will log the error and generate a failure report.
- **Multiple APK Support**: Analyze multiple APKs at once, storing results in separate directories named after the app’s package name.

---

## ⚙️ Requirements

- **Python 3.x**
- **JADX** (must be installed and available in your system’s PATH)
- Python dependencies: Listed in the `requirements.txt`

---

## 🔨 Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/apk-static-analyzer.git
cd apk-static-analyzer
```
### Step 2: Install dependencies

Make sure you have `pip` installed, then run:

```bash
pip install -r requirements.txt
This will install all the necessary dependencies for the tool to work.
```

### Step 3: Install **JADX**

You will need **JADX** installed and available in your system's PATH to decompile APKs. You can get it from [here](https://github.com/skylot/jadx).

To install it manually, download the latest release from the **JADX** GitHub page and ensure it's available globally by adding it to your PATH.

## 🧑‍💻 Usage

Once installed, you can use the tool to analyze APK files by running the following command:

```bash
python apk_analyzer.py /path/to/your.apk
```

### What the Script Does:
- **Decompiles** the APK using **JADX**.
- **Extracts** the **package name** and **permissions** from the `AndroidManifest.xml`.
- **Scans** the decompiled source code for **suspicious strings** (e.g., `password`, `key`, `token`, etc.).
- **Creates** an output directory named after the **package name**, containing the analysis report and any logs.

### Example

```bash
python apk_analyzer.py /path/to/app.apk
```

This command will create a folder like:

```
com.example.myapp_analysis/
├── analysis_report.json
└── logs/
    └── analysis_log.txt
```

- The **`analysis_report.json`** contains details such as the APK path, package name, permissions, and suspicious strings found.
- The **logs** folder will contain any logs generated during the analysis, including potential error logs.

### Multiple APKs

If you have multiple APKs of the same app stored in a folder, the tool can analyze them all. Each APK's output will be saved in a separate directory named after the app’s package name (with additional version identifiers to avoid overwriting).

```bash
python apk_analyzer.py /path/to/folder_with_apks/
```
## 🧑‍🔧 Error Handling

If **JADX** fails to decompile the APK (due to obfuscation, corruption, or other issues), the script will:
- Output an error message explaining the failure.
- Generate a `failed_analysis_report.json` file that logs the failure with context (such as the reason for failure).
- Skip to the next APK (if analyzing a folder of APKs) to ensure the tool continues running.

---

## 🗂️ Project Structure

Here’s a breakdown of the project folder structure:

```
apk-static-analyzer/
├── apk_analyzer.py            # Main script for analyzing APKs
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── samples/                   # Example output files (no real APKs)
├── .gitignore                 # Files and folders to exclude from Git
└── failed_analysis_report.json # Example failed report for debugging
```

- **apk_analyzer.py**: Main script performing static analysis.
- **requirements.txt**: Python modules required to run the tool.
- **samples/**: Folder containing example outputs for demonstration.
- **.gitignore**: Prevents unwanted files from being pushed to GitHub.
- **failed_analysis_report.json**: Captures failure context if decompiling fails.

---

## 🧑‍💻 Example Output

After running the script, a JSON report is generated. Here's an example of the `analysis_report.json`:

```json
{
    "apk_path": "/path/to/app.apk",
    "package_name": "com.example.myapp",
    "permissions": [
        "android.permission.INTERNET",
        "android.permission.ACCESS_FINE_LOCATION"
    ],
    "suspicious_strings": [
        "password",
        "key",
        "token"
    ]
}
```

- **apk_path**: Path to the analyzed APK file.
- **package_name**: Extracted from the AndroidManifest.xml.
- **permissions**: Android permissions declared by the app.
- **suspicious_strings**: Common keywords found that may indicate hardcoded secrets or insecure coding.
