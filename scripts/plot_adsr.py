import os
import subprocess
import wave
import numpy as np
import matplotlib.pyplot as plt

def generar_audio(nombre, adsr_params, eventos_sco):
    orc_path = f"work/{nombre}.orc"
    sco_path = f"work/{nombre}.sco"
    wav_path = f"work/{nombre}.wav"

    with open(orc_path, "w") as f:
        f.write(f"1 InstrumentDumb {adsr_params} N=40;\n")

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
        
        # Extraer la envolvente superior
        ventana = sr // 100
        envolvente = np.zeros_like(signal, dtype=np.float32)
        for i in range(0, len(signal), ventana):
            fin = min(i + ventana, len(signal))
            max_val = np.max(np.abs(signal[i:fin]))
            envolvente[i:fin] = max_val
            
    return t, envolvente

def main():
    if not os.path.exists("work"):
        os.makedirs("work")

    # 1. Genérico
    adsr_gen = "ADSR_A=0.2; ADSR_D=0.1; ADSR_S=0.5; ADSR_R=0.2;"
    sco_gen = [(0, 9, 1, 60, 100), (120, 8, 1, 60, 100), (240, 0, 1, 0, 0)]
    wav_gen = generar_audio("adsr_generico", adsr_gen, sco_gen)

    # 2. Percusivo (final abrupto)
    adsr_perc = "ADSR_A=0.01; ADSR_D=1.0; ADSR_S=0.0; ADSR_R=0.1;"
    sco_perc_abrupto = [(0, 9, 1, 60, 100), (48, 8, 1, 60, 100), (120, 0, 1, 0, 0)]
    wav_perc_abrupto = generar_audio("adsr_perc_abrupto", adsr_perc, sco_perc_abrupto)

    # 3. Percusivo (completa extincion)
    sco_perc_completo = [(0, 9, 1, 60, 100), (240, 8, 1, 60, 100), (360, 0, 1, 0, 0)]
    wav_perc_completo = generar_audio("adsr_perc_completo", adsr_perc, sco_perc_completo)

    # 4. Plano
    adsr_plano = "ADSR_A=0.05; ADSR_D=0.05; ADSR_S=0.9; ADSR_R=0.05;"
    sco_plano = [(0, 9, 1, 60, 100), (120, 8, 1, 60, 100), (240, 0, 1, 0, 0)]
    wav_plano = generar_audio("adsr_plano", adsr_plano, sco_plano)

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    
    t_gen, env_gen = leer_wav(wav_gen)
    axs[0, 0].plot(t_gen, env_gen, color='blue')
    axs[0, 0].set_title("ADSR Genérico (A=0.2, D=0.1, S=0.5, R=0.2)")
    axs[0, 0].set_xlabel("Tiempo (s)")
    axs[0, 0].set_ylabel("Amplitud")
    axs[0, 0].grid(True)

    t_pa, env_pa = leer_wav(wav_perc_abrupto)
    axs[0, 1].plot(t_pa, env_pa, color='red')
    axs[0, 1].set_title("Percusivo - Liberación temprana")
    axs[0, 1].set_xlabel("Tiempo (s)")
    axs[0, 1].set_ylabel("Amplitud")
    axs[0, 1].grid(True)

    t_pc, env_pc = leer_wav(wav_perc_completo)
    axs[1, 0].plot(t_pc, env_pc, color='orange')
    axs[1, 0].set_title("Percusivo - Extinción completa")
    axs[1, 0].set_xlabel("Tiempo (s)")
    axs[1, 0].set_ylabel("Amplitud")
    axs[1, 0].grid(True)

    t_pl, env_pl = leer_wav(wav_plano)
    axs[1, 1].plot(t_pl, env_pl, color='green')
    axs[1, 1].set_title("Plano (A=0.05, D=0.05, S=0.9, R=0.05)")
    axs[1, 1].set_xlabel("Tiempo (s)")
    axs[1, 1].set_ylabel("Amplitud")
    axs[1, 1].grid(True)

    plt.tight_layout()
    plt.savefig("work/adsr_plots.png")
    plt.close()

if __name__ == "__main__":
    main()
