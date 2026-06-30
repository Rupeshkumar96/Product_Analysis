import pandas as pd
from serpapi import GoogleSearch
import streamlit as st
import matplotlib.pyplot as plt


def comapre(med_name):
    params = {
    "engine": "google_shopping",
    "q": med_name,
    "api_key": "3201bbb6dc08f6a8aad79ebe1b100d110ec2b95baa30abcefa5564c48513c86e",
    "gl": "in"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    shopping_results=results.get("shopping_results", [])
    return shopping_results
c1,c2=st.columns(2)
c1.image("images.png", width=200)
c2.header("MediCost Optimizer")


st.sidebar.title("Enter Name of Medicine")
med_name=st.sidebar.text_input("Enter Medicine name")
option=st.sidebar.text_input("Enter Number of options to compare")
company_name=[]
price_analysis=[]
if med_name is not None:
    if st.sidebar.button("Search Results"):
        shopping_results=comapre(med_name)
        lowest_price=float((shopping_results[0].get('extracted_price')))
        lowest_price_index=0
        st.sidebar.image(shopping_results[0].get('thumbnail'), width=200)
        for i in range(int(option)):
            current_price=float((shopping_results[i].get('extracted_price')))
            if current_price<lowest_price:
                lowest_price=current_price
                lowest_price_index=i

            # --Price analysis--------*/
            company_name.append(shopping_results[i].get('source'))
            price_analysis.append(float(shopping_results[i].get('extracted_price')))

            st.title(f'Option {i+1}')

            c1,c2=st.columns(2)
            c1.write("Company Name")
            c2.write(shopping_results[i].get('source'));

            c1.write("Title")
            c2.write(shopping_results[i].get('title'));

            c1.write("Price")
            c2.write(shopping_results[i].get('extracted_price'));
            url=shopping_results[i].get('product_link')
            c1.write("Buy Link")
            c2.write("[Buy Now](%s)" % url);
            """--------------------------------------------------------------"""
        

        st.title("Best Option / Lowest Price ")

        c1,c2=st.columns(2)
        c1.write("Company Name")
        c2.write(shopping_results[lowest_price_index].get('source'));

        c1.write("Title")
        c2.write(shopping_results[lowest_price_index].get('title'));

        c1.write("Price")
        c2.write(shopping_results[lowest_price_index].get('extracted_price'));
        url=shopping_results[lowest_price_index].get('product_link')
        c1.write("Buy Link")
        c2.write("[Buy Now](%s)" % url);

        # Graphical Analysis
        df=pd.DataFrame({
            "Company Name":company_name,
            "Price":price_analysis
        })
        st.title("Graphical Analysis")
        st.bar_chart(df.set_index("Company Name"))

        fig, ax = plt.subplots()
        ax.pie(df["Price"], labels=df["Company Name"], autopct='%1.1f%%')
        ax.set_title("Price Distribution")
        st.pyplot(fig) 
 