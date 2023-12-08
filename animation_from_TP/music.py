from transformers import AutoProcessor, MusicgenForConditionalGeneration
import os
import scipy
import argparse


parser = argparse.ArgumentParser(description="prompt for music generation")
parser.add_argument('--text_file', default='./sound.txt', type=str, help="txt file path")

args = parser.parse_args()

texts = []
if args.text_file != "":
    assert os.path.exists(args.text_file)
    with open(args.text_file, 'r') as f:
        texts = f.readlines()
    texts = [t.replace("\n", "")for t in texts]
    if '' in texts:
        texts.remove('')

processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")

inputs = processor(
    text=[texts[0]],
    padding=True,
    return_tensors="pt",
)

print(texts[0])
audio_values = model.generate(**inputs, max_new_tokens=1500)
sampling_rate = model.config.audio_encoder.sampling_rate
scipy.io.wavfile.write("./static/music/musicgen_out.wav", rate=sampling_rate, data=audio_values[0, 0].numpy())
