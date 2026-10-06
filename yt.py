import yt_dlp
import itertools
import sys

# Membuat iterator untuk animasi spinner
spinner = itertools.cycle(['|', '/', '-', '\\'])

def progress_hook(d):
    if d['status'] == 'downloading':
        # Mengambil persentase dari yt-dlp dan menghapus spasi berlebih
        percent = d.get('_percent_str', '0.0%').strip()
        
        # \r membuat teks selalu menimpa baris yang sama
        # \033[K memastikan sisa karakter di sebelah kanan terhapus bersih
        sys.stdout.write(f"\r⏳ Mendownload {next(spinner)} {percent} \033[K")
        sys.stdout.flush()
        
    elif d['status'] == 'finished':
        # Muncul setiap kali 1 file selesai (YouTube memisah video & audio)
        sys.stdout.write("\r✅ File selesai didownload (100%)! \033[K\n")
        sys.stdout.flush()

def download_youtube_video():
    url = input("🔗 Masukkan link YouTube: ")
    
    print("\nPilih Kualitas Video Maksimal yang Diinginkan:")
    print("1. 360p (Hemat Kuota)")
    print("2. 720p (HD)")
    print("3. 1080p (Full HD)")
    print("4. 1440p (2K)")
    print("5. 2160p (4K)")
    
    pilihan = input("Masukkan angka pilihan (1-5): ")
    
    # Mapping pilihan ke resolusi
    resolusi = {
        "1": "360",
        "2": "720",
        "3": "1080",
        "4": "1440",
        "5": "2160"
    }.get(pilihan, "720")
    
    # Konfigurasi yt-dlp
    ydl_opts = {
        'format': f'bestvideo[height<={resolusi}]+bestaudio/best[height<={resolusi}]/best',
        'outtmpl': '%(title)s.%(ext)s', 
        'merge_output_format': 'mp4',
        
        # Pengaturan agar terminal bersih
        'quiet': True,              # Sembunyikan semua log output bawaan yang panjang
        'noprogress': True,         # Matikan bar progress bawaan
        'progress_hooks': [progress_hook], # Gunakan hook animasi spinner buatan kita
    }
    
    try:
        print(f"\nMempersiapkan video (Target: {resolusi}p)...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("🎉 Semua proses selesai! Video berhasil digabung (MP4) dan disimpan.")
    except Exception as e:
        print(f"\n❌ Terjadi kesalahan: {e}")

if __name__ == "__main__":
    download_youtube_video()