// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop_module.h for the primary calling header

#include "Vtop_module__pch.h"
#include "Vtop_module__Syms.h"
#include "Vtop_module___024root.h"

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop_module___024root___dump_triggers__stl(Vtop_module___024root* vlSelf);
#endif  // VL_DEBUG

VL_ATTR_COLD void Vtop_module___024root___eval_triggers__stl(Vtop_module___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop_module___024root___eval_triggers__stl\n"); );
    Vtop_module__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VstlTriggered.setBit(0U, (IData)(vlSelfRef.__VstlFirstIteration));
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vtop_module___024root___dump_triggers__stl(vlSelf);
    }
#endif
}

VL_ATTR_COLD void Vtop_module___024root___stl_sequent__TOP__0(Vtop_module___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop_module___024root___stl_sequent__TOP__0\n"); );
    Vtop_module__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.walk_left = (0U == (IData)(vlSelfRef.top_module__DOT__state));
    vlSelfRef.walk_right = (1U == (IData)(vlSelfRef.top_module__DOT__state));
    vlSelfRef.aaah = ((2U == (IData)(vlSelfRef.top_module__DOT__state)) 
                      | (3U == (IData)(vlSelfRef.top_module__DOT__state)));
    vlSelfRef.digging = ((4U == (IData)(vlSelfRef.top_module__DOT__state)) 
                         | (5U == (IData)(vlSelfRef.top_module__DOT__state)));
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

VL_ATTR_COLD void Vtop_module___024root___configure_coverage(Vtop_module___024root* vlSelf, bool first) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop_module___024root___configure_coverage\n"); );
    Vtop_module__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    (void)first;  // Prevent unused variable warning
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[0]), first, "top_module.v", 3, 360, ".top_module", "v_line/top_module", "if", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[1]), first, "top_module.v", 3, 361, ".top_module", "v_line/top_module", "else", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[2]), first, "top_module.v", 3, 328, ".top_module", "v_line/top_module", "elsif", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[3]), first, "top_module.v", 3, 326, ".top_module", "v_line/top_module", "case", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[4]), first, "top_module.v", 3, 461, ".top_module", "v_line/top_module", "if", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[5]), first, "top_module.v", 3, 462, ".top_module", "v_line/top_module", "else", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[6]), first, "top_module.v", 3, 434, ".top_module", "v_line/top_module", "elsif", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[7]), first, "top_module.v", 3, 402, ".top_module", "v_line/top_module", "elsif", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[8]), first, "top_module.v", 3, 400, ".top_module", "v_line/top_module", "case", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[9]), first, "top_module.v", 3, 549, ".top_module", "v_branch/top_module", "cond_then", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[10]), first, "top_module.v", 3, 550, ".top_module", "v_branch/top_module", "cond_else", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[11]), first, "top_module.v", 3, 547, ".top_module", "v_branch/top_module", "cond_then", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[12]), first, "top_module.v", 3, 548, ".top_module", "v_branch/top_module", "cond_else", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[13]), first, "top_module.v", 3, 509, ".top_module", "v_line/top_module", "case", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[14]), first, "top_module.v", 3, 614, ".top_module", "v_branch/top_module", "cond_then", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[15]), first, "top_module.v", 3, 615, ".top_module", "v_branch/top_module", "cond_else", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[16]), first, "top_module.v", 3, 612, ".top_module", "v_branch/top_module", "cond_then", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[17]), first, "top_module.v", 3, 613, ".top_module", "v_branch/top_module", "cond_else", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[18]), first, "top_module.v", 3, 574, ".top_module", "v_line/top_module", "case", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[19]), first, "top_module.v", 3, 656, ".top_module", "v_branch/top_module", "cond_then", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[20]), first, "top_module.v", 3, 657, ".top_module", "v_branch/top_module", "cond_else", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[21]), first, "top_module.v", 3, 638, ".top_module", "v_line/top_module", "case", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[22]), first, "top_module.v", 3, 692, ".top_module", "v_branch/top_module", "cond_then", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[23]), first, "top_module.v", 3, 693, ".top_module", "v_branch/top_module", "cond_else", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[24]), first, "top_module.v", 3, 674, ".top_module", "v_line/top_module", "case", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[25]), first, "top_module.v", 3, 710, ".top_module", "v_line/top_module", "case", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[26]), first, "top_module.v", 3, 293, ".top_module", "v_line/top_module", "block", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[27]), first, "top_module.v", 3, 781, ".top_module", "v_branch/top_module", "if", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[28]), first, "top_module.v", 3, 782, ".top_module", "v_branch/top_module", "else", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[29]), first, "top_module.v", 3, 737, ".top_module", "v_line/top_module", "block", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[30]), first, "top_module.v", 3, 902, ".top_module", "v_branch/top_module", "if", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[31]), first, "top_module.v", 3, 903, ".top_module", "v_branch/top_module", "else", "");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[32]), first, "top_module.v", 3, 858, ".top_module", "v_branch/top_module", "if", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[33]), first, "top_module.v", 3, 859, ".top_module", "v_branch/top_module", "else", "3");
    vlSelf->__vlCoverInsert(&(vlSymsp->__Vcoverage[34]), first, "top_module.v", 3, 830, ".top_module", "v_line/top_module", "block", "3");
}
