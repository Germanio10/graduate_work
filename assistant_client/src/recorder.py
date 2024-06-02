import io
import wave

import pyaudio


class Recorder:

    def record_audio(self, seconds, sample_rate,
                     chunk_size=4000, num_channels=1) -> bytes:

        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=num_channels,
            rate=sample_rate,
            input=True,
            frames_per_buffer=chunk_size
        )
        frames = []
        try:
            for i in range(0, int(sample_rate / chunk_size * seconds)):
                data = stream.read(chunk_size)
                frames.append(data)
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

        container = io.BytesIO()
        wf = wave.open(container, 'wb')
        wf.setnchannels(num_channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))
        container.seek(0)
        return container
