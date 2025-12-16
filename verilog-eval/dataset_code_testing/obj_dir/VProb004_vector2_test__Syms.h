// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VPROB004_VECTOR2_TEST__SYMS_H_
#define VERILATED_VPROB004_VECTOR2_TEST__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODEL CLASS

#include "VProb004_vector2_test.h"

// INCLUDE MODULE CLASSES
#include "VProb004_vector2_test___024root.h"

// SYMS CLASS (contains all model state)
class alignas(VL_CACHE_LINE_BYTES)VProb004_vector2_test__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    VProb004_vector2_test* const __Vm_modelp;
    VlDeleter __Vm_deleter;
    bool __Vm_didInit = false;

    // MODULE INSTANCE STATE
    VProb004_vector2_test___024root TOP;

    // CONSTRUCTORS
    VProb004_vector2_test__Syms(VerilatedContext* contextp, const char* namep, VProb004_vector2_test* modelp);
    ~VProb004_vector2_test__Syms();

    // METHODS
    const char* name() { return TOP.name(); }
};

#endif  // guard
