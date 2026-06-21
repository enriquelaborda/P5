#include "sampler.h"
#include "keyvalue.h"
#include "wavfile_mono.h"
#include <math.h>

using namespace upc;
using namespace std;

Sampler::Sampler(const std::string &parametros) 
  : adsr(SamplingRate, parametros) {
  bActive = false;
  x.resize(BSIZE);

  KeyValue kv(parametros);
  string ruta_archivo;
  
  ruta_archivo = kv("fichero");
  if (ruta_archivo == "") {
    ruta_archivo = "default.wav";
  }

  unsigned int frecuencia_muestreo;
  if (readwav_mono(ruta_archivo, frecuencia_muestreo, memoria) < 0) {
    memoria.resize(1);
    memoria[0] = 0.0f;
  }
  
  indice = 0;
  paso = 1.0f;
  amplitud = 0;
}

void Sampler::command(long comando, long nota, long velocidad) {
  if (comando == 9) {
    bActive = true;
    adsr.start();
    indice = 0;
    amplitud = velocidad / 127.0f;
    float frecuencia_base = 440.0f;
    float frecuencia_nota = 440.0f * pow(2.0f, (nota - 69.0f) / 12.0f);
    paso = frecuencia_nota / frecuencia_base;
  }
  else if (comando == 8) {
    adsr.stop();
  }
  else if (comando == 0) {
    adsr.end();
  }
}

const vector<float> & Sampler::synthesize() {
  if (not adsr.active()) {
    x.assign(x.size(), 0);
    bActive = false;
    return x;
  }
  else if (not bActive)
    return x;

  for (unsigned int i = 0; i < x.size(); ++i) {
    if (indice >= memoria.size() - 1) {
      x[i] = 0;
    } else {
      int indice_entero = (int)indice;
      float fraccion = indice - indice_entero;
      float valor = memoria[indice_entero] + fraccion * (memoria[indice_entero + 1] - memoria[indice_entero]);
      x[i] = amplitud * valor;
      indice += paso;
    }
  }
  adsr(x);

  return x;
}
