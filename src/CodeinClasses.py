#!/usr/bin/env python
# coding: utf-8

# In[1]:


class Main: 
    def __init__(self): 
        def Clean_df():
            """
            Clean Dataframe for Data Exploration: import packages, regex, and housekeeping. 
            """
            import pandas as pd
            import numpy as np
            import dataframe_image as dfi 
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


            spattacks2.reset_index(drop= True, inplace= True)
            spattacks2['Species']= spattacks2['Species'].apply(lambda x: x.title())
            return self.spattacks2
        
        def SpeciesAttackFrequencyTable(self): 
            """
            Make Frequency table of ALL species and attacks 
            """
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
            Frequency_Table
            row = pd.Series({'Count':89,'Frequency':4.74},name='Other')
            Frequency_Table = Frequency_Table.append(row)



            #Frequency_Table_Acess
            Frequency_Table['Count']=Frequency_Table['Count'].apply(lambda x: int(x))
            df_styled = Frequency_Table.style.background_gradient().set_precision(2)
            #dfi.export(df_styled,"SharkFrequency.png")
            return self.df_styled
        
        def FatalVsNonFatalTable(self): 
            """
            Group Data by Species and Counts of Fatal vs NonFatal Incidents and return "Frequency Table"
            
            """

            #Group by species number of attacks (both fatal and non)
            Attacks= spattacks2.groupby(['Species']).count()

            #Fatal incidents vs nonfatal 
            Proportion_Fatal= spattacks2.groupby([spattacks2['Fatal?']== 'Y']).count()

            #Group by fatalities 
            fatalities= spattacks2[spattacks2['Fatal?']== 'Y']
            fatal_species_counts= fatalities.groupby(['Species']).count()

            #Non Fatal incidents 
            nonfatal= spattacks2[spattacks2['Fatal?']== 'N']
            nonfatal_species_counts= nonfatal.groupby(['Species']).count()

            ## CREATE FvN DF for Stacked barplot 
            #Group by species number of attacks (both fatal and non)
            nonfatal_species_counts.rename(columns={'Fatal?': 'NonFatal Attacks'}, inplace=True)
            nonfatal_species_counts
            fatal_species_counts.rename(columns= {'Fatal?': 'Fatal Attacks'}, inplace= True)
            fatal_species_counts

            FvsN= nonfatal_species_counts.merge(right= fatal_species_counts, how= 'outer', left_index=True, right_index=True )
            FvsN= FvsN.fillna(0)
            FvsN['Fatal Attacks']= FvsN['Fatal Attacks'].apply(lambda x: int(x))
            FvsN['Total Attacks']= FvsN.apply(np.sum, axis=1)
            FvsN= FvsN.sort_values(by= 'Total Attacks', ascending= False)
            FvsN10= FvsN.iloc[:10]
            FvsN10_styled = FvsN10.style.background_gradient()
            return self.FvsN10_styled
        
        def stackedbargraph(self): 
            """
            Create Stacked Barplot of fatal vs nonfatal incidents per species 
            """
            fig, ax= plt.subplots(1)
            plt.rcParams["figure.figsize"] = (8,6)
            FvN10plot= FvsN10[['NonFatal Attacks', 'Fatal Attacks']].plot(kind='barh', stacked=True, ax=ax, color= {'xkcd:prussian blue', 'xkcd:carolina blue'} )
            plt.title("Which Sharks Should I Worry About?")
            plt.ylabel(' ')
            plt.xlabel("Incidents Recorded")
            plt.savefig('FvsNStackedBar.png',bbox_inches="tight")
            return self.plt.show()
        
        def DonutChart(self): 
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
            return self.plt.show()
        
        def DonutChart2(self): 
            """
            Creates Donut Graph of FATALITY frequency among species
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
            return self.plt.show()
        
        def FatalNonFatalProportionTable(self):
            """
            NOW need % of Incidents Fatal or not 
            """
            # Fatal incidents vs nonfatal           
            Proportion_Fatal= spattacks2.groupby([spattacks2['Fatal?']== 'Y']).count()
            Proportion_Fatal= pd.DataFrame(Proportion_Fatal)
            Proportion_Fatal= Proportion_Fatal.drop(['Fatal?'], axis=1)
            Proportion_Fatal.rename(columns={'Species': 'Incidents'},inplace= True)
            Proportion_Fatal.index.rename(' ', inplace= True)
            Proportion_Fatal.rename({0: 'NonFatal', 1: 'Fatal'}, axis='index', inplace= True)
            Proportion_Fatal_styled = Proportion_Fatal.style.background_gradient()
            Proportion_Fatal_styled
            #dfi.export(Proportion_Fatal_styled,"FatalvsNonFatalProportions.png")
            return self.Proportion_Fatal_styled


# In[ ]:




