// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VProb004_vector2_test.h for the primary calling header

#include "VProb004_vector2_test__pch.h"
#include "VProb004_vector2_test__Syms.h"
#include "VProb004_vector2_test___024root.h"

void VProb004_vector2_test___024root___ctor_var_reset(VProb004_vector2_test___024root* vlSelf);

VProb004_vector2_test___024root::VProb004_vector2_test___024root(VProb004_vector2_test__Syms* symsp, const char* v__name)
    : VerilatedModule{v__name}
    , __VdlySched{*symsp->_vm_contextp__}
    , vlSymsp{symsp}
 {
    // Reset structure values
    VProb004_vector2_test___024root___ctor_var_reset(this);
}

void VProb004_vector2_test___024root::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

VProb004_vector2_test___024root::~VProb004_vector2_test___024root() {
}
