// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop_module.h for the primary calling header

#include "Vtop_module__pch.h"
#include "Vtop_module__Syms.h"
#include "Vtop_module___024root.h"

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop_module___024root___dump_triggers__ico(Vtop_module___024root* vlSelf);
#endif  // VL_DEBUG

void Vtop_module___024root___eval_triggers__ico(Vtop_module___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop_module___024root___eval_triggers__ico\n"); );
    Vtop_module__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VicoTriggered.setBit(0U, (IData)(vlSelfRef.__VicoFirstIteration));
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vtop_module___024root___dump_triggers__ico(vlSelf);
    }
#endif
}

VL_INLINE_OPT void Vtop_module___024root___ico_sequent__TOP__0(Vtop_module___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop_module___024root___ico_sequent__TOP__0\n"); );
    Vtop_module__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((0U == (IData)(vlSelfRef.top_module__DOT__state))) {
        if (vlSelfRef.ground) {
            if (vlSelfRef.dig) {
                vlSelfRef.top_module__DOT__next = 4U;
                ++(vlSymsp->__Vcoverage[0]);
            } else {
                ++(vlSymsp->__Vcoverage[1]);
                vlSelfRef.top_module__DOT__next = 0U;
            }
        } else {
            ++(vlSymsp->__Vcoverage[2]);
            vlSelfRef.top_module__DOT__next = 2U;
        }
        ++(vlSymsp->__Vcoverage[3]);
    } else if ((1U == (IData)(vlSelfRef.top_module__DOT__state))) {
        if (vlSelfRef.ground) {
            if (vlSelfRef.dig) {
                ++(vlSymsp->__Vcoverage[6]);
                vlSelfRef.top_module__DOT__next = 5U;
            } else if (vlSelfRef.bump_right) {
                ++(vlSymsp->__Vcoverage[4]);
                vlSelfRef.top_module__DOT__next = 0U;
            } else {
                ++(vlSymsp->__Vcoverage[5]);
                vlSelfRef.top_module__DOT__next = 1U;
            }
        } else {
            ++(vlSymsp->__Vcoverage[7]);
            vlSelfRef.top_module__DOT__next = 3U;
        }
        ++(vlSymsp->__Vcoverage[8]);
    } else if ((2U == (IData)(vlSelfRef.top_module__DOT__state))) {
        vlSelfRef.top_module__DOT__next = (7U & ((IData)(vlSelfRef.ground)
                                                  ? 
                                                 ([&]() {
                        ++(vlSymsp->__Vcoverage[11]);
                    }(), ((0x14U <= (IData)(vlSelfRef.top_module__DOT__fall_counter))
                           ? ([&]() {
                                ++(vlSymsp->__Vcoverage[9]);
                            }(), 6U) : ([&]() {
                                ++(vlSymsp->__Vcoverage[10]);
                            }(), 0U))) : ([&]() {
                        ++(vlSymsp->__Vcoverage[12]);
                    }(), 2U)));
        ++(vlSymsp->__Vcoverage[13]);
    } else if ((3U == (IData)(vlSelfRef.top_module__DOT__state))) {
        vlSelfRef.top_module__DOT__next = (7U & ((IData)(vlSelfRef.ground)
                                                  ? 
                                                 ([&]() {
                        ++(vlSymsp->__Vcoverage[16]);
                    }(), ((0x14U <= (IData)(vlSelfRef.top_module__DOT__fall_counter))
                           ? ([&]() {
                                ++(vlSymsp->__Vcoverage[14]);
                            }(), 6U) : ([&]() {
                                ++(vlSymsp->__Vcoverage[15]);
                            }(), 1U))) : ([&]() {
                        ++(vlSymsp->__Vcoverage[17]);
                    }(), 3U)));
        ++(vlSymsp->__Vcoverage[18]);
    } else if ((4U == (IData)(vlSelfRef.top_module__DOT__state))) {
        vlSelfRef.top_module__DOT__next = (7U & ((IData)(vlSelfRef.ground)
                                                  ? 
                                                 ([&]() {
                        ++(vlSymsp->__Vcoverage[19]);
                    }(), 4U) : ([&]() {
                        ++(vlSymsp->__Vcoverage[20]);
                    }(), 2U)));
        ++(vlSymsp->__Vcoverage[21]);
    } else if ((5U == (IData)(vlSelfRef.top_module__DOT__state))) {
        vlSelfRef.top_module__DOT__next = (7U & ((IData)(vlSelfRef.ground)
                                                  ? 
                                                 ([&]() {
                        ++(vlSymsp->__Vcoverage[22]);
                    }(), 5U) : ([&]() {
                        ++(vlSymsp->__Vcoverage[23]);
                    }(), 3U)));
        ++(vlSymsp->__Vcoverage[24]);
    } else if ((6U == (IData)(vlSelfRef.top_module__DOT__state))) {
        ++(vlSymsp->__Vcoverage[25]);
        vlSelfRef.top_module__DOT__next = 6U;
    }
    ++(vlSymsp->__Vcoverage[26]);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop_module___024root___dump_triggers__act(Vtop_module___024root* vlSelf);
#endif  // VL_DEBUG

void Vtop_module___024root___eval_triggers__act(Vtop_module___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop_module___024root___eval_triggers__act\n"); );
    Vtop_module__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VactTriggered.setBit(0U, ((IData)(vlSelfRef.areset) 
                                          & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__areset__0))));
    vlSelfRef.__VactTriggered.setBit(1U, ((IData)(vlSelfRef.clk) 
                                          & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk__0))));
    vlSelfRef.__Vtrigprevexpr___TOP__areset__0 = vlSelfRef.areset;
    vlSelfRef.__Vtrigprevexpr___TOP__clk__0 = vlSelfRef.clk;
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vtop_module___024root___dump_triggers__act(vlSelf);
    }
