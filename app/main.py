import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Food Wastage Management", page_icon="🍽️", layout="wide")
st.title("🍽️ Local Food Wastage Management System")

# Connect to database
conn = sqlite3.connect("food.db")
cursor = conn.cursor()

# -------------------------------
# Load unique values for filters
# -------------------------------
cities = pd.read_sql("SELECT DISTINCT City FROM providers", conn)["City"].dropna().tolist()
providers = pd.read_sql("SELECT DISTINCT Name FROM providers", conn)["Name"].dropna().tolist()
food_types = pd.read_sql("SELECT DISTINCT Food_Type FROM food_listings", conn)["Food_Type"].dropna().tolist()
meal_types = pd.read_sql("SELECT DISTINCT Meal_Type FROM food_listings", conn)["Meal_Type"].dropna().tolist()

# -------------------------------
# All 15 Queries (dictionary)
# -------------------------------
queries = {
    "1. Providers count by city": """
        SELECT City, COUNT(*) AS total_providers
        FROM providers
        GROUP BY City
        ORDER BY total_providers DESC;
    """,
    "2. Receivers count by city": """
        SELECT City, COUNT(*) AS total_receivers
        FROM receivers
        GROUP BY City
        ORDER BY total_receivers DESC;
    """,
    "3. Top provider types by contributions": """
        SELECT Type, COUNT(*) AS total
        FROM providers
        GROUP BY Type
        ORDER BY total DESC;
    """,
    "4. Contact info of providers (example: Chennai)": """
        SELECT Name, Contact
        FROM providers
        WHERE City = 'Chennai';
    """,
    "5. Receivers who claimed the most food": """
        SELECT r.Name, COUNT(c.Claim_ID) AS total_claims
        FROM claims c
        JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
        GROUP BY r.Name
        ORDER BY total_claims DESC
        LIMIT 5;
    """,
    "6. Total quantity of food available": """
        SELECT SUM(Quantity) AS total_food_available
        FROM food_listings;
    """,
    "7. City with highest number of food listings": """
        SELECT Location, COUNT(*) AS listings
        FROM food_listings
        GROUP BY Location
        ORDER BY listings DESC
        LIMIT 1;
    """,
    "8. Most common food types": """
        SELECT Food_Type, COUNT(*) AS count
        FROM food_listings
        GROUP BY Food_Type
        ORDER BY count DESC;
    """,
    "9. Claims count per food item": """
        SELECT f.Food_Name, COUNT(c.Claim_ID) AS total_claims
        FROM claims c
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY f.Food_Name
        ORDER BY total_claims DESC;
    """,
    "10. Provider with highest successful claims": """
        SELECT p.Name, COUNT(c.Claim_ID) AS successful_claims
        FROM claims c
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        JOIN providers p ON f.Provider_ID = p.Provider_ID
        WHERE c.Status = 'Completed'
        GROUP BY p.Name
        ORDER BY successful_claims DESC
        LIMIT 1;
    """,
    "11. Claims status distribution": """
        SELECT Status, COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims) AS percentage
        FROM claims
        GROUP BY Status;
    """,
    "12. Avg quantity claimed per receiver": """
        SELECT r.Name, AVG(f.Quantity) AS avg_quantity
        FROM claims c
        JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY r.Name
        ORDER BY avg_quantity DESC
        LIMIT 5;
    """,
    "13. Most claimed meal type": """
        SELECT f.Meal_Type, COUNT(c.Claim_ID) AS claims
        FROM claims c
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY f.Meal_Type
        ORDER BY claims DESC
        LIMIT 1;
    """,
    "14. Total food donated per provider": """
        SELECT p.Name, SUM(f.Quantity) AS total_donated
        FROM food_listings f
        JOIN providers p ON f.Provider_ID = p.Provider_ID
        GROUP BY p.Name
        ORDER BY total_donated DESC;
    """,
    "15. Food wastage risk (items expiring soon)": """
        SELECT Food_Name, Expiry_Date, Quantity
        FROM food_listings
        WHERE DATE(Expiry_Date) <= DATE('now', '+2 days')
        ORDER BY Expiry_Date ASC;
    """
}

# -------------------------------
# Sidebar Navigation
# -------------------------------
menu = st.sidebar.radio("📌 Menu", ["Analysis", "Manage Food Listings", "Manage Claims"])

