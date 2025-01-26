---
title: Static Condensation
---

This example replicates the classic cantilever‐beam problem where:

1. We have two beam elements forming a cantilever of total length \(L\).  
2. Nodes are arranged along the beam so that Node 1 is fixed, and Nodes 2 and 3 are free.  
3. Each free node has two DOFs: transverse displacement \((u)\) and rotation \((\theta)\).  

Accordingly, the system has 4 active DOFs. We will:

1. **Construct** the model in OpenSees using `ndm=2, ndf=3`.  
2. **Extract** the global stiffness and mass matrices by calling `model.getTangent(k=1)` and `model.getTangent(m=1)`.  
3. **Condense** out the rotational DOFs to see how to statically reduce a 4×4 matrix down to 2×2.

---

## 1) Static Condensation

Below is a small helper function `condense()` that takes a square matrix \(K\) (stiffness or mass) and an array of indices `ic` identifying which DOFs to **keep**. All other DOFs are **statically condensed out** using

\[
K_{\mathrm{condensed}} = 
K_{tt} - K_{t0} \; K_{00}^{-1} \; K_{0t}
\]

where \((t)\) are the retained DOFs and \((0)\) are the ones to be condensed out.

```python
def condense(K, ic):
    """
    Perform static condensation on matrix K, returning a smaller matrix
    that retains only the DOFs in the list 'ic' and statically eliminates
    all other DOFs.
    
    Parameters
    ----------
    K  : 2D numpy array
         Full square matrix (e.g., stiffness or mass).
    ic : list of int
         Indices of DOFs we want to keep.
    
    Returns
    -------
    Kc : 2D numpy array
         The condensed matrix of size len(ic) x len(ic).
    """
    import numpy as np
    
    # Convert list to np.array for indexing
    ic = np.array(ic, dtype=int)
    
    # All DOFs = 0..N-1
    N = K.shape[0]
    ix = np.setdiff1d(range(N), ic)  # DOFs to be condensed out
    
    # Partition:
    K_tt = K[np.ix_( ic, ic )]
    K_t0 = K[np.ix_( ic, ix )]
    K_0t = K[np.ix_( ix, ic )]
    K_00 = K[np.ix_( ix, ix )]

    # If there are no DOFs to condense out, just return the original
    if len(ix) == 0:
        return K

    # Perform the usual static condensation formula
    # K_condensed = K_tt - K_t0 * inv(K_00) * K_0t
    Kc = K_tt - K_t0 @ np.linalg.solve(K_00, K_0t)

    return Kc
```

---

## 2) A Cantilever Model

We now create a small function `build_cantilever_model()` that sets up:

- A 2D model (`ndm=2`) with 3 DOFs per node: \((u_x, u_y, \theta_z)\).  
- Three nodes along the \(x\)-axis, with Node 1 fixed in all DOFs, Node 2 and Node 3 each having \(u_x\) fixed (to ensure pure bending), but allowing \(u_y\) and \(\theta_z\).  
- Two elastic beam elements, each of length \(L/2\).  
- Lumped masses at Nodes 2 and 3 in the transverse direction only, matching \(\frac{mL}{4}\) and \(\frac{mL}{2}\) respectively.

```python
import opensees.openseespy as ops

def build_cantilever_model(L=1.0, E=1.0, I=1.0, m=1.0):
    """
    Builds a 2D cantilever of total length L, split into two beam elements.
    Node 1: fully fixed in (ux, uy, rz).
    Node 2 and 3: fix only ux, keep (uy, rz) free.
    
    The beam has E, I for bending. 
    We assign lumped masses at node 2,3 in the y-direction only, with:
      node2 mass = (0, mL/4, 0)
      node3 mass = (0, mL/2, 0)
    """
    # Start the Model: 2D problem, ndf=3
    model = ops.Model(ndm=2, ndf=3)

    # Create 3 nodes at 0, L/2, L along x-axis
    ops.node(1, 0.0,  0.0)
    ops.node(2, L/2,  0.0)
    ops.node(3, L,    0.0)

    # Fix Node 1 in all DOFs (ux, uy, rz)
    ops.fix(1, 1, 1, 1)

    # Node 2, 3: fix only ux => (1, 0, 0)
    ops.fix(2, 1, 0, 0)
    ops.fix(3, 1, 0, 0)

    # Geometric transformation for a linear beam in 2D
    transf_tag = 1
    ops.geomTransf("Linear", transf_tag)

    # Define a 2D elastic beam (elasticBeamColumn)
    A  = 1.0   # cross-sectional area (not crucial for pure bending)
    Iz = I     # moment of inertia
    # E is user-specified
    # We'll ignore axial effects or keep them large to approximate pure bending

    # Element 1: Node 1 -> Node 2
    ops.element("elasticBeamColumn", 1, 1, 2, A, E, Iz, transf_tag)
    # Element 2: Node 2 -> Node 3
    ops.element("elasticBeamColumn", 2, 2, 3, A, E, Iz, transf_tag)

    # Lumped mass at Node 2 and Node 3 in the y-direction only
    ops.mass(2, 0.0, m*L/4, 0.0)
    ops.mass(3, 0.0, m*L/2, 0.0)

    return model
```

---

## 3) Stiffness & Mass Matrices

