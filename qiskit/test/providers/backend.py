# -*- coding: utf-8 -*-

# Copyright 2019, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

"""Base TestCase for testing backends."""

from unittest import SkipTest

from qiskit.tools.compiler import compile  # pylint: disable=redefined-builtin
from ..base import QiskitTestCase
from ..reference_circuits import ReferenceCircuits


class BackendTestCase(QiskitTestCase):
    """Test case for backends.

    Implementers of backends are encouraged to subclass and customize this
    TestCase, as it contains a "canonical" series of tests in order to ensure
    the backend functionality matches the specifications.

    Members:
        backend_cls (BaseBackend): backend to be used in this test case. Its
            instantiation can be further customized by overriding the
            ``_get_backend`` function.
        circuit (QuantumCircuit): circuit to be used for the tests.
    """
    backend_cls = None
    circuit = ReferenceCircuits.bell()

    def setUp(self):
        super().setUp()
        self.backend = self._get_backend()

    @classmethod
    def setUpClass(cls):
        if cls is BackendTestCase:
            raise SkipTest('Skipping base class tests')
        super().setUpClass()

    def _get_backend(self):
        """Return an instance of a Provider."""
        return self.backend_cls()  # pylint: disable=not-callable

    def test_configuration(self):
        """Test backend.configuration()."""
        configuration = self.backend.configuration()
        return configuration

    def test_properties(self):
        """Test backend.properties()."""
        properties = self.backend.properties()
        if self.backend.configuration().simulator:
            self.assertEqual(properties, None)
        return properties

    def test_status(self):
        """Test backend.status()."""
        status = self.backend.status()
        return status

    def test_run_circuit(self):
        """Test running a single circuit."""
        qobj = compile(self.circuit, self.backend)
        job = self.backend.run(qobj)
        result = job.result()
        self.assertEqual(result.success, True)
        return result
