// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "VProb004_vector2_test__pch.h"
#include "VProb004_vector2_test.h"
#include "VProb004_vector2_test___024root.h"

// FUNCTIONS
VProb004_vector2_test__Syms::~VProb004_vector2_test__Syms()
{
}

VProb004_vector2_test__Syms::VProb004_vector2_test__Syms(VerilatedContext* contextp, const char* namep, VProb004_vector2_test* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup module instances
    , TOP{this, namep}
{
        // Check resources
        Verilated::stackCheck(41);
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-12);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
}
