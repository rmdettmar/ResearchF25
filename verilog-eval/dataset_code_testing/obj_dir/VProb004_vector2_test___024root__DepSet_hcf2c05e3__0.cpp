// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VProb004_vector2_test.h for the primary calling header

#include "VProb004_vector2_test__pch.h"
#include "VProb004_vector2_test__Syms.h"
#include "VProb004_vector2_test___024root.h"

#ifdef VL_DEBUG
VL_ATTR_COLD void VProb004_vector2_test___024root___dump_triggers__ico(VProb004_vector2_test___024root* vlSelf);
#endif  // VL_DEBUG

void VProb004_vector2_test___024root___eval_triggers__ico(VProb004_vector2_test___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VProb004_vector2_test___024root___eval_triggers__ico\n"); );
    VProb004_vector2_test__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VicoTriggered.setBit(0U, (IData)(vlSelfRef.__VicoFirstIteration));
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        VProb004_vector2_test___024root___dump_triggers__ico(vlSelf);
    }
#endif
}

#ifdef VL_DEBUG
VL_ATTR_COLD void VProb004_vector2_test___024root___dump_triggers__act(VProb004_vector2_test___024root* vlSelf);
#endif  // VL_DEBUG

void VProb004_vector2_test___024root___eval_triggers__act(VProb004_vector2_test___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VProb004_vector2_test___024root___eval_triggers__act\n"); );
    VProb004_vector2_test__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VactTriggered.setBit(0U, ((IData)(vlSelfRef.tb__DOT__clk) 
                                          ^ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tb__DOT__clk__0)));
    vlSelfRef.__VactTriggered.setBit(1U, vlSelfRef.__VdlySched.awaitingCurrentTime());
    vlSelfRef.__Vtrigprevexpr___TOP__tb__DOT__clk__0 
        = vlSelfRef.tb__DOT__clk;
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        VProb004_vector2_test___024root___dump_triggers__act(vlSelf);
    }
#endif
}
