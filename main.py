import subprocess
from concurrent.futures import ThreadPoolExecutor
import time

# Daftar skrip bot yang akan dijalankan
bot_scripts = [
    "s1.py",
    "s2.py",
    "s3.py",
    "s4.py",
    "s5.py",
    "s6.py"
]

# Fungsi untuk menjalankan skrip bot
def run_bot_script(script_name):
    try:
        print(f"Menjalankan {script_name}...")
        process = subprocess.Popen(['python3', script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Mencetak output dan error jika ada
        print(f"Output dari {script_name}:\n{stdout.decode()}")
        if stderr:
            print(f"Error dari {script_name}:\n{stderr.decode()}")
    except Exception as e:
        print(f"Terjadi kesalahan saat menjalankan {script_name}: {e}")

if __name__ == "__main__":
    # Menjalankan semua skrip bot secara bersamaan menggunakan ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=len(bot_scripts)) as executor:
        futures = [executor.submit(run_bot_script, script) for script in bot_scripts]
        
        # Menunggu semua tugas selesai
        for future in futures:
            future.result()