Once the model is built, we obtain the **global** tangent matrices. The method:

```python
model.getTangent(k=1)  # for stiffness
model.getTangent(m=1)  # for mass
```

returns the entire system matrix, including constrained DOFs. We must then extract the sub-block for the free DOFs, which are:

- **Node 2**: DOFs (u\_x=4, u\_y=5, \(\theta\)=6) but we fixed the x-displacement, so the "active" DOFs are 5 and 6.  
- **Node 3**: DOFs (u\_x=7, u\_y=8, \(\theta\)=9) but we fixed the x-displacement, so the "active" DOFs are 8 and 9.  

Hence the 4 free DOFs in the global system are \([5,6,8,9]\). Let’s see how we do it:

```python
import numpy as np

if __name__ == "__main__":

    # Example parameters
    L = 1.0
    E = 1.0
    I = 1.0
    m = 1.0

    # Build the model
    model = build_cantilever_model(L, E, I, m)

    # Get the full stiffness and mass matrices
    K_full = model.getTangent(k=1)
    M_full = model.getTangent(m=1)

    print("Full system stiffness K_full:\n", K_full, "\n")
    print("Full system mass M_full:\n", M_full, "\n")

    # The 4 active DOFs are [5,6,8,9]
    free_dofs = [5, 6, 8, 9]

    # Extract 4x4 submatrix
    K_4x4 = K_full[np.ix_(free_dofs, free_dofs)]
    M_4x4 = M_full[np.ix_(free_dofs, free_dofs)]

    print("4x4 stiffness matrix (DOFs 5,6,8,9):\n", K_4x4, "\n")
    print("4x4 mass matrix (DOFs 5,6,8,9):\n", M_4x4, "\n")
```

---

## 4) Performing Static Condensation

In the textbook example, the 4 DOFs are labeled:

\[
\mathbf{u} = \{\, u_1,\; u_2,\; u_3,\; u_4 \}
\]

But in our global matrix, we see the order is \((5,6,8,9)\). Typically, we want to **condense out** the rotations (call them \(u_3, u_4\) in the text) and keep the translations (\(u_1, u_2\)).

- If we interpret dof5 and dof8 as the two translations \(u_1, u_2\)  
- and dof6 and dof9 as the two rotations \(u_3, u_4\),  

then we should **reorder** the 4×4 matrix so that translations come first \([5,8]\) and rotations come second \([6,9]\). After reordering, we can apply `condense()` to eliminate the rotation DOFs.

```python
    # Reorder the 4x4 so that translations are in the first block: [5,8], then rotations [6,9].
    reorder = [0, 2, 1, 3]  
    # Explanation: 
    #   0 -> index 0 in K_4x4 is dof5
    #   2 -> index 2 in K_4x4 is dof8
    #   1 -> index 1 in K_4x4 is dof6
    #   3 -> index 3 in K_4x4 is dof9

    K_4x4_reordered = K_4x4[np.ix_(reorder, reorder)]
    print("K_4x4 in 'translation-then-rotation' order:\n", K_4x4_reordered, "\n")

    # DOFs to keep: the first 2 (the translations)
    keep = [0, 1]  # keep indices [0,1] in the reordered matrix
    K_2x2_condensed = condense(K_4x4_reordered, keep)

    print("Condensed 2x2 stiffness (after eliminating rotations):\n", K_2x2_condensed, "\n")
```

Finally, if desired, we can also find the transformation matrix \(\mathbf{T}\) that recovers the condensed DOFs (rotations) in terms of the retained DOFs (translations):

\[
\mathbf{u}_{0} = - \mathbf{K}_{00}^{-1}\,\mathbf{K}_{0t} \;\mathbf{u}_t
\quad\Longrightarrow\quad
\mathbf{T} = - \mathbf{K}_{00}^{-1}\,\mathbf{K}_{0t}
\]

```python
    # Partition K_4x4_reordered as blocks:
    #  K_tt is the top-left 2x2
    #  K_t0 is the top-right 2x2
    #  K_0t is the bottom-left 2x2
    #  K_00 is the bottom-right 2x2
    K_tt = K_4x4_reordered[:2, :2]
    K_t0 = K_4x4_reordered[:2, 2:]
    K_0t = K_4x4_reordered[2:, :2]
    K_00 = K_4x4_reordered[2:, 2:]

    import numpy as np
    T = -np.linalg.solve(K_00, K_0t) 
    print("Transformation matrix T (rotations vs translations):\n", T, "\n")

    print("--- End of demonstration ---")
```

---

## Conclusion

1. **We built** a two-element cantilever in OpenSees with 3 nodes, 4 active DOFs (\(y\)-translations and rotations at nodes `2` and `3`).  
2. **We used** [`model.getTangent()`](https://opensees.stairlab.io/user/manual/output/printA.html) to obtain the global stiffness and mass matrices, then sliced out the $4 \times 4$ sub-block for the free DOFs.  
3. **We performed** static condensation on the $4 \times 4$ matrix to reduce it down to a $2 \times 2$ matrix that retains only the translational DOFs, matching the textbook procedure and final results.  

This illustrates how the new OpenSees Python API can be leveraged for matrix-based analysis, including direct access to system tangents and flexible manipulations such as static condensation.
