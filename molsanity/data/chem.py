"""Reconstruct RDKit molecules from MUTAG-style PyG graphs.

TUDataset/MUTAG ships one-hot atom and bond labels but no SMILES. To run
RDKit-native motif decomposition, Bemis-Murcko scaffolds, and publication-grade
rendering we reconstruct an RDKit molecule from the graph labels.

MUTAG label conventions (Debnath et al. 1991 / TU Dortmund collection):
  atom index -> symbol : 0=C 1=N 2=O 3=F 4=I 5=Cl 6=Br
  bond index -> type   : 0=aromatic 1=single 2=double 3=triple
"""
from __future__ import annotations

from typing import Optional

MUTAG_ATOMS = ["C", "N", "O", "F", "I", "Cl", "Br"]
MUTAG_BONDS = ["aromatic", "single", "double", "triple"]

_RDKIT_LOGS_SILENCED = False


def _silence_rdkit() -> None:
    global _RDKIT_LOGS_SILENCED
    if not _RDKIT_LOGS_SILENCED:
        from rdkit import RDLogger

        RDLogger.DisableLog("rdApp.*")
        _RDKIT_LOGS_SILENCED = True


def _normalise_nitro(rw) -> None:
    """Fix nitro groups so the mol sanitises: N(=O)=O -> [N+](=O)[O-].

    MUTAG encodes nitro nitrogens with a valence RDKit rejects. We detect an N
    bonded to >= 2 O and rewrite it to the charge-separated canonical nitro.
    """
    from rdkit import Chem
    from rdkit.Chem import BondType

    for atom in rw.GetAtoms():
        if atom.GetSymbol() != "N":
            continue
        o_neighbors = [nb for nb in atom.GetNeighbors() if nb.GetSymbol() == "O"]
        if len(o_neighbors) < 2:
            continue
        atom.SetIsAromatic(False)
        atom.SetFormalCharge(1)
        # First O double-bonded (neutral), second O single-bonded (negative).
        for i, o in enumerate(o_neighbors[:2]):
            bond = rw.GetBondBetweenAtoms(atom.GetIdx(), o.GetIdx())
            o.SetIsAromatic(False)
            if i == 0:
                bond.SetBondType(BondType.DOUBLE)
                o.SetFormalCharge(0)
            else:
                bond.SetBondType(BondType.SINGLE)
                o.SetFormalCharge(-1)


def mutag_atom_symbols(data) -> list[str]:
    idx = data.x.argmax(dim=1).tolist()
    return [MUTAG_ATOMS[i] for i in idx]


def graph_to_mol(data, atom_symbols: Optional[list[str]] = None):
    """Build an RDKit mol from a MUTAG-style graph. Returns (mol, atom_symbols).

    Robust to sanitisation failure: we always return a molecule with correct
    connectivity even if full aromaticity perception fails, so structural motif
    (ring) detection still works.
    """
    from rdkit import Chem
    from rdkit.Chem import BondType

    _silence_rdkit()
    if atom_symbols is None:
        atom_symbols = mutag_atom_symbols(data)

    rw = Chem.RWMol()
    for sym in atom_symbols:
        rw.AddAtom(Chem.Atom(sym))

    bond_type_map = {
        0: BondType.AROMATIC,
        1: BondType.SINGLE,
        2: BondType.DOUBLE,
        3: BondType.TRIPLE,
    }

    ei = data.edge_index
    ea = data.edge_attr
    seen = set()
    for k in range(ei.size(1)):
        a, b = int(ei[0, k]), int(ei[1, k])
        if a == b:
            continue
        key = (min(a, b), max(a, b))
        if key in seen:
            continue
        seen.add(key)
        btype = int(ea[k].argmax()) if ea is not None else 1
        bt = bond_type_map.get(btype, BondType.SINGLE)
        rw.AddBond(a, b, bt)
        if bt == BondType.AROMATIC:
            rw.GetAtomWithIdx(a).SetIsAromatic(True)
            rw.GetAtomWithIdx(b).SetIsAromatic(True)

    _normalise_nitro(rw)
    mol = rw.GetMol()
    try:
        Chem.SanitizeMol(mol)
    except Exception:
        # Partial sanitise: keep ring info + symmetry so decomposition works.
        try:
            Chem.SanitizeMol(
                mol,
                sanitizeOps=Chem.SanitizeFlags.SANITIZE_SYMMRINGS
                | Chem.SanitizeFlags.SANITIZE_SETCONJUGATION
                | Chem.SanitizeFlags.SANITIZE_SETHYBRIDIZATION,
            )
        except Exception:
            pass
    return mol, atom_symbols


def mol_to_smiles(mol) -> Optional[str]:
    from rdkit import Chem

    try:
        return Chem.MolToSmiles(mol)
    except Exception:
        return None


def mol_from_data(data):
    """Return an RDKit mol for a graph, dataset-agnostically.

    Datasets that carry a ``smiles`` attribute (e.g. MoleculeNet) parse it
    directly; otherwise we fall back to MUTAG-style reconstruction from
    one-hot atom/bond labels. Returns ``(mol_or_None, source)``.
    """
    from rdkit import Chem

    _silence_rdkit()
    smi = getattr(data, "smiles", None)
    if isinstance(smi, str) and smi:
        mol = Chem.MolFromSmiles(smi)
        if mol is not None and mol.GetNumAtoms() == int(data.num_nodes):
            return mol, "smiles"
        # Atom count mismatch (e.g. explicit Hs / salts): keep mol but flag it.
        if mol is not None:
            return mol, "smiles_mismatch"
    # Fallback: MUTAG-style one-hot reconstruction (needs 7-dim atom one-hot).
    try:
        if data.x is not None and data.x.size(1) == len(MUTAG_ATOMS):
            mol, _ = graph_to_mol(data)
            return mol, "reconstructed"
    except Exception:
        pass
    return None, "none"
