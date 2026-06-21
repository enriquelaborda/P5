import numpy as np
import matplotlib.pyplot as plt
import os

def main():
    if not os.path.exists("work"):
        os.makedirs("work")

    sr = 44100
    t_total = 1.0
    t = np.linspace(0, t_total, int(sr * t_total), endpoint=False)
    
    f_portadora = 20.0 # Baja frecuencia para visualizar
    A = 1.0

    # Tremolo (Modulacion de Amplitud)
    # f_m = frecuencia del LFO (ej: 2 Hz)
    # I_m = indice de modulacion (profundidad, ej: 0.8)
    f_m_trem = 2.0
    I_m_trem = 0.8
    # Envolvente = 1 + I_m * sin(2*pi*f_m*t) o similar, tipicamente 1 + I_m * (LFO)
    # Para que sea Tremolo normal, varia entre 1-I_m y 1+I_m (si esta centrado en 1)
    envolvente_tremolo = 1.0 + I_m_trem * np.sin(2 * np.pi * f_m_trem * t)
    senal_tremolo = envolvente_tremolo * A * np.sin(2 * np.pi * f_portadora * t)

    # Vibrato (Modulacion de Frecuencia)
    # f_m = frecuencia del LFO (ej: 2 Hz)
    # I_m = indice de modulacion (desviacion maxima)
    f_m_vib = 2.0
    # Desviacion = I_m * sin(2*pi*f_m*t)
    # Fase = integral de frecuencia = 2*pi*f_c*t + (I_m/(2*pi*f_m)) * (-cos(2*pi*f_m*t))
    # Para simplificar, la fase varia segun un seno: 2*pi*f_c*t + I_phase * sin(2*pi*f_m*t)
    I_phase = 2.0 # Desviacion de fase
    senal_vibrato = A * np.sin(2 * np.pi * f_portadora * t + I_phase * np.sin(2 * np.pi * f_m_vib * t))

    fig, axs = plt.subplots(2, 1, figsize=(10, 8))
    
    axs[0].plot(t, senal_tremolo, label='Señal con Trémolo')
    axs[0].plot(t, envolvente_tremolo, 'r--', alpha=0.7, label='Envolvente (Modulación AM)')
    axs[0].plot(t, -envolvente_tremolo, 'r--', alpha=0.7)
    axs[0].set_title(f"Efecto Trémolo (Frec. LFO={f_m_trem}Hz, Índice Modulación={I_m_trem})")
    axs[0].set_xlabel("Tiempo (s)")
    axs[0].set_ylabel("Amplitud")
    axs[0].legend(loc="upper right")
    axs[0].grid(True)

    axs[1].plot(t, senal_vibrato, color='green', label='Señal con Vibrato')
    axs[1].set_title(f"Efecto Vibrato (Frec. LFO={f_m_vib}Hz, Modulación FM)")
    axs[1].set_xlabel("Tiempo (s)")
    axs[1].set_ylabel("Amplitud")
    axs[1].legend(loc="upper right")
    axs[1].grid(True)

    plt.tight_layout()
    plt.savefig("work/efectos_plot.png")
    plt.close()

if __name__ == "__main__":
    main()
