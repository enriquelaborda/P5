#include "flanger.h"
#include "keyvalue.h"
#include <math.h>

using namespace upc;
using namespace std;

Flanger::Flanger(const std::string &parametros) {
  KeyValue kv(parametros);
  
  float frecuencia_lfo;
  if (!kv.to_float("frecuencia", frecuencia_lfo)) frecuencia_lfo = 0.5f;
  if (!kv.to_float("profundidad", profundidad)) profundidad = 0.005f;
  if (!kv.to_float("mezcla", mezcla)) mezcla = 0.5f;

  incremento_lfo = 2 * M_PI * frecuencia_lfo / 44100.0f;
  fase_lfo = 0;
  
  int tamano_maximo = 44100 * 0.05f;
  linea_retraso.resize(tamano_maximo, 0.0f);
  posicion_escritura = 0;
}

void Flanger::command(unsigned int comando) {
}

void Flanger::operator()(std::vector<float> &senal) {
  for (unsigned int i = 0; i < senal.size(); ++i) {
    linea_retraso[posicion_escritura] = senal[i];
    
    float retraso_actual = (profundidad / 2.0f) * (1.0f + sin(fase_lfo)) * 44100.0f;
    fase_lfo += incremento_lfo;
    if (fase_lfo >= 2 * M_PI) fase_lfo -= 2 * M_PI;
    
    float posicion_lectura = posicion_escritura - retraso_actual;
    while (posicion_lectura < 0) posicion_lectura += linea_retraso.size();
    
    int indice_entero = (int)posicion_lectura;
    float fraccion = posicion_lectura - indice_entero;
    int siguiente_indice = indice_entero + 1;
    if (siguiente_indice >= linea_retraso.size()) siguiente_indice = 0;
    
    float muestra_retrasada = linea_retraso[indice_entero] + fraccion * (linea_retraso[siguiente_indice] - linea_retraso[indice_entero]);
    
    senal[i] = senal[i] * (1.0f - mezcla) + muestra_retrasada * mezcla;
    
    posicion_escritura++;
    if (posicion_escritura >= linea_retraso.size()) posicion_escritura = 0;
  }
}
