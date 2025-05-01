import os
import sys
import subprocess
import json
import re
from colorama import Fore, Style, init # type: ignore

# Initilize colorama
init(autoreset=True)

def log(message,icon="ℹ️", color=Fore.CYAN):
    print(color + f"{icon} {message}")

def run_jadx(apkPath,output_dir):
    log("Running Jadx to decompile APK...","🛠️",Fore.YELLOW)
    try:
        subprocess.run(["jadx","-d",output_dir,apkPath], check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    except subprocess.CalledProcessError as e:
        log("Couldn't decompile the APK...","⚠️",Fore.RED)
        log(f"Error details: {e.stderr.strip()}", "🧯", Fore.RED)
        sys.exit(1)


def get_package_name_manifest(manifest_path):
    """Extracts package name from decompiled AndroidManifest.xml."""
    try:
        with open(manifest_path,"r",encoding="utf-8") as f:
            content = f.read()
        match = re.search(r'package\s*=\s*"([^"]+)"', content, re.DOTALL)
        return match.group(1) if match else "unknown_pacage"
    except Exception as e:
        log(f"Error reading manifest: {e}", "❌", Fore.RED)
        return "unknown_package"

def extract_permission(manifest_path):
    try:
        with open(manifest_path,"r",encoding="utf-8") as f:
            content = f.read()
        permissions = re.findall(r'android\.permission\.[A-Z_]+',content)
        return sorted(set(permissions))
    except:
        return []

def find_suspicious_strings(output_dir):
    suspicious = []
    for root,_,files in os.walk(output_dir):
        for file in files:
            if file.endswith(".java"):
                path = os.path.join(root,file)
                with open(path,"r",errors="ignore") as f:
                    data = f.read()
                    if any(kw in data for kw in ["getDeviceId", "exec", "loadUrl"]):
                        suspicious.append(os.path.realpath(path,output_dir))
    return suspicious

def main():
    if len(sys.argv)!=2:
        log("Usage: python apk_analyzer.py <path_to_apk>","❌",Fore.RED)
        sys.exit(1)
   
    apk_path = sys.argv[1]
   
    if not os.path.isfile(apk_path):
        log(f"APK file not found : {apk_path}","❌",Fore.RED)
        sys.exit(1)
   
    base_dir = os.path.dirname(os.path.abspath(apk_path))
    temp_jadx_output = os.path.join(base_dir,"temp_jadx_output")

    run_jadx(apk_path,temp_jadx_output)
    for root,_,files in os.walk(temp_jadx_output):
        if "AndroidManifest.xml" in files:
            manifest = os.path.join(root,"AndroidManifest.xml")
    manifest_path = os.path.join(temp_jadx_output,manifest)
    package_name = get_package_name_manifest(manifest_path)

    output_dir = os.path.join(base_dir,f"{package_name}_analysis")
    os.makedirs(output_dir,exist_ok=True)

    log(f"Extracting permissions...", "📜", Fore.YELLOW)
    permissions = extract_permission(manifest_path)

    log(f"Scanning for suspicious code...", "🔍", Fore.YELLOW)
    suspicious_files = find_suspicious_strings(temp_jadx_output)

    report = {
        "apk_path":apk_path,
        "package_name":package_name,
        "permissions":permissions,
        "suspicious_code_files":suspicious_files
    }

    report_path = os.path.join(output_dir,"analysis_report.json")
    with open(report_path,"w") as f:
        json.dump(report,f,indent=4)
    
    final_jadx_path = os.path.join(output_dir,"jadx_output")
    os.rename(temp_jadx_output,final_jadx_path)

    log(f"Package: {package_name}", "📦", Fore.GREEN)
    log(f"Output directory: {output_dir}", "📁", Fore.GREEN)
    log(f"Report saved: {report_path}", "📄", Fore.GREEN)
    log("Analysis complete!", "✅", Fore.GREEN)


if __name__ =="__main__":
    main()