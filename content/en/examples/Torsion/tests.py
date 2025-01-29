import numpy as np

def test_parallel_axis(section, size):
    u = np.random.rand(3)
    u[0] = 0

    u *= size/np.linalg.norm(u)

    A = section.torsion.cnn()[0,0]

    sec_cen = section.translate(section.torsion.centroid())

    sec_ran = sec_cen.translate(u[1:])

    Ir = sec_ran.torsion.cmm()

    Ic = sec_cen.torsion.cmm()

    uou = np.outer(u,u)

    print(Ir)
    print(Ic)
    print(Ir - A*(u.dot(u)*np.eye(3) - uou))



if __name__ == "__main__":
    from steel import wide_flange
    test_parallel_axis(wide_flange(d=612, b=229, tf=19.6, tw=11.9), 400)


