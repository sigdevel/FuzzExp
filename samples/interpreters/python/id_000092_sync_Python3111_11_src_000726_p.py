import logging
import uuid

import pytest
import sympy
from numpy.testing import assert_array_equal, assert_equal

from brian2 import *
from brian2.codegen.generators import NumpyCodeGenerator
from brian2.codegen.permutation_analysis import (
    OrderDependenceError,
    check_for_order_independence,
)
from brian2.codegen.translation import make_statements
from brian2.core.functions import DEFAULT_FUNCTIONS
from brian2.core.network import schedule_propagation_offset
from brian2.core.variables import ArrayVariable, Constant, variables_by_owner
from brian2.devices.cpp_standalone.device import CPPStandaloneDevice
from brian2.devices.device import all_devices, get_device, reinit_and_delete
from brian2.equations.equations import EquationError
from brian2.stateupdaters.base import UnsupportedEquationsException
from brian2.synapses.parse_synaptic_generator_syntax import parse_synapse_generator
from brian2.tests.utils import assert_allclose, exc_isinstance
from brian2.utils.logger import catch_logs
from brian2.utils.stringtools import deindent, get_identifiers, indent, word_substitute


def _compare(synapses, expected):
    conn_matrix = np.zeros((len(synapses.source), len(synapses.target)), dtype=np.int32)
    for _i, _j in zip(synapses.i[:], synapses.j[:]):
        conn_matrix[_i, _j] += 1

    assert_equal(conn_matrix, expected)
    
    incoming = conn_matrix.sum(axis=0)
    outgoing = conn_matrix.sum(axis=1)
    assert all(
        synapses.N_outgoing[:] == outgoing[synapses.i[:]]
    ), "N_outgoing returned an incorrect value"
    assert_array_equal(
        synapses.N_outgoing_pre, outgoing
    ), "N_outgoing_pre returned an incorrect value"
    assert all(
        synapses.N_incoming[:] == incoming[synapses.j[:]]
    ), "N_incoming returned an incorrect value"
    assert_array_equal(
        synapses.N_incoming_post, incoming
    ), "N_incoming_post returned an incorrect value"

    "synapse number" if it exists
    if synapses.multisynaptic_index is not None:
        
        
        synapse_numbers = np.zeros_like(synapses.i[:])
        numbers = {}
        for _i, (source, target) in enumerate(zip(synapses.i[:], synapses.j[:])):
            number = numbers.get((source, target), 0)
            synapse_numbers[_i] = number
            numbers[(source, target)] = number + 1
        assert all(
            synapses.state(synapses.multisynaptic_index)[:] == synapse_numbers
        ), "synapse_number returned an incorrect value"


@pytest.mark.codegen_independent
def test_creation():
    """
    A basic test that creating a Synapses object works.
    """
    G = NeuronGroup(42, "v: 1", threshold="False")
    S = Synapses(G, G, "w:1", on_pre="v+=w")
    
    assert S.source.name == S.target.name == G.name
    assert len(S) == 0
    S = Synapses(G, model="w:1", on_pre="v+=w")
    assert S.source.name == S.target.name == G.name


@pytest.mark.codegen_independent
def test_creation_errors():
    G = NeuronGroup(42, "v: 1", threshold="False")
    
    with pytest.raises(TypeError):
        Synapses(G, G, "w:1", on_pre="v+=w", connect=True)
    
    
    with pytest.raises(TypeError):
        Synapses(G, G, "w:1", pre="v+=w", on_pre="v+=w", connect=True)
    with pytest.raises(TypeError):
        Synapses(G, G, "w:1", post="v+=w", on_post="v+=w", connect=True)


@pytest.mark.codegen_independent
def test_connect_errors():
    G = NeuronGroup(42, "")
    S = Synapses(G, G)

    
    with pytest.raises(TypeError):
        S.connect("i*2")

    
    with pytest.raises(DimensionMismatchError):
        S.connect("i > 3*mV")

    
    with pytest.raises(SyntaxError):
        S.connect("sin(3, 4) > 1")

    
    with pytest.raises(TypeError):
        S.connect("1*mV")

    
    with pytest.raises(SyntaxError):
        S.connect(p="sin(3, 4)")


@pytest.mark.codegen_independent
def test_name_clashes():
    
    
    G1 = NeuronGroup(1, "a : 1")
    G2 = NeuronGroup(1, "b : 1")
    with pytest.raises(ValueError):
        Synapses(G1, G2, "a : 1")
    with pytest.raises(ValueError):
        Synapses(G1, G2, "b : 1")

    
    
    with pytest.raises(ValueError):
        Synapses(G1, G2, "x_pre : 1")
    with pytest.raises(ValueError):
        Synapses(G1, G2, "x_post : 1")
    with pytest.raises(ValueError):
        Synapses(G1, G2, "x_pre = 1 : 1")
    with pytest.raises(ValueError):
        Synapses(G1, G2, "x_post = 1 : 1")
    with pytest.raises(ValueError):
        NeuronGroup(1, "x_pre : 1")
    with pytest.raises(ValueError):
        NeuronGroup(1, "x_post : 1")
    with pytest.raises(ValueError):
        NeuronGroup(1, "x_pre = 1 : 1")
    with pytest.raises(ValueError):
        NeuronGroup(1, "x_post = 1 : 1")

    
    Synapses(G1, G2, "c : 1")
    Synapses(G1, G2, "a_syn : 1")
    Synapses(G1, G2, "b_syn : 1")


@pytest.mark.standalone_compatible
def test_incoming_outgoing():
    """
    Test the count of outgoing/incoming synapses per neuron.
    (It will be also automatically tested for all connection patterns that
    use the above _compare function for testing)
    """
    G1 = NeuronGroup(5, "")
    G2 = NeuronGroup(5, "")
    S = Synapses(G1, G2, "")
    S.connect(i=[0, 0, 0, 1, 1, 2], j=[0, 1, 2, 1, 2, 3])
    run(0 * ms)  
    
    assert all(S.N_outgoing[0, :] == 3)
    assert all(S.N_outgoing[1, :] == 2)
    assert all(S.N_outgoing[2, :] == 1)
    assert all(S.N_outgoing[3:, :] == 0)
    assert_array_equal(S.N_outgoing_pre, [3, 2, 1, 0, 0])
    
    assert all(S.N_incoming[:, 0] == 1)
    assert all(S.N_incoming[:, 1] == 2)
    assert all(S.N_incoming[:, 2] == 2)
    assert all(S.N_incoming[:, 3] == 1)
    assert all(S.N_incoming[:, 4:] == 0)
    assert_array_equal(S.N_incoming_post, [1, 2, 2, 1, 0])


@pytest.mark.standalone_compatible
def test_connection_arrays():
    """
    Test connecting synapses with explictly given arrays
    """
    G = NeuronGroup(42, "")
    G2 = NeuronGroup(17, "")

    
    expected1 = np.eye(len(G2))
    S1 = Synapses(G2)
    S1.connect(i=np.arange(len(G2)), j=np.arange(len(G2)))

    
    expected2 = np.ones((len(G), len(G2)))
    S2 = Synapses(G, G2)
    X, Y = np.meshgrid(np.arange(len(G)), np.arange(len(G2)))
    S2.connect(i=X.flatten(), j=Y.flatten())

    
    expected3 = np.zeros((len(G), len(G2)))
    expected3[3, 3] = 2
    S3 = Synapses(G, G2)
    S3.connect(i=[3, 3], j=[3, 3])

    run(0 * ms)  
    _compare(S1, expected1)
    _compare(S2, expected2)
    _compare(S3, expected3)

    
    S = Synapses(G, G2)
    with pytest.raises(TypeError):
        S.connect(i=[1.1, 2.2], j=[1.1, 2.2])
    with pytest.raises(TypeError):
        S.connect(i=[1, 2], j="string")
    with pytest.raises(TypeError):
        S.connect(i=[1, 2], j=[1, 2], n="i")
    with pytest.raises(TypeError):
        S.connect([1, 2])
    with pytest.raises(ValueError):
        S.connect(i=[1, 2, 3], j=[1, 2])
    with pytest.raises(ValueError):
        S.connect(i=np.ones((3, 3), dtype=np.int32), j=np.ones((3, 1), dtype=np.int32))
    with pytest.raises(IndexError):
        S.connect(i=[41, 42], j=[0, 1])  
    with pytest.raises(IndexError):
        S.connect(i=[0, 1], j=[16, 17])  
    with pytest.raises(IndexError):
        S.connect(i=[0, -1], j=[0, 1])  
    with pytest.raises(IndexError):
        S.connect(i=[0, 1], j=[0, -1])  
    with pytest.raises(ValueError):
        S.connect("i==j", j=np.arange(10))
    with pytest.raises(TypeError):
        S.connect("i==j", n=object())
    with pytest.raises(TypeError):
        S.connect("i==j", p=object())
    with pytest.raises(TypeError):
        S.connect(object())


@pytest.mark.standalone_compatible
def test_connection_string_deterministic_full():
    G = NeuronGroup(17, "")
    G2 = NeuronGroup(4, "")

    
    expected_full = np.ones((len(G), len(G2)))

    S1 = Synapses(G, G2, "")
    S1.connect(True)

    S2 = Synapses(G, G2, "")
    S2.connect("True")

    run(0 * ms)  

    _compare(S1, expected_full)
    _compare(S2, expected_full)


@pytest.mark.standalone_compatible
def test_connection_string_deterministic_full_no_self():
    G = NeuronGroup(17, "v : 1")
    G.v = "i"
    G2 = NeuronGroup(4, "v : 1")
    G2.v = "17 + i"

    
    expected_no_self = np.ones((len(G), len(G))) - np.eye(len(G))

    S1 = Synapses(G, G)
    S1.connect("i != j")

    S2 = Synapses(G, G)
    S2.connect("v_pre != v_post")

    S3 = Synapses(G, G)
    S3.connect(condition="i != j")

    run(0 * ms)  

    _compare(S1, expected_no_self)
    _compare(S2, expected_no_self)
    _compare(S3, expected_no_self)


@pytest.mark.standalone_compatible
def test_connection_string_deterministic_full_one_to_one():
    G = NeuronGroup(17, "v : 1")
    G.v = "i"
    G2 = NeuronGroup(4, "v : 1")
    G2.v = "17 + i"

    
    expected_one_to_one = np.eye(len(G))

    S1 = Synapses(G, G)
    S1.connect("i == j")

    S2 = Synapses(G, G)
    S2.connect("v_pre == v_post")

    S3 = Synapses(
        G,
        G,
        """
        sub_1 = v_pre : 1
        sub_2 = v_post : 1
        w:1
        """,
    )
    S3.connect("sub_1 == sub_2")

    S4 = Synapses(G, G)
    S4.connect(j="i")

    run(0 * ms)  

    _compare(S1, expected_one_to_one)
    _compare(S2, expected_one_to_one)
    _compare(S3, expected_one_to_one)
    _compare(S4, expected_one_to_one)


@pytest.mark.standalone_compatible
def test_connection_string_deterministic_full_custom():
    G = NeuronGroup(17, "")
    G2 = NeuronGroup(4, "")
    
    number = 2
    expected_custom = np.ones((len(G), len(G)))
    expected_custom[:number, :number] = 0
    S1 = Synapses(G, G)
    S1.connect("(i >= number) or (j >= number)")

    S2 = Synapses(G, G)
    S2.connect(
        "(i >= explicit_number) or (j >= explicit_number)",
        namespace={"explicit_number": number},
    )

    
    with pytest.raises(ValueError):
        S2.connect("k for k in range(1)")

    
    if get_device() == all_devices["runtime"]:
        with pytest.raises(BrianObjectException) as exc:
            S2.connect(j="20")
        assert exc_isinstance(exc, IndexError)

    run(0 * ms)  

    _compare(S1, expected_custom)
    _compare(S2, expected_custom)


@pytest.mark.standalone_compatible
def test_connection_string_deterministic_multiple_and():
    
    
    group = NeuronGroup(10, "")
    synapses = Synapses(group, group)
    synapses.connect("i>=5 and i<10 and j>=5")
    run(0 * ms)  
    assert len(synapses) == 25


@pytest.mark.standalone_compatible
def test_connection_random_with_condition():
    G = NeuronGroup(4, "")

    S1 = Synapses(G, G)
    S1.connect("i!=j", p=0.0)

    S2 = Synapses(G, G)
    S2.connect("i!=j", p=1.0)
    expected2 = np.ones((len(G), len(G))) - np.eye(len(G))

    S3 = Synapses(G, G)
    S3.connect("i>=2", p=0.0)

    S4 = Synapses(G, G)
    S4.connect("i>=2", p=1.0)
    expected4 = np.zeros((len(G), len(G)))
    expected4[2, :] = 1
    expected4[3, :] = 1

    S5 = Synapses(G, G)
    S5.connect("j<2", p=0.0)
    S6 = Synapses(G, G)
    S6.connect("j<2", p=1.0)
    expected6 = np.zeros((len(G), len(G)))
    expected6[:, 0] = 1
    expected6[:, 1] = 1

    with catch_logs() as _:  
        run(0 * ms)  

    assert len(S1) == 0
    _compare(S2, expected2)
    assert len(S3) == 0
    _compare(S4, expected4)
    assert len(S5) == 0
    _compare(S6, expected6)


@pytest.mark.standalone_compatible
@pytest.mark.long
def test_connection_random_with_condition_2():
    G = NeuronGroup(4, "")

    
    
    S7 = Synapses(G, G)
    S7.connect("i!=j", p=0.01)

    S8 = Synapses(G, G)
    S8.connect("i!=j", p=0.03)

    S9 = Synapses(G, G)
    S9.connect("i!=j", p=0.3)

    S10 = Synapses(G, G)
    S10.connect("i>=2", p=0.01)

    S11 = Synapses(G, G)
    S11.connect("i>=2", p=0.03)

    S12 = Synapses(G, G)
    S12.connect("i>=2", p=0.3)

    S13 = Synapses(G, G)
    S13.connect("j>=2", p=0.01)

    S14 = Synapses(G, G)
    S14.connect("j>=2", p=0.03)

    S15 = Synapses(G, G)
    S15.connect("j>=2", p=0.3)

    S16 = Synapses(G, G)
    S16.connect("i!=j", p="i*0.1")

    S17 = Synapses(G, G)
    S17.connect("i!=j", p="j*0.1")

    "jump algorithm"
    big_group = NeuronGroup(10000, "")
    S18 = Synapses(big_group, big_group)
    S18.connect("i != j", p=0.001)

    
    S19 = Synapses(big_group, big_group)
    S19.connect("i < int(N_post*0.5)", p=0.001)

    with catch_logs() as _:  
        run(0 * ms)  

    assert not any(S7.i == S7.j)
    assert not any(S8.i == S8.j)
    assert not any(S9.i == S9.j)
    assert all(S10.i >= 2)
    assert all(S11.i >= 2)
    assert all(S12.i >= 2)
    assert all(S13.j >= 2)
    assert all(S14.j >= 2)
    assert all(S15.j >= 2)
    assert not any(S16.i == 0)
    assert not any(S17.j == 0)


