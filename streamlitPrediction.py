import streamlit as st
import joblib
import pandas as pd
import sklearn
import category_encoders

#load model and features names
#preprocessing= joblib.load("preprocessing.pkl")
Model= joblib.load("Zomato_Model_Final.pkl")
Inputs= joblib.load("Zomato_Columns_Final.pkl")
menu_items= joblib.load("Menu_items_liked.pkl")
types= joblib.load("rest_type.pkl")
cuisines= joblib.load("cuisines.pkl")
locations = joblib.load("locations.pkl")
listed_in_cities= joblib.load("listed_in_cities.pkl")
listed_in_types= joblib.load("listed_in_types.pkl")
location_dict= joblib.load("location_dict.pkl")

# function to filter the locations in each city to list in the selectbox list
def locations_list(city):
    for cit , loc in location_dict.items():
        if cit == city:
            return loc

#function to calculate the count of dish liked in inputs
def dish_liked_counts(menu_item,other_menu_items):
    if  (other_menu_items != None):
        if (menu_item != None):
            menu_item = list(menu_item)

        elif menu_item == None:
            menu_item = []
        for item in other_menu_items.split(','):
            try:
                
                lst = item.split()
                item_lst = []
                for i in lst:

                    item_lst.append(i.strip().capitalize())
                item = ' '.join(item_lst)
                if item in menu_items:
                    menu_item.append(item)
            except:
                if item.strip().capitalize() in menu_items:
                    menu_item.append(item)
            else:
                pass
        
    else:
        if (menu_item!=None):
            menu_item = list(menu_item)

        elif menu_item == None:
            menu_item = []
    return len(menu_item)



 #main 
def main():
    ## Setting up the page title and icon
    st.set_page_config(page_icon = 'icon.jpg',page_title= 'Restaurants success Prediction')
    # Add a title in the middle of the page using Markdown and CSS
    st.markdown("<h1 style='text-align: center;text-decoration: underline;color:GoldenRod'>Restaurant's success Prediction</h1>", unsafe_allow_html=True)
    #add restaurant image
    st.image("restaurant-1000x550.jpg")

    #record from user
    
    city = st.selectbox('Select City' ,listed_in_cities)
    loc_list = locations_list(city)
    location = st.selectbox('Select Location',loc_list)
    listed_in_type = st.selectbox("Select Restaurant's Type" ,listed_in_types)
    approx_cost = st.slider('What is the approximate cost(for two people)?' ,40,6000,400)
    
    online_order = st.radio('Has option online_order?',['Yes','No'])
    
    book_table = st.radio('Has option book_table?',['Yes','No'])
    
    rest_types  = st.multiselect("Choose Restaurant's types:",list(types),None)

    rest_cuisines  = st.multiselect("Choose Restaurant's cuisines:",list(cuisines),None)

    menu_item  = st.multiselect('Choose Menu items:',menu_items,list(menu_items)[0])
    other_menu_items = st.text_input('Other menu items (separated by ","):',None)
    
    #calculate rest features by calling its functions
    dish_liked_count = dish_liked_counts(menu_item,other_menu_items)
    
    
    

    
#columns:'location', 'listed_in(city)', 'listed_in(type)','approx_cost(for two people)', 'online_order', 'book_table', 'dish_liked_count', 'Quick_Bites_type',


    #create the dataframe of the user's record 
    df =pd.DataFrame(columns=Inputs)
    df.at[0,'location']= location
    df.at[0,'listed_in(city)']= city
    df.at[0,'listed_in(type)']= listed_in_type
    df.at[0,'approx_cost(for two people)']= approx_cost
    df.at[0,'online_order']=  online_order
    df.at[0,'book_table']= book_table
    df.at[0,'dish_liked_count']=  dish_liked_count


    for typ in types:
        if typ in list(rest_types):
            df.at[0,typ]=  1
        
        else:
            df.at[0,typ]=  0
            
   
    for cuis in cuisines :
        if cuis in list(rest_cuisines):
            df.at[0,cuis]=  1
        else:
            df.at[0,cuis]=  0
    
    #button to predict
    if st.button('predict'):
        if (rest_cuisines != None) or (rest_types != None):
            
                st.dataframe(df)
                result= Model.predict(df)[0]

                
            
                if result == 1:
                    st.success("Congrats, your restaurant has the potential to succeed!!")


                else:
                    st.warning("Sorry! Your restaurant may fail")
            
        else:
            st.warning("Please fill in the Restaurant's cuisines and types.")
            


if __name__ == '__main__':
    main()

