import pyaudio


class AudioPlayer:

    def play_audio(self, audio_data, num_channels=1,
                   sample_rate=16000, chunk_size=2000) -> None:
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=num_channels,
            rate=sample_rate,
            output=True,
            frames_per_buffer=chunk_size
        )

        try:
            for i in range(0, len(audio_data), chunk_size):
                stream.write(audio_data[i:i + chunk_size])
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