@pytest.mark.standalone_compatible
def test_connection_random_with_indices():
    """
    Test random connections.
    """
    G = NeuronGroup(4, "")
    G2 = NeuronGroup(7, "")

    S1 = Synapses(G, G2)
    S1.connect(i=0, j=0, p=0.0)
    expected1 = np.zeros((len(G), len(G2)))

    S2 = Synapses(G, G2)
    S2.connect(i=0, j=0, p=1.0)
    expected2 = np.zeros((len(G), len(G2)))
    expected2[0, 0] = 1

    S3 = Synapses(G, G2)
    S3.connect(i=[0, 1], j=[0, 2], p=1.0)
    expected3 = np.zeros((len(G), len(G2)))
    expected3[0, 0] = 1
    expected3[1, 2] = 1

    
    S4 = Synapses(G, G)
    S4.connect(i=0, j=0, p=0.01)
    S5 = Synapses(G, G)
    S5.connect(i=[0, 1], j=[0, 2], p=0.01)

    S6 = Synapses(G, G)
    S6.connect(i=0, j=0, p=0.03)

    S7 = Synapses(G, G)
    S7.connect(i=[0, 1], j=[0, 2], p=0.03)

    S8 = Synapses(G, G)
    S8.connect(i=0, j=0, p=0.3)

    S9 = Synapses(G, G)
    S9.connect(i=[0, 1], j=[0, 2], p=0.3)

    with catch_logs() as _:  
        run(0 * ms)  

    _compare(S1, expected1)
    _compare(S2, expected2)
    _compare(S3, expected3)
    assert 0 <= len(S4) <= 1
    assert 0 <= len(S5) <= 2
    assert 0 <= len(S6) <= 1
    assert 0 <= len(S7) <= 2
    assert 0 <= len(S8) <= 1
    assert 0 <= len(S9) <= 2


@pytest.mark.standalone_compatible
def test_connection_random_without_condition():
    G = NeuronGroup(
        4,
        """
        v: 1
        x : integer
        """,
    )
    G.x = "i"
    G2 = NeuronGroup(
        7,
        """
        v: 1
        y : 1
        """,
    )
    G2.y = "1.0*i/N"

    S1 = Synapses(G, G2)
    S1.connect(True, p=0.0)

    S2 = Synapses(G, G2)
    S2.connect(True, p=1.0)

    
    S3 = Synapses(G, G2)
    S3.connect(True, p=0.3)

    "stochastic" connections that are
    
    S4 = Synapses(G, G2)
    S4.connect(True, p="int(x_pre==2)*1.0")

    "stochastic" connections that are
    
    S5 = Synapses(G, G2)
    S5.connect(True, p="int(x_pre==2 and y_post > 0.5)*1.0")

    with catch_logs() as _:  
        run(0 * ms)  

    _compare(S1, np.zeros((len(G), len(G2))))
    _compare(S2, np.ones((len(G), len(G2))))
    assert 0 <= len(S3) <= len(G) * len(G2)
    assert len(S4) == 7
    assert_equal(S4.i, np.ones(7) * 2)
    assert_equal(S4.j, np.arange(7))
    assert len(S5) == 3
    assert_equal(S5.i, np.ones(3) * 2)
    assert_equal(S5.j, np.arange(3) + 4)


@pytest.mark.standalone_compatible
def test_connection_multiple_synapses():
    """
    Test multiple synapses per connection.
    """
    G = NeuronGroup(42, "v: 1")
    G.v = "i"
    G2 = NeuronGroup(17, "v: 1")
    G2.v = "i"

    S1 = Synapses(G, G2)
    S1.connect(True, n=0)

    S2 = Synapses(G, G2)
    S2.connect(True, n=2)

    S3 = Synapses(G, G2)
    S3.connect(True, n="j")

    S4 = Synapses(G, G2)
    S4.connect(True, n="i")

    S5 = Synapses(G, G2)
    S5.connect(True, n="int(i>j)*2")

    S6 = Synapses(G, G2)
    S6.connect(True, n="int(v_pre>v_post)*2")

    with catch_logs() as _:  
        run(0 * ms)  

    assert len(S1) == 0
    _compare(S2, 2 * np.ones((len(G), len(G2))))
    _compare(S3, np.arange(len(G2)).reshape(1, len(G2)).repeat(len(G), axis=0))

    _compare(S4, np.arange(len(G)).reshape(len(G), 1).repeat(len(G2), axis=1))
    expected = np.zeros((len(G), len(G2)), dtype=np.int32)
    for source in range(len(G)):
        expected[source, :source] = 2
    _compare(S5, expected)
    _compare(S6, expected)


def test_state_variable_assignment():
    """
    Assign values to state variables in various ways
    """

    G = NeuronGroup(10, "v: volt")
    G.v = "i*mV"
    S = Synapses(G, G, "w:volt")
    S.connect(True)

    
    assignment_expected = [
        (5 * mV, np.ones(100) * 5 * mV),
        (7 * mV, np.ones(100) * 7 * mV),
        (S.i[:] * mV, S.i[:] * np.ones(100) * mV),
        ("5*mV", np.ones(100) * 5 * mV),
        ("i*mV", np.ones(100) * S.i[:] * mV),
        ("i*mV +j*mV", S.i[:] * mV + S.j[:] * mV),
        
        ("v_pre", S.i[:] * mV),
        ("v_post", S.j[:] * mV),
        
    ]

    for assignment, expected in assignment_expected:
        S.w = 0 * volt
        S.w = assignment
        assert_allclose(
            S.w[:], expected, err_msg="Assigning %r gave incorrect result" % assignment
        )
        S.w = 0 * volt
        S.w[:] = assignment
        assert_allclose(
            S.w[:], expected, err_msg="Assigning %r gave incorrect result" % assignment
        )

    
    assignment_expected = [
        (5, np.ones(100) * 5 * volt),
        (7, np.ones(100) * 7 * volt),
        (S.i[:], S.i[:] * np.ones(100) * volt),
        ("5", np.ones(100) * 5 * volt),
        ("i", np.ones(100) * S.i[:] * volt),
        ("i +j", S.i[:] * volt + S.j[:] * volt),
        
    ]

    for assignment, expected in assignment_expected:
        S.w = 0 * volt
        S.w_ = assignment
        assert_allclose(
            S.w[:], expected, err_msg="Assigning %r gave incorrect result" % assignment
        )
        S.w = 0 * volt
        S.w_[:] = assignment
        assert_allclose(
            S.w[:], expected, err_msg="Assigning %r gave incorrect result" % assignment
        )


def test_state_variable_indexing():
    G1 = NeuronGroup(5, "v:volt")
    G1.v = "i*mV"
    G2 = NeuronGroup(7, "v:volt")
    G2.v = "10*mV + i*mV"
    S = Synapses(G1, G2, "w:1", multisynaptic_index="k")
    S.connect(True, n=2)
    S.w[:, :, 0] = "5*i + j"
    S.w[:, :, 1] = "35 + 5*i + j"

    
    assert len(S.w[:]) == len(S.w[:, :]) == len(S.w[:, :, :]) == len(G1) * len(G2) * 2
    assert len(S.w[0:, 0:]) == len(S.w[0:, 0:, 0:]) == len(G1) * len(G2) * 2
    assert len(S.w[0::2, 0:]) == 3 * len(G2) * 2
    assert len(S.w[0, :]) == len(S.w[0, :, :]) == len(G2) * 2
    assert len(S.w[0:2, :]) == len(S.w[0:2, :, :]) == 2 * len(G2) * 2
    assert len(S.w[:2, :]) == len(S.w[:2, :, :]) == 2 * len(G2) * 2
    assert len(S.w[0:4:2, :]) == len(S.w[0:4:2, :, :]) == 2 * len(G2) * 2
    assert len(S.w[:4:2, :]) == len(S.w[:4:2, :, :]) == 2 * len(G2) * 2
    assert len(S.w[:, 0]) == len(S.w[:, 0, :]) == len(G1) * 2
    assert len(S.w[:, 0:2]) == len(S.w[:, 0:2, :]) == 2 * len(G1) * 2
    assert len(S.w[:, :2]) == len(S.w[:, :2, :]) == 2 * len(G1) * 2
    assert len(S.w[:, 0:4:2]) == len(S.w[:, 0:4:2, :]) == 2 * len(G1) * 2
    assert len(S.w[:, :4:2]) == len(S.w[:, :4:2, :]) == 2 * len(G1) * 2
    assert len(S.w[:, :, 0]) == len(G1) * len(G2)
    assert len(S.w[:, :, 0:2]) == len(G1) * len(G2) * 2
    assert len(S.w[:, :, :2]) == len(G1) * len(G2) * 2
    assert len(S.w[:, :, 0:2:2]) == len(G1) * len(G2)
    assert len(S.w[:, :, :2:2]) == len(G1) * len(G2)

    
    assert len(S.w[:]) == len(S.w[0:])
    assert len(S.w[[0, 1]]) == len(S.w[3:5]) == 2
    assert len(S.w[:]) == len(S.w[np.arange(len(G1) * len(G2) * 2)])
    assert S.w[3] == S.w[np.int32(3)] == S.w[np.int64(3)]  

    
    assert_equal(S.w[:, 0:3], S.w[:, [0, 1, 2]])
    assert_equal(S.w[:, 0:3], S.w[np.arange(len(G1)), [0, 1, 2]])

    
    assert_equal(S.w[0:3, :], S.w["i<3"])
    assert_equal(S.w[:, 0:3], S.w["j<3"])
    assert_equal(S.w[:, :, 0], S.w["k == 0"])
    assert_equal(S.w[0:3, :], S.w["v_pre < 2.5*mV"])
    assert_equal(S.w[:, 0:3], S.w["v_post < 12.5*mV"])

    
    with pytest.raises(IndexError):
        S.w.__getitem__((1, 2, 3, 4))
    with pytest.raises(IndexError):
        S.w.__getitem__(object())
    with pytest.raises(IndexError):
        S.w.__getitem__(1.5)


def test_indices():
    G = NeuronGroup(10, "v : 1")
    S = Synapses(G, G, "")
    S.connect()
    G.v = "i"

    assert_equal(S.indices[:], np.arange(10 * 10))
    assert len(S.indices[5, :]) == 10
    assert_equal(S.indices["v_pre >=5"], S.indices[5:, :])
    assert_equal(S.indices["j >=5"], S.indices[:, 5:])


def test_subexpression_references():
    """
    Assure that subexpressions in targeted groups are handled correctly.
    """
    G = NeuronGroup(
        10,
        """
        v : 1
        v2 = 2*v : 1
        """,
    )
    G.v = np.arange(10)
    S = Synapses(
        G,
        G,
        """
        w : 1
        u = v2_post + 1 : 1
        x = v2_pre + 1 : 1
        """,
    )
    S.connect("i==(10-1-j)")
    assert_equal(S.u[:], np.arange(10)[::-1] * 2 + 1)
    assert_equal(S.x[:], np.arange(10) * 2 + 1)


@pytest.mark.standalone_compatible
def test_constant_variable_subexpression_in_synapses():
    G = NeuronGroup(10, "")
    S = Synapses(
        G,
        G,
        """
        dv1/dt = -v1**2 / (10*ms) : 1 (clock-driven)
        dv2/dt = -v_const**2 / (10*ms) : 1 (clock-driven)
        dv3/dt = -v_var**2 / (10*ms) : 1 (clock-driven)
        dv4/dt = -v_noflag**2 / (10*ms) : 1 (clock-driven)
        v_const = v2 : 1 (constant over dt)
        v_var = v3 : 1
        v_noflag = v4 : 1
        """,
        method="rk2",
    )
    S.connect(j="i")
    S.v1 = "1.0*i/N"
    S.v2 = "1.0*i/N"
    S.v3 = "1.0*i/N"
    S.v4 = "1.0*i/N"

    run(10 * ms)
    "variable over dt" subexpressions are directly inserted into the equation
    assert_allclose(S.v3[:], S.v1[:])
    assert_allclose(S.v4[:], S.v1[:])
    "constant over dt" subexpressions will keep a fixed value over the time
    
    
    assert np.sum((S.v2 - S.v1) ** 2) > 1e-10


@pytest.mark.standalone_compatible
def test_nested_subexpression_references():
    """
    Assure that subexpressions in targeted groups are handled correctly.
    """
    G = NeuronGroup(
        10,
        """
        v : 1
        v2 = 2*v : 1
        v3 = 1.5*v2 : 1
        """,
        threshold="v>=5",
    )
    G2 = NeuronGroup(10, "v : 1")
    G.v = np.arange(10)
    S = Synapses(G, G2, on_pre="v_post += v3_pre")
    S.connect(j="i")
    run(defaultclock.dt)
    assert_allclose(G2.v[:5], 0.0)
    assert_allclose(G2.v[5:], (5 + np.arange(5)) * 3)


@pytest.mark.codegen_independent
def test_equations_unit_check():
    group = NeuronGroup(1, "v : volt", threshold="True")
    syn = Synapses(
        group,
        group,
        """
        sub1 = 3 : 1
        sub2 = sub1 + 1*mV : volt
        """,
        on_pre="v += sub2",
    )
    syn.connect()
    net = Network(group, syn)
    with pytest.raises(BrianObjectException) as exc:
        net.run(0 * ms)
    assert exc_isinstance(exc, DimensionMismatchError)


def test_delay_specification():
    
    
    G = NeuronGroup(10, "x : meter", threshold="False")
    G.x = "i*mmeter"
    
    S = Synapses(G, G, "w:1", on_pre="v+=w")
    S.connect(j="i")
    assert len(S.delay[:]) == len(G)
    S.delay = "i*ms"
    assert_allclose(S.delay[:], np.arange(len(G)) * ms)
    velocity = 1 * meter / second
    S.delay = "abs(x_pre - (N_post-j)*mmeter)/velocity"
    assert_allclose(S.delay[:], abs(G.x - (10 - G.i) * mmeter) / velocity)
    S.delay = 5 * ms
    assert_allclose(S.delay[:], np.ones(len(G)) * 5 * ms)
    
    S.delay_ = float(7 * ms)
    assert_allclose(S.delay[:], np.ones(len(G)) * 7 * ms)

    
    S = Synapses(G, G, "w:1", on_pre="v+=w", delay=5 * ms)
    assert_allclose(S.delay[:], 5 * ms)
    S.connect(j="i")
    S.delay = "3*ms"
    assert_allclose(S.delay[:], 3 * ms)
    S.delay = 10 * ms
    assert_allclose(S.delay[:], 10 * ms)
    
    S.delay_ = float(20 * ms)
    assert_allclose(S.delay[:], 20 * ms)

    
    with pytest.raises(DimensionMismatchError):
        Synapses(G, G, "w:1", on_pre="v+=w", delay=5 * mV)
    with pytest.raises(TypeError):
        Synapses(G, G, "w:1", on_pre="v+=w", delay=object())
    with pytest.raises(ValueError):
        Synapses(G, G, "w:1", delay=5 * ms)
    with pytest.raises(ValueError):
        Synapses(G, G, "w:1", on_pre="v+=w", delay={"post": 5 * ms})


