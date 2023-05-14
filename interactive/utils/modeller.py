import numpy as np

def Cone(r, h, n=36):
    '''
    Return 5D vertex array (x,y,z,u,v). Y is up as per convention.
    Base is at y = 0, top is at y = h.
    Parameters:
        r (float): radius at base
        h (float): height
        n (int): number of sides
    '''
    # Prepare 2d array
    # Each side consists of a triangle, hence 3 points per side
    vertices = np.empty((3 * n, 5))

    # triangles should face outward, counterclockwise
    for i in range(n):
        f0 = i / n
        f1 = (i + 1) / n

        x0 = r * np.cos(f0 * 2.0 * np.pi)
        z0 = r * np.sin(f0 * 2.0 * np.pi)
        x1 = r * np.cos(f1 * 2.0 * np.pi)
        z1 = r * np.sin(f1 * 2.0 * np.pi)

        # first triangle
        vertices[3*i, :]   = [0,  h,  0, f0, 0]
        vertices[3*i+1, :] = [x0, 0, z0, f0, 1]
        vertices[3*i+2, :] = [x1, 0, z1, f1, 1]

    return vertices
