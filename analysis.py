import sqlite3
import pandas as pd

# Connect to SQLite DB
conn = sqlite3.connect("food.db")

# Dictionary of queries (key = question, value = SQL query)
queries = {
    # Food Providers & Receivers
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

    # Food Listings & Availability
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

    # Claims & Distribution
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

    # Analysis & Insights
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

# Run all queries and print results
for title, query in queries.items():
    print("\n" + "="*80)
    print(title)
    print("-"*80)
    try:
        df = pd.read_sql(query, conn)
        print(df.to_string(index=False) if not df.empty else "⚠️ No results found")
    except Exception as e:
        print(f"❌ Error running query: {e}")

conn.close()
print("\n✅ All queries executed successfully!")
