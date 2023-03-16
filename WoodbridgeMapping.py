import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

WoodbridgeVoting = pd.read_excel(r"C:\Users\TaneeshA\Downloads\WoodbridgeVoting2.xlsx")
WoodbridgeMap = gpd.read_file(r"C:\Users\TaneeshA\Downloads\WoodbridgeTownship.shp")

# extract last 5 characters from ELECD_KEY column
WoodbridgeMap['label'] = WoodbridgeMap['ELECD_KEY'].apply(lambda x: x[-5:])

WoodbridgeTownship = WoodbridgeMap.merge(WoodbridgeVoting, on='OBJECTID')
WoodbridgeTownship['Diff'] = WoodbridgeTownship['DemPercent'] - WoodbridgeTownship['RepPercent']
cmap = plt.cm.get_cmap('RdBu')
norm = plt.Normalize(vmin=-50, vmax=50)
cmaplist = [cmap(x) for x in np.linspace(0, 1, 256)]
cmap = cmap.from_list('Custom cmap', cmaplist, len(cmaplist))
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)

ax = WoodbridgeTownship.plot(column='Diff', cmap=cmap, norm=norm, figsize=(10, 10), edgecolor='black', legend=False)
ax.axis('off')
ax.set_title('Woodbridge Township', fontsize=16)
cbar = plt.colorbar(sm)
cbar.set_label('DemPercent - RepPercent', fontsize=14)

# add labels based on the 'label' column
for _, row in WoodbridgeTownship.iterrows():
    ax.annotate(text=row['label'], xy=row['geometry'].centroid.coords[0], ha='center', fontsize=4,
            fontweight='bold', color='gray')


plt.show()
