import enum

import numpy as np
import pydantic
from more_itertools import all_equal

from classiq_interface.generator.complex_type import Complex
from classiq_interface.helpers.custom_pydantic_types import (
    pydanticPauliList,
    pydanticPauliMonomialStr,
)


class PauliOperator(pydantic.BaseModel):
    """
    Specification of a Pauli sum operator.
    """

    pauli_list: pydanticPauliList = pydantic.Field(
        description="A list of lists each containing a pauli string comprised of IXYZ characters and a complex coefficient.",
    )

    def show(self) -> str:
        if self.to_hermitian():
            return "\n".join(
                f"{summand[1].real:+.3f} * {summand[0]}" for summand in self.pauli_list
            )
        return "\n".join(
            f"+({summand[1]:+.3f}) * {summand[0]}" for summand in self.pauli_list
        )

    def to_hermitian(self) -> bool:
        if not all(
            np.isclose(complex(summand[1]).real, summand[1])
            for summand in self.pauli_list
        ):
            return False
        self.pauli_list = [
            [summand[0], complex(summand[1].real)] for summand in self.pauli_list
        ]
        return True

    @pydantic.validator("pauli_list", each_item=True)
    def validate_pauli_monomials(cls, monomial):
        parsed_monomial = PauliMonomial(string=monomial[0], coeff=monomial[1])
        return [parsed_monomial.string, parsed_monomial.coeff]

    @pydantic.validator("pauli_list")
    def validate_pauli_list(cls, pauli_list):
        if not all_equal(len(summand[0]) for summand in pauli_list):
            raise ValueError("Pauli strings have incompatible lengths.")
        return pauli_list


@pydantic.dataclasses.dataclass
class PauliMonomial:
    string: pydanticPauliMonomialStr
    coeff: Complex


class OperatorStatus(str, enum.Enum):
    SUCCESS = "success"
    ERROR = "error"


class OperatorResult(pydantic.BaseModel):
    status: OperatorStatus
    details: PauliOperator
