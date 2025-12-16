// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VProb004_vector2_test.h for the primary calling header

#include "VProb004_vector2_test__pch.h"
#include "VProb004_vector2_test___024root.h"

VL_ATTR_COLD void VProb004_vector2_test___024root___eval_static__TOP(VProb004_vector2_test___024root* vlSelf);

VL_ATTR_COLD void VProb004_vector2_test___024root___eval_static(VProb004_vector2_test___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VProb004_vector2_test___024root___eval_static\n"); );
    VProb004_vector2_test__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    VProb004_vector2_test___024root___eval_static__TOP(vlSelf);
    vlSelfRef.__Vtrigprevexpr___TOP__tb__DOT__clk__0 = 0U;
}

VL_ATTR_COLD void VProb004_vector2_test___024root___eval_static__TOP(VProb004_vector2_test___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VProb004_vector2_test___024root___eval_static__TOP\n"); );
    VProb004_vector2_test__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.tb__DOT__clk = 0U;
}

VL_ATTR_COLD void VProb004_vector2_test___024root___eval_final__TOP(VProb004_vector2_test___024root* vlSelf);

VL_ATTR_COLD void VProb004_vector2_test___024root___eval_final(VProb004_vector2_test___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VProb004_vector2_test___024root___eval_final\n"); );
    VProb004_vector2_test__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    VProb004_vector2_test___024root___eval_final__TOP(vlSelf);
}