def test_delays_pathways():
    G = NeuronGroup(10, "x: meter", threshold="False")
    G.x = "i*mmeter"
    
    S = Synapses(G, G, "w:1", on_pre={"pre1": "v+=w", "pre2": "v+=w"}, on_post="v-=w")
    S.connect(j="i")
    assert len(S.pre1.delay[:]) == len(G)
    assert len(S.pre2.delay[:]) == len(G)
    assert len(S.post.delay[:]) == len(G)
    S.pre1.delay = "i*ms"
    S.pre2.delay = "j*ms"
    velocity = 1 * meter / second
    S.post.delay = "abs(x_pre - (N_post-j)*mmeter)/velocity"
    assert_allclose(S.pre1.delay[:], np.arange(len(G)) * ms)
    assert_allclose(S.pre2.delay[:], np.arange(len(G)) * ms)
    assert_allclose(S.post.delay[:], abs(G.x - (10 - G.i) * mmeter) / velocity)
    S.pre1.delay = 5 * ms
    S.pre2.delay = 10 * ms
    S.post.delay = 1 * ms
    assert_allclose(S.pre1.delay[:], np.ones(len(G)) * 5 * ms)
    assert_allclose(S.pre2.delay[:], np.ones(len(G)) * 10 * ms)
    assert_allclose(S.post.delay[:], np.ones(len(G)) * 1 * ms)
    
    assert len(S.pre1.delay["j<5"]) == 5
    assert_allclose(S.pre1.delay["j<5"], 5 * ms)
    
    assert len(S.post.delay[[3, 4], :]) == 2
    assert_allclose(S.post.delay[[3, 4], :], 1 * ms)
    assert len(S.pre2.delay[:, 7]) == 1
    assert_allclose(S.pre2.delay[:, 7], 10 * ms)
    assert len(S.pre1.delay[[1, 2], [1, 2]]) == 2
    assert_allclose(S.pre1.delay[[1, 2], [1, 2]], 5 * ms)

    
    S = Synapses(
        G,
        G,
        "w:1",
        on_pre={"pre1": "v+=w", "pre2": "v+=w"},
        on_post="v-=w",
        delay={"pre1": 5 * ms, "post": 1 * ms},
    )
    assert_allclose(S.pre1.delay[:], 5 * ms)
    assert_allclose(S.post.delay[:], 1 * ms)
    S.connect(j="i")
    assert len(S.pre2.delay[:]) == len(G)
    S.pre1.delay = 10 * ms
    assert_allclose(S.pre1.delay[:], 10 * ms)
    S.post.delay = "3*ms"
    assert_allclose(S.post.delay[:], 3 * ms)


def test_delays_pathways_subgroups():
    G = NeuronGroup(10, "x: meter", threshold="False")
    G.x = "i*mmeter"
    
    S = Synapses(
        G[:5], G[5:], "w:1", on_pre={"pre1": "v+=w", "pre2": "v+=w"}, on_post="v-=w"
    )
    S.connect(j="i")
    assert len(S.pre1.delay[:]) == 5
    assert len(S.pre2.delay[:]) == 5
    assert len(S.post.delay[:]) == 5
    S.pre1.delay = "i*ms"
    S.pre2.delay = "j*ms"
    velocity = 1 * meter / second
    S.post.delay = "abs(x_pre - (N_post-j)*mmeter)/velocity"
    assert_allclose(S.pre1.delay[:], np.arange(5) * ms)
    assert_allclose(S.pre2.delay[:], np.arange(5) * ms)
    assert_allclose(S.post.delay[:], abs(G[:5].x - (5 - G[:5].i) * mmeter) / velocity)
    S.pre1.delay = 5 * ms
    S.pre2.delay = 10 * ms
    S.post.delay = 1 * ms
    assert_allclose(S.pre1.delay[:], np.ones(5) * 5 * ms)
    assert_allclose(S.pre2.delay[:], np.ones(5) * 10 * ms)
    assert_allclose(S.post.delay[:], np.ones(5) * 1 * ms)


@pytest.mark.codegen_independent
def test_pre_before_post():
    
    G = NeuronGroup(
        1,
        """
        x : 1
        y : 1
        """,
        threshold="True",
    )
    S = Synapses(G, G, "", on_pre="x=1; y=1", on_post="x=2")
    S.connect()
    run(defaultclock.dt)
    
    
    assert G.x == 2
    assert G.y == 1


@pytest.mark.standalone_compatible
def test_pre_post_simple():
    
    G1 = SpikeGeneratorGroup(1, [0], [1] * ms)
    G2 = SpikeGeneratorGroup(1, [0], [2] * ms)
    with catch_logs() as l:
        S = Synapses(
            G1,
            G2,
            """
            pre_value : 1
            post_value : 1
            """,
            pre="pre_value +=1",
            post="post_value +=2",
        )
    S.connect()
    syn_mon = StateMonitor(S, ["pre_value", "post_value"], record=[0], when="end")
    run(3 * ms)
    offset = schedule_propagation_offset()
    assert_allclose(syn_mon.pre_value[0][syn_mon.t < 1 * ms + offset], 0)
    assert_allclose(syn_mon.pre_value[0][syn_mon.t >= 1 * ms + offset], 1)
    assert_allclose(syn_mon.post_value[0][syn_mon.t < 2 * ms + offset], 0)
    assert_allclose(syn_mon.post_value[0][syn_mon.t >= 2 * ms + offset], 2)


@pytest.mark.standalone_compatible
def test_transmission_simple():
    source = SpikeGeneratorGroup(2, [0, 1], [2, 1] * ms)
    target = NeuronGroup(2, "v : 1")
    syn = Synapses(source, target, on_pre="v += 1")
    syn.connect(j="i")
    mon = StateMonitor(target, "v", record=True, when="end")
    run(2.5 * ms)
    offset = schedule_propagation_offset()
    assert_allclose(mon[0].v[mon.t < 2 * ms + offset], 0.0)
    assert_allclose(mon[0].v[mon.t >= 2 * ms + offset], 1.0)
    assert_allclose(mon[1].v[mon.t < 1 * ms + offset], 0.0)
    assert_allclose(mon[1].v[mon.t >= 1 * ms + offset], 1.0)


@pytest.mark.standalone_compatible
def test_transmission_custom_event():
    source = NeuronGroup(
        2,
        "",
        events={
            "custom": (
                "timestep(t,dt)>=timestep((2-i)*ms, dt) "
                "and timestep(t,dt)<timestep((2-i)*ms + dt, dt)"
            )
        },
    )
    target = NeuronGroup(2, "v : 1")
    syn = Synapses(source, target, on_pre="v += 1", on_event="custom")
    syn.connect(j="i")
    mon = StateMonitor(target, "v", record=True, when="end")
    run(2.5 * ms)
    assert_allclose(mon[0].v[mon.t < 2 * ms], 0.0)
    assert_allclose(mon[0].v[mon.t >= 2 * ms], 1.0)
    assert_allclose(mon[1].v[mon.t < 1 * ms], 0.0)
    assert_allclose(mon[1].v[mon.t >= 1 * ms], 1.0)


@pytest.mark.codegen_independent
def test_invalid_custom_event():
    group1 = NeuronGroup(
        2,
        "v : 1",
        events={
            "custom": (
                "timestep(t,dt)>=timesteep((2-i)*ms,dt) "
                "and timestep(t, dt)<timestep((2-i)*ms + dt, dt)"
            )
        },
    )
    group2 = NeuronGroup(2, "v : 1", threshold="v>1")
    with pytest.raises(ValueError) as ex:
        Synapses(group1, group1, on_pre="v+=1")
    assert "threshold" in str(ex)  
    with pytest.raises(ValueError):
        Synapses(group2, group2, on_pre="v+=1", on_event="custom")


def test_transmission():
    default_dt = defaultclock.dt
    delays = [
        [0, 0, 0, 0] * ms,
        [1, 1, 1, 0] * ms,
        [0, 1, 2, 3] * ms,
        [2, 2, 0, 0] * ms,
        [2, 1, 0, 1] * ms,
    ]
    for delay in delays:
        
        source = NeuronGroup(
            4,
            """
            dv/dt = rate : 1
            rate : Hz
            """,
            threshold="v>1",
            reset="v=0",
        )
        source.rate = [51, 101, 101, 51] * Hz
        target = NeuronGroup(4, "v:1", threshold="v>1", reset="v=0")

        source_mon = SpikeMonitor(source)
        target_mon = SpikeMonitor(target)

        S = Synapses(source, target, on_pre="v+=1.1")
        S.connect(j="i")
        S.delay = delay
        net = Network(S, source, target, source_mon, target_mon)
        net.run(50 * ms + default_dt + max(delay))
        
        
        for d in range(len(delay)):
            assert_allclose(
                source_mon.t[source_mon.i == d],
                target_mon.t[target_mon.i == d] - default_dt - delay[d],
            )


@pytest.mark.standalone_compatible
def test_transmission_all_to_one_heterogeneous_delays():
    source = SpikeGeneratorGroup(
        6,
        [0, 1, 4, 5, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5],
        [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2] * defaultclock.dt,
    )
    target = NeuronGroup(1, "v : 1")
    synapses = Synapses(source, target, "w : 1", on_pre="v_post += w")
    synapses.connect()
    synapses.w = [1, 2, 3, 4, 5, 6]
    synapses.delay = [0, 0, 0, 1, 2, 1] * defaultclock.dt

    mon = StateMonitor(target, "v", record=True, when="end")
    if schedule_propagation_offset() == 0 * second:
        offset = 0
    else:
        offset = 1
    run((4 + offset) * defaultclock.dt)
    assert mon[0].v[0 + offset] == 3
    assert mon[0].v[1 + offset] == 12
    assert mon[0].v[2 + offset] == 33
    assert mon[0].v[3 + offset] == 48


@pytest.mark.standalone_compatible
def test_transmission_one_to_all_heterogeneous_delays():
    source = SpikeGeneratorGroup(1, [0, 0], [0, 2] * defaultclock.dt)
    target = NeuronGroup(6, "v:integer")
    synapses = Synapses(source, target, on_pre="v_post += 1")
    synapses.connect()
    synapses.delay = [
        1,
        1,
        2,
        4,
        3,
        2,
    ] * defaultclock.dt - schedule_propagation_offset()

    mon = StateMonitor(target, "v", record=True, when="end")
    run(5 * defaultclock.dt)
    assert_allclose(mon[0].v, [0, 1, 1, 2, 2])
    assert_allclose(mon[1].v, [0, 1, 1, 2, 2])
    assert_allclose(mon[2].v, [0, 0, 1, 1, 2])
    assert_allclose(mon[3].v, [0, 0, 0, 0, 1])
    assert_allclose(mon[4].v, [0, 0, 0, 1, 1])
    assert_allclose(mon[5].v, [0, 0, 1, 1, 2])


@pytest.mark.standalone_compatible
def test_transmission_scalar_delay():
    inp = SpikeGeneratorGroup(2, [0, 1], [0, 1] * ms)
    target = NeuronGroup(2, "v:1")
    S = Synapses(inp, target, on_pre="v+=1", delay=0.5 * ms)
    S.connect(j="i")
    mon = StateMonitor(target, "v", record=True, when="end")
    run(2 * ms)
    offset = schedule_propagation_offset()
    assert_allclose(mon[0].v[mon.t < 0.5 * ms + offset - defaultclock.dt / 2], 0)
    assert_allclose(mon[0].v[mon.t >= 0.5 * ms + offset - defaultclock.dt / 2], 1)
    assert_allclose(mon[1].v[mon.t < 1.5 * ms + offset - defaultclock.dt / 2], 0)
    assert_allclose(mon[1].v[mon.t >= 1.5 * ms + offset - defaultclock.dt / 2], 1)


@pytest.mark.standalone_compatible
def test_transmission_scalar_delay_different_clocks():
    inp = SpikeGeneratorGroup(
        2,
        [0, 1],
        [0, 1] * ms,
        dt=0.5 * ms,
        
        
        name="sg_%d" % uuid.uuid4(),
    )
    target = NeuronGroup(2, "v:1", dt=0.1 * ms)
    S = Synapses(inp, target, on_pre="v+=1", delay=0.5 * ms)
    S.connect(j="i")
    mon = StateMonitor(target, "v", record=True, when="end")

    if get_device() == all_devices["runtime"]:
        
        with catch_logs() as l:
            run(2 * ms)
            assert len(l) == 1, "expected a warning, got %d" % len(l)
            assert l[0][1].endswith("synapses_dt_mismatch")

    run(0 * ms)
    assert_allclose(mon[0].v[mon.t < 0.5 * ms], 0)
    assert_allclose(mon[0].v[mon.t >= 0.5 * ms], 1)
    assert_allclose(mon[1].v[mon.t < 1.5 * ms], 0)
    assert_allclose(mon[1].v[mon.t >= 1.5 * ms], 1)


@pytest.mark.standalone_compatible
def test_transmission_boolean_variable():
    source = SpikeGeneratorGroup(4, [0, 1, 2, 3], [2, 1, 2, 1] * ms)
    target = NeuronGroup(4, "v : 1")
    syn = Synapses(source, target, "use : boolean (constant)", on_pre="v += int(use)")
    syn.connect(j="i")
    syn.use = "i<2"
    mon = StateMonitor(target, "v", record=True, when="end")
    run(2.5 * ms)
    offset = schedule_propagation_offset()
    assert_allclose(mon[0].v[mon.t < 2 * ms + offset], 0.0)
    assert_allclose(mon[0].v[mon.t >= 2 * ms + offset], 1.0)
    assert_allclose(mon[1].v[mon.t < 1 * ms + offset], 0.0)
    assert_allclose(mon[1].v[mon.t >= 1 * ms + offset], 1.0)
    assert_allclose(mon[2].v, 0.0)
    assert_allclose(mon[3].v, 0.0)


@pytest.mark.codegen_independent
def test_clocks():
    """
    Make sure that a `Synapse` object uses the correct clocks.
    """
    source_dt = 0.05 * ms
    target_dt = 0.1 * ms
    synapse_dt = 0.2 * ms
    source = NeuronGroup(1, "v:1", dt=source_dt, threshold="False")
    target = NeuronGroup(1, "v:1", dt=target_dt, threshold="False")
    synapse = Synapses(
        source, target, "w:1", on_pre="v+=1", on_post="v+=1", dt=synapse_dt
    )
    synapse.connect()

    assert synapse.pre.clock is source.clock
    assert synapse.post.clock is target.clock
    assert synapse.pre._clock.dt == source_dt
    assert synapse.post._clock.dt == target_dt
    assert synapse._clock.dt == synapse_dt


def test_equations_with_clocks():
    """
    Make sure that dt of a `Synapse` object is correctly resolved.
    """
    source_dt = 0.1 * ms
    synapse_dt = 1 * ms
    source_target = NeuronGroup(1, "v:1", dt=source_dt, threshold="False")
    synapse = Synapses(
        source_target,
        source_target,
        "dw/dt = 1/ms : 1 (clock-driven)",
        dt=synapse_dt,
        method="euler",
    )
    synapse.connect()
    synapse.w = 0
    run(1 * ms)

    assert synapse.w[0] == 1


def test_changed_dt_spikes_in_queue():
    defaultclock.dt = 0.5 * ms
    G1 = NeuronGroup(1, "v:1", threshold="v>1", reset="v=0")
    G1.v = 1.1
    G2 = NeuronGroup(10, "v:1", threshold="v>1", reset="v=0")
    S = Synapses(G1, G2, on_pre="v+=1.1")
    S.connect(True)
    S.delay = "j*ms"
    mon = SpikeMonitor(G2)
    net = Network(G1, G2, S, mon)
    net.run(5 * ms)
    defaultclock.dt = 1 * ms
    net.run(3 * ms)
    defaultclock.dt = 0.1 * ms
    net.run(2 * ms)
    
    
    expected = [
        0.5,
        1.5,
        2.5,
        3.5,
        4.5,  
        6,
        7,
        8,  
        8.1,
        9.1,  
    ] * ms
    assert_allclose(mon.t[:], expected)


@pytest.mark.codegen_independent
def test_no_synapses():
    
    G1 = NeuronGroup(1, "", threshold="True")
    G2 = NeuronGroup(1, "v:1")
    S = Synapses(G1, G2, on_pre="v+=1")
    net = Network(G1, G2, S)
    with pytest.raises(BrianObjectException) as exc:
        net.run(0 * ms)
    assert exc_isinstance(exc, TypeError)


