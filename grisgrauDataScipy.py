import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import statistics
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
import pydeck as pdk

plt.style.use('seaborn')

grisgrau = pd.read_excel(r'C:\Users\letic\Documents\grisGrau\grisgrau.xlsx', index_col=0, converters={'longitude':float,'latitude':float})
grisgrauBerlin = grisgrau[grisgrau['CITY'] =='Berlin']
grisgrauJapan = grisgrau[grisgrau['COUNTRY'] =='Japan']
grisgrauSKorea = grisgrau[grisgrau['COUNTRY'] =='South Korea']
grisgrauTrier = grisgrau[grisgrau['CITY'] =='Trier']

st.title(":fork_and_knife: Data from grisGrau Blog")
st.write("## __*Berlin and Japan Food Guide*__")
st.write("### Behind the scenes —*from Data Analysis to Machine Learning*")
st.write("[grisGrau Blog](http://grisgrau.wordpress.com)")
st.write("\n")
st.write("\n")

st.write("### 0. Dataset")
st.write("\n")
st.write("Displaying data from table:")

col_names = grisgrau.columns.tolist()
col_select = st.multiselect("Columns",col_names, default = col_names)
st.dataframe(grisgrau[col_select])
st.write("\n")
st.write("\n")

st.write("#### 1.0  Berlin Food Guide")
st.write("\n")

expensesBerlin = grisgrauBerlin['EXPENSES_PER_PERSON']
colorsb = ['purple','navy', 'turquoise', 'coral', 'purple', 'navy', 'turquoise', 'coral', 'purple', 'navy', 'turquoise', 'coral', 'purple', 'navy', 'turquoise', 'coral', 'purple', 'navy', 'turquoise', 'coral', 'purple', 'navy', 'turquoise', 'coral', 'purple', 'navy', 'turquoise', 'coral', 'purple', 'navy', 'turquoise', 'coral', 'purple', 'navy', 'turquoise', 'coral']
# modify quantity of colors according to the quantity of rows, i.e. 37 rows => 37 colors

colors = {'Restaurant':'purple', 'Ice Cream Shop':'yellow', 'Cafe':'turquoise', 'Food Stand':'#33CC33', 'Bakery':'navy', 'Bar': 'coral'}

fig, ax = plt.subplots()
ax = plt.scatter(x=grisgrauBerlin['EXPENSES_PER_PERSON'], y=grisgrauBerlin['RATING'], s = np.array(expensesBerlin) * 90, alpha = 0.5, c=grisgrauBerlin['TYPE'].apply(lambda x: colors[x]))

type_a = mpatches.Patch(color='#993399', label='Restaurant')
type_b = mpatches.Patch(color='#12F5B6', label='Cafe')
type_c = mpatches.Patch(color='#33CC33', label='Food Stand')
type_d = mpatches.Patch(color='#F2FD08', label='Ice Cream Shop')
type_e = mpatches.Patch(color='#6273BE', label='Bakery')
type_f = mpatches.Patch(color='#6273BE', label='Bar')

plt.legend(handles=[type_a,type_b,type_c, type_d,type_e], loc='lower right', title='Type')

plt.ylabel("grisGrau's Rating ~max: 10~")
plt.xlabel('Average in EUR per person')
plt.xlim(1.9,35)
plt.ylim(6.5, 10)
plt.xscale('linear')
plt.title('Berlin Food Guide')
st.pyplot(fig)

st.write("#### 1.1. Global Statistics")

st.write()

def myformat(x):
    return ('%.2f' % x).rstrip('0').rstrip('.')

st.write(pd.DataFrame({
     'Description': ["Global - Max", "Berlin - Max","Global - Min", "Berlin - Min"],
     'Rating': [myformat(grisgrau['RATING'].max()) , grisgrauBerlin['RATING'].max(),grisgrau['RATING'].min() , grisgrauBerlin['RATING'].min() ],
     'Place name' :[grisgrau.loc[grisgrau['RATING'] == grisgrau['RATING'].max(), 'PLACE_NAME'].values[0],
     grisgrauBerlin.loc[grisgrauBerlin['RATING'] == grisgrauBerlin['RATING'].max(), 'PLACE_NAME'].values[0],
     grisgrau.loc[grisgrau['RATING'] == grisgrau['RATING'].min(), 'PLACE_NAME'].values[0],
     grisgrauBerlin.loc[grisgrauBerlin['RATING'] == grisgrauBerlin['RATING'].min(), 'PLACE_NAME'].values[0]
     ],
 }))


