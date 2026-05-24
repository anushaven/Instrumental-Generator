import os
import subprocess

print("RUNNING FILE:", __file__)

OUTPUT_DIR = "separated"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def separate_audio(audio_path):
    print("START DEMUCS")

    command = [
        "python",
        "-m",
        "demucs",
        "-n",
        "mdx",
        "--two-stems=vocals",
        "--segment",
        "10",
        "-o",
        OUTPUT_DIR,
        audio_path,
    ]

    subprocess.run(command, check=True)

    filename = os.path.splitext(
        os.path.basename(audio_path)
    )[0]

    instrumental_path = os.path.join(
        OUTPUT_DIR,
        "mdx",
        filename,
        "no_vocals.wav"
    )

    print("INSTRUMENTAL PATH:", instrumental_path)

    if not os.path.exists(instrumental_path):
        raise FileNotFoundError(
            f"Instrumental file not found: {instrumental_path}"
        )

    return instrumental_path