from typing import List, Optional

import pydantic

from classiq_interface.generator.function_params import FunctionParams

CTRL_IN = "CTRL_IN"
TARGET_QUBIT_IN = "TARGET_QUBIT"
CTRL_OUT = "CTRL_OUT"
TARGET_QUBIT_OUT = "TARGET_QUBIT_OUT"


class Mcx(FunctionParams):
    """
    multi-controlled x-gate
    """

    num_ctrl_qubits: pydantic.PositiveInt = pydantic.Field(
        description="The number of control qubits."
    )
    ctrl_state: Optional[str] = pydantic.Field(
        default=None, description="string of the control state"
    )

    @pydantic.validator("ctrl_state", always=True)
    def validate_ctrl_state(cls, ctrl_state, values):
        num_ctrl_qubits = values.get("num_ctrl_qubits")
        if ctrl_state is None:
            return "1" * num_ctrl_qubits

        if len(ctrl_state) != num_ctrl_qubits:
            raise ValueError(
                "control state length should be equal to the number of control qubits"
            )
        return ctrl_state

    _input_names: List[str] = pydantic.PrivateAttr(default=[CTRL_IN, TARGET_QUBIT_IN])
    _output_names: List[str] = pydantic.PrivateAttr(
        default=[CTRL_OUT, TARGET_QUBIT_OUT]
    )
