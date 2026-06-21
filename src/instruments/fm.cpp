#include <iostream>
#include <math.h>
#include "fm.h"
#include "keyvalue.h"

#include <stdlib.h>

using namespace upc;
using namespace std;

FM::FM(const std::string &param) 
  : adsr(SamplingRate, param) {
  bActive = false;
  x.resize(BSIZE);

  KeyValue kv(param);
  int N;

  if (!kv.to_int("N", N))
    N = 1024;
    
  if (!kv.to_float("N1", N1)) N1 = 1.0f;
  if (!kv.to_float("N2", N2)) N2 = 1.0f;
  if (!kv.to_float("I", I_semi)) I_semi = 0.0f;

  tbl.resize(N);
  float phase = 0, phase_step = 2 * M_PI / (float)N;
  for (int i = 0; i < N; ++i) {
    tbl[i] = sin(phase);
    phase += phase_step;
  }
  
  index_c = 0;
  index_m = 0;
  step_c = 0;
  step_m = 0;
  I_real = 0;
  A = 0;
}

void FM::command(long cmd, long note, long vel) {
  if (cmd == 9) {
    bActive = true;
    adsr.start();
    index_c = 0;
    index_m = 0;
    A = vel / 127.0f;
    float f0 = 440.0f * pow(2.0f, (note - 69.0f) / 12.0f);
    
    float fc = N1 * f0;
    float fm = N2 * f0;
    
    step_c = fc * tbl.size() / SamplingRate;
    if (fm > 0) {
        step_m = fm * tbl.size() / SamplingRate;
        float d = fc * (pow(2.0f, I_semi / 12.0f) - 1.0f);
        I_real = d / fm;
    } else {
        step_m = 0;
        I_real = 0;
    }
  }
  else if (cmd == 8) {
    adsr.stop();
  }
  else if (cmd == 0) {
    adsr.end();
  }
}

const vector<float> & FM::synthesize() {
  if (not adsr.active()) {
    x.assign(x.size(), 0);
    bActive = false;
    return x;
  }
  else if (not bActive)
    return x;

  for (unsigned int i = 0; i < x.size(); ++i) {
    float mod_val = tbl[(int)index_m];
    float phase_offset = (I_real * mod_val) / (2.0f * M_PI) * tbl.size();
    
    float final_index = index_c + phase_offset;
    
    while (final_index >= tbl.size()) final_index -= tbl.size();
    while (final_index < 0) final_index += tbl.size();
    
    x[i] = A * tbl[(int)final_index];
    
    index_c += step_c;
    while (index_c >= tbl.size()) index_c -= tbl.size();
    
    index_m += step_m;
    while (index_m >= tbl.size()) index_m -= tbl.size();
  }
  adsr(x);

  return x;
}