#endif
}

VL_INLINE_OPT void Vtop_module___024root___nba_sequent__TOP__0(Vtop_module___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop_module___024root___nba_sequent__TOP__0\n"); );
    Vtop_module__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (((2U == (IData)(vlSelfRef.top_module__DOT__state)) 
         | (3U == (IData)(vlSelfRef.top_module__DOT__state)))) {
        if ((0x14U > (IData)(vlSelfRef.top_module__DOT__fall_counter))) {
            vlSelfRef.top_module__DOT__fall_counter 
                = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.top_module__DOT__fall_counter)));
            ++(vlSymsp->__Vcoverage[30]);
        } else {
            ++(vlSymsp->__Vcoverage[31]);
        }
        ++(vlSymsp->__Vcoverage[32]);
    } else {
        ++(vlSymsp->__Vcoverage[33]);
        vlSelfRef.top_module__DOT__fall_counter = 0U;
    }
    ++(vlSymsp->__Vcoverage[34]);
}

VL_INLINE_OPT void Vtop_module___024root___nba_sequent__TOP__1(Vtop_module___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop_module___024root___nba_sequent__TOP__1\n"); );
    Vtop_module__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.areset) {
        ++(vlSymsp->__Vcoverage[27]);
        vlSelfRef.top_module__DOT__state = 0U;
    } else {
        ++(vlSymsp->__Vcoverage[28]);
        vlSelfRef.top_module__DOT__state = vlSelfRef.top_module__DOT__next;
    }
    ++(vlSymsp->__Vcoverage[29]);
    vlSelfRef.walk_left = (0U == (IData)(vlSelfRef.top_module__DOT__state));
    vlSelfRef.walk_right = (1U == (IData)(vlSelfRef.top_module__DOT__state));
    vlSelfRef.aaah = ((2U == (IData)(vlSelfRef.top_module__DOT__state)) 
                      | (3U == (IData)(vlSelfRef.top_module__DOT__state)));
    vlSelfRef.digging = ((4U == (IData)(vlSelfRef.top_module__DOT__state)) 
                         | (5U == (IData)(vlSelfRef.top_module__DOT__state)));
}
