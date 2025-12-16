// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vtop_module.h for the primary calling header

#ifndef VERILATED_VTOP_MODULE___024ROOT_H_
#define VERILATED_VTOP_MODULE___024ROOT_H_  // guard

#include "verilated.h"
#include "verilated_cov.h"


class Vtop_module__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vtop_module___024root final : public VerilatedModule {
  public:

    // DESIGN SPECIFIC STATE
    VL_IN8(clk,0,0);
    VL_IN8(areset,0,0);
    VL_IN8(bump_left,0,0);
    VL_IN8(bump_right,0,0);
    VL_IN8(ground,0,0);
    VL_IN8(dig,0,0);
    VL_OUT8(walk_left,0,0);
    VL_OUT8(walk_right,0,0);
    VL_OUT8(aaah,0,0);
    VL_OUT8(digging,0,0);
    CData/*2:0*/ top_module__DOT__state;
    CData/*2:0*/ top_module__DOT__next;
    CData/*4:0*/ top_module__DOT__fall_counter;
    CData/*0:0*/ __VstlFirstIteration;
    CData/*0:0*/ __VicoFirstIteration;
    CData/*0:0*/ __Vtrigprevexpr___TOP__areset__0;
    CData/*0:0*/ __Vtrigprevexpr___TOP__clk__0;
    CData/*0:0*/ __VactContinue;
    IData/*31:0*/ __VactIterCount;
    VlTriggerVec<1> __VstlTriggered;
    VlTriggerVec<1> __VicoTriggered;
    VlTriggerVec<2> __VactTriggered;
    VlTriggerVec<2> __VnbaTriggered;

    // INTERNAL VARIABLES
    Vtop_module__Syms* const vlSymsp;

    // CONSTRUCTORS
    Vtop_module___024root(Vtop_module__Syms* symsp, const char* v__name);
    ~Vtop_module___024root();
    VL_UNCOPYABLE(Vtop_module___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
    void __vlCoverInsert(uint32_t* countp, bool enable, const char* filenamep, int lineno, int column,
        const char* hierp, const char* pagep, const char* commentp, const char* linescovp);
};


#endif  // guard
