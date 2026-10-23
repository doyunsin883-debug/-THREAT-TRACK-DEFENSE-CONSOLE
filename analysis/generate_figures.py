"""Reproduce README Matplotlib graphics using documented sources.

The measured trace is manually transcribed from a photograph taken during my Arduino IDE testing session. Other plots illustrate the V5 firmware's mathematical decision rules,
not measured experimental performance.
"""
from pathlib import Path
import csv

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/charts'
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 11,
    'axes.titlesize': 16,
    'axes.labelsize': 11,
    'figure.dpi': 160,
    'savefig.dpi': 200,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# Figure 1: Actual values visible in my original Serial Monitor photograph.
rows = list(csv.DictReader((ROOT/'data/serial_monitor_photo_readings.csv').open(encoding='utf-8')))
idx = [int(r['sample_index']) for r in rows]
values = [float(r['distance_cm']) for r in rows]
fig, ax = plt.subplots(figsize=(10.4, 4.5))
ax.plot(idx, values, marker='o', linewidth=2.3)
ax.set_xticks(idx)
ax.set_ylim(0, max(values) + 3.2)
ax.set_xlabel('Visible measurement sequence (sample index, not time)')
ax.set_ylabel('Distance (cm)')
ax.set_title('HC-SR04: actual Serial Monitor photo readings')
ax.grid(axis='y', alpha=0.26)
for x, y in zip(idx, values):
    ax.annotate(f'{y:.2f}', (x, y), xytext=(0, 10), textcoords='offset points',
                ha='center', fontsize=9)
fig.text(.1, .01, 'Source: original Arduino IDE screenshot from the build; only eight visible values. Not a calibrated test.',
         fontsize=9, color='#555555')
fig.tight_layout(rect=(0,.04,1,1))
fig.savefig(OUT/'serial-readings-photo.png', facecolor='white')
plt.close(fig)

# Firmware decision map. TTC is computed only for estimated approach speed >10cm/s.
def alert_state(d: float, v: float) -> int:
    ttc = d/v if v > 10 else None
    danger = d <= 30 or (ttc is not None and 0 < ttc <= 1.5)
    warning = d <= 70 or (ttc is not None and 0 < ttc <= 3.0)
    return 2 if danger else 1 if warning else 0

D = np.linspace(2, 150, 375)
V = np.linspace(0, 80, 321)
Z = np.array([[alert_state(d, v) for d in D] for v in V])
fig, ax = plt.subplots(figsize=(10.4, 5.1))
cmap = ListedColormap(['#22946a','#f0c550','#db615f'])
norm = BoundaryNorm([-0.5,0.5,1.5,2.5], cmap.N)
ax.pcolormesh(D,V,Z,cmap=cmap,norm=norm,shading='nearest')
ax.axvline(30, linewidth=1.1, linestyle='--', alpha=0.8, color='black')
ax.axvline(70, linewidth=1.1, linestyle='--', alpha=0.8, color='black')
ax.text(31, 77, '30 cm', fontsize=9)
ax.text(71, 77, '70 cm', fontsize=9)
ax.set_xlabel('Distance to object (cm)')
ax.set_ylabel('Estimated approach speed (cm/s)')
ax.set_title('V5 alert-decision map: distance + TTC')
ax.legend(handles=[Patch(facecolor=cmap(i), label=x) for i,x in enumerate(['SAFE','WARNING','DANGER'])],
          loc='upper right', framealpha=.9, ncol=3)
fig.text(.1,.01,'Deterministic plot of firmware thresholds; analytical illustration, not a measured detection-accuracy result.',
         fontsize=9,color='#555555')
fig.tight_layout(rect=(0,.04,1,1))
fig.savefig(OUT/'alert-decision-map.png',facecolor='white')
plt.close(fig)

# TTC model, not a validation trace.
fig,ax=plt.subplots(figsize=(10.4,4.6))
x = np.linspace(2,150,300)
for v in (15,30,60):
    ax.plot(x,x/v,label=f'{v} cm/s approach',linewidth=2)
ax.axhline(1.5,linestyle='--',alpha=.85,label='1.5 s DANGER TTC')
ax.axhline(3.0,linestyle=':',alpha=.85,label='3.0 s WARNING TTC')
ax.set_ylim(0,8)
ax.set_xlim(2,150)
ax.set_xlabel('Distance (cm)')
ax.set_ylabel('Time to contact, d / v (s)')
ax.set_title('Why approach speed matters: TTC model')
ax.legend(ncol=2,fontsize=9,loc='upper left')
ax.grid(axis='y',alpha=.25)
fig.text(.1,.01,'Constant-velocity model (v > 10 cm/s); assumes direct radial motion. Not measured TTC.',fontsize=9,color='#555555')
fig.tight_layout(rect=(0,.04,1,1))
fig.savefig(OUT/'ttc-model.png',facecolor='white')
plt.close(fig)
print('Generated',len(list(OUT.glob('*.png'))),'reproducible figures')
