from __future__ import annotations

from typing import Tuple, List, Iterable, Optional, Dict, Union, Callable
from abc import ABC, abstractmethod
import math


def get_op(code: int):
    return {
        1: Add,
        2: Mult,
        3: Input,
        4: Output,
        5: JumpIfTrue,
        6: JumpIfFalse,
        7: LessThan,
        8: Equals,
        99: Halt
    }[code]


class Op(ABC):

    @staticmethod
    @abstractmethod
    def param_count():
        return 0

    def __init__(self, code: int, *params: Union[Tuple[int, int], int]):
        if len(params) != self.param_count():
            raise Exception("Invalid number of args (%d) for opcode '%d'." % (len(params), code))
        self.code = code
        self.params = [(x, 0) if type(x) == int else x for x in params]

    @abstractmethod
    def execute(self, state: Computer) -> Optional[int]:
        pass

    def param_val(self, num: int, state: Computer) -> int:
        param = self.params[num]
        return param[0] if param[1] == 1 else state.registers[param[0]]

    @staticmethod
    def parse(state: Computer) -> Op:
        full_code = state.registers[state.pos]
        opcode = full_code % 100
        op_class = get_op(opcode)
        param_count = op_class.param_count()
        params = [(
            p,
            math.floor(full_code / (10 ** (i + 2))) % 10
        ) for i, p in enumerate(state.registers[state.pos+1:state.pos+1+param_count])]

        return op_class(*params)


#


class Add(Op):

    @staticmethod
    def param_count():
        return 3

    def __init__(self, *params: Union[Tuple[int, int], int]):
        super(Add, self).__init__(1, *params)

    def execute(self, state: Computer) -> Optional[int]:
        val1 = self.param_val(0, state)
        val2 = self.param_val(1, state)
        state.registers[self.params[2][0]] = val1 + val2
        return 4

#


class Mult(Op):

    @staticmethod
    def param_count():
        return 3

    def __init__(self, *params: Union[Tuple[int, int], int]):
        super(Mult, self).__init__(2, *params)

    def execute(self, state: Computer) -> Optional[int]:
        val1 = self.param_val(0, state)
        val2 = self.param_val(1, state)
        state.registers[self.params[2][0]] = val1 * val2
        return 4
#


class Halt(Op):

    @staticmethod
    def param_count():
        return 0

    def __init__(self, *params: Union[Tuple[int, int], int]):
        super(Halt, self).__init__(99, *params)

    def execute(self, state: Computer) -> Optional[int]:
        return None

#


class Input(Op):

    @staticmethod
    def param_count():
        return 1

    def __init__(self, *params: Union[Tuple[int, int], int]):
        super(Input, self).__init__(3, *params)

    def execute(self, state: Computer) -> Optional[int]:
        state.registers[self.params[0][0]] = state.request_input()
        return 2

#


class Output(Op):

    @staticmethod
    def param_count():
        return 1

    def __init__(self, *params: Union[Tuple[int, int], int]):
        super(Output, self).__init__(4, *params)

    def execute(self, state: Computer) -> Optional[int]:
        state.output(state.registers[self.params[0][0]])
        return 2

#


class JumpIfTrue(Op):

    @staticmethod
    def param_count():
        return 2

    def __init__(self, *params: Union[Tuple[int, int], int]):
        super(JumpIfTrue, self).__init__(5, *params)

    def execute(self, state: Computer) -> Optional[int]:
        if self.param_val(0, state) != 0:
            return self.param_val(1, state) - state.pos
        return 3

#


class JumpIfFalse(Op):

    @staticmethod
    def param_count():
        return 2

    def __init__(self, *params: Union[Tuple[int, int], int]):
        super(JumpIfFalse, self).__init__(6, *params)

    def execute(self, state: Computer) -> Optional[int]:
        if self.param_val(0, state) == 0:
            return self.param_val(1, state) - state.pos
        return 3

#


class LessThan(Op):

    @staticmethod
    def param_count():
        return 3

    def __init__(self, *params: Union[Tuple[int, int], int]):
        super(LessThan, self).__init__(7, *params)

    def execute(self, state: Computer) -> Optional[int]:
        val = 1 if self.param_val(0, state) < self.param_val(1, state) else 0
        state.registers[self.params[2][0]] = val
        return 4

#


class Equals(Op):

    @staticmethod
    def param_count():
        return 3

    def __init__(self, *params: Union[Tuple[int, int], int]):
        super(Equals, self).__init__(8, *params)

    def execute(self, state: Computer) -> Optional[int]:
        val = 1 if self.param_val(0, state) == self.param_val(1, state) else 0
        state.registers[self.params[2][0]] = val
        return 4

#

#


class Computer:

    def __init__(self, registers: List[int], pos: int = 0, inputs: Optional[List[int]] = None):
        self.registers = registers
        self.pos = pos
        self.inputs = inputs if inputs else []
        self.outputs = []

    def request_input(self) -> int:
        if len(self.inputs) == 0:
            return int(input("?? "))
        else:
            return self.inputs.pop(0)

    def output(self, val: int):
        self.outputs.append(val)

    def next(self) -> bool:
        shift = Op.parse(self).execute(self)
        if shift is None:
            return False
        self.pos += shift
        if self.pos >= len(self.registers):
            raise Exception("Invalid state.")
        return True

    def run(self) -> List[int]:
        running = self.pos < len(self.registers)
        while running:
            running = self.next()
        return self.outputs

    def run_until_output(self) -> Optional[int]:
        """
        Operates similar to run(), but when it detects output having been generated, pauses the running
        of the computer and pops that output value from the output list and returns it.  If the computer halts
        rather than producing an output, returns None.
        """
        running = self.pos < len(self.registers)
        while running:
            if len(self.outputs) > 0:
                return self.outputs.pop(0)
            running = self.next()
        return None

    @classmethod
    def from_string(cls, s: str, inputs: Optional[List[int]] = None) -> Computer:
        return Computer(cls.parse_registers(s), inputs=inputs)

    @staticmethod
    def parse_registers(s: str) -> List[int]:
        return [int(x.strip()) for x in s.split(",")]
