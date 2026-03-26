import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AgriStats & Epidemiology Calculator", page_icon="🌱", layout="wide")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Methodology & Documentation", "Paired t-test Calculator", "AUPPC / AUDPC Calculator"])

# ==========================================
# PAGE 1: METHODOLOGY & DOCUMENTATION
# ==========================================
if page == "Methodology & Documentation":
    st.title("🌱 Agricultural Statistics & Epidemiology Calculator")
    st.subheader("Core Methodology & Documentation")
    
    st.markdown("""
    This application utilizes three distinct analytical methods to evaluate agricultural field data. While the **Paired t-test** is a statistical tool used to compare averages, **AUDPC** and **AUPPC** are epidemiological metrics used to measure the total cumulative burden of diseases or pests over a specific season.

    ---

    ### 1. Paired t-test (Statistical Comparison)
    The paired t-test is a fundamental statistical hypothesis test used to compare the means (averages) of two related groups. In agricultural trials, it is used to determine if the population differences between two specific locations or treatments, observed over the same time periods, are statistically significant or just due to random chance.

    * **What it measures:** The difference between two averages.
    * **The Output:** A $p$-value (e.g., $p < 0.05$) and a $t$-statistic.
    * **Limitation:** It only compares averages. It cannot calculate the total severity or duration of an infestation.
    * **Example Use Case:** *"Does Location A have a significantly higher average pest population than Location B?"*

    ---

    ### 2. Area Under Disease Progress Curve (AUDPC)
    AUDPC is a standard epidemiological metric strictly used in **Plant Pathology**. It estimates the total accumulation and severity of a plant disease (such as rust, blight, or mildew) over a specific crop season. 

    * **What it measures:** Total cumulative disease severity over time.
    * **The Output:** A total scalar value measured in **"Disease-Days"**.
    * **First Proposed By:** J.E. Vanderplank (1963) for measuring plant disease epidemics.

    ---

    ### 3. Area Under Pest Progress Curve (AUPPC)
    AUPPC is a metric strictly used in **Agricultural Entomology**. It uses the exact same mathematical foundation as AUDPC, but the terminology is adapted to reflect insect or mite populations rather than plant pathogens.

    * **What it measures:** Total cumulative pest population and duration.
    * **The Output:** A total scalar value measured in **"Pest-Days"**. This single number combines *Intensity* (how high the population got) with *Duration* (how long the pests survived).
    * **First Proposed By:** Robert F. Ruppel (1983).

    ### The AUPPC / AUDPC Formula (Trapezoidal Method)
    Both metrics calculate the total area under a population curve by dividing the graph into a series of trapezoids based on sampling intervals.
    
    **The Equation:** $A = \sum_{i=1}^{n-1} \left[ \\frac{y_i + y_{i+1}}{2} \\right] (t_{i+1} - t_i)$
    
    *(Where $y$ is the pest/disease count, and $t$ is the time in days).*

    ---

    ### 💡 Real-World Example: Interpreting AUPPC
    The number given by the AUPPC (for example, **1769.80 for Bardoli**) is called the **Total Cumulative Pest Burden**, and its unit of measurement is **"Pest-Days"**. Here is the exact breakdown of what that number means biologically and practically:

    #### 1. The Core Meaning: "Pest-Days"
    Imagine you are measuring how much damage a pest does to a crop. Damage doesn't just happen on the day the population is highest; it happens every single day the pest is present in the field.
    * If you have **10 pests** on a plant for **1 day**, that is 10 Pest-Days of damage.
    * If you have **2 pests** on a plant for **5 days**, that is *also* 10 Pest-Days of damage.
    
    When we calculated 1769.80 for Bardoli, it literally means that over the course of the entire 12-month season, the crop in Bardoli suffered the equivalent of **1,769 days of feeding by a single pest** (or 1 pest feeding for 1,769 days).

    #### 2. Intensity + Duration (Why the number is so important)
    The actual meaning of the AUPPC number is that it combines two dangerous things into one single score:
    * **Intensity:** How high did the pest population get? (e.g., Bardoli reached over 12 pests per unit).
    * **Duration:** How long did the pests stay in the field before dying off?
    
    If a location has a huge pest outbreak that lasts for only one week, the AUPPC will be low. But if a location has a moderate pest population that stays alive for 6 months, the AUPPC will be massive. **Bardoli's high number (1769.80)** means the pests there were not only high in number, but they survived and stayed active in the field for a very long time.

    #### 3. Comparing the Numbers (What it tells you)
    Let's look at pooled results for two locations:
    * **Bardoli:** 1769.80
    * **Chalthan:** 1055.92
    
    The actual meaning of this difference is **Crop Damage Potential**. Even though both locations had the exact same weather season and the exact same crop, the plants in Bardoli endured almost **70% more total pest pressure** over the year than the plants in Chalthan.

    #### 🎓 How to explain this in your thesis/viva:
    If an examiner asks you, *"What does this AUPPC value of 1769 actually mean?"*
    
    **You should answer:** *"The AUPPC value of 1769 represents the total accumulated pest-days over the entire cropping season. It proves that Bardoli did not just have a higher peak population on a single day, but that the overall prolonged burden and total feeding pressure on the crop throughout the year was mathematically much heavier than in Chalthan."*
    """)

