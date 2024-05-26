from rdkit import Chem
from rdkit.Chem.SaltRemover import SaltRemover
from rdkit.Chem.rdmolfiles import MolFromSmarts, MolFromSmiles


mol = MolFromSmiles("NCCCCC[PH](c1ccccc1)(c1ccccc1)c1ccccc1")
for atom in mol.GetAtoms():
    atom_index = atom.GetIdx()  # Atom index
    atomic_number = atom.GetAtomicNum()  # Atomic number
    symbol = atom.GetSymbol()  # Element symbol
    atom_type = atom.GetAtomicNum()  # Atom type (same as atomic number in this example)
    formal_charge = atom.GetFormalCharge()  # Formal charge
    hybridization = atom.GetHybridization()  # Hybridization
    num_explicit_hs = atom.GetNumExplicitHs()  # Number of explicit hydrogens
    num_implicit_hs = atom.GetNumImplicitHs()  # Number of implicit hydrogens
    is_aromatic = atom.GetIsAromatic()  # Aromaticity

    print(f"Atom {atom_index}: {symbol} (Atomic number: {atomic_number}, Atom type: {atom_type})")