# -------------------------------
# 1. Analysis Section (with filters)
# -------------------------------
if menu == "Analysis":
    st.sidebar.subheader("📊 Choose Analysis")
    query_choice = st.sidebar.selectbox("Select a query:", list(queries.keys()))

    # --- Filters ---
    st.sidebar.subheader("🔎 Filters")
    selected_city = st.sidebar.selectbox("City", ["All"] + cities)
    selected_provider = st.sidebar.selectbox("Provider", ["All"] + providers)
    selected_food_type = st.sidebar.selectbox("Food Type", ["All"] + food_types)
    selected_meal_type = st.sidebar.selectbox("Meal Type", ["All"] + meal_types)

    base_query = queries[query_choice]
    filters = []

    if selected_city != "All":
        filters.append(f"(City = '{selected_city}' OR Location = '{selected_city}')")
    if selected_provider != "All":
        filters.append(f"Name = '{selected_provider}'")
    if selected_food_type != "All":
        filters.append(f"Food_Type = '{selected_food_type}'")
    if selected_meal_type != "All":
        filters.append(f"Meal_Type = '{selected_meal_type}'")

    # Apply filters dynamically
    if filters:
        if "FROM providers" in base_query:
            base_query = base_query.replace("FROM providers", f"FROM providers WHERE {' AND '.join(filters)}")
        elif "FROM food_listings" in base_query:
            base_query = base_query.replace("FROM food_listings", f"FROM food_listings WHERE {' AND '.join(filters)}")
        elif "FROM claims" in base_query:
            base_query = """
            SELECT c.Claim_ID, c.Status, c.Timestamp, f.Food_Name, r.Name AS Receiver, p.Name AS Provider
            FROM claims c
            JOIN food_listings f ON c.Food_ID=f.Food_ID
            JOIN providers p ON f.Provider_ID=p.Provider_ID
            JOIN receivers r ON c.Receiver_ID=r.Receiver_ID
            WHERE """ + " AND ".join(filters)

    # Run query
    df = pd.read_sql(base_query, conn)

    # Show results
    st.subheader(query_choice)
    st.dataframe(df)

    # Charts
    if query_choice == "11. Claims status distribution" and not df.empty:
        st.bar_chart(df.set_index("Status"))
    elif query_choice == "8. Most common food types" and not df.empty:
        st.bar_chart(df.set_index("Food_Type"))
    elif query_choice == "13. Most claimed meal type" and not df.empty:
        st.bar_chart(df.set_index("Meal_Type"))
    elif query_choice == "3. Top provider types by contributions" and not df.empty:
        st.bar_chart(df.set_index("Type"))

# -------------------------------
# 2. Manage Food Listings (CRUD)
# -------------------------------
elif menu == "Manage Food Listings":
    st.subheader("🍲 Manage Food Listings")
    crud_choice = st.radio("Action", ["Add New Food", "View All", "Update Food", "Delete Food"])

    # CREATE
    if crud_choice == "Add New Food":
        with st.form("add_food_form"):
            food_id = st.number_input("Food ID", min_value=1, step=1)
            food_name = st.text_input("Food Name")
            quantity = st.number_input("Quantity", min_value=1, step=1)
            expiry_date = st.date_input("Expiry Date")
            provider_id = st.number_input("Provider ID", min_value=1, step=1)
            provider_type = st.text_input("Provider Type")
            location = st.text_input("Location")
            food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
            meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"])
            submit = st.form_submit_button("Add Food")

            if submit:
                cursor.execute("""
                    INSERT INTO food_listings (Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type))
                conn.commit()
                st.success(f"✅ Food '{food_name}' added successfully!")

    # READ
    elif crud_choice == "View All":
        df = pd.read_sql("SELECT * FROM food_listings", conn)
        st.dataframe(df)

    # UPDATE
    elif crud_choice == "Update Food":
        df = pd.read_sql("SELECT * FROM food_listings", conn)
        if not df.empty:
            food_ids = df["Food_ID"].tolist()
            food_to_update = st.selectbox("Select Food ID", food_ids)
            food_details = df[df["Food_ID"] == food_to_update].iloc[0]
            new_name = st.text_input("Food Name", value=food_details["Food_Name"])
            new_quantity = st.number_input("Quantity", value=int(food_details["Quantity"]))
            new_expiry = st.date_input("Expiry Date")
            update_btn = st.button("Update Food")

            if update_btn:
                cursor.execute("""
                    UPDATE food_listings
                    SET Food_Name=?, Quantity=?, Expiry_Date=?
                    WHERE Food_ID=?
                """, (new_name, new_quantity, new_expiry, food_to_update))
                conn.commit()
                st.success("✅ Food updated successfully!")

    # DELETE
    elif crud_choice == "Delete Food":
        df = pd.read_sql("SELECT * FROM food_listings", conn)
        if not df.empty:
            food_ids = df["Food_ID"].tolist()
            food_to_delete = st.selectbox("Select Food ID to Delete", food_ids)
            delete_btn = st.button("Delete")
            if delete_btn:
                cursor.execute("DELETE FROM food_listings WHERE Food_ID=?", (food_to_delete,))
                conn.commit()
                st.warning(f"🗑️ Food with ID {food_to_delete} deleted!")

# -------------------------------
# 3. Manage Claims (CRUD)
# -------------------------------
elif menu == "Manage Claims":
    st.subheader("📦 Manage Claims")
    crud_choice = st.radio("Action", ["View Claims", "Update Claim Status", "Delete Claim"])

    # READ
    if crud_choice == "View Claims":
        df = pd.read_sql("SELECT * FROM claims", conn)
        st.dataframe(df)

    # UPDATE
    elif crud_choice == "Update Claim Status":
        df = pd.read_sql("SELECT * FROM claims", conn)
        if not df.empty:
            claim_ids = df["Claim_ID"].tolist()
            claim_to_update = st.selectbox("Select Claim ID", claim_ids)
            new_status = st.selectbox("New Status", ["Pending", "Completed", "Cancelled"])
            update_btn = st.button("Update Status")
            if update_btn:
                cursor.execute("UPDATE claims SET Status=? WHERE Claim_ID=?", (new_status, claim_to_update))
                conn.commit()
                st.success(f"✅ Claim {claim_to_update} updated to {new_status}")

    # DELETE
    elif crud_choice == "Delete Claim":
        df = pd.read_sql("SELECT * FROM claims", conn)
        if not df.empty:
            claim_ids = df["Claim_ID"].tolist()
            claim_to_delete = st.selectbox("Select Claim ID to Delete", claim_ids)
            delete_btn = st.button("Delete Claim")
            if delete_btn:
                cursor.execute("DELETE FROM claims WHERE Claim_ID=?", (claim_to_delete,))
                conn.commit()
                st.warning(f"🗑️ Claim {claim_to_delete} deleted!")

# Close DB
conn.close()