@pytest.mark.codegen_independent
def test_no_synapses_variable_write():
    
    G1 = NeuronGroup(1, "", threshold="True")
    G2 = NeuronGroup(1, "v:1")
    S = Synapses(G1, G2, "w : 1", on_pre="v+=w")
    
    with pytest.raises(TypeError):
        setattr(S, "w", 1)
    with pytest.raises(TypeError):
        setattr(S, "delay", 1 * ms)


@pytest.mark.standalone_compatible
def test_summed_variable():
    source = NeuronGroup(2, "v : volt", threshold="v>1*volt", reset="v=0*volt")
    source.v = 1.1 * volt  
    target = NeuronGroup(2, "v : volt")
    S = Synapses(
        source,
        target,
        """
        w : volt
        x : volt
        v_post = 2*x : volt (summed)
        """,
        on_pre="x+=w",
        multisynaptic_index="k",
    )
    S.connect("i==j", n=2)
    S.w["k == 0"] = "i*volt"
    S.w["k == 1"] = "(i + 0.5)*volt"
    net = Network(source, target, S)
    net.run(1 * ms)

    
    assert_allclose(target.v, np.array([1.0, 5.0]) * volt)


@pytest.mark.standalone_compatible
def test_summed_variable_pre_and_post():
    G1 = NeuronGroup(
        4,
        """
        neuron_var : 1
        syn_sum : 1
        neuron_sum : 1
        """,
    )
    G1.neuron_var = "i"
    G2 = NeuronGroup(
        4,
        """
        neuron_var : 1
        syn_sum : 1
        neuron_sum : 1
        """,
    )
    G2.neuron_var = "i+4"

    synapses = Synapses(
        G1,
        G2,
        """
        syn_var : 1
        neuron_sum_pre = neuron_var_post : 1 (summed)
        syn_sum_pre = syn_var : 1 (summed)
        neuron_sum_post = neuron_var_pre : 1 (summed)
        syn_sum_post = syn_var : 1 (summed)
        """,
    )
    
    
    synapses.connect(i=[0, 1, 2, 3, 3, 3], j=[0, 0, 0, 1, 2, 3])
    synapses.syn_var = [0, 1, 2, 3, 4, 5]

    run(defaultclock.dt)
    assert_allclose(G1.syn_sum[:], [0, 1, 2, 12])
    assert_allclose(G1.neuron_sum[:], [4, 4, 4, 18])
    assert_allclose(G2.syn_sum[:], [3, 3, 4, 5])
    assert_allclose(G2.neuron_sum[:], [3, 3, 3, 3])


@pytest.mark.standalone_compatible
def test_summed_variable_differing_group_size():
    G1 = NeuronGroup(2, "var : 1", name="G1")
    G2 = NeuronGroup(10, "var : 1", name="G2")
    G2.var[:5] = 1
    G2.var[5:] = 10
    syn1 = Synapses(
        G1,
        G2,
        """
        syn_var : 1
        var_pre = syn_var + var_post : 1 (summed)
        """,
    )
    syn1.connect(i=0, j=[0, 1, 2, 3, 4])
    syn1.connect(i=1, j=[5, 6, 7, 8, 9])
    syn1.syn_var = np.arange(10)
    
    G3 = NeuronGroup(10, "var : 1", name="G3")
    G4 = NeuronGroup(2, "var : 1", name="G4")
    G3.var[:5] = 1
    G3.var[5:] = 10
    syn2 = Synapses(
        G3,
        G4,
        """
        syn_var : 1
        var_post = syn_var + var_pre : 1 (summed)
        """,
    )
    syn2.connect(i=[0, 1, 2, 3, 4], j=0)
    syn2.connect(i=[5, 6, 7, 8, 9], j=1)
    syn2.syn_var = np.arange(10)

    run(defaultclock.dt)

    assert_allclose(G1.var[0], 5 * 1 + 0 + 1 + 2 + 3 + 4)
    assert_allclose(G1.var[1], 5 * 10 + 5 + 6 + 7 + 8 + 9)

    assert_allclose(G4.var[0], 5 * 1 + 0 + 1 + 2 + 3 + 4)
    assert_allclose(G4.var[1], 5 * 10 + 5 + 6 + 7 + 8 + 9)


def test_summed_variable_errors():
    G = NeuronGroup(
        10,
        """
        dv/dt = -v / (10*ms) : volt
        sub = 2*v : volt
        p : volt
        """,
        threshold="False",
        reset="",
    )

    
    with pytest.raises(ValueError):
        Synapses(G, G, """dp_post/dt = -p_post / (10*ms) : volt (summed)""")
    with pytest.raises(ValueError):
        Synapses(G, G, """p_post : volt (summed)""")

    
    with pytest.raises(ValueError):
        Synapses(G, G, """p = 3*volt : volt (summed)""")
    
    with pytest.raises(ValueError):
        Synapses(G, G, """q_post = 3*volt : volt (summed)""")

    
    with pytest.raises(ValueError):
        Synapses(G, G, """sub_post = 3*volt : volt (summed)""")
    with pytest.raises(ValueError):
        Synapses(G, G, """v_post = 3*volt : volt (summed)""")

    
    with pytest.raises(DimensionMismatchError):
        Synapses(G, G, """p_post = 3*second : second (summed)""")

    
    with pytest.raises(ValueError):
        Synapses(
            G,
            G,
            """
            p_post = 3*volt : volt (summed)
            p_pre = 3*volt : volt (summed)
            """,
        )

    
    with pytest.raises(EquationError) as ex:
        Synapses(
            G,
            G,
            """
            ds/dt = -s/(3*ms) : volt (event-driven)
            p_post = s : volt (summed)
            """,
            on_pre="s += 1*mV",
        )
    assert "'p_post'" in str(ex.value) and "'s'" in str(ex.value)

    
    with pytest.raises(EquationError) as ex:
        Synapses(
            G,
            G,
            """
            ds/dt = -s/(3*ms) : volt (event-driven)
            x = s : volt
            y = x : volt
            p_post = y : 1 (summed)
            """,
            on_pre="s += 1*mV",
        )
    assert "'p_post'" in str(ex.value) and "'s'" in str(ex.value)
    assert "'x'" in str(ex.value) and "'y'" in str(ex.value)

    with pytest.raises(BrianObjectException) as ex:
        S = Synapses(
            G,
            G,
            """
            y : siemens
            p_post = y : volt (summed)
            """,
        )
        run(0 * ms)

    assert isinstance(ex.value.__cause__, DimensionMismatchError)


@pytest.mark.codegen_independent
def test_multiple_summed_variables():
    
    source = NeuronGroup(1, "")
    target = NeuronGroup(10, "v : 1")
    syn1 = Synapses(source, target, "v_post = 1 : 1 (summed)")
    syn1.connect()
    syn2 = Synapses(source, target, "v_post = 1 : 1 (summed)")
    syn2.connect()
    net = Network(collect())
    with pytest.raises(NotImplementedError):
        net.run(0 * ms)


@pytest.mark.standalone_compatible
def test_summed_variables_subgroups():
    source = NeuronGroup(1, "")
    target = NeuronGroup(10, "v : 1")
    subgroup1 = target[:6]
    subgroup2 = target[6:]
    syn1 = Synapses(source, subgroup1, "v_post = 1 : 1 (summed)")
    syn1.connect(n=2)
    syn2 = Synapses(source, subgroup2, "v_post = 1 : 1 (summed)")
    syn2.connect()
    run(defaultclock.dt)
    assert_allclose(target.v[:6], 2 * np.ones(6))
    assert_allclose(target.v[6:], 1 * np.ones(4))


@pytest.mark.codegen_independent
def test_summed_variables_overlapping_subgroups():
    
    source = NeuronGroup(1, "")
    target = NeuronGroup(10, "v : 1")
    
    subgroup1 = target[:7]
    subgroup2 = target[6:]
    syn1 = Synapses(source, subgroup1, "v_post = 1 : 1 (summed)")
    syn1.connect(n=2)
    syn2 = Synapses(source, subgroup2, "v_post = 1 : 1 (summed)")
    syn2.connect()
    net = Network(collect())
    with pytest.raises(NotImplementedError):
        net.run(0 * ms)


@pytest.mark.codegen_independent
def test_summed_variables_linked_variables():
    source = NeuronGroup(1, "")
    target1 = NeuronGroup(10, "v : 1")
    target2 = NeuronGroup(10, "v : 1 (linked)")
    target2.v = linked_var(target1.v)
    
    syn1 = Synapses(source, target1, "v_post = 1 : 1 (summed)")
    syn1.connect()
    syn2 = Synapses(source, target2, "v_post = 1 : 1 (summed)")
    syn2.connect()
    net = Network(collect())
    with pytest.raises(NotImplementedError):
        net.run(0 * ms)


def test_scalar_parameter_access():
    G = NeuronGroup(
        10,
        """
        v : 1
        scalar : Hz (shared)
        """,
        threshold="False",
    )
    S = Synapses(
        G,
        G,
        """
        w : 1
        s : Hz (shared)
        number : 1 (shared)
        """,
        on_pre="v+=w*number",
    )
    S.connect()

    
    S.s = 100 * Hz
    assert_allclose(S.s[:], 100 * Hz)
    S.s[:] = 200 * Hz
    assert_allclose(S.s[:], 200 * Hz)
    S.s = "s - 50*Hz + number*Hz"
    assert_allclose(S.s[:], 150 * Hz)
    S.s[:] = "50*Hz"
    assert_allclose(S.s[:], 50 * Hz)

    
    S.scalar_post = 100 * Hz
    assert_allclose(G.scalar[:], 100 * Hz)
    S.scalar_post[:] = 100 * Hz
    assert_allclose(G.scalar[:], 100 * Hz)

    
    assert_allclose(np.asanyarray(S.s), 50 * Hz)

    
    with pytest.raises(IndexError):
        S.s[0]
    with pytest.raises(IndexError):
        S.s[1]
    with pytest.raises(IndexError):
        S.s[0:1]
    with pytest.raises(IndexError):
        S.s["i>5"]

    with pytest.raises(ValueError):
        S.s.set_item(slice(None), [0, 1] * Hz)
    with pytest.raises(IndexError):
        S.s.set_item(0, 100 * Hz)
    with pytest.raises(IndexError):
        S.s.set_item(1, 100 * Hz)
    with pytest.raises(IndexError):
        S.s.set_item("i>5", 100 * Hz)


def test_scalar_subexpression():
    G = NeuronGroup(
        10,
        """
        v : 1
        number : 1 (shared)
        """,
        threshold="False",
    )
    S = Synapses(
        G,
        G,
        """
        s : 1 (shared)
        sub = number_post + s : 1 (shared)
        """,
        on_pre="v+=s",
    )
    S.connect()
    S.s = 100
    G.number = 50
    assert S.sub[:] == 150

    with pytest.raises(SyntaxError):
        Synapses(
            G,
            G,
            """
            s : 1 (shared)
            sub = v_post + s : 1 (shared)
            """,
            on_pre="v+=s",
        )


@pytest.mark.standalone_compatible
def test_sim_with_scalar_variable():
    inp = SpikeGeneratorGroup(2, [0, 1], [0, 0] * ms)
    out = NeuronGroup(2, "v : 1")
    syn = Synapses(
        inp,
        out,
        """
        w : 1
        s : 1 (shared)
        """,
        on_pre="v += s + w",
    )
    syn.connect(j="i")
    syn.w = [1, 2]
    syn.s = 5
    run(2 * defaultclock.dt)
    assert_allclose(out.v[:], [6, 7])


@pytest.mark.standalone_compatible
def test_sim_with_scalar_subexpression():
    inp = SpikeGeneratorGroup(2, [0, 1], [0, 0] * ms)
    out = NeuronGroup(2, "v : 1")
    syn = Synapses(
        inp,
        out,
        """
        w : 1
        s = 5 : 1 (shared)
        """,
        on_pre="v += s + w",
    )
    syn.connect(j="i")
    syn.w = [1, 2]
    run(2 * defaultclock.dt)
    assert_allclose(out.v[:], [6, 7])


@pytest.mark.standalone_compatible
def test_sim_with_constant_subexpression():
    inp = SpikeGeneratorGroup(2, [0, 1], [0, 0] * ms)
    out = NeuronGroup(2, "v : 1")
    syn = Synapses(
        inp,
        out,
        """
        w : 1
        s = 5 : 1 (constant over dt)
        """,
        on_pre="v += s + w",
    )
    syn.connect(j="i")
    syn.w = [1, 2]
    run(2 * defaultclock.dt)
    assert_allclose(out.v[:], [6, 7])


@pytest.mark.standalone_compatible
def test_external_variables():
    
    source = SpikeGeneratorGroup(1, [0], [0] * ms)
    target = NeuronGroup(1, "v:1")
    w_var = 1
    amplitude = 2
    syn = Synapses(source, target, "w=w_var : 1", on_pre="v+=amplitude*w")
    syn.connect()
    run(defaultclock.dt)
    assert target.v[0] == 2


@pytest.mark.standalone_compatible
def test_event_driven():
    
    
    
    pre = NeuronGroup(
        2,
        """
        dv/dt = rate : 1
        rate : Hz
        """,
        threshold="v>1",
        reset="v=0",
    )
    pre.rate = [1000, 1500] * Hz
    post = NeuronGroup(
        2,
        """
        dv/dt = rate : 1
        rate : Hz
        """,
        threshold="v>1",
        reset="v=0",
    )
    post.rate = [1100, 1400] * Hz
    
    taupre = 20 * ms
    taupost = taupre
    gmax = 0.01
    dApre = 0.01
    dApost = -dApre * taupre / taupost * 1.05
    dApost *= gmax
    dApre *= gmax
    
    S1 = Synapses(
        pre,
        post,
        """
        w : 1
        dApre/dt = -Apre/taupre : 1 (event-driven)
        dApost/dt = -Apost/taupost : 1 (event-driven)
        """,
        on_pre="""
        Apre += dApre
        w = clip(w+Apost, 0, gmax)
        """,
        on_post="""
        Apost += dApost
        w = clip(w+Apre, 0, gmax)
        """,
    )
    S1.connect(j="i")
    
    S2 = Synapses(
        pre,
        post,
        """
        w : 1
        Apre : 1
        Apost : 1
        lastupdate : second
        """,
        on_pre="""
        Apre=Apre*exp((lastupdate-t)/taupre)+dApre
        Apost=Apost*exp((lastupdate-t)/taupost)
        w = clip(w+Apost, 0, gmax)
        lastupdate = t
        """,
        on_post="""
        Apre=Apre*exp((lastupdate-t)/taupre)
        Apost=Apost*exp((lastupdate-t)/taupost) +dApost
        w = clip(w+Apre, 0, gmax)
        lastupdate = t
        """,
    )
    S2.connect(j="i")
    S1.w = 0.5 * gmax
    S2.w = 0.5 * gmax
    run(25 * ms)
    
    assert_allclose(S1.w[:], S2.w[:])


@pytest.mark.codegen_independent
def test_event_driven_dependency_checks():
    dummy = NeuronGroup(1, "", threshold="False", reset="")

    
    syn = Synapses(
        dummy,
        dummy,
        """
        da/dt = (a-b) / (5*ms): 1 (event-driven)
        b : 1""",
        on_pre="b+=1",
    )
    syn.connect()

    
    syn2 = Synapses(
        dummy,
        dummy,
        """
        da/dt = (a-b) / (5*ms): 1 (event-driven)
        b = c : 1
        c : 1""",
        on_pre="c+=1",
    )
    syn2.connect()
    run(0 * ms)


