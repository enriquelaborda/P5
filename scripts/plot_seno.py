import numpy as np
import matplotlib.pyplot as plt
import os

def main():
    if not os.path.exists("work"):
        os.makedirs("work")

    # Tamaño de tabla y generacion de la misma
    N = 40
    tabla = np.sin(2 * np.pi * np.arange(N) / N)

    # Parametros para la senal generada
    sr = 44100
    f = 440.0 * 8 # Una frecuencia alta para que se vean pocos periodos y se note el muestreo
    step = f * N / sr
    
    num_muestras = int(sr / f * 2) # Mostrar 2 periodos
    senal_generada = np.zeros(num_muestras)
    
    indices_usados = []
    index = 0.0
    for i in range(num_muestras):
        idx_entero = int(index)
        senal_generada[i] = tabla[idx_entero]
        indices_usados.append((i, idx_entero))
        index += step
        if index >= N:
            index -= N

    # Graficar
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Dibujar la tabla continua (como referencia)
    x_continuo = np.linspace(0, N, 500)
    y_continuo = np.sin(2 * np.pi * x_continuo / N)
    ax.plot(x_continuo, y_continuo, 'k--', alpha=0.3, label='Seno ideal')
    
    # Puntos de la tabla
    ax.plot(np.arange(N), tabla, 'bo', label='Valores de la tabla', alpha=0.5)
    
    # Puntos seleccionados para la señal generada
    x_gen = [item[1] for item in indices_usados]
    y_gen = senal_generada
    ax.plot(x_gen, y_gen, 'rX', markersize=8, label='Señal generada (truncamiento)')
    
    # Conectar los valores seleccionados en el orden de generación
    for i in range(len(x_gen)-1):
        if x_gen[i+1] > x_gen[i]:
            ax.plot([x_gen[i], x_gen[i+1]], [y_gen[i], y_gen[i+1]], 'r-', alpha=0.4)
            
    ax.set_title("Método de Truncamiento para Síntesis por Tabla de Búsqueda")
    ax.set_xlabel("Índice de la Tabla")
    ax.set_ylabel("Amplitud")
    ax.legend()
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig("work/seno_plot.png")
    plt.close()

if __name__ == "__main__":
    main()
