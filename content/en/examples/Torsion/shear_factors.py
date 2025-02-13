def wide_flange(tw, tf, d, b, nu):
    m = 2*b*tf/(d*tw)
    n = b/d
    return (10*(1+nu)*(1+3*m)**2)/((12+72*m + 150*m**2 + 90*m**3) + nu*(11+66*m + 135*m**2 + 90*m**3) + 30*n**2*(m + m**2) + 5*nu*n**2*(8*m+9*m**2))


