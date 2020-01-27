import rasterio
import numpy as np
from affine import Affine
from pyproj import Proj, transform
import sys

def main():
  fname = sys.argv[1]
  out_name = sys.argv[2]

  with rasterio.open(fname) as r:
      T0 = r.transform  
      p1 = Proj(r.crs)
      A = r.read() 

  cols, rows = np.meshgrid(np.arange(A.shape[2]), np.arange(A.shape[1]))
  T1 = T0 * Affine.translation(0.5, 0.5)
  rc2en = lambda r, c: (c, r) * T1
  eastings, northings = np.vectorize(rc2en, otypes=[np.float, np.float])(rows, cols)

  p2 = Proj(proj='latlong',datum='WGS84')
  longs, lats = transform(p1, p2, eastings, northings)

  M = np.stack([longs.ravel(),lats.ravel(),A.ravel()], 1)

  np.savetxt(out_name,X=M,delimiter=",", header="longitude, latitude, altitude")

if __name__ == "__main__":
  main()