st.write("#### 1.1  Berlin Food Guide")
st.write("\n")


fig, ax = plt.subplots()
ax =sns.barplot(x=grisgrauBerlin['EXPENSES_PER_PERSON'], y=grisgrauBerlin['RATING'], alpha=0.5, palette="viridis", order= grisgrauBerlin.sort_values('RATING').EXPENSES_PER_PERSON, ci=None) #rocket, hls 
plt.xscale('linear')
plt.xlim(-1,55)
plt.ylim(6.5,10)
plt.ylabel("grisGrau's Rating ~max: 10~")
plt.xlabel('Average in EUR per person')
plt.title('Berlin Food Guide')
#ax.xaxis.set_major_formatter(plt.FixedFormatter(grisgrauBerlin['DATE'].to_series().dt.strftime("%Y-%m-%d")))
st.pyplot(fig)

df = pd.DataFrame(grisgrauBerlin, columns=['longitude', 'latitude', 'TYPE'])


TYPE_COLORS = {
    'Restaurant': [255, 32, 32, 160],
    'Bakery': [64, 128, 64, 160],
    'Cafe': [32, 128, 255, 160],
    'Ice Cream Shop': [0, 255, 0, 160],
    'Food Stand': [139, 69, 19, 160]
}
df["type_color"] = df["TYPE"].apply(lambda x: TYPE_COLORS[x])

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/streets-v9', #v-11
    initial_view_state=pdk.ViewState(
        latitude=52.520008,
        longitude=13.404954,
        zoom=10.5,
        pitch=50,
    ),
    layers=[
#        pdk.Layer(
#            'HexagonLayer',
#            data=df,
#            get_position='[longitude, latitude]',
#            radius=100,
#            elevation_scale=3,
#            elevation_range=[0, 100],
#            pickable=True,
#            extruded=True,
#        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=df,
            get_position='[longitude, latitude]',
            get_fill_color="type_color",
            get_radius=100,
        ),
    ],
))


###Plotting
st.write("# Food Map Berlin")
##display figures
fig,ax = plt.subplots() #must create a subplot
ax = sns.scatterplot(x = grisgrauBerlin["latitude"], y = grisgrauBerlin["longitude"])
st.pyplot(fig)


##display map data
st.write("## plotting geographical data")
st.map(grisgrauBerlin, zoom = 11.5)

st.write("#### 1.2  Berlin Food Guide - Cafes")
st.write("\n")


fig, ax = plt.subplots()
# def display_figures(ax,df):
#     show=df.MONTH.to_list()
#     i=0
#     for p in ax.patches:
#         h=p.get_height()
#         if (h>0):
#             value=show[i]
#             ax.text(p.get_x()+p.get_width()/2,h+10, value, ha='center')
#             i=i+1

#plt.figure(figsize=(15,10))
plot_data=grisgrauBerlin[grisgrauBerlin.TYPE=="Cafe"].sort_values(by=['YEAR','MONTH'])
ax=sns.barplot(x='PLACE_NAME',y='RATING',data=plot_data, hue='CUISINE', palette="mako",dodge=False)
#display_figures(ax,plot_data)

#plt.xlim(-1,55)
plt.ylim(6.5,10)
plt.ylabel("grisGrau's Rating ~max: 10~")
plt.xlabel('Average in EUR per person')
plt.title('Berlin Food Guide')
plt.xticks(rotation=90)
#ax.xaxis.set_major_formatter(plt.FixedFormatter(grisgrauBerlin['DATE'].to_series().dt.strftime("%Y-%m-%d")))
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
st.pyplot(fig)

st.write("#### 1.3  Berlin Food Guide - Restaurants")
st.write("\n")

plt.figure(figsize=(25,10))
fig, ax = plt.subplots()
# def display_figures(ax,df):
#     show=df.MONTH.to_list()
#     i=0
#     for p in ax.patches:
#         h=p.get_height()
#         if (h>0):
#             value=show[i]
#             ax.text(p.get_x()+p.get_width()/2,h+10, value, ha='center')
#             i=i+1


plot_data=grisgrauBerlin[grisgrauBerlin.TYPE=="Restaurant"].sort_values(by='EXPENSES_PER_PERSON')
ax=sns.barplot(x='PLACE_NAME',y='RATING',data=plot_data, hue='MONTH',alpha = 0.5, dodge=False)
#display_figures(ax,plot_data)

