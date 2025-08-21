# 🍽️ Local Food Wastage Management System

A **Streamlit + SQLite + Python** project designed to **reduce food wastage** by connecting surplus food providers (restaurants, grocery stores, individuals) with receivers (NGOs, community centers, individuals in need).  

This project demonstrates **SQL database design, CRUD operations, data analysis, and visualization** in a real-world social good context.  

---

## 📌 Features

✅ Restaurants & individuals can list surplus food.  
✅ NGOs or receivers can claim available food.  
✅ SQL database to store food donations, receivers, and claims.  
✅ Streamlit web app with filtering, CRUD operations, and visualization.  
✅ Data analysis with **15+ SQL queries** to track food donation and wastage trends.  

## 🗄️ Database Schema

### 1. Providers Table
- `Provider_ID` (PK)  
- `Name`  
- `Type` (Restaurant, Grocery, Supermarket, etc.)  
- `Address`  
- `City`  
- `Contact`  

### 2. Receivers Table
- `Receiver_ID` (PK)  
- `Name`  
- `Type` (NGO, Individual, Community Center)  
- `City`  
- `Contact`  

### 3. Food Listings Table
- `Food_ID` (PK)  
- `Food_Name`  
- `Quantity`  
- `Expiry_Date`  
- `Provider_ID` (FK)  
- `Provider_Type`  
- `Location`  
- `Food_Type` (Veg/Non-Veg/Vegan)  
- `Meal_Type` (Breakfast/Lunch/Dinner/Snacks)  

### 4. Claims Table
- `Claim_ID` (PK)  
- `Food_ID` (FK)  
- `Receiver_ID` (FK)  
- `Status` (Pending/Completed/Cancelled)  
- `Timestamp`  

---

## 🔍 SQL Queries & Analysis

The project answers **15+ business questions** using SQL queries, such as:

1. How many food providers and receivers are in each city?  
2. Which type of provider contributes the most food?  
3. What is the contact info of providers in a specific city?  
4. Which receivers have claimed the most food?  
5. What is the total quantity of food available?  
6. Which city has the highest number of food listings?  
7. What are the most common food types?  
8. How many food claims exist per food item?  
9. Which provider had the highest successful claims?  
10. % of claims (Completed vs Pending vs Cancelled).  
11. Avg. food quantity claimed per receiver.  
12. Most claimed meal type.  
13. Total donations by each provider.  
14. Trends in donations by city.  
15. Wastage patterns (unclaimed/expired items).  

---

## 🚀 Getting Started

### 1️⃣ Clone Repository
```bash
git clone https://github.com/yourusername/food_wastage_system.git
cd food_wastage_system
2️⃣ Install Requirements
bash
Copy
Edit
pip install -r requirements.txt
Example requirements.txt:

php
Copy
Edit
pandas
streamlit
sqlite3-binary
3️⃣ Create Database
bash
Copy
Edit
python create_db.py
4️⃣ Run Streamlit App
bash
Copy
Edit
streamlit run app/main.py
App will be available at:
👉 http://localhost:8501

📊 Deliverables
Streamlit App with filtering, CRUD, and visualization.

15+ SQL Queries displayed with insights.

Data Analysis on wastage trends.

SQLite Database with structured records.

📈 Example Visualizations
Food donations by city (bar chart)

Claims status distribution (pie chart)

Most claimed meal types (bar chart)

Provider contributions (ranking table)

🏆 Evaluation Metrics
✅ Completeness of SQL database

✅ Accuracy of SQL queries

✅ CRUD operations in Streamlit

✅ User-friendliness of UI

📚 References
Streamlit Docs

SQLite Tutorial

Project Orientation Materials (English/Tamil/Hindi)

👩‍💻 Tech Stack
Python

SQLite

Streamlit

Pandas

✨ This project contributes to reducing food wastage and promoting social good through data-driven insights and an easy-to-use platform.
