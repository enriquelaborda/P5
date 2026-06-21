#ifndef EFFECT_FLANGER
#define EFFECT_FLANGER

#include <vector>
#include <string>
#include "effect.h"

namespace upc {
  class Flanger: public upc::Effect {
    std::vector<float> linea_retraso;
    int posicion_escritura;
    float fase_lfo;
    float incremento_lfo;
    float profundidad;
    float mezcla;
  public:
    Flanger(const std::string &parametros = "");
    void command(unsigned int comando);
    void operator()(std::vector<float> &senal);
  };
}

#endif
