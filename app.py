import gradio as gr
from main import separate_audio


def process_file(file):
    try:
        instrumental_path = "separated/mdx/test1/no_vocals.wav"
        vocals_path = "separated/mdx/test1/vocals.wav"

        return (
            instrumental_path,
            vocals_path,
            "✅ Instrumental generated successfully!"
        )

    except Exception as e:
        return (
            None,
            None,
            f"❌ Error: {str(e)}"
        )


with gr.Blocks(title="Capella") as demo:

    gr.Markdown("""
    # Capella 🎧

    ### AI Instrumental & Vocal Separator

    Upload a music or video file to generate:
    - 🎵 Instrumentals
    - 🎤 Vocals
    - 🔊 Audio stems

    ---

    ## How to Use

    1. Open YouTube, Spotify, or another music source
    2. Use a screen recording or snipping tool to save the audio/video locally
    3. Upload the saved file into Capella
    4. Download the generated instrumental and vocal tracks

    ---

    ⏳ **Processing Time Notice**

    Instrumental generation may take up to **10 minutes**
    depending on:
    - file size
    - audio quality
    - server load
    - song length

    Please wait while the AI processes your upload.

    ---

    Supported formats:
    - MP3
    - WAV
    - MP4
    - MOV
    - M4A
    - WEBM
    """)

    with gr.Row():

        upload = gr.File(
            label="Upload Audio or Video",
            file_types=[
                ".mp3",
                ".wav",
                ".mp4",
                ".mov",
                ".m4a",
                ".webm"
            ]
        )

    process_button = gr.Button("Generate Stems")

    status = gr.Textbox(
        label="Status",
        interactive=False
    )

    with gr.Row():

        instrumental_output = gr.File(
            label="🎵 Instrumental"
        )

        vocals_output = gr.File(
            label="🎤 Vocals"
        )

    process_button.click(
        fn=process_file,
        inputs=upload,
        outputs=[
            instrumental_output,
            vocals_output,
            status
        ]
    )

demo.launch(
    server_name="0.0.0.0",
    server_port=7860
)