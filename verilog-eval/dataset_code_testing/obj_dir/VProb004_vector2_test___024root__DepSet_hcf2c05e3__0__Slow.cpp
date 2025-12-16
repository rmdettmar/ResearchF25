// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VProb004_vector2_test.h for the primary calling header

#include "VProb004_vector2_test__pch.h"
#include "VProb004_vector2_test__Syms.h"
#include "VProb004_vector2_test___024root.h"

VL_ATTR_COLD void VProb004_vector2_test___024root___eval_initial__TOP(VProb004_vector2_test___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VProb004_vector2_test___024root___eval_initial__TOP\n"); );
    VProb004_vector2_test__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSymsp->_vm_contextp__->dumpfile(std::string{"wave.vcd"});
    VL_PRINTF_MT("-Info: Prob004_vector2_test.sv:66: $dumpvar ignored, as Verilated without --trace\n");
}

#ifdef VL_DEBUG
VL_ATTR_COLD void VProb004_vector2_test___024root___dump_triggers__stl(VProb004_vector2_test___024root* vlSelf);
#endif  // VL_DEBUG

VL_ATTR_COLD void VProb004_vector2_test___024root___eval_triggers__stl(VProb004_vector2_test___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VProb004_vector2_test___024root___eval_triggers__stl\n"); );
    VProb004_vector2_test__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VstlTriggered.setBit(0U, (IData)(vlSelfRef.__VstlFirstIteration));
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        VProb004_vector2_test___024root___dump_triggers__stl(vlSelf);
    }
#endif
}
