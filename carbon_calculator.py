import streamlit as st
import matplotlib.pyplot as plt

# ---- Page Config ----
st.set_page_config(page_title="Carbon Footprint Calculator", layout="wide")

# ---- Theme ----
theme_color = "#FFFFFF"
text_color = "#000000"
st.markdown(f"""
    <style>
        body {{
            background-color: {theme_color};
            color: {text_color};
        }}
    </style>
""", unsafe_allow_html=True)

# ---- Sidebar Navigation ----
st.sidebar.title("🌿 Navigation")
page = st.sidebar.radio("Go to", ["Home", "About Us", "Calculator"])

# ---- Home Page ----
if page == "Home":
    st.title("🌍 Welcome to the Carbon Footprint Calculator")

    st.write("""
        **Why Measure Your Carbon Footprint?**  
        Every activity we do contributes to carbon emissions, impacting climate change.  
        This tool helps you estimate your daily carbon footprint and provides tips to reduce it.  
    """)
    st.subheader("💡 Features of this Tool:")
    st.markdown("- 📊 **Interactive Carbon Calculator**")
    st.markdown("- 🏡 **Personalized Reduction Tips**")
    st.markdown("- 📌 **User-Friendly Interface**")
    st.markdown("- 🌎 **Learn About Climate Change**")

# ---- About Us Page ----
elif page == "About Us":
    st.title("ℹ️ About Us")
    st.write("""
        **Mission:** Our goal is to spread awareness about carbon footprints and  
        encourage people to adopt sustainable practices for a greener planet. 🌱  

        **How It Works:**  
        - This tool calculates CO₂ emissions from electricity, transportation, and diet.  
        - It gives you **personalized tips** to reduce your footprint.  
        - We provide **data visualizations** to make the information easier to understand.  

        **Why It Matters?**  
        Climate change is one of the biggest challenges today. Small daily actions,  
        like using energy-efficient appliances or reducing meat consumption, can make  
        a **big difference**! 🌎  
    """)
# ---- Calculator Page ----
elif page == "Calculator":
    st.title("📊 Carbon Footprint Calculator")
    
    # Reset Functionality
    def reset_values():
        st.session_state.electricity = 0.0
        st.session_state.car_km = 0.0
        st.session_state.public_transit_km = 0.0
        st.session_state.meat_consumption = "Daily"
    
    # Sidebar Inputs
    st.sidebar.header("🌱 Enter Your Daily Activities")
    electricity = st.sidebar.number_input("Electricity Consumption (kWh per month)", min_value=0.0, step=0.1, key="electricity")
    car_km = st.sidebar.number_input("Distance Traveled by Car (km per day)", min_value=0.0, step=0.1, key="car_km")
    public_transit_km = st.sidebar.number_input("Public Transport Usage (km per day)", min_value=0.0, step=0.1, key="public_transit_km")
    meat_consumption = st.sidebar.selectbox("How often do you eat meat?", ["Daily", "Few times a week", "Rarely", "Never"], key="meat_consumption")
    
    # Reset Button
    st.sidebar.button("🔄 Reset", on_click=reset_values)
    
    # Carbon Emission Factors (kg CO₂ per unit)
    carbon_factors = {
        "electricity": 0.92,
        "car": 0.21,
        "public_transit": 0.10,
        "meat": {"Daily": 3.3, "Few times a week": 2.0, "Rarely": 1.0, "Never": 0.1}
    }

    # Calculate Carbon Footprint
    electricity_emission = electricity * carbon_factors["electricity"] / 30  # daily
    car_emission = car_km * carbon_factors["car"]
    transit_emission = public_transit_km * carbon_factors["public_transit"]
    meat_emission = carbon_factors["meat"][meat_consumption]
    total_emission = electricity_emission + car_emission + transit_emission + meat_emission

    # Display Results
    st.subheader("🌍 Your Estimated Daily Carbon Footprint")
    st.write(f"**Total Emissions:** `{total_emission:.2f} kg CO₂ per day`")

    # Progress Bar (Target: 5 kg CO₂/day)
    target = 5.0
    percent = min(total_emission / target, 1.0)
    st.progress(percent, text=f"{int(percent*100)}% of recommended daily limit (5.0 kg)")

    # Visualization: Pie Chart
    st.subheader("📊 Emissions Breakdown")

    labels = ["Electricity", "Car", "Public Transport", "Meat Consumption"]
    values = [electricity_emission, car_emission, transit_emission, meat_emission]

    # Filter out zero values
    filtered_labels = [label for label, val in zip(labels, values) if val > 0]
    filtered_values = [val for val in values if val > 0]

    if filtered_values:
        fig, ax = plt.subplots()
        ax.pie(filtered_values, labels=filtered_labels, autopct="%1.1f%%", startangle=90,
               colors=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"])
        ax.axis("equal")
        st.pyplot(fig)
    else:
        st.info("No emissions data to display. Please enter some values.")

    # Reduction Tips
    st.subheader("♻️ How to Reduce Your Carbon Footprint?")
    if electricity_emission > 1:
        st.write("✅ Use energy-efficient appliances & LED lights.")
        st.write("✅ Unplug devices when not in use.")
    if car_emission > 1:
        st.write("✅ Consider carpooling, biking, or using public transport more often.")
        st.write("✅ Use electric or hybrid vehicles if possible.")
    if meat_emission > 1:
        st.write("✅ Reduce meat consumption and switch to plant-based meals.")

    st.success("Small changes can create a big impact! 🌱")

    # --- Did You Know? ---
    with st.expander("💡 Did You Know?"):
        st.markdown("""
        - Producing 1 kg of beef emits around **27 kg of CO₂**.
        - Flying economy emits less CO₂ per passenger than business class.
        - A 5-minute shower can use up to **75 liters** of hot water!
        """)

    # --- Feedback ---
    st.markdown("---")
    st.subheader("📝 Was this calculator helpful?")
    feedback = st.radio("Your feedback:", ["👍 Yes", "👎 No"], horizontal=True)
    if feedback:
        st.write("Thank you for your feedback!")

    st.caption("🌍 Created for a cleaner tomorrow | Learn more: [UN Climate Action](https://www.un.org/en/climatechange)")
