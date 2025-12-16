// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See VProb004_vector2_test.h for the primary calling header

#ifndef VERILATED_VPROB004_VECTOR2_TEST___024ROOT_H_
#define VERILATED_VPROB004_VECTOR2_TEST___024ROOT_H_  // guard

#include "verilated.h"
#include "verilated_timing.h"


class VProb004_vector2_test__Syms;

class alignas(VL_CACHE_LINE_BYTES) VProb004_vector2_test___024root final : public VerilatedModule {
  public:

    // DESIGN SPECIFIC STATE
    CData/*0:0*/ tb__DOT__clk;
    VL_OUT8(TestModuleI__02Eout,32,31);
    VL_OUT8(TestModuleIII__02Eout,32,31);
    CData/*0:0*/ __VstlFirstIteration;
    CData/*0:0*/ __VicoFirstIteration;
    CData/*0:0*/ __Vtrigprevexpr___TOP__tb__DOT__clk__0;
    CData/*0:0*/ __VactContinue;
    VL_IN(TestModuleI__02Ein,31,0);
    VL_IN(TestModuleII__02Ein,31,0);
    VL_OUT(TestModuleII__02Eout,31,0);
    VL_IN(TestModuleIII__02Ein,31,0);
    VL_IN(TestModuleIV__02Ein,31,0);
    VL_OUT(TestModuleIV__02Eout,31,0);
    VL_OUT(TestModuleV__02Eout,31,0);
    IData/*31:0*/ tb__DOT__stats1__BRA__159__03a128__KET__;
    IData/*31:0*/ tb__DOT__stats1__BRA__95__03a64__KET__;
    IData/*31:0*/ tb__DOT__stats1__BRA__63__03a32__KET__;
    IData/*31:0*/ tb__DOT__stats1__BRA__31__03a0__KET__;
    IData/*31:0*/ tb__DOT__in;
    IData/*31:0*/ tb__DOT__out_ref;
    IData/*31:0*/ tb__DOT__out_dut;
    IData/*31:0*/ __VactIterCount;
    VL_IN64(TestModuleV__02Ein,32,0);
    VlDelayScheduler __VdlySched;
    VlTriggerScheduler __VtrigSched_h4e77a109__0;
    VlTriggerVec<1> __VstlTriggered;
    VlTriggerVec<1> __VicoTriggered;
    VlTriggerVec<2> __VactTriggered;
    VlTriggerVec<2> __VnbaTriggered;

    // INTERNAL VARIABLES
    VProb004_vector2_test__Syms* const vlSymsp;

    // CONSTRUCTORS
    VProb004_vector2_test___024root(VProb004_vector2_test__Syms* symsp, const char* v__name);
    ~VProb004_vector2_test___024root();
    VL_UNCOPYABLE(VProb004_vector2_test___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
