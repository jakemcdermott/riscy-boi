"""Instruction decoder tests"""
import os

import nmigen.sim

from riscy_boi import alu
from riscy_boi import encoding
from riscy_boi import instruction_decoder


def test_decoding_addi():
    idec = instruction_decoder.InstructionDecoder()

    def testbench():
        immediate = 0b100011110000
        opcode = encoding.Opcode.OP_IMM
        funct = encoding.IntRegImmFunct.ADDI
        rs1 = 1
        rd = 2
        instruction = encoding.IType.encode(immediate, rs1, funct, rd, opcode)

        yield idec.instr.eq(instruction)
        yield nmigen.sim.Settle()
        assert (yield idec.pc_load) == 0
        assert (yield idec.rf_read_select_1) == rs1
        assert (yield idec.alu_op) == alu.ALUOp.ADD
        assert (yield idec.alu_imm) == 0b11111111111111111111100011110000

        assert (yield idec.rf_write_enable) == 1
        assert (yield idec.rf_write_select) == rd

    sim = nmigen.sim.Simulator(idec)
    sim.add_process(testbench)
    with sim.write_vcd(os.path.join("tests", "vcd", "idec-addi.vcd")):
        sim.run_until(100e-6)


def test_decoding_jal():
    idec = instruction_decoder.InstructionDecoder()

    def testbench():
        immediate = int("1" * 20, base=2)
        rd = 5
        instruction = encoding.JType.encode(immediate, rd)

        yield idec.instr.eq(instruction)
        yield nmigen.sim.Settle()
        assert (yield idec.pc_load) == 1
        assert (yield idec.alu_op) == alu.ALUOp.ADD
        assert (yield idec.alu_imm) == int("1" * 32, base=2)

    sim = nmigen.sim.Simulator(idec)
    sim.add_process(testbench)
    with sim.write_vcd(os.path.join("tests", "vcd", "idec-jal.vcd")):
        sim.run_until(100e-6)
