import subprocess

def target_video_kbps(target_mb, duration_s, audio_kbps=128):
    total_kbps = (target_mb * 8192) / duration_s
    return max(int(total_kbps - audio_kbps), 0)

def get_duration(path):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of", "csv=p=0", str(path)],
                            capture_output=True, text=True, check=True,)
    return float(result.stdout.strip())


def compress(input_path, output_path, target_mb, audio_kbps=128):
    duration = get_duration(input_path)
    video_kbps = target_video_kbps(target_mb, duration, audio_kbps)

    subprocess.run(["ffmpeg", "-i", str(input_path),
                    "-c:v", "libx264", "-b:v", f"{video_kbps}k",
                    "-c:a", "aac", "-b:a", f"{audio_kbps}k",
                    str(output_path)],
                    check=True)

if __name__ == "__main__":
    compress("test.mp4", "output_test_10mb.mp4", 10)