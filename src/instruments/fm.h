#ifndef INSTRUMENT_FM
#define INSTRUMENT_FM

#include <vector>
#include <string>
#include "instrument.h"
#include "envelope_adsr.h"

namespace upc {
  class FM: public upc::Instrument {
    EnvelopeADSR adsr;
    float index_c;
    float index_m;
    float step_c;
    float step_m;
    float I_real;
    float A;
    float N1, N2, I_semi;
    std::vector<float> tbl;
  public:
    FM(const std::string &param = "");
    void command(long cmd, long note, long velocity=1); 
    const std::vector<float> & synthesize();
  };
}

#endif
