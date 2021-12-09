import pytest


class TestProva:
    def setup(self):
        # this is called as an `__init__()`
        self.p = 4

    def test_prova(self):
        pp = self.p**2
        assert pp == 16

    def test_prova2(self):
        ok = "ciao"
        assert ok == "ciao"
