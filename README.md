![Image](https://motor.elpais.com/wp-content/uploads/2017/06/2017_06_25_foster.jpg)

# Ironhack Final-Project


### :fuelpump: **About** 

This is the Data Analysis Bootcamp Final Project, where I have created an application which allows users to enter an address and find the nearest gas stations. In addition, they will be able to see their location and price from gasoline 95 and diesel.
This project is made with the aim to cover all the tech we have studied along the bootcamp. Also, I have used some libraries I have not seen before such as Prophet and Streamlit.   

<p align="center"><img src="https://media.giphy.com/media/3ohzdGGktYVpPRtgRy/giphy.gif"></p>


### **Step 1. Getting started**

First, fork this repository to your **GitHub** and clone it in your local hard drive. 

```
$ git clone https://github.com/<your-account>/<lab-repo>.git
```
Then you will obtain a folder named as the repository you have cloned. Now, you can start working with this. Enjoy it!

### **Step 2. Install** 

Now, you must create a new environment in the terminal and install python and kernel as is show below.
```
Conda create -n “name”
conda install ipykernel
conda install python=3.7
```
To run this code you should use Visual Studio Code. Click [here](https://docs.microsoft.com/es-es/visualstudio/mac/installation?view=vsmac-2019) to download it. 

To execute the code, you must install some libraries and import them:

```
pip install pandas
conda install requests
conda install geocoders
pip install folium
pip install prophet
pip install streamlit
```

### **Step 3. Data Acquisition**

To get the data from **today´s prices** from all the gas stations in Spain, we work with the rest API. To obtain the price history, there is an **accumulated file** with the prices from 04/04/2022 until today. Each time we run this code; the API data will get saved in the accumulated file. Here you can visit the web for the [API](https://sede.serviciosmin.gob.es/es-ES/datosabiertos/catalogo/precios-carburantes).

### **Step 4. Analysis**

Once the user introduces the location in the Streamlit app, it will take the coordinates of that place and start working with them. Distance will be calculated thanks to Geocoders library, and it will get a final DataFrame with the 10 nearest gas stations ordered by distance from the location introduced.

### :chart_with_downwards_trends: **Step 5. Reporting**

The result is a map, created with folium library with several markers which mean the following: 
    
    •Grey marker with the house: your current location
    •Color markers: gas stations
        ·Red: Above average price
        ·Orange: Average price for all gas stations in Spain
        ·Green: Below the average price

As a final step, a prediction for prices in the next week will be seen in a graphic made with Prophet library. The prices are calculated with the median number for all the gas stations in Spain for each day. Here you can observe the prices of the gasoline in Spain from April 4th until today, and the prediction for the next prices. In addition, a range of error is displayed.

### **Setting up the app**

To run the app, execute this code in the terminal and the browser will open. You have to enter the location you want and then click the “Search!” button.
````
streamlit run main.py 
````

### **Roadmap**

In the future, some releases will be made is to add a filter for the user to select the type of fuel, as well as the number of liters of the car's tank. In this way, it will be possible to estimate the total cost of filling the tank and show the user only the prices according to their needs.
Another improvement to implement will be to estimate which day of the week is the cheapest and create a graph.
Implement the way to calculate the route from the current location to the gas station selected on the map.

### **Contributing**

ll contributions, ideas and bug reports are more than welcome!
If you have any suggestions to implement to improve the code, please, feel free to fork, clone the repo and open a pull request from your fork back to the original main branch. Little by little, with small changes that we incorporate we can create a great project that can become a mobile app.

### :computer: **Tech-stack**

• [Requests](https://docs.python-requests.org/en/latest/)

• [Pandas](https://pandas.pydata.org/pandas-docs/stable/)

• [Folium](https://python-visualization.github.io/folium/modules.html)

• [Geocoders](https://geocoder.readthedocs.io/)

• [Prophet](https://facebook.github.io/prophet/)

• [Streamlit](https://streamlit.io/)

## Happy coding!