@pytest.mark.codegen_independent
def test_event_driven_dependency_error():
    stim = SpikeGeneratorGroup(1, [0], [0] * ms, period=5 * ms)
    syn = Synapses(
        stim,
        stim,
        """
        da/dt = -a / (5*ms) : 1 (event-driven)
        db/dt = -b / (5*ms) : 1 (event-driven)
        dc/dt = a*b / (5*ms) : 1 (event-driven)""",
        on_pre="a+=1",
    )
    syn.connect()
    net = Network(collect())
    with pytest.raises(BrianObjectException) as exc:
        net.run(0 * ms)
    assert exc_isinstance(exc, UnsupportedEquationsException)


@pytest.mark.codegen_independent
def test_event_driven_dependency_error2():
    stim = SpikeGeneratorGroup(1, [0], [0] * ms, period=5 * ms)
    tau = 5 * ms
    with pytest.raises(EquationError) as exc:
        syn = Synapses(
            stim,
            stim,
            """
            da/dt = -a / (5*ms) : 1 (clock-driven)
            db/dt = -b / (5*ms) : 1 (clock-driven)
            dc/dt = a*b / (5*ms) : 1 (event-driven)
            """,
            on_pre="a+=1",
        )
    assert "'c'" in str(exc.value) and (
        "'a'" in str(exc.value) or "'b'" in str(exc.value)
    )

    
    with pytest.raises(EquationError) as exc:
        syn = Synapses(
            stim,
            stim,
            """
            da/dt = -a / (5*ms) : 1 (clock-driven)
            b = a : 1
            dc/dt = b / (5*ms) : 1 (event-driven)
            """,
            on_pre="a+=1",
        )
    assert (
        "'c'" in str(exc.value) and "'a'" in str(exc.value) and "'b'" in str(exc.value)
    )


@pytest.mark.codegen_independent
def test_event_driven_dependency_error3():
    P = NeuronGroup(10, "dv/dt = -v/(10*ms) : volt")
    with pytest.raises(EquationError) as ex:
        Synapses(
            P,
            P,
            """
            ds/dt = -s/(3*ms) : 1 (event-driven)
            df/dt = f*s/(5*ms) : 1 (clock-driven)
            """,
            on_pre="s += 1",
        )
    assert "'s'" in str(ex.value) and "'f'" in str(ex.value)

    
    with pytest.raises(EquationError) as ex:
        Synapses(
            P,
            P,
            """
            ds/dt = -s/(3*ms) : 1 (event-driven)
            x = s : 1
            y = x : 1
            df/dt = f*y/(5*ms) : 1 (clock-driven)
            """,
            on_pre="s += 1",
        )
    assert "'s'" in str(ex.value) and "'f'" in str(ex.value)
    assert "'x'" in str(ex.value) and "'y'" in str(ex.value)


@pytest.mark.codegen_independent
def test_repr():
    G = NeuronGroup(1, "v: volt", threshold="False")
    S = Synapses(
        G,
        G,
        """
        w : 1
        dApre/dt = -Apre/taupre : 1 (event-driven)
        dApost/dt = -Apost/taupost : 1 (event-driven)
        """,
        on_pre="""
        Apre += dApre
        w = clip(w+Apost, 0, gmax)
        """,
        on_post="""
        Apost += dApost
        w = clip(w+Apre, 0, gmax)
        """,
    )
    
    for func in [str, repr, sympy.latex]:
        assert len(func(S.equations))


@pytest.mark.codegen_independent
def test_pre_post_variables():
    G = NeuronGroup(10, "v : 1", threshold="False")
    G2 = NeuronGroup(
        10,
        """
        v : 1
        w : 1
        """,
        threshold="False",
    )
    S = Synapses(G, G2, "x : 1")
    
    for var in [
        "v_pre",
        "v",
        "v_post",
        "w",
        "w_post",
        "x",
        "N_pre",
        "N_post",
        "N_incoming",
        "N_outgoing",
        "i",
        "j",
        "t",
        "dt",
    ]:
        assert var in S.variables
    
    
    assert S.variables["v"] is S.variables["v_post"]
    assert S.variables["w"] is S.variables["w_post"]

    
    assert "_spikespace_pre" not in S.variables
    assert "_spikespace" not in S.variables
    assert "_spikespace_post" not in S.variables


@pytest.mark.codegen_independent
def test_variables_by_owner():
    
    G = NeuronGroup(10, "v : 1")
    G2 = NeuronGroup(
        10,
        """
        v : 1
        w : 1
        """,
    )
    S = Synapses(G, G2, "x : 1")

    
    
    
    G_variables = {
        key: value for key, value in G.variables.items() if value.owner.name == G.name
    }  
    G2_variables = {
        key: value for key, value in G2.variables.items() if value.owner.name == G2.name
    }
    assert set(G_variables.values()) == set(variables_by_owner(S.variables, G).values())
    assert set(G2_variables.values()) == set(
        variables_by_owner(S.variables, G2).values()
    )
    assert len(set(variables_by_owner(S.variables, S)) & set(G_variables.values())) == 0
    assert (
        len(set(variables_by_owner(S.variables, S)) & set(G2_variables.values())) == 0
    )
    
    assert all(
        varname in variables_by_owner(S.variables, S)
        for varname in ["x", "N", "N_incoming", "N_outgoing"]
    )


@pytest.mark.codegen_independent
def check_permutation_code(code):
    from collections import defaultdict

    vars = get_identifiers(code)
    indices = defaultdict(lambda: "_idx")
    for var in vars:
        if var.endswith("_syn"):
            indices[var] = "_idx"
        elif var.endswith("_pre"):
            indices[var] = "_presynaptic_idx"
        elif var.endswith("_post"):
            indices[var] = "_postsynaptic_idx"
        elif var.endswith("_const"):
            indices[var] = "0"
    variables = dict()
    variables.update(DEFAULT_FUNCTIONS)
    for var in indices:
        if var.endswith("_const"):
            variables[var] = Constant(var, 42, owner=device)
        else:
            variables[var] = ArrayVariable(var, None, 10, device)
    variables["_presynaptic_idx"] = ArrayVariable(var, None, 10, device)
    variables["_postsynaptic_idx"] = ArrayVariable(var, None, 10, device)
    scalar_statements, vector_statements = make_statements(code, variables, float64)
    check_for_order_independence(vector_statements, variables, indices)


def numerically_check_permutation_code(code):
    
    
    
    
    
    code = deindent(code)
    from collections import defaultdict

    vars = get_identifiers(code)
    indices = defaultdict(lambda: "_idx")
    vals = {}
    for var in vars:
        if var.endswith("_syn"):
            indices[var] = "_idx"
            vals[var] = zeros(9)
        elif var.endswith("_pre"):
            indices[var] = "_presynaptic_idx"
            vals[var] = zeros(3)
        elif var.endswith("_post"):
            indices[var] = "_postsynaptic_idx"
            vals[var] = zeros(3)
        elif var.endswith("_shared"):
            indices[var] = "0"
            vals[var] = zeros(1)
        elif var.endswith("_const"):
            indices[var] = "0"
            vals[var] = 42
    subs = {
        var: var + "[" + idx + "]"
        for var, idx in indices.items()
        if not var.endswith("_const")
    }
    code = word_substitute(code, subs)
    code = f"""
from numpy import *
from numpy.random import rand, randn
for _idx in shuffled_indices:
    _presynaptic_idx = presyn[_idx]
    _postsynaptic_idx = postsyn[_idx]
{indent(code)}
    """
    ns = vals.copy()
    ns["shuffled_indices"] = arange(9)
    ns["presyn"] = arange(9) % 3
    ns["postsyn"] = arange(9) / 3
    for _ in range(10):
        origvals = {}
        for k, v in vals.items():
            if not k.endswith("_const"):
                v[:] = randn(len(v))
                origvals[k] = v.copy()
        exec(code, ns)
        endvals = {}
        for k, v in vals.items():
            endvals[k] = copy(v)
        for _ in range(10):
            for k, v in vals.items():
                if not k.endswith("_const"):
                    v[:] = origvals[k]
            shuffle(ns["shuffled_indices"])
            exec(code, ns)
            for k, v in vals.items():
                try:
                    assert_allclose(v, endvals[k])
                except AssertionError:
                    raise OrderDependenceError()


SANITY_CHECK_PERMUTATION_ANALYSIS_EXAMPLE = False

permutation_analysis_good_examples = [
    "v_post += w_syn",
    "v_post *= w_syn",
    "v_post = v_post + w_syn",
    "v_post = v_post * w_syn",
    "v_post = w_syn * v_post",
    "v_post += 1",
    "v_post = 1",
    "v_post = c_const",
    "v_post = x_shared",
    "v_post += v_post ",
    "v_post += c_const",
    "v_post += x_shared",
    
    "v_post += sin(-v_post) ",
    "v_post += u_post",
    "v_post += w_syn*v_pre",
    "v_post += sin(-v_post) ",
    "v_post -= sin(v_post) ",
    "v_post += v_pre",
    "v_pre += v_post",
    "v_pre += c_const",
    "v_pre += x_shared",
    "w_syn = v_pre",
    "w_syn = a_syn",
    "w_syn += a_syn",
    "w_syn *= a_syn",
    "w_syn -= a_syn",
    "w_syn /= a_syn",
    "w_syn += 1",
    "w_syn += c_const",
    "w_syn += x_shared",
    "w_syn *= 2",
    "w_syn *= c_const",
    "w_syn *= x_shared",
    """
    w_syn = a_syn
    a_syn += 1
    """,
    """
    w_syn = a_syn
    a_syn += c_const
    """,
    """
    w_syn = a_syn
    a_syn += x_shared
    """,
    "v_post *= 2",
    "v_post *= w_syn",
    """
    v_pre = 0
    w_syn = v_pre
    """,
    """
    v_pre = c_const
    w_syn = v_pre
    """,
    """
    v_pre = x_shared
    w_syn = v_pre
    """,
    """
    ge_syn += w_syn
    Apre_syn += 3
    w_syn = clip(w_syn + Apost_syn, 0, 10)
    """,
    """
    ge_syn += w_syn
    Apre_syn += c_const
    w_syn = clip(w_syn + Apost_syn, 0, 10)
    """,
    """
    ge_syn += w_syn
    Apre_syn += x_shared
    w_syn = clip(w_syn + Apost_syn, 0, 10)
    """,
    """
    a_syn = v_pre
    v_post += a_syn
    """,
    """
    v_post += v_post 
    v_post += v_post
    """,
    """
    v_post += 1
    x = v_post
    """,
]

permutation_analysis_bad_examples = [
    "v_pre = w_syn",
    "v_post = v_pre",
    "v_post = w_syn",
    "v_post += w_syn+v_post",
    "v_post += rand()",  
    """
    a_syn = v_post
    v_post += w_syn
    """,
    """
    x = w_syn
    v_pre = x
    """,
    """
    x = v_pre
    v_post = x
    """,
    """
    v_post += v_pre
    v_pre += v_post
    """,
    """
    b_syn = v_post
    v_post += a_syn
    """,
    """
    v_post += w_syn
    u_post += v_post
    """,
    """
    v_post += 1
    w_syn = v_post
    """,
]


@pytest.mark.codegen_independent
def test_permutation_analysis():
    
    for example in permutation_analysis_good_examples:
        if SANITY_CHECK_PERMUTATION_ANALYSIS_EXAMPLE:
            try:
                numerically_check_permutation_code(example)
            except OrderDependenceError:
                raise AssertionError(
                    "Test unexpectedly raised a numerical "
                    "OrderDependenceError on these "
                    "statements:\n"
                    + example
                )
        try:
            check_permutation_code(example)
        except OrderDependenceError:
            raise AssertionError(
                "Test unexpectedly raised an "
                "OrderDependenceError on these "
                "statements:\n"
                + example
            )

    for example in permutation_analysis_bad_examples:
        if SANITY_CHECK_PERMUTATION_ANALYSIS_EXAMPLE:
            try:
                with pytest.raises(OrderDependenceError):
                    numerically_check_permutation_code(example)
            except AssertionError:
                raise AssertionError(
                    "Order dependence not raised numerically for example: " + example
                )
        try:
            with pytest.raises(OrderDependenceError):
                check_permutation_code(example)
        except AssertionError:
            raise AssertionError("Order dependence not raised for example: " + example)


@pytest.mark.standalone_compatible
def test_vectorisation():
    source = NeuronGroup(10, "v : 1", threshold="v>1")
    target = NeuronGroup(
        10,
        """
        x : 1
        y : 1
        """,
    )
    syn = Synapses(
        source,
        target,
        "w_syn : 1",
        on_pre="""
        v_pre += w_syn
        x_post = y_post
        """,
    )
    syn.connect()
    syn.w_syn = 1
    source.v["i<5"] = 2
    target.y = "i"
    run(defaultclock.dt)
    assert_allclose(source.v[:5], 12)
    assert_allclose(source.v[5:], 0)
    assert_allclose(target.x[:], target.y[:])


@pytest.mark.standalone_compatible
def test_vectorisation_STDP_like():
    
    
    w_max = 10
    neurons = NeuronGroup(
        6,
        """
        dv/dt = rate : 1
        ge : 1
        rate : Hz
        dA/dt = -A/(1*ms) : 1
        """,
        threshold="v>1",
        reset="v=0",
    )
    
    
    "depression" and "facilitation" completely. The example also uses
    
    
    
    syn = Synapses(
        neurons[:3],
        neurons[3:],
        """
        w_dep : 1
        w_fac : 1
        """,
        on_pre="""
        ge_post += w_dep - w_fac
        A_pre += 1
        w_dep = clip(w_dep + A_post, 0, w_max)
        """,
        on_post="""
        A_post += 1
        w_fac = clip(w_fac + A_pre, 0, w_max)
        """,
    )
    syn.connect()
    neurons.rate = 1000 * Hz
    neurons.v = "abs(3-i)*0.1 + 0.7"
    run(2 * ms)
    
    indices = np.argsort(
        np.array(list(zip(syn.i[:], syn.j[:])), dtype=[("i", "<i4"), ("j", "<i4")]),
        order=["i", "j"],
    )
    assert_allclose(
        syn.w_dep[:][indices],
        [
            1.29140162,
            1.16226149,
            1.04603529,
            1.16226149,
            1.04603529,
            0.94143176,
            1.04603529,
            0.94143176,
            6.2472887,
        ],
        atol=0.0001,
    )
    assert_allclose(
        syn.w_fac[:][indices],
        [
            5.06030369,
            5.62256002,
            6.2472887,
            5.62256002,
            6.2472887,
            6.941432,
            6.2472887,
            6.941432,
            1.04603529,
        ],
        atol=0.0001,
    )
    assert_allclose(
        neurons.A[:],
        [1.69665715, 1.88517461, 2.09463845, 2.32737606, 2.09463845, 1.88517461],
        atol=0.0001,
    )
    assert_allclose(
        neurons.ge[:],
        [0.0, 0.0, 0.0, -7.31700015, -8.13000011, -4.04603529],
        atol=0.0001,
    )


@pytest.mark.standalone_compatible
def test_synaptic_equations():
    
    G = NeuronGroup(10, "")
    tau = 10 * ms
    S = Synapses(G, G, "dw/dt = -w / tau : 1 (clock-driven)")
    S.connect(j="i")
    S.w = "i"
    run(10 * ms)
    assert_allclose(S.w[:], np.arange(10) * np.exp(-1))


@pytest.mark.standalone_compatible
def test_synapse_with_run_regularly():
    
    G = NeuronGroup(10, "v : 1", threshold="False")
    tau = 10 * ms
    S = Synapses(G, G, "w : 1", on_pre="v += w")
    S.connect(j="i")
    S.run_regularly("w = i")
    run(defaultclock.dt)
    assert_allclose(S.w[:], np.arange(10))


