import os
import shutil
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "EduManage_Offline_Software")

def create_package():
    print("========================================================")
    print("Creating Offline Portable Package for another PC...")
    print("========================================================")

    # Step 1: Ensure PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("[+] Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Step 2: Build EduManage.exe
    print("[+] Compiling launcher.py into standalone EduManage.exe...")
    pyinstaller_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--noconsole",
        "--name=EduManage",
        os.path.join(BASE_DIR, "launcher.py")
    ]
    subprocess.call(pyinstaller_cmd)

    exe_path = os.path.join(BASE_DIR, "dist", "EduManage.exe")
    if not os.path.exists(exe_path):
        print("[-] Build status check: EduManage.exe was not created in dist.")
        # Fallback check if existing EduManage.exe is present in root
        if os.path.exists(os.path.join(BASE_DIR, "EduManage.exe")):
            exe_path = os.path.join(BASE_DIR, "EduManage.exe")
        else:
            print("[-] Error: Executable could not be found.")
            return

    # Step 3: Prepare output directory
    if os.path.exists(OUTPUT_DIR):
        try:
            shutil.rmtree(OUTPUT_DIR)
        except Exception:
            pass
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Step 4: Copy EduManage.exe and essential project directories/files
    print("[+] Packaging application files into EduManage_Offline_Software folder...")
    shutil.copy(exe_path, os.path.join(OUTPUT_DIR, "EduManage.exe"))

    if os.path.exists(os.path.join(BASE_DIR, "db.sqlite3")):
        shutil.copy(os.path.join(BASE_DIR, "db.sqlite3"), os.path.join(OUTPUT_DIR, "db.sqlite3"))

    items_to_copy_dir = ["apps", "school_management", "templates", "static", "media", "locale"]
    for item in items_to_copy_dir:
        src = os.path.join(BASE_DIR, item)
        dst = os.path.join(OUTPUT_DIR, item)
        if os.path.exists(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)

    # Copy launcher scripts
    helper_files = ["Start_EduManage.bat", "Run_Offline_App.bat", "EduManage_Launcher.vbs", "launch_desktop.pyw"]
    for hf in helper_files:
        src = os.path.join(BASE_DIR, hf)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(OUTPUT_DIR, hf))

    # Create Bangla Instruction file for user
    instruction_text = """========================================================================
EduManage Academy - অন্য পিসিতে সফটওয়্যারটি চালানোর গাইডলাইন
========================================================================

এই ফোল্ডারটি একটি সম্পূর্ণ অফলাইন সফটওয়্যার প্যাকেজ। অন্য কোনো পিসিতে চালাতে নিচের নিয়ম অনুসরণ করুন:

১. কিভাবে অন্য পিসিতে স্থানান্তর করবেন:
   - "EduManage_Offline_Software" সম্পূর্ণ ফোল্ডারটি আপনার পেনড্রাইভ (Pen Drive), মেমোরি কার্ড বা গুগল ড্রাইভে কপি করে অন্য পিসিতে নিন।

২. কিভাবে অন্য পিসিতে চালু করবেন:
   - অন্য পিসিতে ফোল্ডারটি পেস্ট করুন।
   - ফোল্ডারের ভেতর থাকা "EduManage.exe" আইকনে ডাবল ক্লিক (Double Click) করুন।
   - সফটওয়্যারটি কোনো ইন্টারনেট ছাড়াই সরাসরি উইন্ডোজে ডেসktop অ্যাপের মতো চালু হয়ে যাবে!
   - অন্য পিসিতে Python বা অন্য কিছু ইনস্টল করার কোনো প্রয়োজন নেই।

৩. ডাটা এবং তথ্য সংরক্ষণ:
   - আপনার বর্তমান পিসির সমস্ত ভর্তি তথ্য, রেটিং ও ছবি এই ফোল্ডারের db.sqlite3 এবং media ফোল্ডারে হুবহু কপি করা আছে।

ধন্যবাদ!
========================================================================
"""
    with open(os.path.join(OUTPUT_DIR, "কিভাবে_অন্য_পিসিতে_চালাবেন.txt"), "w", encoding="utf-8") as f:
        f.write(instruction_text)

    # Cleanup temporary PyInstaller files
    if os.path.exists(os.path.join(BASE_DIR, "build")):
        try:
            shutil.rmtree(os.path.join(BASE_DIR, "build"))
        except Exception:
            pass
    if os.path.exists(os.path.join(BASE_DIR, "dist")):
        try:
            shutil.rmtree(os.path.join(BASE_DIR, "dist"))
        except Exception:
            pass
    spec_file = os.path.join(BASE_DIR, "EduManage.spec")
    if os.path.exists(spec_file):
        try:
            os.remove(spec_file)
        except Exception:
            pass

    print("\n========================================================")
    print("SUCCESS! Your Offline Portable Package is Ready!")
    print(f"Package Folder Location: {OUTPUT_DIR}")
    print("Simply copy 'EduManage_Offline_Software' folder to Pen Drive and run on any PC!")
    print("========================================================")

if __name__ == "__main__":
    create_package()
