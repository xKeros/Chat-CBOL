import assemblyai as aai

aai.settings.api_key = f"8b72d5120f5c40099a653d0210714078"

transcriber = aai.Transcriber()

audio_url = (
    "C:\Users\keros\Documents\Codes\Jobs\Intento 2\Audio-de-WhatsApp-2023-11-30-a-las-19.59.11_130c392b.mp3"
)

config = aai.TranscriptionConfig(speaker_labels=True)

transcript = transcriber.transcribe(audio_url, config)

print(transcript.text)

for utterance in transcript.utterances:
    print(f"Speaker {utterance.speaker}: {utterance.text}")