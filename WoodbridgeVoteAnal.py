import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display
import geopandas as gpd
import plotly.express as px
from scipy import stats
import plotly.graph_objs as go

# Read in the shapefile
WoodBridgeVoting = pd.read_excel(r"C:\Users\TaneeshA\Downloads\detailwithoutvotetypes.xlsx", sheet_name="2", skiprows=[0,2])
WoodbridgeDemographics = pd.read_excel(r"C:\Users\TaneeshA\Downloads\WoodBridgeDataUpdateTwo.xlsx", dtype={"Zipcode" : 'str'})
WoodbridgeTurnout = pd.read_excel(r"C:\Users\TaneeshA\Downloads\detailwithoutvotetypes.xlsx", sheet_name="Registered Voters", header=0, skiprows=list(range(1, 600)) + list(range(680, 999999)))

WoodBridgeVoting = pd.DataFrame(WoodBridgeVoting)
RepublicanAreas = WoodBridgeVoting[WoodBridgeVoting['Susan M. KILEY'] > WoodBridgeVoting['Frank PALLONE Jr.']]
pd.set_option('display.max_rows', 420)

total = WoodBridgeVoting['Susan M. KILEY'] + WoodBridgeVoting['Frank PALLONE Jr.'] + WoodBridgeVoting['Inder Jit SONI'] + WoodBridgeVoting['Tara FISHER'] + WoodBridgeVoting['Eric ANTISELL']
WoodBridgeVoting = WoodBridgeVoting.assign(totalVotes=total)

percentRepublican = WoodBridgeVoting['Susan M. KILEY'] / total * 100
percentDemocratic = WoodBridgeVoting['Frank PALLONE Jr.']  / total * 100

WoodBridgeVoting = WoodBridgeVoting.assign(RepPercent=percentRepublican)
WoodBridgeVoting = WoodBridgeVoting.assign(DemPercent=percentDemocratic)

WoodBridgeVoting = WoodBridgeVoting[WoodBridgeVoting['County'].notna() & WoodBridgeVoting['County'].str.contains("Woodbridge")]

WoodBridgeVoting = WoodBridgeVoting.reset_index(drop=True)
WoodBridgeVoting['Ward'] = WoodBridgeVoting['County'].str.extract(r'Ward (\d+)')


fig = px.scatter(WoodBridgeVoting, x="RepPercent", y="DemPercent", 
                 hover_name='County', title='Woodbridge Voting Percent REP vs Percent DEM', color='Ward', hover_data={'Susan M. KILEY', 'Frank PALLONE Jr.'})            
fig.update_layout(yaxis=dict(title="Percent Democrat Vote"), xaxis=dict(title="Percent Republican Vote"))
fig.show()

WoodBridgeVoting.dropna(subset=['DemPercent'], inplace=True)
WoodBridgeVoting['Ward'] = pd.to_numeric(WoodBridgeVoting['Ward'])
colors = ['Red', 'Purple', 'Yellow', 'Green', 'Blue']
wards = [1,2,3,4,5]

for ward in wards:
    if not (ward in WoodBridgeVoting.Ward.unique()):
        WoodBridgeVoting = WoodBridgeVoting.append(pd.DataFrame({"Ward":[ward], "DemPercent":[np.nan]}))

fig, ax = plt.subplots()

for i, (ward, group) in enumerate(WoodBridgeVoting.groupby("Ward")):
    ax.boxplot(group["DemPercent"], positions=[i], patch_artist=True, boxprops=dict(facecolor=colors[ward-1], color='black'))
fig.set_size_inches(12, 6)
plt.title("Democrat Voting Percentage By Ward")
plt.xlabel("Wards") 
plt.ylabel("Percentages")
plt.xticks(range(len(wards)), wards)
plt.show()


WoodBridgeVoting['Ward'] = pd.to_numeric(WoodBridgeVoting['Ward'])
WoodbridgeDemographics['Ward'] = pd.to_numeric(WoodbridgeDemographics['Ward'])
WoodbridgeVoting = WoodBridgeVoting.merge(WoodbridgeDemographics, on="Ward")


WoodbridgeVoting['Ward'] = pd.to_numeric(WoodbridgeVoting['Ward'])

WoodbridgeVotingIselin = WoodbridgeVoting[WoodbridgeVoting['Ward'] == 4]

WoodbridgeVoting.columns = WoodbridgeVoting.columns.str.strip()
fig2 = px.scatter(WoodbridgeVoting, x='White', y='DemPercent')
fig2.show()
WoodbridgeVoting = WoodbridgeTurnout.merge(WoodbridgeVoting, on="County")


WoodbridgeVoting.merge(WoodbridgeTurnout, on="County")
WoodbridgeVoting['Voter Turnout'] = WoodbridgeVoting['Voter Turnout'].apply(lambda x: float(x.replace("%", "")) / 100.0)
WoodbridgeVoting = WoodbridgeVoting[WoodbridgeVoting['Voter Turnout'] > 0]
WardString = WoodbridgeVoting["Ward"].astype('string')
fig3 = px.scatter(WoodbridgeVoting, x="Voter Turnout", y="DemPercent",  
                 hover_name='County', title='Woodbridge Voting Percent REP vs Percent DEM', color=WardString, hover_data={'Susan M. KILEY', 'Frank PALLONE Jr.'})
fig3.show()

slope, intercept, r_value, p_value, std_err = stats.linregress(WoodbridgeVoting['Voter Turnout'], WoodbridgeVoting['DemPercent'])


line = slope * WoodbridgeVoting['Voter Turnout'] + intercept


fig4 = px.scatter(WoodbridgeVoting, x="Voter Turnout", y="DemPercent")
fig4.add_trace(go.Scatter(x=WoodbridgeVoting['Voter Turnout'], y=line, name='Regression Line'))
fig4.show()

print('Slope:', slope)
print('Intercept:', intercept)
print('R', r_value)
print('R-squared:', r_value**2)
print('P-value:', p_value)
print('Standard error:', std_err)