#plt.xlim(-1,55)
plt.ylim(6.5,10)
plt.ylabel("grisGrau's Rating ~max: 10~")
plt.xlabel('Average in EUR per person')
plt.title('Berlin Food Guide')
plt.xticks(rotation=90)
#plt.xticks(np.arange(0, 20, step=0.2))  # Set label locations.
#ax.xaxis.set_major_formatter(plt.FixedFormatter(grisgrauBerlin['DATE'].to_series().dt.strftime("%Y-%m-%d")))
ax.set_xticklabels(ax.get_xticklabels(), fontsize=7)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.tight_layout()
st.pyplot(fig)

#######################################################################################################

st.write("#### 1.3  Berlin Food Guide - Restaurant per year")
st.write("\n")

plt.figure(figsize=(25,10))
fig, ax = plt.subplots()
# def display_figures(ax,df):
#     show=df.MONTH.to_list()
#     i=0
#     for p in ax.patches:
#         h=p.get_height()
#         if (h>0):
#             value=show[i]
#             ax.text(p.get_x()+p.get_width()/2,h+10, value, ha='center')
#             i=i+1


plot_data=grisgrauBerlin[grisgrauBerlin.TYPE=="Restaurant"].sort_values(by=['YEAR','MONTH'])
ax=sns.barplot(x='PLACE_NAME',y='RATING',data=plot_data, hue='CUISINE', dodge=False)
#display_figures(ax,plot_data)

#plt.xlim(-1,55)
plt.ylim(6.5,10)
plt.ylabel("grisGrau's Rating ~max: 10~")
plt.xlabel('Average in EUR per person')
plt.title('Berlin Food Guide')
plt.xticks(rotation=90)
#plt.xticks(np.arange(0, 20, step=0.2))  # Set label locations.
#ax.xaxis.set_major_formatter(plt.FixedFormatter(grisgrauBerlin['DATE'].to_series().dt.strftime("%Y-%m-%d")))
ax.set_xticklabels(ax.get_xticklabels(), fontsize=7)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0, fontsize=7)
plt.tight_layout()
st.pyplot(fig)

###############################################################################################

#######################################################################################################

st.write("#### 1.4  Berlin Food Guide - German Cuisine")
st.write("\n")

plt.figure(figsize=(25,10))
fig, ax = plt.subplots()
# def display_figures(ax,df):
#     show=df.MONTH.to_list()
#     i=0
#     for p in ax.patches:
#         h=p.get_height()
#         if (h>0):
#             value=show[i]
#             ax.text(p.get_x()+p.get_width()/2,h+10, value, ha='center')
#             i=i+1


plot_data=grisgrauBerlin[grisgrauBerlin.CUISINE=="German Cuisine"].sort_values(by=['YEAR','MONTH'])
ax=sns.barplot(x='PLACE_NAME',y='RATING',data=plot_data, hue='TYPE', dodge=False)
#display_figures(ax,plot_data)

#plt.xlim(-1,55)
plt.ylim(6.5,10)
plt.ylabel("grisGrau's Rating ~max: 10~")
plt.xlabel('Average in EUR per person')
plt.title('Berlin Food Guide')
plt.xticks(rotation=90)
#plt.xticks(np.arange(0, 20, step=0.2))  # Set label locations.
#ax.xaxis.set_major_formatter(plt.FixedFormatter(grisgrauBerlin['DATE'].to_series().dt.strftime("%Y-%m-%d")))
ax.set_xticklabels(ax.get_xticklabels(), fontsize=7)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0, fontsize=7)
plt.tight_layout()
st.pyplot(fig)

###############################################################################################

st.write("#### 2.0  Japan Food Guide")
st.write("\n")

plt.figure(figsize=(25,10))
fig, ax = plt.subplots()

plot_data=grisgrauJapan[grisgrauJapan.TYPE=="Restaurant"].sort_values(by='EXPENSES_PER_PERSON')
ax=sns.barplot(x='PLACE_NAME',y='RATING',data=plot_data, hue='MONTH',alpha = 0.5, dodge=False)
#display_figures(ax,plot_data)