@pytest.mark.standalone_compatible
def test_synapses_to_synapses():
    source = SpikeGeneratorGroup(3, [0, 1, 2], [0, 0, 0] * ms, period=2 * ms)
    modulator = SpikeGeneratorGroup(3, [0, 2], [1, 3] * ms)
    target = NeuronGroup(3, "v : integer")
    conn = Synapses(source, target, "w : integer", on_pre="v += w")
    conn.connect(j="i")
    conn.w = 1
    modulatory_conn = Synapses(modulator, conn, on_pre="w += 1")
    modulatory_conn.connect(j="i")
    run(5 * ms)
    
    
    assert_array_equal(target.v, [5, 3, 4])


@pytest.mark.standalone_compatible
def test_synapses_to_synapses_connection_array():
    source = SpikeGeneratorGroup(3, [0, 1, 2], [0, 0, 0] * ms, period=2 * ms)
    modulator = SpikeGeneratorGroup(3, [0, 2], [1, 3] * ms)
    target = NeuronGroup(3, "v : integer")
    conn = Synapses(source, target, "w : integer", on_pre="v += w")
    conn.connect(i=[0, 1, 2], j=[0, 1, 2])
    conn.w = 1
    modulatory_conn = Synapses(modulator, conn, on_pre="w += 1")
    modulatory_conn.connect(i=[0, 1, 2], j=[0, 1, 2])
    run(5 * ms)
    
    
    assert_array_equal(target.v, [5, 3, 4])


@pytest.mark.standalone_compatible
def test_synapses_to_synapses_rule_and_array():
    source = SpikeGeneratorGroup(3, [0, 1, 2], [0, 0, 0] * ms, period=2 * ms)
    modulator = SpikeGeneratorGroup(3, [0, 2], [1, 3] * ms)
    target = NeuronGroup(3, "v : integer")
    conn = Synapses(source, target, "w : integer", on_pre="v += w")
    conn.connect(j="i")
    conn.w = 1
    modulatory_conn = Synapses(modulator, conn, on_pre="w += 1")
    
    
    
    with catch_logs() as l:
        modulatory_conn.connect(i=[0, 1, 2], j=[0, 1, 2])
    if isinstance(get_device(), CPPStandaloneDevice):
        assert len(l) == 1
        assert l[0][0] == "WARNING"
        assert l[0][1] == "brian2.synapses.synapses.cannot_check_synapse_indices"
    else:
        assert len(l) == 0
    run(5 * ms)
    
    
    assert_array_equal(target.v, [5, 3, 4])


@pytest.mark.standalone_compatible
def test_synapses_to_synapses_statevar_access():
    source = NeuronGroup(10, "v:1")
    modulator = NeuronGroup(40, "")
    target = NeuronGroup(10, "v:1")
    conn = Synapses(source, target)
    conn.connect(j="i", n=2)
    modulator_to_conn = Synapses(modulator, conn)
    modulator_to_conn.connect(j="int(i/2)")
    conn_to_modulator = Synapses(conn, modulator)
    conn_to_modulator.connect(j="i")
    conn_to_modulator.connect(j="i + 20")
    run(0 * ms)
    assert_equal(modulator_to_conn.i, np.arange(40))
    assert_equal(modulator_to_conn.j, np.repeat(np.arange(20), 2))
    assert_equal(modulator_to_conn.i_post, np.repeat(np.arange(10), 4))
    assert_equal(modulator_to_conn.j_post, np.repeat(np.arange(10), 4))
    assert_equal(conn_to_modulator.i, np.hstack([np.arange(20), np.arange(20)]))
    assert_equal(
        conn_to_modulator.i_pre,
        np.hstack([np.repeat(np.arange(10), 2), np.repeat(np.arange(10), 2)]),
    )
    assert_equal(
        conn_to_modulator.j_pre,
        np.hstack([np.repeat(np.arange(10), 2), np.repeat(np.arange(10), 2)]),
    )
    assert_equal(conn_to_modulator.j, np.arange(40))


@pytest.mark.standalone_compatible
def test_synapses_to_synapses_different_sizes():
    source = NeuronGroup(100, "v : 1", threshold="False")
    source.v = "i"
    modulator = NeuronGroup(1, "v : 1", threshold="False")
    target = NeuronGroup(100, "v : 1")
    target.v = "i + 100"
    conn = Synapses(source, target, "w:1", multisynaptic_index="k")
    conn.connect(j="i", n=2)
    conn.w = "i + j"
    modulatory_conn = Synapses(modulator, conn)
    modulatory_conn.connect("k_post == 1")  
    run(0 * ms)
    assert_allclose(modulatory_conn.w_post, 2 * np.arange(100))


def test_ufunc_at_vectorisation():
    if prefs.codegen.target != "numpy":
        pytest.skip("numpy-only test")
    for code in permutation_analysis_good_examples:
        should_be_able_to_use_ufunc_at = not "NOT_UFUNC_AT_VECTORISABLE" in code
        if should_be_able_to_use_ufunc_at:
            use_ufunc_at_list = [False, True]
        else:
            use_ufunc_at_list = [True]
        code = deindent(code)
        vars = get_identifiers(code)
        vars_src = []
        vars_tgt = []
        vars_syn = []
        vars_shared = []
        vars_const = {}
        for var in vars:
            if var.endswith("_pre"):
                vars_src.append(var[:-4])
            elif var.endswith("_post"):
                vars_tgt.append(var[:-5])
            elif var.endswith("_syn"):
                vars_syn.append(var[:-4])
            elif var.endswith("_shared"):
                vars_shared.append(var[:-7])
            elif var.endswith("_const"):
                vars_const[var[:-6]] = 42
        eqs_src = "\n".join(var + ":1" for var in vars_src)
        eqs_tgt = "\n".join(var + ":1" for var in vars_tgt)
        eqs_syn = "\n".join(var + ":1" for var in vars_syn)
        eqs_syn += "\n" + "\n".join(var + ":1 (shared)" for var in vars_shared)
        origvals = {}
        endvals = {}
        try:
            BrianLogger._log_messages.clear()
            with catch_logs(log_level=logging.INFO) as caught_logs:
                for use_ufunc_at in use_ufunc_at_list:
                    NumpyCodeGenerator._use_ufunc_at_vectorisation = use_ufunc_at
                    src = NeuronGroup(3, eqs_src, threshold="True", name="src")
                    tgt = NeuronGroup(3, eqs_tgt, name="tgt")
                    syn = Synapses(
                        src,
                        tgt,
                        eqs_syn,
                        on_pre=code.replace("_syn", "")
                        .replace("_const", "")
                        .replace("_shared", ""),
                        name="syn",
                        namespace=vars_const,
                    )
                    syn.connect()
                    for G, vars in [(src, vars_src), (tgt, vars_tgt), (syn, vars_syn)]:
                        for var in vars:
                            fullvar = var + G.name
                            if fullvar in origvals:
                                G.state(var)[:] = origvals[fullvar]
                            else:
                                val = rand(len(G))
                                G.state(var)[:] = val
                                origvals[fullvar] = val.copy()
                    Network(src, tgt, syn).run(defaultclock.dt)
                    for G, vars in [(src, vars_src), (tgt, vars_tgt), (syn, vars_syn)]:
                        for var in vars:
                            fullvar = var + G.name
                            val = G.state(var)[:].copy()
                            if fullvar in endvals:
                                assert_allclose(val, endvals[fullvar])
                            else:
                                endvals[fullvar] = val
                numpy_generator_messages = [
                    l
                    for l in caught_logs
                    if l[1] == "brian2.codegen.generators.numpy_generator"
                ]
                if should_be_able_to_use_ufunc_at:
                    assert len(numpy_generator_messages) == 0
                else:
                    assert len(numpy_generator_messages) == 1
                    log_lev, log_mod, log_msg = numpy_generator_messages[0]
                    assert log_msg.startswith("Failed to vectorise code")
        finally:
            NumpyCodeGenerator._use_ufunc_at_vectorisation = True  


def test_fallback_loop_and_stateless_func():
    
    if prefs.codegen.target != "numpy":
        pytest.skip("numpy-only test")
    source = NeuronGroup(2, "", threshold="True")
    target = NeuronGroup(1, "v : 1")
    synapses = Synapses(
        source,
        target,
        "x : 1",
        on_pre="""x = rand()
                                  v_post += 0.5*(1-v_post)""",
    )
    synapses.connect()
    with catch_logs():  
        run(defaultclock.dt)


@pytest.mark.standalone_compatible
def test_synapses_to_synapses_summed_variable():
    source = NeuronGroup(5, "")
    target = NeuronGroup(5, "")
    conn = Synapses(source, target, "w : integer")
    conn.connect(j="i")
    conn.w = 1
    summed_conn = Synapses(
        source,
        conn,
        """
        w_post = x : integer (summed)
        x : integer
        """,
    )
    summed_conn.connect("i>=j")
    summed_conn.x = "i"
    run(defaultclock.dt)
    assert_array_equal(conn.w[:], [10, 10, 9, 7, 4])


@pytest.mark.codegen_independent
def test_synapse_generator_syntax():
    parsed = parse_synapse_generator("k for k in sample(1, N, p=p) if abs(i-k)<10")
    assert parsed["element"] == "k"
    assert parsed["inner_variable"] == "k"
    assert parsed["iterator_func"] == "sample"
    assert parsed["iterator_kwds"]["low"] == "1"
    assert parsed["iterator_kwds"]["high"] == "N"
    assert parsed["iterator_kwds"]["step"] == "1"
    assert parsed["iterator_kwds"]["p"] == "p"
    assert parsed["iterator_kwds"]["size"] is None
    assert parsed["iterator_kwds"]["sample_size"] == "random"
    assert parsed["if_expression"] == "abs(i - k) < 10"
    parsed = parse_synapse_generator("k for k in sample(N, size=5) if abs(i-k)<10")
    assert parsed["element"] == "k"
    assert parsed["inner_variable"] == "k"
    assert parsed["iterator_func"] == "sample"
    assert parsed["iterator_kwds"]["low"] == "0"
    assert parsed["iterator_kwds"]["high"] == "N"
    assert parsed["iterator_kwds"]["step"] == "1"
    assert parsed["iterator_kwds"]["p"] is None
    assert parsed["iterator_kwds"]["size"] == "5"
    assert parsed["iterator_kwds"]["sample_size"] == "fixed"
    assert parsed["if_expression"] == "abs(i - k) < 10"
    parsed = parse_synapse_generator("k+1 for k in range(i-100, i+100, 2)")
    assert parsed["element"] == "k + 1"
    assert parsed["inner_variable"] == "k"
    assert parsed["iterator_func"] == "range"
    assert parsed["iterator_kwds"]["low"] == "i - 100"
    assert parsed["iterator_kwds"]["high"] == "i + 100"
    assert parsed["iterator_kwds"]["step"] == "2"
    assert parsed["if_expression"] == "True"
    with pytest.raises(SyntaxError):
        parse_synapse_generator("mad rubbish")
    with pytest.raises(SyntaxError):
        parse_synapse_generator("k+1")
    with pytest.raises(SyntaxError):
        parse_synapse_generator("k for k in range()")
    with pytest.raises(SyntaxError):
        parse_synapse_generator("k for k in range(1,2,3,4)")
    with pytest.raises(SyntaxError):
        parse_synapse_generator("k for k in range(1,2,3) if ")
    with pytest.raises(SyntaxError):
        parse_synapse_generator("k[1:3] for k in range(1,2,3)")
    with pytest.raises(SyntaxError):
        parse_synapse_generator("k for k in x")
    with pytest.raises(SyntaxError):
        parse_synapse_generator("k for k in x[1:5]")
    with pytest.raises(SyntaxError):
        parse_synapse_generator("k for k in sample()")
    with pytest.raises(SyntaxError):
        parse_synapse_generator("k for k in sample(N, p=0.1, size=5)")
    with pytest.raises(SyntaxError):
        parse_synapse_generator("k for k in sample(N, q=0.1)")


def test_synapse_generator_out_of_range():
    G = NeuronGroup(16, "v : 1")
    G2 = NeuronGroup(4, "v : 1")
    G2.v = "16 + i"

    S1 = Synapses(G, G2, "")
    with pytest.raises(BrianObjectException) as exc:
        S1.connect(j="k for k in range(0, N_post*2)")
        exc.errisinstance(IndexError)

    
    S2 = Synapses(G, G, "")
    S2.connect(j="i+k for k in range(0, 5) if i <= N_post-5")
    expected = np.zeros((len(G), len(G)))
    expected[np.triu_indices(len(G))] = 1
    expected[np.triu_indices(len(G), 5)] = 0
    expected[len(G) - 4 :, :] = 0
    _compare(S2, expected)

    
    S2 = Synapses(G, G, "")
    S2.connect(j="i+k for k in range(0, 5) if i <= N_post-5 and rand() <= 1")
    _compare(S2, expected)

    
    
    
    
    S3 = Synapses(G, G, "")
    with pytest.raises(BrianObjectException) as exc:
        S3.connect(j="i+k for k in range(0, 5) if i <= N_post-5 and v_post >= 0")
    assert exc_isinstance(exc, IndexError)
    assert "outside allowed range" in str(exc.value.__cause__)


@pytest.mark.standalone_compatible
def test_synapse_generator_deterministic():
    "test_connection_string_deterministic" but using the generator
    
    G = NeuronGroup(16, "v : 1")
    G.v = "i"
    G2 = NeuronGroup(4, "v : 1")
    G2.v = "16 + i"

    
    expected_full = np.ones((len(G), len(G2)))

    S1 = Synapses(G, G2)
    S1.connect(j="k for k in range(N_post)")

    
    expected_no_self = np.ones((len(G), len(G))) - np.eye(len(G))

    S2 = Synapses(G, G)
    S2.connect(j="k for k in range(N_post) if k != i")

    S3 = Synapses(G, G)
    
    S3.connect(j="k for k in range(N_post) if j != i")

    S4 = Synapses(G, G)
    S4.connect(j="k for k in range(N_post) if v_post != v_pre")

    
    expected_one_to_one = np.eye(len(G))

    S5 = Synapses(G, G)
    S5.connect(j="k for k in range(N_post) if k == i")  

    S6 = Synapses(G, G)
    
    S6.connect(j="k for k in range(N_post) if j == i")  

    S7 = Synapses(G, G)
    S7.connect(j="k for k in range(N_post) if v_pre == v_post")  

    S8 = Synapses(G, G)
    S8.connect(j="i for _ in range(1)")  

    S9 = Synapses(G, G)
    S9.connect(j="i")  

    with catch_logs() as _:  
        run(0 * ms)  

    _compare(S1, expected_full)
    _compare(S2, expected_no_self)
    _compare(S3, expected_no_self)
    _compare(S4, expected_no_self)
    _compare(S5, expected_one_to_one)
    _compare(S6, expected_one_to_one)
    _compare(S7, expected_one_to_one)
    _compare(S8, expected_one_to_one)
    _compare(S9, expected_one_to_one)


