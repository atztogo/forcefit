import unittest
import numpy as np

from phonopy.interface.phonopy_yaml import get_unitcell_from_phonopy_yaml
from phonopy.structure.cells import get_supercell
from phonopy.structure.symmetry import Symmetry
from force_fit.fc2 import FC2allFit
from phonopy.interface.vasp import read_vasp, read_XDATCAR

class TestFC2allFit(unittest.TestCase):

    def setUp(self):
        self._symprec = 1e-5

    
    def tearDown(self):
        pass
    
    def test_search_operations(self):
        self._set_cell_NaCl()
        self.assertTrue(self._fc2allfit._search_operations())

    def test_get_displacements(self):
        scell = read_vasp("POSCAR-Si")
        scells_with_disps, lattice = read_XDATCAR(filename="XDATCAR-Si-2fs")
        symmetry = Symmetry(scell, symprec=self._symprec)
        fc2allfit = FC2allFit(scell,
                              scells_with_disps,
                              symmetry)
        for i in range(len(scells_with_disps)):
            disps = fc2allfit._get_displacements(i)
            self.assertTrue((np.abs(disps.ravel()) < 1e-1).all())
                


    def _set_cell_NaCl(self):
        filename = "../phonopy/NaCl.yaml"
        self._cell = get_unitcell_from_phonopy_yaml(filename)
        self._scell = get_supercell(self._cell,
                                    np.diag([2, 2, 2]),
                                    symprec=self._symprec)
        self._symmetry = Symmetry(self._scell, symprec=self._symprec)
        self._fc2allfit = FC2allFit(self._scell,
                                    None,
                                    self._symmetry)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFC2allFit)
    unittest.TextTestRunner(verbosity=2).run(suite)
    # unittest.main()
