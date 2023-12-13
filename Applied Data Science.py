
"""
Created on Thu Dec 13 08:52:54 2023

@author: Saman
"""

import numpy as np
import pandas as pd
import scipy.stats as sp
import matplotlib.pyplot as plt


def read_world_bank_data(filename):
    """
    read the world bank data with filename.
    processed the dataframe into worldbank format.
    created two dataframes with years as index and countries as index.

    Parameters
    ----------
    filename : String
        input the filename of csv.

    Returns
    -------
    df_year_index : Pandas.Dataframe
        dataframe with years as index.
    df_country_index : Pandas.Dataframe
        dataframe with countries as index.

    """

    # Read the World Bank data into the dataframe
    df = pd.read_csv(filename, skiprows=4)
    # years from 1991 to 2012 are selected
    all_cols_list = ["Country Name", "1991", "1992", "1993", "1994",
                     "1995", "1996", "1997", "1998", "1999", "2000",
                     "2001", "2002", "2003", "2004", "2005", "2006",
                     "2007", "2008", "2009", "2010", "2011", "2012"]
    # ten countries from different continents are selected
    country_list = ["Ecuador", "Algeria", "Canada", "France",
                    "Malaysia", "Spain", "Nepal", "Pakistan",
                    "Norway", "United Arab Emirates"]
    # two dataframes with years in column and countries as column
    # and drop NA values
    df.dropna(axis=1)
    df = df.loc[df["Country Name"].isin(country_list),
                all_cols_list]
    df.index = df["Country Name"]
    df.drop("Country Name", axis=1, inplace=True)
    df.columns = df.columns.astype(int)

    return df.T, df


def show_stat(title, df_stats):
    """
    exploring statistical properties using describe() method.
    also used median(), kurtosis(), skewness() methods for dataframes.

    Parameters
    ----------
    title : string
        print title on table chart.
    df_stat : pandas dataframe
        it is used to plot table chart of statistical properties.

    Returns
    -------
    None.

    """
    # print the title
    print("====="+title+"=====")

    # using Decrible method
    print("======Describe=====")
    print(df_stats.describe())
    # using Median method

    print("======median======")
    print(df_stats.median())
    # using Kurtosis method

    print("======kurtosis======")
    kur = pd.DataFrame(sp.kurtosis(df_stats),
                       index=df_stats.columns, columns=[""])
    print(kur)
    # using Skewness method

    print("======skewness======")
    ske = pd.DataFrame(sp.skew(df_stats), index=df_stats.columns, columns=[""])
    print(ske)
    print()


def create_corr(country, df_m, df_gdp, df_agr, df_cer, df_pop, df_elec):
    """
    finding correlation between different parameters


    Parameters
    ----------
    country : String
        name of countries for which coorelation is finded.
    df_M : float
        Dataframe for methane emission.
    df_Gdp : float
        Dataframe for GDP.
    df_Agr : float
        Dataframe for agricultural land.
    df_Cer : float
        Dataframe for cereal yield.
    df_Pop : float
        Dataframe for population growth.
    df_Elec : float
        Dataframe of electric power consumption.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """

    df_corr = pd.DataFrame()
    df_corr["CH4 Emission"] = df_m[country].values
    df_corr["GDP"] = df_gdp[country].values
    df_corr["Agr. Land"] = df_agr[country].values
    df_corr["Cer. Yield"] = df_cer[country].values
    df_corr["Pop. Growth"] = df_pop[country].values
    df_corr["EPC"] = df_elec[country].values

    corr = df_corr.corr()
    return corr.round(2)


def show_corr(title, corr, cmap):
    """
    creating heatmaps for Spain, United Arab Emirates and Pakistan to
    to show the correlation among all indicators.

    Parameters
    ----------
    title : string
        country name.
    corr : float
        it shows interrelation among factors.
    cmap : string
        it select the colors for heatmaps.

    Returns
    -------
    None.

    """

    plt.figure()
    plt.imshow(corr, cmap=cmap, vmin=-1, vmax=1)
    plt.colorbar()
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.title(title, fontsize=14, y=1.03)
    for (i, j), z in np.ndenumerate(corr):
        plt.text(j, i, '{:0.2f}'.format(z), ha='center', va='center')
    plt.savefig(title+".png", dpi=300, bbox_inches="tight")
    plt.show()