VL_ATTR_COLD void VProb004_vector2_test___024root___eval_final__TOP(VProb004_vector2_test___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VProb004_vector2_test___024root___eval_final__TOP\n"); );
    VProb004_vector2_test__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((0U != vlSelfRef.tb__DOT__stats1__BRA__95__03a64__KET__)) {
        VL_WRITEF_NX("Hint: Output 'out' has %0d mismatches. First mismatch occurred at time %0d.\n",0,
                     32,vlSelfRef.tb__DOT__stats1__BRA__95__03a64__KET__,
                     32,vlSelfRef.tb__DOT__stats1__BRA__63__03a32__KET__);
    } else {
        VL_WRITEF_NX("Hint: Output 'out' has no mismatches.\n",0);
    }
    VL_WRITEF_NX("Hint: Total mismatched samples is %1d out of %1d samples\n\nSimulation finished at %0# ps\nMismatches: %1d in %1d samples\n",0,
                 32,vlSelfRef.tb__DOT__stats1__BRA__159__03a128__KET__,
                 32,vlSelfRef.tb__DOT__stats1__BRA__31__03a0__KET__,
                 64,VL_TIME_UNITED_Q(1),32,vlSelfRef.tb__DOT__stats1__BRA__159__03a128__KET__,
                 32,vlSelfRef.tb__DOT__stats1__BRA__31__03a0__KET__);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void VProb004_vector2_test___024root___dump_triggers__stl(VProb004_vector2_test___024root* vlSelf);
#endif  // VL_DEBUG
VL_ATTR_COLD bool VProb004_vector2_test___024root___eval_phase__stl(VProb004_vector2_test___024root* vlSelf);

VL_ATTR_COLD void VProb004_vector2_test___024root___eval_settle(VProb004_vector2_test___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VProb004_vector2_test___024root___eval_settle\n"); );
    VProb004_vector2_test__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    IData/*31:0*/ __VstlIterCount;
    CData/*0:0*/ __VstlContinue;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    __VstlContinue = 1U;
    while (__VstlContinue) {
        if (VL_UNLIKELY(((0x64U < __VstlIterCount)))) {
#ifdef VL_DEBUG
            VProb004_vector2_test___024root___dump_triggers__stl(vlSelf);
#endif
            VL_FATAL_MT("Prob004_vector2_ref.sv", 11, "", "Settle region did not converge.");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        __VstlContinue = 0U;
        if (VProb004_vector2_test___024root___eval_phase__stl(vlSelf)) {
            __VstlContinue = 1U;
        }
        vlSelfRef.__VstlFirstIteration = 0U;
    }
}

#ifdef VL_DEBUG
VL_ATTR_COLD void VProb004_vector2_test___024root___dump_triggers__stl(VProb004_vector2_test___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VProb004_vector2_test___024root___dump_triggers__stl\n"); );
    VProb004_vector2_test__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VstlTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VstlTriggered.word(0U))) {
        VL_DBG_MSGF("         'stl' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void VProb004_vector2_test___024root___stl_sequent__TOP__0(VProb004_vector2_test___024root* vlSelf);

VL_ATTR_COLD void VProb004_vector2_test___024root___eval_stl(VProb004_vector2_test___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VProb004_vector2_test___024root___eval_stl\n"); );
    VProb004_vector2_test__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VstlTriggered.word(0U))) {
        VProb004_vector2_test___024root___stl_sequent__TOP__0(vlSelf);
    }
}

VL_ATTR_COLD void VProb004_vector2_test___024root___stl_sequent__TOP__0(VProb004_vector2_test___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VProb004_vector2_test___024root___stl_sequent__TOP__0\n"); );
    VProb004_vector2_test__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    SData/*15:0*/ tb__DOT__top_module1__DOT____VdfgRegularize_h45ca6e9a_0_0;
    tb__DOT__top_module1__DOT____VdfgRegularize_h45ca6e9a_0_0 = 0;
    // Body
    vlSelfRef.TestModuleII__02Eout = ((0xfe000000U 
                                       & (vlSelfRef.TestModuleII__02Ein 
                                          << 0x18U)) 
                                      | ((0xff0000U 
                                          & (vlSelfRef.TestModuleII__02Ein 
                                             << 8U)) 
                                         | ((0xff00U 
                                             & (vlSelfRef.TestModuleII__02Ein 
                                                >> 8U)) 
                                            | (vlSelfRef.TestModuleII__02Ein 
                                               >> 0x18U))));
    vlSelfRef.TestModuleIV__02Eout = (((vlSelfRef.TestModuleIV__02Ein 
                                        << 0x18U) | 
                                       (0xf00000U & 
                                        (vlSelfRef.TestModuleIV__02Ein 
                                         << 8U))) | 
                                      ((0xf00U & (vlSelfRef.TestModuleIV__02Ein 
                                                  >> 8U)) 
                                       | (vlSelfRef.TestModuleIV__02Ein 
                                          >> 0x18U)));
    vlSelfRef.TestModuleV__02Eout = (((IData)((vlSelfRef.TestModuleV__02Ein 
                                               >> 8U)) 
                                      << 0x10U) | (
                                                   (0xff00U 
                                                    & ((IData)(
                                                               (vlSelfRef.TestModuleV__02Ein 
                                                                >> 0x10U)) 
                                                       << 8U)) 
                                                   | (0xffU 
                                                      & (IData)(
                                                                (vlSelfRef.TestModuleV__02Ein 
                                                                 >> 0x18U)))));
    tb__DOT__top_module1__DOT____VdfgRegularize_h45ca6e9a_0_0 
        = ((0xff00U & (vlSelfRef.tb__DOT__in >> 8U)) 
           | (vlSelfRef.tb__DOT__in >> 0x18U));
    vlSelfRef.tb__DOT__out_ref = ((vlSelfRef.tb__DOT__in 
                                   << 0x18U) | ((0xff0000U 
                                                 & (vlSelfRef.tb__DOT__in 
                                                    << 8U)) 
                                                | (IData)(tb__DOT__top_module1__DOT____VdfgRegularize_h45ca6e9a_0_0)));
    vlSelfRef.tb__DOT__out_dut = ((0U == (3U & vlSelfRef.tb__DOT__in))
                                   ? ((0xffff0000U 
                                       & ((0xff000000U 
                                           & (vlSelfRef.tb__DOT__in 
                                              << 0x10U)) 
                                          | (0xff0000U 
                                             & (vlSelfRef.tb__DOT__in 
                                                << 8U)))) 
                                      | (IData)(tb__DOT__top_module1__DOT____VdfgRegularize_h45ca6e9a_0_0))
                                   : vlSelfRef.tb__DOT__out_ref);
}

VL_ATTR_COLD void VProb004_vector2_test___024root___eval_triggers__stl(VProb004_vector2_test___024root* vlSelf);

VL_ATTR_COLD bool VProb004_vector2_test___024root___eval_phase__stl(VProb004_vector2_test___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VProb004_vector2_test___024root___eval_phase__stl\n"); );
    VProb004_vector2_test__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __VstlExecute;
    // Body
    VProb004_vector2_test___024root___eval_triggers__stl(vlSelf);
    __VstlExecute = vlSelfRef.__VstlTriggered.any();
    if (__VstlExecute) {
        VProb004_vector2_test___024root___eval_stl(vlSelf);
    }
    return (__VstlExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void VProb004_vector2_test___024root___dump_triggers__ico(VProb004_vector2_test___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VProb004_vector2_test___024root___dump_triggers__ico\n"); );
    VProb004_vector2_test__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VicoTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VicoTriggered.word(0U))) {
        VL_DBG_MSGF("         'ico' region trigger index 0 is active: Internal 'ico' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

#ifdef VL_DEBUG
VL_ATTR_COLD void VProb004_vector2_test___024root___dump_triggers__act(VProb004_vector2_test___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VProb004_vector2_test___024root___dump_triggers__act\n"); );
    VProb004_vector2_test__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VactTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 0 is active: @(edge tb.clk)\n");
    }
    if ((2ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 1 is active: @([true] __VdlySched.awaitingCurrentTime())\n");
    }
}
#endif  // VL_DEBUG

#ifdef VL_DEBUG
VL_ATTR_COLD void VProb004_vector2_test___024root___dump_triggers__nba(VProb004_vector2_test___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VProb004_vector2_test___024root___dump_triggers__nba\n"); );
    VProb004_vector2_test__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VnbaTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 0 is active: @(edge tb.clk)\n");
    }
    if ((2ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 1 is active: @([true] __VdlySched.awaitingCurrentTime())\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void VProb004_vector2_test___024root___ctor_var_reset(VProb004_vector2_test___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    VProb004_vector2_test___024root___ctor_var_reset\n"); );
    VProb004_vector2_test__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->name());
    vlSelf->TestModuleI__02Ein = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16485924942884709454ull);
    vlSelf->TestModuleI__02Eout = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17623250481041541986ull);
    vlSelf->TestModuleII__02Ein = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17327198175425105848ull);
    vlSelf->TestModuleII__02Eout = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12244041828343517034ull);
    vlSelf->TestModuleIII__02Ein = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9950784915688185377ull);
    vlSelf->TestModuleIII__02Eout = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6459523243315702307ull);
    vlSelf->TestModuleIV__02Ein = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15315970746732061538ull);
    vlSelf->TestModuleIV__02Eout = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9381154518846545907ull);
    vlSelf->TestModuleV__02Ein = VL_SCOPED_RAND_RESET_Q(33, __VscopeHash, 2078900494465390801ull);
    vlSelf->TestModuleV__02Eout = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15547384284006164330ull);
    vlSelf->tb__DOT__stats1__BRA__159__03a128__KET__ = 0;
    vlSelf->tb__DOT__stats1__BRA__95__03a64__KET__ = 0;
    vlSelf->tb__DOT__stats1__BRA__63__03a32__KET__ = 0;
    vlSelf->tb__DOT__stats1__BRA__31__03a0__KET__ = 0;
    vlSelf->tb__DOT__clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6743979137201610926ull);
    vlSelf->tb__DOT__in = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14361395156134582772ull);
    vlSelf->tb__DOT__out_ref = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12088917061226620127ull);
    vlSelf->tb__DOT__out_dut = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7526293502792665379ull);
    vlSelf->__Vtrigprevexpr___TOP__tb__DOT__clk__0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3935217543338555246ull);
}
