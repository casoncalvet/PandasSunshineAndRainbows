# Should We Fear Sharks?
![This is an image](https://i.natgeofe.com/n/5d0635af-3b57-4507-8a5f-9eaf9959a083/01surfersharkattack_16x9.jpg?w=1200)



## Hypothesis: 
#### A subset shark of species are responsible for the majority of reported shark attacks. 
(Thus, we should only fear **some** sharks)  


### Cleaning Dataset retrieved from Kaggle:
https://www.kaggle.com/datasets/teajay/global-shark-attacks

```python
import pandas as pd
import numpy as np
import dataframe_image as dfi
import matplotlib.pyplot as plt


df= pd.read_csv ('../datasets/attacks.csv', encoding='unicode_escape')

#Check for duplicates in DF 
df[df.duplicated()== True].dropna()

## isolate Attacks and Dropna 
spattacks= df[['Fatal (Y/N)', 'Species ']].dropna()

## Need to clean spaces and odd characters from spattacks df 
spattacks['Species ']= spattacks['Species '].apply(lambda x: x.strip())
spattacks['better'] = spattacks['Species '].replace('[-]',' ', regex=True)
spattacks['better']=spattacks['better'].apply(lambda x: x.lower())

#Drop unused columns 
spattacks= spattacks.drop('Species ', axis=1)


# Extract only information on shark species 
spattacks['Species']= spattacks['better'].str.extract(r'(\w{3,}\sshark|\w{3,}\sshark|blue nose shark)')
spattacks= spattacks.dropna()

#Create list to drop Regex mismatchess 
droplist= ['female shark','the shark', 'nosed shark', 'from shark', 'two shark' , 'colored shark', 'metre shark', 'small shark', 'foot shark', 'captive shark', 'several shark', 'little shark', 'large shark', 'another shark', 'saw shark', 'same shark', '30kg shark', 'larger shark', 'young shark', 'juvenile shark', 'unidentified shark', 'finned shark', 'gaffed shark', 'for shark', 'hooked shark', 'ground shark', 'red shark']
spattacks2= spattacks[~spattacks['Species'].isin(droplist)]
spattacks2['Species'].unique()

#Drop unwanted column and reset index 
spattacks2.reset_index(drop= True, inplace= True)
spattacks2= spattacks2.drop('better', axis=1)
spattacks2['Species'].unique()

# Remove NON Y and N entries from Y/N
def condition(x): 
    if x == 'Y': 
        return x
    elif x == 'N': 
        return x

# Create new column with only Y or N
spattacks2['Fatal?']= spattacks2['Fatal (Y/N)'].apply(condition)
spattacks2= spattacks2.drop('Fatal (Y/N)', axis=1)
spattacks2= spattacks2.dropna()
spattacks2.reset_index(drop= True, inplace= True)


# Correct misspelled categories 
spattacks2['Species'].replace('zambezi shark', 'zambesi shark', inplace= True)
spattacks2['Species'].replace('tipped shark', 'blacktip shark', inplace= True)
spattacks2['Species'].replace('gill shark', 'sevengill shark', inplace= True)
spattacks2['Species'].replace('carcharinid shark', 'carcharhinid shark', inplace= True)
spattacks2['Species'].replace('gray shark', 'grey shark', inplace= True)
spattacks2['Species'].replace('jackson shark', 'port jackson shark', inplace= True)
spattacks2['Species'].replace('brown shark', 'sandbar shark', inplace= True)
spattacks2['Species'].replace('copper shark', 'whaler shark', inplace= True)
spattacks2['Species'].replace('white shark', 'great white shark', inplace= True)
spattacks2['Species'].replace('blacktip shark', 'reef shark', inplace= True)
spattacks2['Species'].replace('blacktip shark', 'reef shark', inplace= True)
spattacks2['Species'].replace('whitetip shark', 'reef shark', inplace= True)

# Add Title Format 
spattacks2.reset_index(drop= True, inplace= True)
spattacks2['Species']= spattacks2['Species'].apply(lambda x: x.title())


```


## Data Exploration ## 

```python
#Group by species number of attacks (both fatal and nonfatal)
Attacks= spattacks2.groupby(['Species']).count()
Attacks

#Fatal incidents vs nonfatal 
Proportion_Fatal= spattacks2.groupby([spattacks2['Fatal?']== 'Y']).count()

#Group by fatalities 
fatalities= spattacks2[spattacks2['Fatal?']== 'Y']
fatal_species_counts= fatalities.groupby(['Species']).count()

#Non Fatal incidents 
nonfatal= spattacks2[spattacks2['Fatal?']== 'N']
nonfatal_species_counts= nonfatal.groupby(['Species']).count()
```

# Visualize Shark Attacks by Species 
<iframe src="https://giphy.com/embed/Rfex2rSEpNFZ1GdtPl" width="480" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/sharkweek-Rfex2rSEpNFZ1GdtPl">via GIPHY</a></p>

### Creating a Frequency Table of all Incidents, Organized by Species

```python
 
# Make column of species counts frequency 
Frequency = (spattacks2['Species'].value_counts()/spattacks2['Species'].count())*100
Count= spattacks2['Species'].value_counts()


#Frequency Table 
Frequency = pd.DataFrame(Frequency)
Frequency= Frequency.rename({'Species':'Frequency'}, axis=1)
Frequency['Frequency']=Frequency['Frequency'].apply(lambda x: round(x,2))


Count= pd.DataFrame(Count)
Count=Count.rename({'Species':'Count'}, axis=1)

Frequency_Table= pd.merge(Count, Frequency, left_index=True, right_index=True)
sub= Frequency_Table.iloc[18:,:]
sub['Count'].sum()

## From row 18 down represents less than 5% of shark attacks 
Frequency_Table.iloc[:17]
sub['Frequency'].sum()

Frequency_Table= Frequency_Table.iloc[:17]

#Merge sharks responsible for less than 5% of attacks into "Other" Category 
row = pd.Series({'Count':89,'Frequency':4.74},name='Other')
Frequency_Table = Frequency_Table.append(row)

#Frequency_Table_Acess
Frequency_Table['Count']=Frequency_Table['Count'].apply(lambda x: int(x))

df_styled = Frequency_Table.style.background_gradient().set_precision(2)

#Export table
dfi.export(df_styled,"SharkFrequency.png")

```
## Incident Frequency Table 
![This is an image](../PandasSunshineAndRainbows/images/SharkFrequency.png)
## Visualize Table: Create stacked barplot for Species Incidents 
``` python 
#Create Stacked Barplot
sns.set_style("darkgrid")
fig, ax= plt.subplots(1)
plt.rcParams["figure.figsize"] = (8,6)
FvN10plot= FvsN10[['NonFatal Attacks', 'Fatal Attacks']].plot(kind='barh', stacked=True, ax=ax, color= {'xkcd:prussian blue', 'xkcd:carolina blue'} )
plt.title("Which Sharks Should I Worry About?")
plt.ylabel(' ')
plt.xlabel("Incidents Recorded")
# Save figure 
plt.savefig('FvsNStackedBar.png',bbox_inches="tight")
```

### Top 10 Offenders
![This is an image](../images/FvsNStackedBar.png) 

## Creation of Fatal vs NonFatal Incidents Table
#### (for later use in Donut Chart)

```python 

# Create DataFrames of Nonfatal and Fatal Incidents (created in Data Exploration), grouped by Species
nonfatal_species_counts.rename(columns={'Fatal?': 'NonFatal Attacks'}, inplace=True)
nonfatal_species_counts
fatal_species_counts.rename(columns= {'Fatal?': 'Fatal Attacks'}, inplace= True)
fatal_species_counts

#Merge DataFrames
FvsN= nonfatal_species_counts.merge(right= fatal_species_counts, how= 'outer', left_index=True, right_index=True )
FvsN= FvsN.fillna(0)
FvsN['Fatal Attacks']= FvsN['Fatal Attacks'].apply(lambda x: int(x))
FvsN['Total Attacks']= FvsN.apply(np.sum, axis=1)
FvsN= FvsN.sort_values(by= 'Total Attacks', ascending= False)
FvsN10= FvsN.iloc[:10]
FvsN10_styled = FvsN10.style.background_gradient()
```
## Reported Incidents per Species (Top 10)
#####  *(These are the sharks to worry about)*
![This is an image](../PandasSunshineAndRainbows/images/FatalvsNonFatalAttacks.png)


## Creating Donut Chart

``` python 
def DonutChart(): 
    """
    Creates Donut Graph of incident frequency among species
    """
    
    
    
    fig, ax= plt.subplots(1)
    plt.rcParams["figure.figsize"] = (8,8)
    colors = sns.color_palette("mako")
    plt.tight_layout()
    patches, texts, autotexts= plt.pie(x= Frequency_Table['Frequency'], 
                                       labels = Frequency_Table.index, colors=colors, 
                                       rotatelabels= 0.25,
                                       autopct='%0.0f%%', 
                                       pctdistance=0.85,
                                       labeldistance=1)
    [autotexts.set_color('white') for autotexts in autotexts]

    ax.axis('equal')
    circle = plt.Circle( (0,0), 0.7, color='white')
    p=plt.gcf()
    p.gca().add_artist(circle)
    plt.title('Frequency of Incidents', pad=-260)
    #plt.savefig('DonutChart.png',bbox_inches="tight")
    return plt.show()
DonutChart()
``` 
### All Offenders (Fatal and NonFatal)
![This is an image](../PandasSunshineAndRainbows/images/DonutChart.png) 
#### Great White Sharks, Tiger Sharks, and Bull Sharks are responsible for 50% of all incidents. 

## So, who's responsible for the fatalities? 
<iframe src="https://giphy.com/embed/3owypntx89D6RRur7y" width="480" height="270" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/syfy-sharknado-4-the-4th-awakens-3owypntx89D6RRur7y">via GIPHY</a></p>

# Create Donut Chart of Fatal Suspects
``` python 
## Fatal vs Nonfatal Attacks Percentages 
FvsN10['NonFatalpor']= FvsN10['NonFatal Attacks'].div(FvsN10['Total Attacks'])
FvsN10['Fatalpor']= FvsN10['Fatal Attacks'].div(FvsN10['Total Attacks'])
# Remove 0% so it doesn't appear on chart 
nozeropercent= FvsN10['Fatal Attacks'].loc[~(FvsN10==0).any(axis=1)]

def DonutChart2(): 
    """
    Creates Donut Graph of incident frequency among species
    """
    fig, ax= plt.subplots(1)
    plt.rcParams["figure.figsize"] = (8,8)
    colors = sns.color_palette("mako")
    plt.tight_layout()
    ax.axis('equal')
    trydis= FvsN10['Fatal Attacks'].loc[~(FvsN10==0|1).any(axis=1)]
    patches, texts, autotexts= plt.pie(x= nozeropercent, 
                                       labels = nozeropercent.index, colors=colors, 
                                       rotatelabels= 0.25,
                                       autopct='%0.0f%%', 
                                       pctdistance=0.85,
                                       labeldistance=1.05)
    
    [autotexts.set_color('white') for autotexts in autotexts]
    
    circle = plt.Circle( (0,0), 0.7, color='white')
    p=plt.gcf()
    p.gca().add_artist(circle)
    plt.title('Fatal Attacks', pad=-260)
    #plt.savefig('DonutChart2.png',bbox_inches="tight")
return plt.show()
```
#### Great White Sharks are responsible for over 50% of fatal attacks! 
![This is an image](../PandasSunshineAndRainbows/images/DonutChart2.png) 

## This graphic is scary!


#### Let's put things back into perspective: 
``` python 
# NOW need Proportion of Fatal to NonFatal Incidents 
Proportion_Fatal= spattacks2.groupby([spattacks2['Fatal?']== 'Y']).count()
Proportion_Fatal= pd.DataFrame(Proportion_Fatal)
Proportion_Fatal= Proportion_Fatal.drop(['Fatal?'], axis=1)
Proportion_Fatal.rename(columns={'Species': 'Incidents'},inplace= True)
Proportion_Fatal.index.rename(' ', inplace= True)
Proportion_Fatal.rename({0: 'NonFatal', 1: 'Fatal'}, axis='index', inplace= True)
Proportion_Fatal_styled = Proportion_Fatal.style.background_gradient()
# export table 
dfi.export(Proportion_Fatal_styled,"FatalvsNonFatalProportions.png")
```

![This is an image](../PandasSunshineAndRainbows/images/FatalvsNonFatalProportions.png) 
#### Don't worry! Only about 16% of reported (measurable) incidents were fatal! 

<iframe src="https://giphy.com/embed/SShJcu4ySty1G6MX9A" width="480" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/echilibrultau-emoji-emoticon-emojis-SShJcu4ySty1G6MX9A">via GIPHY</a></p>

#### And if you're in doubt, just avoid areas with great whites, bull sharks, or tiger sharks. 