#include <iostream>
#include <math.h>
#include "seno.h"
#include "keyvalue.h"
#include <stdlib.h>

using namespace upc;
using namespace std;

Seno::Seno(const std::string &parametros) 
  : adsr(SamplingRate, parametros) {
  bActive = false;
  x.resize(BSIZE);

  KeyValue kv(parametros);
  int tamano_tabla;

  if (!kv.to_int("N", tamano_tabla))
    tamano_tabla = 1024;

  tbl.resize(tamano_tabla);
  float fase_actual = 0;
  float incremento_fase = 2 * M_PI / (float)tamano_tabla;
  for (int i = 0; i < tamano_tabla; ++i) {
    tbl[i] = sin(fase_actual);
    fase_actual += incremento_fase;
  }
  
  indice = 0;
  paso = 0;
  amplitud = 0;
}

void Seno::command(long comando, long nota, long velocidad) {
  if (comando == 9) {
    bActive = true;
    adsr.start();
    indice = 0;
    amplitud = velocidad / 127.0f;
    float frecuencia = 440.0f * pow(2.0f, (nota - 69.0f) / 12.0f);
    paso = frecuencia * tbl.size() / SamplingRate;
  }
  else if (comando == 8) {
    adsr.stop();
  }
  else if (comando == 0) {
    adsr.end();
  }
}

const vector<float> & Seno::synthesize() {
  if (not adsr.active()) {
    x.assign(x.size(), 0);
    bActive = false;
    return x;
  }
  else if (not bActive)
    return x;

  for (unsigned int i = 0; i < x.size(); ++i) {
    int indice_entero = (int)indice;
    float fraccion = indice - indice_entero;
    int siguiente_indice = indice_entero + 1;
    if (siguiente_indice >= tbl.size()) {
      siguiente_indice = 0;
    }
    
    float valor_interpolado = tbl[indice_entero] + fraccion * (tbl[siguiente_indice] - tbl[indice_entero]);
    x[i] = amplitud * valor_interpolado;
    
    indice += paso;
    while (indice >= tbl.size()) {
      indice -= tbl.size();
    }
  }
  adsr(x);

  return x;
}