#plt.xlim(-1,55)
plt.ylim(6.5,10)
plt.ylabel("grisGrau's Rating ~max: 10~")
plt.xlabel('Average in EUR per person')
plt.title('Japan Food Guide')
plt.xticks(rotation=90)
#plt.xticks(np.arange(0, 20, step=0.2))  # Set label locations.
#ax.xaxis.set_major_formatter(plt.FixedFormatter(grisgrauBerlin['DATE'].to_series().dt.strftime("%Y-%m-%d")))
ax.set_xticklabels(ax.get_xticklabels(), fontsize=7)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.tight_layout()
st.pyplot(fig)


st.write("#### 1.0  Japan Food Guide")
st.write("\n")

expensesJapan = grisgrauJapan['EXPENSES_PER_PERSON']


colors = {'Restaurant':'purple',  'Cafe':'turquoise', 'Food Stand':'#33CC33', 'Bar': 'coral', 'Bakery':'navy' }

fig, ax = plt.subplots()
ax = plt.scatter(x=grisgrauJapan['EXPENSES_PER_PERSON'], y=grisgrauJapan['RATING'], s = np.array(expensesJapan)*1.8, alpha = 0.5, c=grisgrauJapan['TYPE'].apply(lambda x: colors[x]))

typea = mpatches.Patch(color='#993399', label='Restaurant')
typeb = mpatches.Patch(color='#12F5B6', label='Cafe')
typec = mpatches.Patch(color='#33CC33', label='Food Stand')
typed = mpatches.Patch(color='coral', label='Bar')
typee = mpatches.Patch(color='#6273BE', label='Bakery')

plt.legend(handles=[typea,typeb,typec, typed,typee], loc='lower right', title='Type')

plt.ylabel("grisGrau's Rating ~max: 10~")
plt.xlabel('Average in JPY per person')
plt.xlim(0,3500)
plt.ylim(6.5, 10)
plt.xscale('linear')
plt.title('Japan Food Guide')
st.pyplot(fig)


###############################################################################################

st.write("#### 2.0  South Korean Food Guide")
st.write("\n")

plt.figure(figsize=(25,10))
fig, ax = plt.subplots()

plot_data=grisgrauSKorea[grisgrauSKorea.TYPE=="Restaurant"].sort_values(by='EXPENSES_PER_PERSON')
ax=sns.barplot(x='PLACE_NAME',y='RATING',data=plot_data, hue='MONTH',alpha = 0.5, dodge=False)
#display_figures(ax,plot_data)

#plt.xlim(-1,55)
plt.ylim(6.5,10)
plt.ylabel("grisGrau's Rating ~max: 10~")
plt.xlabel('Average in KRW per person')
plt.title('South Korea Food Guide')
plt.xticks(rotation=90)
#plt.xticks(np.arange(0, 20, step=0.2))  # Set label locations.
#ax.xaxis.set_major_formatter(plt.FixedFormatter(grisgrauBerlin['DATE'].to_series().dt.strftime("%Y-%m-%d")))
ax.set_xticklabels(ax.get_xticklabels(), fontsize=7)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.tight_layout()
st.pyplot(fig)


st.write("#### 1.0  South Korean Food Guide")
st.write("\n")

expensesSKorea = grisgrauSKorea['EXPENSES_PER_PERSON']


colors = {'Restaurant':'purple',  'Cafe':'turquoise', 'Food Stand':'#33CC33', 'Bar': 'coral', 'Bakery':'navy' }

fig, ax = plt.subplots()
ax = plt.scatter(x=grisgrauSKorea['EXPENSES_PER_PERSON'], y=grisgrauSKorea['RATING'], s = np.array(expensesSKorea)*0.4, alpha = 0.5, c=grisgrauSKorea['TYPE'].apply(lambda x: colors[x]))

typeaa = mpatches.Patch(color='#993399', label='Restaurant')
typebb = mpatches.Patch(color='#12F5B6', label='Cafe')
typecc = mpatches.Patch(color='#33CC33', label='Food Stand')
typedd = mpatches.Patch(color='coral', label='Bar')
typeee = mpatches.Patch(color='#6273BE', label='Bakery')

plt.legend(handles=[typeaa,typebb,typecc, typedd,typeee], loc='lower right', title='Type')

plt.ylabel("grisGrau's Rating ~max: 10~")
plt.xlabel('Average in KRW per person')
plt.xlim(3000,20000)
plt.ylim(6.5, 10)
plt.xscale('linear')
plt.title('South Korean Food Guide')
st.pyplot(fig)