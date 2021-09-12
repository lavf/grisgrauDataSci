import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import statistics
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches

plt.style.use('seaborn')

grisgrau = pd.read_excel(r'C:\Users\letic\Documents\grisGrau\grisgrau.xlsx', index_col=0)
grisgrauBerlin = grisgrau[grisgrau['CITY'] =='Berlin']
grisgrauJapan = grisgrau[grisgrau['COUNTRY'] =='Japan']

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

colors = {'Restaurant':'purple', 'Ice Cream Shop':'yellow', 'Cafe':'turquoise', 'Food Stand':'#33CC33', 'Bakery':'navy'}

fig, ax = plt.subplots()
ax = plt.scatter(x=grisgrauBerlin['EXPENSES_PER_PERSON'], y=grisgrauBerlin['RATING'], s = np.array(expensesBerlin) * 90, alpha = 0.5, c=grisgrauBerlin['TYPE'].apply(lambda x: colors[x]))

type_a = mpatches.Patch(color='#993399', label='Restaurant')
type_b = mpatches.Patch(color='#12F5B6', label='Cafe')
type_c = mpatches.Patch(color='#33CC33', label='Food Stand')
type_d = mpatches.Patch(color='#F2FD08', label='Ice Cream Shop')
type_e = mpatches.Patch(color='#6273BE', label='Bakery')

plt.legend(handles=[type_a,type_b,type_c, type_d,type_e], loc='lower right', title='Type')

plt.ylabel("grisGrau's Rating ~max: 10~")
plt.xlabel('Average in EUR per person')
plt.xlim(1.9,30)
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
plt.xlim(-1,27)
plt.ylim(6.5,10)
plt.ylabel("grisGrau's Rating ~max: 10~")
plt.xlabel('Average in EUR per person')
plt.title('Berlin Food Guide')
st.pyplot(fig)

st.write("#### 1.0  Japan Food Guide")
st.write("\n")

expensesJapan = grisgrauJapan['EXPENSES_PER_PERSON']


colors = {'Restaurant':'purple', 'Bar':'yellow', 'Cafe':'turquoise', 'Food Stand':'#33CC33', 'Bakery':'navy'}

fig, ax = plt.subplots()
ax = plt.scatter(x=grisgrauJapan['EXPENSES_PER_PERSON'], y=grisgrauJapan['RATING'], s = np.array(expensesJapan)*1.8, alpha = 0.5, c=grisgrauJapan['TYPE'].apply(lambda x: colors[x]))

typea = mpatches.Patch(color='#993399', label='Restaurant')
typeb = mpatches.Patch(color='#12F5B6', label='Cafe')
typec = mpatches.Patch(color='#33CC33', label='Food Stand')
typed = mpatches.Patch(color='#F2FD08', label='Bar')
typee = mpatches.Patch(color='#6273BE', label='Bakery')

plt.legend(handles=[typea,typeb,typec, typed,typee], loc='lower right', title='Type')

plt.ylabel("grisGrau's Rating ~max: 10~")
plt.xlabel('Average in JPY per person')
plt.xlim(100,1600)
plt.ylim(6.5, 10)
plt.xscale('linear')
plt.title('Japan Food Guide')
st.pyplot(fig)