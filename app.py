import gradio as gr
import os
import subprocess


def find_demucs_output(base_dir, filename):
    """
    Finds the correct Demucs output folder regardless of model name (htdemucs, mdx, etc.)
    """
    if not os.path.exists(base_dir):
        return None

    for model_dir in os.listdir(base_dir):
        track_path = os.path.join(base_dir, model_dir, filename)
        if os.path.exists(track_path):
            return track_path

    return None


def process_file(file):
    try:
        print("START DEMUCS")

        if file is None:
            return None, None, "❌ No file uploaded"

        input_path = file

        # Run Demucs
        subprocess.run(
            ["python", "-m", "demucs", "--two-stems=vocals", input_path],
            check=True
        )

        # Extract filename safely
        filename = os.path.splitext(os.path.basename(input_path))[0]

        base_dir = "/app/separated"

        track_dir = find_demucs_output(base_dir, filename)

        if track_dir is None:
            return None, None, "❌ Demucs output folder not found"

        instrumental_path = os.path.join(track_dir, "no_vocals.wav")
        vocals_path = os.path.join(track_dir, "vocals.wav")

        print("TRACK DIR:", track_dir)
        print("INSTRUMENTAL PATH:", instrumental_path)
        print("VOCALS PATH:", vocals_path)

        # Verify files exist before returning (VERY important for Gradio)
        if not os.path.exists(instrumental_path):
            return None, None, f"❌ Missing instrumental file: {instrumental_path}"

        if not os.path.exists(vocals_path):
            return None, None, f"❌ Missing vocals file: {vocals_path}"

        return (
            instrumental_path,
            vocals_path,
            "✅ Instrumental generated successfully!"
        )

    except Exception as e:
        return None, None, f"❌ Error: {str(e)}"


# ---------------- UI ---------------- #

upload = gr.File(label="Upload Audio/Video")

instrumental_output = gr.Audio(label="Instrumental")
vocals_output = gr.Audio(label="Vocals")
status = gr.Textbox(label="Status")

process_button = gr.Button("Generate Instrumental")

process_button.click(
    fn=process_file,
    inputs=upload,
    outputs=[instrumental_output, vocals_output, status]
)

demo = gr.Blocks()
with demo:
    gr.Markdown("# 🎵 Instrumental Generator (Demucs)")
    upload.render()
    process_button.render()
    instrumental_output.render()
    vocals_output.render()
    status.render()

demo.launch()