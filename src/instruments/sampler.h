#ifndef INSTRUMENT_SAMPLER
#define INSTRUMENT_SAMPLER

#include <vector>
#include <string>
#include "instrument.h"
#include "envelope_adsr.h"

namespace upc {
  class Sampler: public upc::Instrument {
    EnvelopeADSR adsr;
    float indice;
    float paso;
    float amplitud;
    std::vector<float> memoria;
  public:
    Sampler(const std::string &parametros = "");
    void command(long comando, long nota, long velocidad=1); 
    const std::vector<float> & synthesize();
  };
}

#endif