@pytest.mark.standalone_compatible
def test_synapse_generator_deterministic_over_postsynaptic():
    "test_connection_string_deterministic" but using the generator
    
    G = NeuronGroup(16, "v : 1")
    G.v = "i"
    G2 = NeuronGroup(4, "v : 1")
    G2.v = "16 + i"

    
    expected_full = np.ones((len(G), len(G2)))

    S1 = Synapses(G, G2)
    S1.connect(i="k for k in range(N_pre)")

    
    expected_no_self = np.ones((len(G), len(G))) - np.eye(len(G))

    S2 = Synapses(G, G)
    S2.connect(i="k for k in range(N_pre) if k != j")

    S3 = Synapses(G, G)
    
    S3.connect(i="k for k in range(N_pre) if i != j")

    S4 = Synapses(G, G)
    S4.connect(j="k for k in range(N_pre) if v_pre != v_post")

    
    expected_one_to_one = np.eye(len(G))

    S5 = Synapses(G, G)
    S5.connect(i="k for k in range(N_pre) if k == j")  

    S6 = Synapses(G, G)
    
    S6.connect(i="k for k in range(N_pre) if i == j")  

    S7 = Synapses(G, G)
    S7.connect(i="k for k in range(N_pre) if v_pre == v_post")  

    S8 = Synapses(G, G)
    S8.connect(i="j for _ in range(1)")  

    S9 = Synapses(G, G)
    S9.connect(i="j")  

    with catch_logs() as _:  
        run(0 * ms)  

    _compare(S1, expected_full)
    _compare(S2, expected_no_self)
    _compare(S3, expected_no_self)
    _compare(S4, expected_no_self)
    _compare(S5, expected_one_to_one)
    _compare(S6, expected_one_to_one)
    _compare(S7, expected_one_to_one)
    _compare(S8, expected_one_to_one)
    _compare(S9, expected_one_to_one)


@pytest.mark.standalone_compatible
@pytest.mark.long
def test_synapse_generator_deterministic_2():
    "test_connection_string_deterministic" but using the generator
    
    G = NeuronGroup(16, "")
    G2 = NeuronGroup(4, "")
    
    

    
    S10 = Synapses(G, G)
    S10.connect(j="(i + (-1)**k) % N_post for k in range(2)")
    expected_ring = np.zeros((len(G), len(G)), dtype=np.int32)
    expected_ring[np.arange(15), np.arange(15) + 1] = 1  
    expected_ring[np.arange(1, 16), np.arange(15)] = 1  
    expected_ring[[0, 15], [15, 0]] = 1  

    
    S11 = Synapses(G2, G)
    S11.connect(j="i*4 + k for k in range(4)")
    expected_diverging = np.zeros((len(G2), len(G)), dtype=np.int32)
    for source in range(4):
        expected_diverging[source, np.arange(4) + source * 4] = 1

    
    S11b = Synapses(G2, G2)
    S11b.connect(j="k for k in range(i-3, i+4) if i!=k", skip_if_invalid=True)
    expected_diverging_b = np.zeros((len(G2), len(G2)), dtype=np.int32)
    for source in range(len(G2)):
        expected_diverging_b[
            source, np.clip(np.arange(-3, 4) + source, 0, len(G2) - 1)
        ] = 1
        expected_diverging_b[source, source] = 0

    
    S12 = Synapses(G, G2)
    S12.connect(j="int(i/4)")
    expected_converging = np.zeros((len(G), len(G2)), dtype=np.int32)
    for target in range(4):
        expected_converging[np.arange(4) + target * 4, target] = 1

    
    S13 = Synapses(G2, G2)
    S13.connect(j="i+(-1)**k for k in range(2)", skip_if_invalid=True)
    expected_offdiagonal = np.zeros((len(G2), len(G2)), dtype=np.int32)
    expected_offdiagonal[np.arange(len(G2) - 1), np.arange(len(G2) - 1) + 1] = 1
    expected_offdiagonal[np.arange(len(G2) - 1) + 1, np.arange(len(G2) - 1)] = 1

    
    S14 = Synapses(G, G2)
    S14.connect(j="int(i/4) if i % 2 == 0")
    expected_converging_restricted = np.zeros((len(G), len(G2)), dtype=np.int32)
    for target in range(4):
        expected_converging_restricted[np.arange(4, step=2) + target * 4, target] = 1

    
    expected_diagonal = np.zeros((len(G), len(G)), dtype=np.int32)
    expected_diagonal[np.triu_indices(len(G))] = 1
    S15 = Synapses(G, G)
    S15.connect(j="i + k for k in range(0, N_post-i)")

    S15b = Synapses(G, G)
    S15b.connect(j="i + k for k in range(0, N_post)", skip_if_invalid=True)

    S15c = Synapses(G, G)
    S15c.connect(j="i + k for k in range(0, N_post) if j < N_post")

    S15d = Synapses(G, G)
    S15d.connect(j="i + k for k in range(0, N_post) if i + k < N_post")

    with catch_logs() as _:  
        run(0 * ms)  

    _compare(S10, expected_ring)
    _compare(S11, expected_diverging)
    _compare(S11b, expected_diverging_b)
    _compare(S12, expected_converging)
    _compare(S13, expected_offdiagonal)
    _compare(S14, expected_converging_restricted)
    _compare(S15, expected_diagonal)
    _compare(S15b, expected_diagonal)
    _compare(S15c, expected_diagonal)
    _compare(S15d, expected_diagonal)


@pytest.mark.standalone_compatible
def test_synapse_generator_random():
    
    
    G = NeuronGroup(4, "x : integer")
    G.x = "i"
    G2 = NeuronGroup(7, "")

    S1 = Synapses(G, G2)
    S1.connect(j="k for k in sample(N_post, p=0)")

    S2 = Synapses(G, G2)
    S2.connect(j="k for k in sample(N_post, p=1)")

    
    S3 = Synapses(G, G2)
    S3.connect(j="k for k in sample(N_post, p=0.3)")

    "stochastic" connections that are
    
    S4 = Synapses(G, G2)
    S4.connect(j="k for k in sample(N_post, p=int(x_pre==2)*1.0)")

    with catch_logs() as _:  
        run(0 * ms)  

    assert len(S1) == 0
    _compare(S2, np.ones((len(G), len(G2))))
    assert 0 <= len(S3) <= len(G) * len(G2)
    assert len(S4) == 7
    assert_equal(S4.i, np.ones(7) * 2)
    assert_equal(S4.j, np.arange(7))


@pytest.mark.standalone_compatible
def test_synapse_generator_random_over_postsynaptic():
    
    
    G = NeuronGroup(4, "")
    G2 = NeuronGroup(7, "y : 1")
    G2.y = "i"

    S1 = Synapses(G, G2)
    S1.connect(i="k for k in sample(N_pre, p=0)")

    S2 = Synapses(G, G2)
    S2.connect(i="k for k in sample(N_pre, p=1)")

    
    S3 = Synapses(G, G2)
    S3.connect(i="k for k in sample(N_pre, p=0.3)")

    "stochastic" connections that are
    
    S4 = Synapses(G, G2)
    S4.connect(i="k for k in sample(N_pre, p=int(y_post==2)*1.0)")

    with catch_logs() as _:  
        run(0 * ms)  

    assert len(S1) == 0
    _compare(S2, np.ones((len(G), len(G2))))
    assert 0 <= len(S3) <= len(G) * len(G2)
    assert len(S4) == 4
    assert_equal(S4.i, np.arange(4))
    assert_equal(S4.j, np.ones(4) * 2)


@pytest.mark.standalone_compatible
def test_synapse_generator_random_positive_steps():
    
    G = NeuronGroup(4, "x : integer")
    G.x = "i"
    G2 = NeuronGroup(7, "")

    S1 = Synapses(G, G2)
    S1.connect(j="k for k in sample(2, N_post, 2, p=0)")

    S2 = Synapses(G, G2)
    S2.connect(j="k for k in sample(2, N_post, 2, p=1)")

    
    "jump method", so
    
    S3 = Synapses(G, G2)
    S3.connect(j="k for k in sample(2, N_post, 2, p=0.2)")

    S3b = Synapses(G, G2)
    S3b.connect(j="k for k in sample(2, N_post, 2, p=0.3)")

    "stochastic" connections that are
    
    S4 = Synapses(G, G2)
    S4.connect(j="k for k in sample(2, N_post, 2, p=int(x_pre==2)*1.0)")

    with catch_logs() as _:  
        run(0 * ms)  

    assert len(S1) == 0
    S2_comp = np.zeros((len(G), len(G2)))
    S2_comp[:, 2::2] = 1
    _compare(S2, S2_comp)
    assert 0 <= len(S3) <= len(G) * 3
    assert all(S3.j[:] % 2 == 0)
    assert all(S3.j >= 2)
    assert 0 <= len(S3b) <= len(G) * 3
    assert all(S3b.j[:] % 2 == 0)
    assert all(S3b.j >= 2)
    assert len(S4) == 3
    assert_equal(S4.i, np.ones(3) * 2)
    assert_equal(S4.j, np.arange(2, 7, 2))


@pytest.mark.standalone_compatible
def test_synapse_generator_random_negative_steps():
    
    
    G = NeuronGroup(4, "x : integer")
    G.x = "i"
    G2 = NeuronGroup(7, "")

    S1 = Synapses(G, G2)
    S1.connect(j="k for k in sample(N_post-1, 0, -2, p=0)")

    S2 = Synapses(G, G2)
    S2.connect(j="k for k in sample(N_post-1, 0, -2, p=1)")

    
    "jump method", so
    
    S3 = Synapses(G, G2)
    S3.connect(j="k for k in sample(N_post-1, 0, -2, p=0.2)")

    S3b = Synapses(G, G2)
    S3b.connect(j="k for k in sample(N_post-1, 0, -2, p=0.3)")

    "stochastic" connections that are
    
    S4 = Synapses(G, G2)
    S4.connect(j="k for k in sample(N_post-1, 0, -2, p=int(x_pre==2)*1.0)")

    with catch_logs() as _:  
        run(0 * ms)  

    assert len(S1) == 0
    S2_comp = np.zeros((len(G), len(G2)))
    S2_comp[:, 2::2] = 1
    _compare(S2, S2_comp)
    assert 0 <= len(S3) <= len(G) * 3
    assert all(S3.j[:] % 2 == 0)
    assert all(S3.j >= 2)
    assert 0 <= len(S3b) <= len(G) * 3
    assert all(S3b.j[:] % 2 == 0)
    assert all(S3b.j >= 2)
    assert len(S4) == 3
    assert_array_equal(S4.i, np.ones(3) * 2)
    assert_array_equal(S4.j, [6, 4, 2])


@pytest.mark.standalone_compatible
def test_synapse_generator_fixed_random():
    
    G = NeuronGroup(4, "x : integer")
    G.x = "i"
    G2 = NeuronGroup(7, "")

    S1 = Synapses(G, G2)
    S1.connect(j="k for k in sample(N_post, size=0)")

    S2 = Synapses(G, G2)
    S2.connect(j="k for k in sample(N_post, size=N_post)")

    S3 = Synapses(G, G2)
    S3.connect(j="k for k in sample(N_post, size=3)")

    "stochastic" connections that are
    
    S4 = Synapses(G, G2)
    S4.connect(j="k for k in sample(N_post, size=int(x_pre==2)*N_post)")

    with catch_logs() as _:  
        run(0 * ms)  

    assert len(S1) == 0
    _compare(S2, np.ones((len(G), len(G2))))
    
    assert_array_equal(S3.N_outgoing_pre, np.ones(4) * 3)
    
    for source_idx in range(4):
        assert len(set(S3.j[source_idx, :])) == 3
        assert all(S3.j[source_idx, :] == sorted(S3.j[source_idx, :]))
    assert len(S4) == 7
    assert_equal(S4.i, np.ones(7) * 2)
    assert_equal(S4.j, np.arange(7))


@pytest.mark.standalone_compatible
def test_synapse_generator_fixed_random_over_postsynaptic():
    
    G = NeuronGroup(4, "")
    G2 = NeuronGroup(7, "y : integer")
    G2.y = "i"

    S1 = Synapses(G, G2)
    S1.connect(i="k for k in sample(N_pre, size=0)")

    S2 = Synapses(G, G2)
    S2.connect(i="k for k in sample(N_pre, size=N_pre)")

    S3 = Synapses(G, G2)
    S3.connect(i="k for k in sample(N_pre, size=3)")

    "stochastic" connections that are
    
    S4 = Synapses(G, G2)
    S4.connect(i="k for k in sample(N_pre, size=int(y_post==2)*N_pre)")

    with catch_logs() as _:  
        run(0 * ms)  

    assert len(S1) == 0
    _compare(S2, np.ones((len(G), len(G2))))
    
    assert_array_equal(S3.N_incoming_post, np.ones(7) * 3)
    
    for target_idx in range(7):
        assert len(set(S3.i[:, target_idx])) == 3
        assert all(S3.i[:, target_idx] == sorted(S3.i[:, target_idx]))
    assert len(S4) == 4
    assert_equal(S4.j, np.ones(4) * 2)
    assert_equal(S4.i, np.arange(4))


@pytest.mark.standalone_compatible
def test_synapse_generator_fixed_random_positive_steps():
    
    
    G = NeuronGroup(4, "x : integer")
    G.x = "i"
    G2 = NeuronGroup(7, "")

    S1 = Synapses(G, G2)
    S1.connect(j="k for k in sample(2, N_post, 2, size=0)")

    S2 = Synapses(G, G2)
    S2.connect(j="k for k in sample(2, N_post, 2, size=3)")

    
    S3 = Synapses(G, G2)
    S3.connect(j="k for k in sample(2, N_post, 2, size=2)")

    "stochastic" connections that are
    
    S4 = Synapses(G, G2)
    S4.connect(j="k for k in sample(2, N_post, 2, size=int(x_pre==2)*3)")

    with catch_logs() as _:  
        run(0 * ms)  

    assert len(S1) == 0
    S2_comp = np.zeros((len(G), len(G2)))
    S2_comp[:, 2::2] = 1
    _compare(S2, S2_comp)
    assert len(S3) == len(G) * 2
    assert all(S3.N_outgoing_pre == 2)
    assert all(S3.j[:] % 2 == 0)
    assert all(S3.j >= 2)
    assert all([len(S3.j[x, :]) == len(set(S3.j[x, :])) for x in range(len(G))])
    assert len(S4) == 3
    assert_equal(S4.i, np.ones(3) * 2)
    assert_equal(S4.j, np.arange(2, 7, 2))


@pytest.mark.standalone_compatible
def test_synapse_generator_fixed_random_negative_steps():
    
    
    G = NeuronGroup(4, "x : integer")
    G.x = "i"
    G2 = NeuronGroup(7, "")

    S1 = Synapses(G, G2)
    S1.connect(j="k for k in sample(N_post-1, 0, -2, size=0)")

    S2 = Synapses(G, G2)
    S2.connect(j="k for k in sample(N_post-1, 0, -2, size=3)")

    
    S3 = Synapses(G, G2)
    S3.connect(j="k for k in sample(N_post-1, 0, -2, size=2)")

    "stochastic" connections that are
    
    S4 = Synapses(G, G2, "w:1")
    S4.connect(j="k for k in sample(N_post-1, 0, -2, size=int(x_pre==2)*3)")

    with catch_logs() as _:  
        run(0 * ms)  

    assert len(S1) == 0
    S2_comp = np.zeros((len(G), len(G2)))
    S2_comp[:, 2::2] = 1
    _compare(S2, S2_comp)
    assert len(S3) == len(G) * 2
    assert all(S3.N_outgoing_pre == 2)
    assert all(S3.j[:] % 2 == 0)
    assert all(S3.j >= 2)
    assert all([len(S3.j[x, :]) == len(set(S3.j[x, :])) for x in range(len(G))])
    assert len(S4) == 3
    assert_equal(S4.i, np.ones(3) * 2)
    assert_equal(S4.j, np.arange(6, 0, -2))


@pytest.mark.standalone_compatible
def test_synapse_generator_fixed_random_error1():
    G = NeuronGroup(5, "")
    G2 = NeuronGroup(7, "")
    S = Synapses(G, G2)
    with pytest.raises((BrianObjectException, IndexError, RuntimeError)):
        
        S.connect(j="k for k in sample(N_post, size=i+4)")
        run(0 * ms)  


