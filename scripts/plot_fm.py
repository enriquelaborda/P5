import os
import subprocess
import wave
import numpy as np
import matplotlib.pyplot as plt

def generar_audio(nombre, params, eventos_sco):
    orc_path = f"work/{nombre}.orc"
    sco_path = f"work/{nombre}.sco"
    wav_path = f"work/{nombre}.wav"

    with open(orc_path, "w") as f:
        f.write(f"1 FM {params} N=1024;\n")

    with open(sco_path, "w") as f:
        for ev in eventos_sco:
            f.write(f"{ev[0]}\t{ev[1]}\t{ev[2]}\t{ev[3]}\t{ev[4]}\n")

    cmd = ["/home/cibber/PAV/bin/synth", orc_path, sco_path, wav_path]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return wav_path

def leer_wav(wav_path):
    with wave.open(wav_path, 'r') as wf:
        n_frames = wf.getnframes()
        audio = wf.readframes(n_frames)
        sr = wf.getframerate()
        signal = np.frombuffer(audio, dtype=np.int16)
        t = np.linspace(0, n_frames / sr, num=n_frames)
    return t, signal

def main():
    if not os.path.exists("work"):
        os.makedirs("work")

    # Vibrato FM
    # N1 = 1 (portadora igual a fundamental)
    # N2 = 0.02 (f_m = 0.02 * f_0). Si f_0=440Hz, f_m = 8.8Hz.
    # I = 0.5 semitonos de variacion
    params = "ADSR_A=0.1; ADSR_D=0.1; ADSR_S=0.8; ADSR_R=0.2; N1=1.0; N2=0.02; I=0.5;"
    sco = [(0, 9, 1, 69, 100), (240, 8, 1, 69, 100), (360, 0, 1, 0, 0)]
    wav_path = generar_audio("fm_vibrato", params, sco)

    t, signal = leer_wav(wav_path)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(t, signal, color='purple', alpha=0.8)
    ax.set_title("Efecto Vibrato usando Síntesis FM (N1=1.0, N2=0.02, I=0.5)")
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Amplitud")
    
    # Zoom para mostrar que la frecuencia varia (opcional, pero se aprecia visualmente la envolvente densa)
    ax.grid(True)
    plt.tight_layout()
    plt.savefig("work/fm_plot.png")
    plt.close()

if __name__ == "__main__":
    main()
