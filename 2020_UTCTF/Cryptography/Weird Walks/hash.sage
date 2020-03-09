import sage.all

def convert(h):
    return bin(int(h, 16))[3:]

def hash(m):
    p = 59779
    # STEP 1: Find a single supersingular curve over F_{p^2}.
    q = next(q for q in Primes() if q%4 == 3 and kronecker_symbol(-q,p) == -1)
    K = QuadraticField(-q)
    H = K.hilbert_class_polynomial()
    j0 = 1728

    # STEP 2: Walk along the isogeny graph.
    phi = ClassicalModularPolynomialDatabase()[2]
    def get_neighbors(j):
        """
        This function returns a list of all roots of Phi_l(j,X), repeated with
        appropiate multiplicity.
        """
        R.<x> = GF(p^2)[]
        return flatten([[j2]*k for j2,k in phi(j,x).roots()])


    previous_node = j0
    current_node = j0

    for b in '0' + convert(m):
        neighbors = get_neighbors(current_node)
        neighbors.remove(previous_node)
        previous_node = current_node
        current_node = neighbors[int(b)]

    return ZZ(current_node.polynomial()(1337))

print(hash('ff'))
