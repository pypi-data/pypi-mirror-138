import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from .fit_tools import *

def banana_diagram (freq, psd, back, pkb, n=30, k=30, 
                    angle_min=0, angle_max=90, split_min=0, split_max=2, 
                    figsize=(9,6), shading='auto', marker_color='black',
                    cmap='plasma', contour_color='black', marker='o', 
                    annotate_max=True, show_contour=True, 
                    param_wdw=None, instr='geometric',
                    use_sinc=False, asym_profile='korzennik', fit_amp=False,
                    projected_splittings=False, add_colorbar=False, 
                    pcolormesh_options={}, contour_options={}) : 
  '''
  Compute banana diagram (see Ballot et al 2006) for a given
  set of fitted parameters. Parameters are fixed, except for
  angles and splittings which are set to vary between 0 and
  90 degrees and 0 and 2 muHz, respectively.

  :param freq: frequency vector.
  :type freq: ndarray

  :param psd: psd vector.
  :type psd: ndarray

  :param back: background vector.
  :type back: ndarray

  :param pkb: pkb array that will be used to compute the
    model and the likelihood.
  :type pkb: ndarray

  :param n: number of elements along angle axis. Optional,
     default 30.
  :type n: int

  :param k: number of elements along splittings axis.
    Optional, default 30.
  :type k: int

  :param angle_min: minimal value for angle on the diagram. 
    Optional, default 0.
  :type angle: float

  :param angle_max: maximal value for angle on the diagram. 
    Optional, default 90.
  :type angle: float

  :param split_min: minimal value for splittings on the diagram. 
    Optional, default 0.
  :type angle: float

  :param split_max: maximal value for splittings on the diagram. 
    Optional, default 2.
  :type angle: float

  :param pcolormesh_options: ditionary that will be passed as 
    the ``kwargs`` for matplotlib.axes.Axes.pcolormesh.
  :type pcolormesh_options: dict

  :param contour_options: ditionary that will be passed as 
    the ``kwargs`` for matplotlib.axes.Axes.contour.
  :type contour_options: dict

  :return: tuple with likelihood-grid and figure
  :rtype: tuple
  '''

  grid = np.zeros ((k, n))
  angles = np.linspace (angle_min, angle_max, n)
  splittings = np.linspace (split_min, split_max, k)

  index = np.argsort (pkb[:,2])
  pkb = pkb[index] 

  if pkb.shape[1]==20 :
    i_width = 8
    i_angle = 11
    i_split = 14
  else :
    i_width = 6
    i_angle = 8
    i_split = 10
  cond = (freq>pkb[0,2]-10*pkb[0,i_width])&(freq<pkb[-1,2]+10*pkb[-1,i_width])
  freq = freq[cond]
  psd = psd[cond]
  back = back[cond]

  snr = psd/back

  for ii in tqdm (range (n)) :
    for jj in range (k) :
      pkb[:, i_angle] = angles[ii]
      pkb[:, i_split] = splittings[jj]
      model = compute_model (freq, pkb, param_wdw=param_wdw, instr=instr,
                             use_sinc=use_sinc, asym_profile=asym_profile, fit_amp=fit_amp,
                             projected_splittings=projected_splittings)
      model = model / back
      model += 1
      aux = snr / model + np.log (model)
      log_l = np.sum (aux)
      grid[jj, ii] = log_l

  fig, ax = plt.subplots (figsize=figsize)
  pcm = ax.pcolormesh (angles, splittings, -grid, shading=shading, cmap=cmap, 
                       **pcolormesh_options)
  if add_colorbar :
    cbar = fig.colorbar (pcm)
    cbar.ax.set_ylabel ('$\ln \mathcal{L}$', fontsize=20)
  if show_contour :
    ax.contour (angles, splittings, -grid, colors=contour_color, 
                **contour_options)
  if annotate_max :
    xmax = angles[np.unravel_index (np.argmin (grid), grid.shape)[1]]
    ymax = splittings[np.unravel_index (np.argmin (grid), grid.shape)[0]]
    ax.scatter (xmax, ymax, marker=marker, color=marker_color, 
                label='({:.1f}$^{{\circ}}$, {:.3f} $\mu$Hz)'.format (xmax, ymax))
  ax.legend (facecolor='white', framealpha=1)
  ax.set_ylabel (r'$\nu_s$ ($\mu$Hz)')
  ax.set_xlabel ('$i$ ($^{\circ}$)')

  return grid, fig
