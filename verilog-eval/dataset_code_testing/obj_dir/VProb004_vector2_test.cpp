// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "VProb004_vector2_test__pch.h"

//============================================================
// Constructors

VProb004_vector2_test::VProb004_vector2_test(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new VProb004_vector2_test__Syms(contextp(), _vcname__, this)}
    , TestModuleI__02Eout{vlSymsp->TOP.TestModuleI__02Eout}
    , TestModuleIII__02Eout{vlSymsp->TOP.TestModuleIII__02Eout}
    , TestModuleI__02Ein{vlSymsp->TOP.TestModuleI__02Ein}
    , TestModuleII__02Ein{vlSymsp->TOP.TestModuleII__02Ein}
    , TestModuleII__02Eout{vlSymsp->TOP.TestModuleII__02Eout}
    , TestModuleIII__02Ein{vlSymsp->TOP.TestModuleIII__02Ein}
    , TestModuleIV__02Ein{vlSymsp->TOP.TestModuleIV__02Ein}
    , TestModuleIV__02Eout{vlSymsp->TOP.TestModuleIV__02Eout}
    , TestModuleV__02Eout{vlSymsp->TOP.TestModuleV__02Eout}
    , TestModuleV__02Ein{vlSymsp->TOP.TestModuleV__02Ein}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

VProb004_vector2_test::VProb004_vector2_test(const char* _vcname__)
    : VProb004_vector2_test(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

VProb004_vector2_test::~VProb004_vector2_test() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void VProb004_vector2_test___024root___eval_debug_assertions(VProb004_vector2_test___024root* vlSelf);
#endif  // VL_DEBUG
void VProb004_vector2_test___024root___eval_static(VProb004_vector2_test___024root* vlSelf);
void VProb004_vector2_test___024root___eval_initial(VProb004_vector2_test___024root* vlSelf);
void VProb004_vector2_test___024root___eval_settle(VProb004_vector2_test___024root* vlSelf);
void VProb004_vector2_test___024root___eval(VProb004_vector2_test___024root* vlSelf);

void VProb004_vector2_test::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate VProb004_vector2_test::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    VProb004_vector2_test___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        vlSymsp->__Vm_didInit = true;
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        VProb004_vector2_test___024root___eval_static(&(vlSymsp->TOP));
        VProb004_vector2_test___024root___eval_initial(&(vlSymsp->TOP));
        VProb004_vector2_test___024root___eval_settle(&(vlSymsp->TOP));
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    VProb004_vector2_test___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool VProb004_vector2_test::eventsPending() { return !vlSymsp->TOP.__VdlySched.empty(); }

uint64_t VProb004_vector2_test::nextTimeSlot() { return vlSymsp->TOP.__VdlySched.nextTimeSlot(); }

//============================================================
// Utilities

const char* VProb004_vector2_test::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void VProb004_vector2_test___024root___eval_final(VProb004_vector2_test___024root* vlSelf);

VL_ATTR_COLD void VProb004_vector2_test::final() {
    VProb004_vector2_test___024root___eval_final(&(vlSymsp->TOP));
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* VProb004_vector2_test::hierName() const { return vlSymsp->name(); }
const char* VProb004_vector2_test::modelName() const { return "VProb004_vector2_test"; }
unsigned VProb004_vector2_test::threads() const { return 1; }
void VProb004_vector2_test::prepareClone() const { contextp()->prepareClone(); }
void VProb004_vector2_test::atClone() const {
    contextp()->threadPoolpOnClone();
}
