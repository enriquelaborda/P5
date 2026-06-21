#ifndef INSTRUMENT_SENO
#define INSTRUMENT_SENO

#include <vector>
#include <string>
#include "instrument.h"
#include "envelope_adsr.h"

namespace upc {
  class Seno: public upc::Instrument {
    EnvelopeADSR adsr;
    float indice;
    float paso;
    float amplitud;
    std::vector<float> tbl;
  public:
    Seno(const std::string &parametros = "");
    void command(long comando, long nota, long velocidad=1); 
    const std::vector<float> & synthesize();
  };
}

#endif