@pytest.mark.standalone_compatible
def test_synapse_generator_fixed_random_error2():
    G = NeuronGroup(5, "")
    G2 = NeuronGroup(7, "")
    S = Synapses(G, G2)
    with pytest.raises((BrianObjectException, IndexError, RuntimeError)):
        
        S.connect(j="k for k in sample(N_post, size=3-i)")
        run(0 * ms)  


@pytest.mark.standalone_compatible
def test_synapse_generator_fixed_random_skip_if_invalid():
    G = NeuronGroup(5, "")
    G2 = NeuronGroup(7, "")
    S1 = Synapses(G, G2)
    S2 = Synapses(G, G2)
    
    S1.connect(j="k for k in sample(N_post, size=i+4)", skip_if_invalid=True)
    
    S2.connect(j="k for k in sample(N_post, size=3-i)", skip_if_invalid=True)
    run(0 * ms)  
    assert_array_equal(S1.N_outgoing_pre, [4, 5, 6, 7, 7])
    assert_array_equal(S2.N_outgoing_pre, [3, 2, 1, 0, 0])


@pytest.mark.standalone_compatible
def test_synapse_generator_random_with_condition():
    G = NeuronGroup(4, "")

    S1 = Synapses(G, G)
    S1.connect(j="k for k in sample(N_post, p=0) if i != k")

    S2 = Synapses(G, G)
    S2.connect(j="k for k in sample(N_post, p=1) if i != k")
    expected2 = np.ones((len(G), len(G))) - np.eye(len(G))

    S3 = Synapses(G, G)
    S3.connect(j="k for k in sample(N_post, p=0) if i >= 2")

    S4 = Synapses(G, G)
    S4.connect(j="k for k in sample(N_post, p=1.0) if i >= 2")
    expected4 = np.zeros((len(G), len(G)))
    expected4[2, :] = 1
    expected4[3, :] = 1

    S5 = Synapses(G, G)
    S5.connect(j="k for k in sample(N_post, p=0) if j < 2")  

    S6 = Synapses(G, G)
    S6.connect(j="k for k in sample(2, p=0)")  

    S7 = Synapses(G, G)
    expected7 = np.zeros((len(G), len(G)))
    expected7[:, 0] = 1
    expected7[:, 1] = 1
    S7.connect(j="k for k in sample(N_post, p=1.0) if j < 2")  

    S8 = Synapses(G, G)
    S8.connect(j="k for k in sample(2, p=1.0)")  

    with catch_logs() as _:  
        run(0 * ms)  

    assert len(S1) == 0
    _compare(S2, expected2)
    assert len(S3) == 0
    _compare(S4, expected4)
    assert len(S5) == 0
    assert len(S6) == 0
    _compare(S7, expected7)
    _compare(S8, expected7)


@pytest.mark.standalone_compatible
@pytest.mark.long
def test_synapse_generator_random_with_condition_2():
    G = NeuronGroup(4, "")

    
    
    S9 = Synapses(G, G)
    S9.connect(j="k for k in sample(N_post, p=0.001) if i != k")

    S10 = Synapses(G, G)
    S10.connect(j="k for k in sample(N_post, p=0.03) if i != k")

    S11 = Synapses(G, G)
    S11.connect(j="k for k in sample(N_post, p=0.1) if i != k")

    S12 = Synapses(G, G)
    S12.connect(j="k for k in sample(N_post, p=0.9) if i != k")

    S13 = Synapses(G, G)
    S13.connect(j="k for k in sample(N_post, p=0.001) if i >= 2")

    S14 = Synapses(G, G)
    S14.connect(j="k for k in sample(N_post, p=0.03) if i >= 2")

    S15 = Synapses(G, G)
    S15.connect(j="k for k in sample(N_post, p=0.1) if i >= 2")

    S16 = Synapses(G, G)
    S16.connect(j="k for k in sample(N_post, p=0.9) if i >= 2")

    S17 = Synapses(G, G)
    S17.connect(j="k for k in sample(N_post, p=0.001) if j < 2")

    S18 = Synapses(G, G)
    S18.connect(j="k for k in sample(N_post, p=0.03) if j < 2")

    S19 = Synapses(G, G)
    S19.connect(j="k for k in sample(N_post, p=0.1) if j < 2")

    S20 = Synapses(G, G)
    S20.connect(j="k for k in sample(N_post, p=0.9) if j < 2")

    S21 = Synapses(G, G)
    S21.connect(j="k for k in sample(2, p=0.001)")

    S22 = Synapses(G, G)
    S22.connect(j="k for k in sample(2, p=0.03)")

    S23 = Synapses(G, G)
    S23.connect(j="k for k in sample(2, p=0.1)")

    S24 = Synapses(G, G)
    S24.connect(j="k for k in sample(2, p=0.9)")

    
    S25 = Synapses(G, G)
    S25.connect(j="i+1 for _ in sample(1, p=0.5) if i < N_post-1")

    S26 = Synapses(G, G)
    S26.connect(j="i+k for k in sample(N_post-i, p=0.5)")

    with catch_logs() as _:  
        run(0 * ms)  

    assert not any(S9.i == S9.j)
    assert 0 <= len(S9) <= len(G) * (len(G) - 1)
    assert not any(S10.i == S10.j)
    assert 0 <= len(S10) <= len(G) * (len(G) - 1)
    assert not any(S11.i == S11.j)
    assert 0 <= len(S11) <= len(G) * (len(G) - 1)
    assert not any(S12.i == S12.j)
    assert 0 <= len(S12) <= len(G) * (len(G) - 1)
    assert all(S13.i[:] >= 2)
    assert 0 <= len(S13) <= len(G) * (len(G) - 1)
    assert all(S14.i[:] >= 2)
    assert 0 <= len(S14) <= len(G) * (len(G) - 1)
    assert all(S15.i[:] >= 2)
    assert 0 <= len(S15) <= len(G) * (len(G) - 1)
    assert all(S16.i[:] >= 2)
    assert 0 <= len(S16) <= len(G) * (len(G) - 1)
    assert all(S17.j[:] < 2)
    assert 0 <= len(S17) <= len(G) * (len(G) - 1)
    assert all(S18.j[:] < 2)
    assert 0 <= len(S18) <= len(G) * (len(G) - 1)
    assert all(S19.j[:] < 2)
    assert 0 <= len(S19) <= len(G) * (len(G) - 1)
    assert all(S20.j[:] < 2)
    assert 0 <= len(S20) <= len(G) * (len(G) - 1)
    assert all(S21.j[:] < 2)
    assert 0 <= len(S21) <= len(G) * (len(G) - 1)
    assert all(S22.j[:] < 2)
    assert 0 <= len(S22) <= len(G) * (len(G) - 1)
    assert all(S23.j[:] < 2)
    assert 0 <= len(S23) <= len(G) * (len(G) - 1)
    assert all(S24.j[:] < 2)
    assert 0 <= len(S24) <= len(G) * (len(G) - 1)
    assert 0 <= len(S25) <= len(G)
    assert_equal(S25.j[:], S25.i[:] + 1)
    assert 0 <= len(S26) <= (1 + len(G)) * (len(G) / 2)
    assert all(S26.j[:] >= S26.i[:])


@pytest.mark.standalone_compatible
def test_synapses_refractory():
    source = NeuronGroup(10, "", threshold="True")
    target = NeuronGroup(
        10,
        "dv/dt = 0/second : 1 (unless refractory)",
        threshold="i>=5",
        refractory=defaultclock.dt,
    )
    S = Synapses(source, target, on_pre="v += 1")
    S.connect(j="i")
    run(defaultclock.dt + schedule_propagation_offset())
    assert_allclose(target.v[:5], 1)
    assert_allclose(target.v[5:], 0)


@pytest.mark.standalone_compatible
def test_synapses_refractory_rand():
    source = NeuronGroup(10, "", threshold="True")
    target = NeuronGroup(
        10,
        "dv/dt = 0/second : 1 (unless refractory)",
        threshold="i>=5",
        refractory=defaultclock.dt,
    )
    S = Synapses(source, target, on_pre="v += rand()")
    S.connect(j="i")
    with catch_logs() as _:
        
        
        
        
        run(defaultclock.dt + schedule_propagation_offset())
    assert all(target.v[:5] > 0)
    assert_allclose(target.v[5:], 0)


@pytest.mark.codegen_independent
def test_synapse_generator_range_noint():
    
    G = NeuronGroup(42, "")
    S = Synapses(G, G)
    msg = (
        r"The '{}' argument of the range function was .+, but it needs to be an"
        r" integer\."
    )
    with pytest.raises(TypeError, match=msg.format("high")):
        S.connect(j="k for k in range(42.0)")
    with pytest.raises(TypeError, match=msg.format("low")):
        S.connect(j="k for k in range(0.0, 42)")
    with pytest.raises(TypeError, match=msg.format("high")):
        S.connect(j="k for k in range(0, 42.0)")
    with pytest.raises(TypeError, match=msg.format("step")):
        S.connect(j="k for k in range(0, 42, 1.0)")
    with pytest.raises(TypeError, match=msg.format("low")):
        S.connect(j="k for k in range(True, 42)")
    with pytest.raises(TypeError, match=msg.format("high")):
        S.connect(j="k for k in range(0, True)")
    with pytest.raises(TypeError, match=msg.format("step")):
        S.connect(j="k for k in range(0, 42, True)")


@pytest.mark.codegen_independent
def test_missing_lastupdate_error_syn_pathway():
    G = NeuronGroup(1, "v : 1", threshold="False")
    S = Synapses(G, G, on_pre="v += exp(-lastupdate/dt)")
    S.connect()
    with pytest.raises(BrianObjectException) as exc:
        run(0 * ms)
    assert exc_isinstance(exc, KeyError)
    assert "lastupdate = t" in str(exc.value.__cause__)
    assert "lastupdate : second" in str(exc.value.__cause__)


@pytest.mark.codegen_independent
def test_missing_lastupdate_error_run_regularly():
    G = NeuronGroup(1, "v : 1")
    S = Synapses(G, G)
    S.connect()
    S.run_regularly("v += exp(-lastupdate/dt")
    with pytest.raises(BrianObjectException) as exc:
        run(0 * ms)
    assert exc_isinstance(exc, KeyError)
    assert "lastupdate = t" in str(exc.value.__cause__)
    assert "lastupdate : second" in str(exc.value.__cause__)


@pytest.mark.codegen_independent
def test_synaptic_subgroups():
    source = NeuronGroup(5, "")
    target = NeuronGroup(3, "")
    syn = Synapses(source, target)
    syn.connect()
    assert len(syn) == 15

    from_3 = syn[3, :]
    assert len(from_3) == 3
    assert all(syn.i[from_3] == 3)
    assert_array_equal(syn.j[from_3], np.arange(3))

    to_2 = syn[:, 2]
    assert len(to_2) == 5
    assert all(syn.j[to_2] == 2)
    assert_array_equal(syn.i[to_2], np.arange(5))

    mixed = syn[1:3, :2]
    assert len(mixed) == 4
    connections = {(i, j) for i, j in zip(syn.i[mixed], syn.j[mixed])}
    assert connections == {(1, 0), (1, 1), (2, 0), (2, 1)}


@pytest.mark.codegen_independent
def test_incorrect_connect_N_incoming_outgoing():
    
    source = NeuronGroup(5, "")
    target = NeuronGroup(3, "")
    syn = Synapses(source, target)

    with pytest.raises(ValueError) as ex:
        syn.connect("N_incoming < 5")
        assert "N_incoming" in str(ex)

    with pytest.raises(ValueError) as ex:
        syn.connect("N_outgoing < 5")
        assert "N_outgoing" in str(ex)


@pytest.mark.codegen_independent
def test_setting_from_weight_matrix():
    
    
    weights = np.array([[1, 2, 3], [4, 5, 6]])

    source = NeuronGroup(2, "")
    target = NeuronGroup(3, "")

    syn = Synapses(source, target, "w : 1")
    syn.connect()
    syn.w[:] = weights.flatten()

    for (i, j), w in np.ndenumerate(weights):
        assert all(syn.w[i, j] == weights[i, j])


if __name__ == "__main__":
    SANITY_CHECK_PERMUTATION_ANALYSIS_EXAMPLE = True
    
    
    import time

    from _pytest.outcomes import Skipped

    from brian2 import prefs

    start = time.time()

    test_creation()
    test_name_clashes()
    test_incoming_outgoing()
    test_connection_string_deterministic_full()
    test_connection_string_deterministic_full_no_self()
    test_connection_string_deterministic_full_one_to_one()
    test_connection_string_deterministic_full_custom()
    test_connection_string_deterministic_multiple_and()
    test_connection_random_with_condition()
    test_connection_random_with_condition_2()
    test_connection_random_without_condition()
    test_connection_random_with_indices()
    test_connection_multiple_synapses()
    test_connection_arrays()
    reinit_and_delete()
    test_state_variable_assignment()
    test_state_variable_indexing()
    test_indices()
    test_subexpression_references()
    test_nested_subexpression_references()
    test_constant_variable_subexpression_in_synapses()
    test_equations_unit_check()
    test_delay_specification()
    test_delays_pathways()
    test_delays_pathways_subgroups()
    test_pre_before_post()
    test_pre_post_simple()
    test_transmission_simple()
    test_transmission_custom_event()
    test_invalid_custom_event()
    test_transmission()
    test_transmission_all_to_one_heterogeneous_delays()
    test_transmission_one_to_all_heterogeneous_delays()
    test_transmission_scalar_delay()
    test_transmission_scalar_delay_different_clocks()
    test_transmission_boolean_variable()
    test_clocks()
    test_changed_dt_spikes_in_queue()
    test_no_synapses()
    test_no_synapses_variable_write()
    test_summed_variable()
    test_summed_variable_pre_and_post()
    test_summed_variable_differing_group_size()
    test_summed_variable_errors()
    test_multiple_summed_variables()
    test_summed_variables_subgroups()
    test_summed_variables_overlapping_subgroups()
    test_summed_variables_linked_variables()
    test_scalar_parameter_access()
    test_scalar_subexpression()
    test_sim_with_scalar_variable()
    test_sim_with_scalar_subexpression()
    test_sim_with_constant_subexpression()
    test_external_variables()
    test_event_driven()
    test_event_driven_dependency_error()
    test_event_driven_dependency_error2()
    test_event_driven_dependency_error3()
    test_repr()
    test_pre_post_variables()
    test_variables_by_owner()
    test_permutation_analysis()
    test_vectorisation()
    test_vectorisation_STDP_like()
    test_synaptic_equations()
    test_synapse_with_run_regularly()
    test_synapses_to_synapses()
    test_synapses_to_synapses_statevar_access()
    test_synapses_to_synapses_different_sizes()
    test_synapses_to_synapses_summed_variable()
    try:
        test_ufunc_at_vectorisation()
        test_fallback_loop_and_stateless_func()
    except Skipped:
        print("Skipping numpy-only test")
    test_synapse_generator_syntax()
    test_synapse_generator_out_of_range()
    test_synapse_generator_deterministic()
    test_synapse_generator_deterministic_2()
    test_synapse_generator_random()
    test_synapse_generator_random_with_condition()
    test_synapse_generator_random_with_condition_2()
    test_synapses_refractory()
    test_synapses_refractory_rand()
    test_synapse_generator_range_noint()
    test_missing_lastupdate_error_syn_pathway()
    test_missing_lastupdate_error_run_regularly()
    test_synaptic_subgroups()
    test_incorrect_connect_N_incoming_outgoing()
    test_setting_from_weight_matrix()
    print("Tests took", time.time() - start)