def line_plot(df, title, ylabel):
    """
    creating line plot for two indicators of Dataframe df

    Parameters
    ----------
    df : pandas.dataframe
        create line plot for df.
    title : string
        title of the line plot.
    ylabel : string
        set y label of the plot.

    Returns
    -------
    None.

    """
    df.plot()
    plt.title(title, fontsize=14, y=1.03)
    plt.xlabel("Years")
    plt.ylabel(ylabel)
    plt.legend(["ECU", "ALG", "CAN", "FRA", "MAL", "SPA", "NPL",
                "PAK", "NOR", "UAE"], loc="upper left", fontsize=6)
    plt.minorticks_on()
    plt.savefig(title+".png", dpi=300, bbox_inches="tight")
    plt.show()


def bar_plot(df, title, ylabel):
    """
    creating bar plot for two indicators dataframe df


    Parameters
    ----------
    df : pandas.dataframe
        create bar plot for dataframe df.
    title : string
        title of the bar plot.
    ylabel : string
        set the y label of the plot.

    Returns
    -------
    None.

    """

    df.loc[:, [1997, 2000, 2003, 2006, 2009, 2012]].plot.bar()
    plt.title(title, fontsize=14, y=1.03)
    plt.xlabel("Countries")
    plt.ylabel(ylabel)
    plt.legend([1997, 2000, 2003, 2006, 2009, 2012], loc="upper right",
               fontsize=6)
    plt.xticks(rotation=65)
    plt.savefig(title+".png", dpi=300, bbox_inches="tight")
    plt.show()


# Example usage
# Replace with your actual file path
M_Years_df, M_countries_df = read_world_bank_data("Methane_Emission.csv")
Gdp_Years_df, Gdp_countries_df = read_world_bank_data("GDP.csv")
Agr_Years_df, Agr_countries_df = read_world_bank_data("Agricultural_Land.csv")
Cer_Years_df, Cer_countries_df = read_world_bank_data("Cereal_Yield.csv")
Pop_Years_df, Pop_countries_df = read_world_bank_data("Population_Growth.csv")
Elec_Years_df, Elec_countries_df = read_world_bank_data(
    "Electric_Power_Consumption.csv")


# statistical methods describe(), median(), kurtosis() and skewness()
show_stat("Methane Emission", M_Years_df)
show_stat("GDP", Gdp_Years_df)
show_stat("Agricultural Land", Agr_Years_df)
show_stat("Cereal Yield", Cer_Years_df)
show_stat("Population Growth", Pop_Years_df)
show_stat("Electric Power Consumption", Elec_Years_df)


# correlation between indicators for Spain
corr_Spain = create_corr("Spain", M_Years_df, Gdp_Years_df, Agr_Years_df,
                         Cer_Years_df, Pop_Years_df, Elec_Years_df)
show_corr("Spain", corr_Spain, "PRGn")

# correlation between indicators for United Arab emirates
corr_United_Arab_Emirates =\
    create_corr("United Arab Emirates", M_Years_df,
                Gdp_Years_df, Agr_Years_df, Cer_Years_df,
                Pop_Years_df, Elec_Years_df)
show_corr("United Arab Emirates", corr_United_Arab_Emirates, "magma")

# correlation between indicators for Pakistan
corr_Pakistan = create_corr("Pakistan", M_Years_df, Gdp_Years_df, Agr_Years_df,
                            Cer_Years_df, Pop_Years_df, Elec_Years_df)
show_corr("Pakistan", corr_Pakistan, "pink")


# line plot of Agricultural land
line_plot(Agr_Years_df, "Agricultural Land of 10 Different Countries",
          "agricultural land(sq. km)")

# line plot of Cereal yield
line_plot(Cer_Years_df, "Cereal Yield of 10 Different Countries",
          "cereal yield(kg per hectare)")


# bar plot of Methane emission
bar_plot(M_countries_df, "Methane Emission of 10 Different Countries",
         "methane emission(% change)")

# bar plot of GDP
bar_plot(Gdp_countries_df, "GDP of 10 Different Countries",
         "GDP(Current US$)")
