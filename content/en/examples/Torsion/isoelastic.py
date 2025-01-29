#!/usr/bin/env python
import argparse

class IsotropicElasticConstants:
    """
    A class to convert between various common isotropic elastic constant pairs.
    
    Supported pairs (or minimal sets) of input parameters:
        (E, nu), (G, nu), (K, nu),
        (lam, mu), (E, G), (K, G).
    
    After initialization, you can get any other parameter via the
    property getters: E, nu, G, K, lambda_, mu.
    """

    def __init__(self,
                 E=None,      # Young's modulus
                 nu=None,     # Poisson's ratio
                 G=None,      # Shear modulus
                 K=None,      # Bulk modulus
                 lam=None,    # Lamé's first parameter (lambda)
                 mu=None      # Lamé's second parameter (mu) = shear modulus G
                 ):

        self._tol = 1e-14

        provided = {
            'E': E,
            'nu': nu,
            'G': G,
            'K': K,
            'lam': lam,
            'mu': mu
        }
        not_none = [k for k,v in provided.items() if v is not None]

        # Helper function to check if exactly a set of keys is provided
        def have(*keys):
            s_keys = set(keys)
            s_provided = set(not_none)
            return s_keys.issubset(s_provided) and s_provided.issubset(s_keys)

        # We'll solve for (E, nu) first, then compute the rest.
        E_calc, nu_calc = None, None

        # 1) (E, nu)
        if have('E', 'nu'):
            E_calc = E
            nu_calc = nu

        # 2) (G, nu) => E = 2G(1+nu)
        elif have('G', 'nu'):
            E_calc = 2.0 * G * (1.0 + nu)
            nu_calc = nu

        # 3) (K, nu) => E = 3K(1 - 2nu)
        elif have('K', 'nu'):
            E_calc = 3.0 * K * (1.0 - 2.0 * nu)
            nu_calc = nu

        # 4) (lam, mu) => E = mu(3lambda + 2mu)/(lambda + mu), nu = lambda/(2*(lambda + mu))
        elif have('lam', 'mu'):
            E_calc = mu * (3.0 * lam + 2.0 * mu) / (lam + mu)
            nu_calc = lam / (2.0 * (lam + mu))

        # 5) (E, G) => from G = E / [2(1 + nu)]
        elif have('E', 'G'):
            E_calc = E
            nu_calc = (E / (2.0 * G)) - 1.0

        # 6) (K, G) => E = 9KG / (3K + G),  nu = (3K - 2G) / [2(3K + G)]
        elif have('K', 'G'):
            E_calc = (9.0 * K * G) / (3.0 * K + G)
            nu_calc = (3.0 * K - 2.0 * G) / (2.0 * (3.0 * K + G))

        else:
            raise ValueError(
                f"Insufficient or unsupported combination of parameters: {not_none}. "
                "Provide exactly one complete pair (or minimal set) from: "
                "(E, nu), (G, nu), (K, nu), (lam, mu), (E, G), (K, G)."
            )

        # Store the canonical E, nu
        self._E = E_calc
        self._nu = nu_calc

        # Compute the rest
        self._G = self._E / (2.0 * (1.0 + self._nu))          # Shear modulus
        self._K = self._E / (3.0 * (1.0 - 2.0 * self._nu))     # Bulk modulus
        self._lam = (self._E * self._nu /
                     ((1.0 + self._nu) * (1.0 - 2.0 * self._nu)))  # Lamé's lambda
        self._mu = self._G  # mu is G for isotropic

    @property
    def E(self):
        """Young's modulus."""
        return self._E

    @property
    def nu(self):
        """Poisson's ratio."""
        return self._nu

    @property
    def G(self):
        """Shear modulus."""
        return self._G

    @property
    def K(self):
        """Bulk modulus."""
        return self._K

    @property
    def lambda_(self):
        """Lamé's first parameter (lambda)."""
        return self._lam

    @property
    def mu(self):
        """Lamé's second parameter (mu = G for isotropic)."""
        return self._mu

def main():
    """
    Command-line interface for converting between isotropic elastic constants.
    
    Example usage:
        python isoelastic.py --E 210e9 --nu 0.3
        python isoelastic.py --K 140e9 --G 80e9
        python isoelastic.py --lam 60e9 --mu 40e9
        etc.

    After running, it prints out all equivalent constants.
    """
    parser = argparse.ArgumentParser(
        description="Convert between common isotropic elastic constants."
    )
    parser.add_argument('--E', type=float, help="Young's modulus (Pa)")
    parser.add_argument('--nu', type=float, help="Poisson's ratio (dimensionless)")
    parser.add_argument('--G', type=float, help="Shear modulus (Pa)")
    parser.add_argument('--K', type=float, help="Bulk modulus (Pa)")
    parser.add_argument('--lam', type=float, help="Lamé's first parameter, lambda (Pa)")
    parser.add_argument('--mu', type=float, help="Lamé's second parameter, mu (Pa)")

    args = parser.parse_args()

    # Attempt to create the IsotropicElasticConstants object from the CLI arguments
    try:
        mat = IsotropicElasticConstants(
            E=args.E, nu=args.nu, G=args.G,
            K=args.K, lam=args.lam, mu=args.mu
        )
    except ValueError as e:
        parser.error(str(e))

    # Print all derived constants in a nicely formatted way
    print(f"Results (SI units):")
    print(f"  E      = {mat.E:.6g} Pa")
    print(f"  nu     = {mat.nu:.6g}")
    print(f"  G      = {mat.G:.6g} Pa")
    print(f"  K      = {mat.K:.6g} Pa")
    print(f"  lambda = {mat.lambda_:.6g} Pa")
    print(f"  mu     = {mat.mu:.6g} Pa")

if __name__ == "__main__":
    main()

