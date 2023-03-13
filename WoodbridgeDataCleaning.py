import pandas as pd

#Reading all of the files
iselinRace = pd.read_csv(r"C:\Users\TaneeshA\Downloads\ACSST5Y2021.S0501-2023-01-31T045452.csv")
avenelRace = pd.read_csv(r"C:\Users\TaneeshA\Downloads\ACSST5Y2021.S0601-2023-01-31T045554.csv")
prRace = pd.read_csv(r"C:\Users\TaneeshA\Downloads\ACSST5Y2021.S0601-2023-01-31T045619.csv")
coloniaRace = pd.read_csv(r"C:\Users\TaneeshA\Downloads\ACSST5Y2021.S0601-2023-01-31T180603.csv")
seaWarenRace = pd.read_csv(r"C:\Users\TaneeshA\Downloads\ACSST5Y2021.S0601-2023-01-31T180227.csv")
wpRace = pd.read_csv(r"C:\Users\TaneeshA\Downloads\ACSST5Y2021.S0601-2023-01-31T180205.csv")
keasbyRace = pd.read_csv(r"C:\Users\TaneeshA\Downloads\ACSST5Y2021.S0601-2023-01-31T180143.csv")
fordsRace = pd.read_csv(r"C:\Users\TaneeshA\Downloads\ACSST5Y2021.S0601-2023-01-31T180023.csv")

#Transposing them for the sake of merging
iselinRace = iselinRace.T
avenelRace = avenelRace.T
prRace = prRace.T
coloniaRace = coloniaRace.T
seaWarenRace = seaWarenRace.T
wpRace = wpRace.T 
keasbyRace = keasbyRace.T 
fordsRace = fordsRace.T
#merging them all together
woodbridgeRaceCheck = pd.concat([iselinRace, avenelRace, prRace, coloniaRace, seaWarenRace, wpRace, keasbyRace, fordsRace])

firstrow = woodbridgeRaceCheck.iloc[0]
woodbridgeRaceCheck.columns = firstrow
woodbridgeRaceCheck = woodbridgeRaceCheck[woodbridgeRaceCheck["Total population"]!="Total population"]


woodbridgeRaceCheck.dropna(axis=1, thresh=20, inplace=True)

numbers = woodbridgeRaceCheck.index
result = [s.split()[1] for s in numbers]

result = [s.split("!")[0] for s in result]

woodbridgeRaceCheck.index = result

woodbridgeRaceCheck = woodbridgeRaceCheck.drop_duplicates()

duplicaterows = woodbridgeRaceCheck.index.duplicated(keep="first")
woodbridgeRaceCheck = woodbridgeRaceCheck[~duplicaterows]

woodbridgeRaceCheck.to_excel(r"C:\Users\TaneeshA\Downloads\WoodBridgeDataUpdateTwo.xlsx")