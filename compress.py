import subprocess

def target_video_kbps(target_mb, duration_s, audio_kbps=128):
    total_kbps = (target_mb * 8192) / duration_s
    return max(int(total_kbps - audio_kbps), 0)

def get_duration(path):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of", "csv=p=0", str(path)],
                            capture_output=True, text=True, check=True,)
    return float(result.stdout.strip())

if __name__ == "__main__":
    d = get_duration("testoutput.mp4")
    print(d, target_video_kbps(10, d))