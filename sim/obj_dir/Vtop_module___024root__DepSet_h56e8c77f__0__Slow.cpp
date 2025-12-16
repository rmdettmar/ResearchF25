// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop_module.h for the primary calling header

#include "Vtop_module__pch.h"
#include "Vtop_module___024root.h"

VL_ATTR_COLD void Vtop_module___024root___eval_static(Vtop_module___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop_module___024root___eval_static\n"); );
    Vtop_module__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__Vtrigprevexpr___TOP__areset__0 = vlSelfRef.areset;
    vlSelfRef.__Vtrigprevexpr___TOP__clk__0 = vlSelfRef.clk;
}

VL_ATTR_COLD void Vtop_module___024root___eval_initial(Vtop_module___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop_module___024root___eval_initial\n"); );
    Vtop_module__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

VL_ATTR_COLD void Vtop_module___024root___eval_final(Vtop_module___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop_module___024root___eval_final\n"); );
    Vtop_module__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop_module___024root___dump_triggers__stl(Vtop_module___024root* vlSelf);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vtop_module___024root___eval_phase__stl(Vtop_module___024root* vlSelf);

VL_ATTR_COLD void Vtop_module___024root___eval_settle(Vtop_module___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop_module___024root___eval_settle\n"); );
    Vtop_module__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
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
            Vtop_module___024root___dump_triggers__stl(vlSelf);
#endif
            VL_FATAL_MT("top_module.v", 3, "", "Settle region did not converge.");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        __VstlContinue = 0U;
        if (Vtop_module___024root___eval_phase__stl(vlSelf)) {
            __VstlContinue = 1U;
        }
        vlSelfRef.__VstlFirstIteration = 0U;
    }
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop_module___024root___dump_triggers__stl(Vtop_module___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop_module___024root___dump_triggers__stl\n"); );
    Vtop_module__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
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

VL_ATTR_COLD void Vtop_module___024root___stl_sequent__TOP__0(Vtop_module___024root* vlSelf);

VL_ATTR_COLD void Vtop_module___024root___eval_stl(Vtop_module___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop_module___024root___eval_stl\n"); );
    Vtop_module__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VstlTriggered.word(0U))) {
        Vtop_module___024root___stl_sequent__TOP__0(vlSelf);
    }
}

VL_ATTR_COLD void Vtop_module___024root___eval_triggers__stl(Vtop_module___024root* vlSelf);

VL_ATTR_COLD bool Vtop_module___024root___eval_phase__stl(Vtop_module___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop_module___024root___eval_phase__stl\n"); );
    Vtop_module__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __VstlExecute;
    // Body
    Vtop_module___024root___eval_triggers__stl(vlSelf);
    __VstlExecute = vlSelfRef.__VstlTriggered.any();
    if (__VstlExecute) {
        Vtop_module___024root___eval_stl(vlSelf);
    }
    return (__VstlExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop_module___024root___dump_triggers__ico(Vtop_module___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop_module___024root___dump_triggers__ico\n"); );
    Vtop_module__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
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
VL_ATTR_COLD void Vtop_module___024root___dump_triggers__act(Vtop_module___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop_module___024root___dump_triggers__act\n"); );
    Vtop_module__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VactTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 0 is active: @(posedge areset)\n");
    }
    if ((2ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 1 is active: @(posedge clk)\n");
    }
}
#endif  // VL_DEBUG

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop_module___024root___dump_triggers__nba(Vtop_module___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop_module___024root___dump_triggers__nba\n"); );
    Vtop_module__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VnbaTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 0 is active: @(posedge areset)\n");
    }
    if ((2ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 1 is active: @(posedge clk)\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vtop_module___024root___ctor_var_reset(Vtop_module___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop_module___024root___ctor_var_reset\n"); );
    Vtop_module__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->name());
    vlSelf->clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16707436170211756652ull);
    vlSelf->areset = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17430697350190813730ull);
    vlSelf->bump_left = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5729710541284066176ull);
    vlSelf->bump_right = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14741765023761155444ull);
    vlSelf->ground = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5559230265223984522ull);
    vlSelf->dig = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4885036060200124158ull);
    vlSelf->walk_left = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16438538073155596056ull);
    vlSelf->walk_right = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4655861305782901394ull);
    vlSelf->aaah = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9531490485207904187ull);
    vlSelf->digging = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11567499669812378961ull);
    vlSelf->top_module__DOT__state = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4836515097629899100ull);
    vlSelf->top_module__DOT__next = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17891282283853424336ull);
    vlSelf->top_module__DOT__fall_counter = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 10434997080166912933ull);
    vlSelf->__Vtrigprevexpr___TOP__areset__0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1340528480001893565ull);
    vlSelf->__Vtrigprevexpr___TOP__clk__0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9526919608049418986ull);
}