# ==========================================
# PAGE 2: PAIRED T-TEST CALCULATOR
# ==========================================
elif page == "Paired t-test Calculator":
    st.title("📊 Paired t-test Calculator")
    st.write("Upload a CSV file containing your observation data. Each column should represent a different location or treatment.")
    
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"], key="ttest")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### Data Preview")
        st.dataframe(df.head())
        
        st.write("### Select Columns for Comparison")
        col1, col2 = st.columns(2)
        with col1:
            var1 = st.selectbox("Select Group 1 (e.g., Bardoli)", df.columns)
        with col2:
            var2 = st.selectbox("Select Group 2 (e.g., Gandevi)", df.columns)
            
        if st.button("Run Paired t-test"):
            # Drop NA values for the selected columns
            data1 = pd.to_numeric(df[var1], errors='coerce').dropna()
            data2 = pd.to_numeric(df[var2], errors='coerce').dropna()
            
            # Ensure equal lengths for paired t-test
            min_len = min(len(data1), len(data2))
            data1, data2 = data1[:min_len], data2[:min_len]
            
            # Calculate
            t_stat, p_val = stats.ttest_rel(data1, data2)
            mean_diff = np.mean(data1 - data2)
            
            st.success("Analysis Complete!")
            st.write(f"**Mean Difference:** {mean_diff:.3f}")
            st.write(f"**Calculated t-statistic:** {abs(t_stat):.3f}")
            st.write(f"**p-value:** {p_val:.4f}")
            
            if p_val < 0.01:
                st.info("Result: **Highly Significant (**)**. There is a statistically significant difference between the two groups.")
            elif p_val < 0.05:
                st.info("Result: **Significant (*)**. There is a statistically significant difference between the two groups.")
            else:
                st.warning("Result: **Non-Significant (NS)**. There is no statistically significant difference between the two groups.")

# ==========================================
# PAGE 3: AUPPC / AUDPC CALCULATOR
# ==========================================
elif page == "AUPPC / AUDPC Calculator":
    st.title("📈 AUPPC / AUDPC Calculator")
    st.write("Calculate the Area Under the Pest/Disease Progress Curve using the trapezoidal method.")
    
    time_interval = st.number_input("Enter Time Interval between observations (in days)", min_value=1, value=15, step=1)
    
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"], key="auppc")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### Data Preview")
        st.dataframe(df.head())
        
        target_cols = st.multiselect("Select Locations/Treatments to Calculate Area:", df.columns)
        
        if st.button("Calculate Area (Pest-Days / Disease-Days)"):
            area_results = []  # Changed name to prevent DataFrame conflicts
            for col in target_cols:
                y_values = pd.to_numeric(df[col], errors='coerce').dropna().values
                
                # Trapezoidal calculation
                if len(y_values) > 1:
                    area = np.trapz(y_values, dx=time_interval)
                    area_results.append({"Location / Treatment": col, "Total Burden (Area)": round(area, 2)})
                else:
                    st.error(f"Not enough data points in {col} to calculate area.")
                    
            # Explicitly check length to avoid the Ambiguous Truth Value error
            if len(area_results) > 0: 
                result_df = pd.DataFrame(area_results)
                st.success(f"Calculated successfully using a {time_interval}-day interval!")
                st.table(result_df)
                
                # Allow user to download results
                csv = result_df.to_csv(index=False).encode('utf-8')
                st.download_button("Download Results as CSV", data=csv, file_name="AUPPC_Results.csv", mime="text/csv")
