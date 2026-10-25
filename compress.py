import subprocess
import argparse
from pathlib import Path

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


def main():
    parser = argparse.ArgumentParser(description="Compress")
    parser.add_argument("input", help="path to the video file")
    parser.add_argument("-t", "--target", type=float,  default=10,
                            help="target size in MB (default: 10)")
    parser.add_argument("-o", "--output",
                        help="output path")
    args = parser.parse_args()

    input_path = Path(args.input)
    if args.output:
        output_path = Path(args.output)
    else:
        output_path =input_path.with_name(f"{input_path.stem}_{args.target:g}MB.mp4")

    compress(input_path, output_path, args.target)
    size_mb = output_path.stat().st_size / 1048576
    print(f"Wrote {output_path} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()