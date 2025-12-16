
#include "rfuzz-harness.h"
#include <vector>
#include <string>
#include <memory>
#include <iostream>
#include <verilated.h>
#include "Vtop_module.h"
#include <sstream>

int fuzz_poke() {
    int unpass = 0;
    VerilatedContext* contextp;
    Vtop_module* top;

    // Scenario: NormalWalking
    const std::unique_ptr<VerilatedContext> contextp_0 {new VerilatedContext};
    contextp = contextp_0.get();
    top = new Vtop_module;
    top->eval();
    // Scenario: FallingAndSplattering
    const std::unique_ptr<VerilatedContext> contextp_1 {new VerilatedContext};
    contextp = contextp_1.get();
    top = new Vtop_module;
    top->eval();
    // Scenario: DiggingAndFalling
    const std::unique_ptr<VerilatedContext> contextp_2 {new VerilatedContext};
    contextp = contextp_2.get();
    top = new Vtop_module;
    top->eval();
    // Scenario: SimultaneousBumps
    const std::unique_ptr<VerilatedContext> contextp_3 {new VerilatedContext};
    contextp = contextp_3.get();
    top = new Vtop_module;
    top->eval();
    // Scenario: RandomScenario0
    const std::unique_ptr<VerilatedContext> contextp_4 {new VerilatedContext};
    contextp = contextp_4.get();
    top = new Vtop_module;
    top->eval();
    // Scenario: RandomScenario1
    const std::unique_ptr<VerilatedContext> contextp_5 {new VerilatedContext};
    contextp = contextp_5.get();
    top = new Vtop_module;
    top->eval();
    // Scenario: RandomScenario2
    const std::unique_ptr<VerilatedContext> contextp_6 {new VerilatedContext};
    contextp = contextp_6.get();
    top = new Vtop_module;
    top->eval();
    // Scenario: RandomScenario3
    const std::unique_ptr<VerilatedContext> contextp_7 {new VerilatedContext};
    contextp = contextp_7.get();
    top = new Vtop_module;
    top->eval();
    // Scenario: RandomScenario4
    const std::unique_ptr<VerilatedContext> contextp_8 {new VerilatedContext};
    contextp = contextp_8.get();
    top = new Vtop_module;
    top->eval();
    // Scenario: RandomScenario5
    const std::unique_ptr<VerilatedContext> contextp_9 {new VerilatedContext};
    contextp = contextp_9.get();
    top = new Vtop_module;
    top->eval();
    // Scenario: RandomScenario6
    const std::unique_ptr<VerilatedContext> contextp_10 {new VerilatedContext};
    contextp = contextp_10.get();
    top = new Vtop_module;
    top->eval();
    // Scenario: RandomScenario7
    const std::unique_ptr<VerilatedContext> contextp_11 {new VerilatedContext};
    contextp = contextp_11.get();
    top = new Vtop_module;
    top->eval();
    // Scenario: RandomScenario8
    const std::unique_ptr<VerilatedContext> contextp_12 {new VerilatedContext};
    contextp = contextp_12.get();
    top = new Vtop_module;
    top->eval();
    // Scenario: RandomScenario9
    const std::unique_ptr<VerilatedContext> contextp_13 {new VerilatedContext};
    contextp = contextp_13.get();
    top = new Vtop_module;
    top->eval();

    if (unpass == 0) {
        std::cout << "All tests passed!" << std::endl;
    } else {
        std::cout << "Found " << unpass << " mismatches." << std::endl;
    }
    return unpass;
}
