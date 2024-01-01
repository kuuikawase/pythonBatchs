from faster_whisper import WhisperModel


class WhisperModelWrapper:
    def __init__(self):
        self.model_size_or_path = "large-v2"
        self.model = WhisperModel(
            self.model_size_or_path, device="cuda", compute_type="int8_float32"
        )

    def transcribe(self):
        tsss = "E:\\record.wav"
        test = "C:\\Users\\kuui\\PycharmProjects\\pythonProject6\\batch\MIMI『ルルージュ』feat初音ミク.mp3"
        segments, tesssss = self.model.transcribe(
            audio=test, beam_size=5, language="ja", without_timestamps=True
        )
        return segments, tesssss


# ssdar, tesssssss = WhisperModelWrapper().transcribe();
# print("test")
# print("Detected language '%s' with probability %f" % (tesssssss.language, tesssssss.language_probability))
# ssdar = list(ssdar)
# print(ssdar)
# for seg in ssdar:
#     print(seg.text)
#
# print("test")

model_size = "large-v2"

# Run on GPU with FP16
model = WhisperModel(model_size, device="cuda", compute_type="int8")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

segments, info = model.transcribe("C:\\Users\\kuui\\PycharmProjects\\pythonProject6\\batch\\MIMI『ルルージュ』feat初音ミク.mp3", beam_size=5)

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))