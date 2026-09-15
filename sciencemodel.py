import sqlite3
import pandas as pd
import streamlit as st

# Mobile viewport optimization
st.set_page_config(
    page_title="Science Model Marking",
    page_icon="🔬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Mobile Custom CSS (Bade Touch Targets aur Clean Cards)
st.markdown(
    """
    <style>
        .block-container { padding: 1rem 0.8rem; }
        .stButton>button {
            width: 100%;
            height: 3.2rem;
            font-size: 1.1rem !important;
            font-weight: bold;
            border-radius: 10px;
        }
        .model-card {
            background-color: #f0f4f8;
            border-left: 5px solid #0066cc;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 12px;
            color: #1a1a1a;
        }
        .rank-card {
            background-color: #fff9e6;
            border: 1px solid #ffd700;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 10px;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# ----------------- Database Setup -----------------
conn = sqlite3.connect("competition_mobile.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS marks (
    model_id INTEGER,
    judge_name TEXT,
    crit1 REAL,
    crit2 REAL,
    crit3 REAL,
    total REAL,
    remarks TEXT,
    PRIMARY KEY (model_id, judge_name)
)
""")
conn.commit()

# ----------------- Competition Data -----------------
DATA = [
    {
        "id": 1,
        "class": "6 A",
        "name": "Excilator",
        "type": "वर्किंग मॉडल",
        "cat": "विज्ञान (General Science)",
        "students": (
            "Arindam Kumar (40248), Kavyansh Kumar (40249), Sagar Gupta (40218)"
        ),
    },
    {
        "id": 2,
        "class": "6 B",
        "name": "water purifier for home",
        "type": "वर्किंग मॉडल",
        "cat": "दैनिक जीवन की समस्याओं के समाधान",
        "students": (
            "BULBUL YADAV (40308), AASHI SINGH (40192), ANIKA CHOUBEY (40326)"
        ),
    },
    {
        "id": 3,
        "class": "6 C",
        "name": "Smart toilet",
        "type": "वर्किंग मॉडल",
        "cat": "दैनिक जीवन की समस्याओं के समाधान",
        "students": (
            "Ayush Kumar singh (40287), Vivek Kumar (40312), Amar Jaiswal"
            " (40327)"
        ),
    },
    {
        "id": 4,
        "class": "6 D",
        "name": "Chandrayaan 3",
        "type": "वर्किंग मॉडल",
        "cat": "इंजीनियरिंग एवं तकनीकी नवाचार",
        "students": (
            "Renu Jaiswal (44 40380), Aakriti raj (12 40350), Pari tiwari"
            " (40303)"
        ),
    },
    {
        "id": 5,
        "class": "6 D",
        "name": "चन्द्र यान 3",
        "type": "वर्किंग मॉडल",
        "cat": "विज्ञान (General Science)",
        "students": (
            "रेनू जायसवाल (44 40380), आकृति राज (12 40350), परी तिवारी (40"
            " 40303)"
        ),
    },
    {
        "id": 6,
        "class": "6 D",
        "name": "Water purification",
        "type": "वर्किंग मॉडल",
        "cat": "विज्ञान (General Science)",
        "students": (
            "Srishti (40195), Srishti kumari (40226), pari kumari (40352)"
        ),
    },
    {
        "id": 7,
        "class": "9 G",
        "name": "Science Model (General)",
        "type": "वर्किंग मॉडल",
        "cat": "विज्ञान (General Science)",
        "students": "Sana (39687), Ankita (39688), Aliya (39689)",
    },
    {
        "id": 8,
        "class": "7 A",
        "name": "Smart flood rescue and drainage system",
        "type": "वर्किंग मॉडल",
        "cat": "पर्यावरण संरक्षण एवं ऊर्जा",
        "students": (
            "Shubham singh (39696), Arunendra mishra (39701), Amit kumar"
            " (39644)"
        ),
    },
    {
        "id": 9,
        "class": "7 B",
        "name": "संघनन की प्रक्रिया",
        "type": "वर्किंग मॉडल",
        "cat": "पर्यावरण संरक्षण एवं ऊर्जा",
        "students": (
            "Afrin Nisha (39657), Sandhya Yadav (39664), Parveen Nisha (39656)"
        ),
    },
    {
        "id": 10,
        "class": "7 C",
        "name": "Mini Water Dispenser",
        "type": "वर्किंग मॉडल",
        "cat": "इंजीनियरिंग एवं तकनीकी नवाचार",
        "students": (
            "Amit Raj (39853), Nihal Singh (39828), Vishal Kumar (39881)"
        ),
    },
    {
        "id": 11,
        "class": "7 D",
        "name": "पौधों में पोषण",
        "type": "वर्किंग मॉडल",
        "cat": "विज्ञान (General Science)",
        "students": (
            "आलिया बरकाती (39845/4), श्रद्धा पटेल (39744/61), अंशिका तिवारी"
            " (39679/13)"
        ),
    },
    {
        "id": 12,
        "class": "8 B",
        "name": "Hybrid Wind - Hydro Power",
        "type": "वर्किंग मॉडल",
        "cat": "पर्यावरण संरक्षण एवं ऊर्जा",
        "students": (
            "Anushka Singh (39285), Shubhi Prajapati (40437), Rishi (40439)"
        ),
    },
    {
        "id": 13,
        "class": "8 C",
        "name": "Pawan chakki",
        "type": "वर्किंग मॉडल",
        "cat": "विज्ञान (General Science)",
        "students": (
            "Anish Kumar (39231), Aadarsh Kumar Tiwari (39295), Danish Raja"
            " (39297)"
        ),
    },
    {
        "id": 14,
        "class": "8 D",
        "name": "Eco Alert Bin",
        "type": "वर्किंग मॉडल",
        "cat": "इंजीनियरिंग एवं तकनीकी नवाचार",
        "students": (
            "Aditi Jaiswal (39269), Tanwangi Yadav (39260), Khushi Gupta"
            " (39395)"
        ),
    },
    {
        "id": 15,
        "class": "9 A",
        "name": "Zero west to energy",
        "type": "स्टिल मॉडल",
        "cat": "विज्ञान (General Science)",
        "students": "Satyadev (36), Adarsh Singh (4), Suraj Narayan Yadav (51)",
    },
    {
        "id": 16,
        "class": "9 B",
        "name": "AI Robot assistant",
        "type": "वर्किंग मॉडल",
        "cat": "इंजीनियरिंग एवं तकनीकी नवाचार",
        "students": (
            "Abhijit Singh (38629), Rishabh yadav (38773), Naveen kumar Gupta"
            " (40518)"
        ),
    },
    {
        "id": 17,
        "class": "9 C",
        "name": "Robot",
        "type": "वर्किंग मॉडल",
        "cat": "इंजीनियरिंग एवं तकनीकी नवाचार",
        "students": (
            "Khusi kumari (38717), Sanjeevani pandey (39908), Chandani Maurya"
            " (38593)"
        ),
    },
    {
        "id": 18,
        "class": "9 C",
        "name": "Water power plant",
        "type": "वर्किंग मॉडल",
        "cat": "पर्यावरण संरक्षण एवं ऊर्जा",
        "students": (
            "Ramkrishn (38596), Ajay patel (38692), Akarshit Tiwari (38821)"
        ),
    },
    {
        "id": 19,
        "class": "9 C",
        "name": "Water purefire",
        "type": "वर्किंग मॉडल",
        "cat": "दैनिक जीवन की समस्याओं के समाधान",
        "students": (
            "Divya jaiswal (38601), Nainshi verma (38719), Priyanshu (38721)"
        ),
    },
    {
        "id": 20,
        "class": "9 D",
        "name": "मानव फेफड़ा",
        "type": "वर्किंग मॉडल",
        "cat": "विज्ञान (General Science)",
        "students": (
            "ADITI KUMARI YADAV (38656), SADHANA BHARTI (39910), NIDHI SHARMA"
            " (38648)"
        ),
    },
    {
        "id": 21,
        "class": "9 D",
        "name": "चंद्रयान 3",
        "type": "वर्किंग मॉडल",
        "cat": "विज्ञान (General Science)",
        "students": (
            "AARUSHI (38647), KHUSHI SHARMA (38598), SONAKSHI SAHANI (38784)"
        ),
    },
    {
        "id": 22,
        "class": "9 D",
        "name": "RAINWATER HARVESTING",
        "type": "वर्किंग मॉडल",
        "cat": "पर्यावरण संरक्षण एवं ऊर्जा",
        "students": (
            "VAISHNAVI SRIVASTAVA (40504), SAPNA KUMARI (40519), ANJALI KUMARI"
            " (40510)"
        ),
    },
    {
        "id": 23,
        "class": "9 E",
        "name": "Water cycle",
        "type": "वर्किंग मॉडल",
        "cat": "पर्यावरण संरक्षण एवं ऊर्जा",
        "students": (
            "Vaibhav pandey (38613), Utkarsh Kumar (40468), Suraj Kumar (38742)"
        ),
    },
    {
        "id": 24,
        "class": "9 F",
        "name": "ECO AND GREEN CITY",
        "type": "वर्किंग मॉडल",
        "cat": "पर्यावरण संरक्षण एवं ऊर्जा",
        "students": (
            "Divyansh Gupta (38728), Shubham Kumar (40530), Shubham Singh"
            " (38665)"
        ),
    },
    {
        "id": 25,
        "class": "9 G",
        "name": "Production of Biogas from Dung & Vegetable Peels.",
        "type": "वर्किंग मॉडल",
        "cat": "पर्यावरण संरक्षण एवं ऊर्जा",
        "students": (
            "Aakriti (38616), Sonam Singh (38627), Shikha Jaiswal (38624)"
        ),
    },
    {
        "id": 26,
        "class": "9 G",
        "name": "Road Safety",
        "type": "वर्किंग मॉडल",
        "cat": "दैनिक जीवन की समस्याओं के समाधान",
        "students": (
            "Rinni Kumari (40513), Arati Kumari (40535), Anushka Yadav (38803)"
        ),
    },
    {
        "id": 27,
        "class": "9 H",
        "name": "Automatic Street Light Working Model",
        "type": "वर्किंग मॉडल",
        "cat": "इंजीनियरिंग एवं तकनीकी नवाचार",
        "students": (
            "Pihu Kumari (Sr- 38678), Anshika Prajapati (38654), Pihu (40462)"
        ),
    },
    {
        "id": 28,
        "class": "9 H",
        "name": "Hydraulic lift model based on pascal's law",
        "type": "वर्किंग मॉडल",
        "cat": "विज्ञान (General Science)",
        "students": (
            "Saniya Khatoon (38819), Nagma Khatoon (38753), Anchal Kumari"
            " (40514)"
        ),
    },
    {
        "id": 29,
        "class": "10 B",
        "name": "Accident prevention left",
        "type": "वर्किंग मॉडल",
        "cat": "दैनिक जीवन की समस्याओं के समाधान",
        "students": (
            "Abhinav Bharati (39937), Shivam Gupta (39933), Aditya Yadav"
            " (39940)"
        ),
    },
    {
        "id": 30,
        "class": "10 D",
        "name": "Automatic flood route safety system",
        "type": "वर्किंग मॉडल",
        "cat": "इंजीनियरिंग एवं तकनीकी नवाचार",
        "students": (
            "Preeti Mishra (38102, Roll 32), Sakshi jaiswal (38077, Roll 43),"
            " Ragini yadav (38032, Roll 38)"
        ),
    },
    {
        "id": 31,
        "class": "10 E",
        "name": "Solar agro drier with Humidity",
        "type": "वर्किंग मॉडल",
        "cat": "विज्ञान (General Science)",
        "students": (
            "Krishna Jaiswal (40005), Roshan prajapati (39975), Abhishek Pathak"
            " (38100)"
        ),
    },
    {
        "id": 32,
        "class": "10 F",
        "name": "Simple Bridge Construction Engineering",
        "type": "स्टिल मॉडल",
        "cat": "इंजीनियरिंग एवं तकनीकी नवाचार",
        "students": (
            "Nishant Kumar Mishra (38020), Sudhanshu Kumar Mishra (38025), Ansh"
            " Kumar Sonkar (40082)"
        ),
    },
    {
        "id": 33,
        "class": "10 G",
        "name": "Human Eye model",
        "type": "स्टिल मॉडल",
        "cat": "विज्ञान (General Science)",
        "students": "Diksha Rao, Vaishnavi (38225), Sapna (38124)",
    },
    {
        "id": 34,
        "class": "10 H",
        "name": "AI road detect machine",
        "type": "वर्किंग मॉडल",
        "cat": "विज्ञान (General Science)",
        "students": (
            "Sakshi Chaurasiya (38174, Roll 47), Shruti Singh (38154, Roll 54),"
            " Shareen Bano (38042, Roll 52)"
        ),
    },
    {
        "id": 35,
        "class": "10 H",
        "name": "School model",
        "type": "स्टिल मॉडल",
        "cat": "अन्य (Other)",
        "students": (
            "Sonali Sharma (38222), Sonali (Roll 55), Soni Paswan (Roll 58)"
        ),
    },
]

df_base = pd.DataFrame(DATA)

# ----------------- App Header -----------------
st.markdown("### 🔬 विज्ञान मॉडल मूल्यांकन")
menu = st.radio(
    "",
    ["📝 मार्किंग फीड करें", "🏆 लाइव रैंक व रिजल्ट"],
    horizontal=True,
    label_visibility="collapsed",
)

# ----------------- 1. मार्किंग स्क्रीन (Mobile Optimized) -----------------
if menu == "📝 मार्किंग फीड करें":
  judge_name = st.selectbox(
      "👤 शिक्षक (Judge Name):",
      ["Shree S.K. Nayak", "Shri B.N.R. Tripathi", "Shri S.N. Singh"],
  )

  class_list = ["सभी कक्षाएं (All)"] + sorted(list(df_base["class"].unique()))
  selected_class = st.selectbox("🏫 कक्षा चुनें:", class_list)

  if selected_class != "सभी कक्षाएं (All)":
    filtered_df = df_base[df_base["class"] == selected_class]
  else:
    filtered_df = df_base

  model_options = {
      f"#{r['id']} ({r['class']}) - {r['name']}": r["id"]
      for _, r in filtered_df.iterrows()
  }

  if not model_options:
    st.warning("कोई मॉडल उपलब्ध नहीं है।")
  else:
    selected_label = st.selectbox("📦 मॉडल चुनें:", list(model_options.keys()))
    selected_id = model_options[selected_label]
    model_row = df_base[df_base["id"] == selected_id].iloc[0]

    # Student Card for Mobile
    st.markdown(
        f"""
        <div class="model-card">
            <div style="font-size: 1.1rem; font-weight: bold;">{model_row['name']}</div>
            <div style="font-size: 0.85rem; color: #555;">कक्षा: <b>{model_row['class']}</b> | {model_row['type']}</div>
            <div style="font-size: 0.85rem; margin-top: 5px;">👥 <b>विद्यार्थी:</b> {model_row['students']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Existing marks retrieval
    c.execute(
        "SELECT crit1, crit2, crit3, remarks FROM marks WHERE model_id=? AND"
        " judge_name=?",
        (selected_id, judge_name),
    )
    existing = c.fetchone()
    init_c1 = float(existing[0]) if existing else 0.0
    init_c2 = float(existing[1]) if existing else 0.0
    init_c3 = float(existing[2]) if existing else 0.0
    init_rem = existing[3] if existing else ""

    st.markdown("**मार्क्स दर्ज करें (कुल 15 में से):**")

    # Mobile-friendly sliders (Finger drag)
    crit1 = st.slider(
        "1. नवाचार / Creativity (0-5)",
        0.0,
        5.0,
        init_c1,
        0.5,
        key=f"m1_{selected_id}_{judge_name}",
    )
    crit2 = st.slider(
        "2. सिद्धांत / Working (0-5)",
        0.0,
        5.0,
        init_c2,
        0.5,
        key=f"m2_{selected_id}_{judge_name}",
    )
    crit3 = st.slider(
        "3. प्रस्तुति / Viva (0-5)",
        0.0,
        5.0,
        init_c3,
        0.5,
        key=f"m3_{selected_id}_{judge_name}",
    )

    total_judge = crit1 + crit2 + crit3

    st.markdown(
        f"<div style='text-align:center; font-size:1.2rem; margin:10px;"
        f" font-weight:bold;'>आपका स्कोर: <span style='color:#008000;'>{total_judge}"
        " / 15</span></div>",
        unsafe_allow_html=True,
    )

    remarks = st.text_input("टिप्पणी / Remarks:", value=init_rem)

    if st.button("💾 सुरक्षित करें (SAVE)", type="primary"):
      c.execute(
          """
            INSERT INTO marks (model_id, judge_name, crit1, crit2, crit3, total, remarks)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(model_id, judge_name) 
            DO UPDATE SET crit1=excluded.crit1, crit2=excluded.crit2, crit3=excluded.crit3, total=excluded.total, remarks=excluded.remarks
            """,
          (selected_id, judge_name, crit1, crit2, crit3, total_judge, remarks),
      )
      conn.commit()
      st.toast(
          f"✅ सुरक्षित हुआ! {judge_name}: {total_judge}/15", icon="🎉"
      )

# ----------------- 2. लाइव रैंक स्क्रीन -----------------
else:
  st.markdown("#### 🏆 45 में से लाइव मेरिट सूची")

  df_scores = pd.read_sql_query("SELECT * FROM marks", conn)

  if df_scores.empty:
    st.info("अभी तक कोई अंक दर्ज नहीं किए गए हैं।")
  else:
    pivoted = df_scores.pivot(
        index="model_id", columns="judge_name", values="total"
    ).reset_index()
    merged = pd.merge(df_base, pivoted, left_on="id", right_on="model_id", how="left")

    for j in ["Shree S.K. Nayak", "Shri B.N.R. Tripathi", "Shri S.N. Singh"]:
      if j not in merged.columns:
        merged[j] = 0.0
      else:
        merged[j] = merged[j].fillna(0.0)

    merged["Total"] = (
        merged["Shree S.K. Nayak"]
        + merged["Shri B.N.R. Tripathi"]
        + merged["Shri S.N. Singh"]
    )

    ranked_df = (
        merged[merged["Total"] > 0]
        .sort_values(by="Total", ascending=False)
        .reset_index(drop=True)
    )
    ranked_df["Rank"] = ranked_df["Total"].rank(
        ascending=False, method="min"
    ).astype(int)

    # Top 3 Card View for Mobile
    st.markdown("**शीर्ष 3 विजेता:**")
    medals = ["🥇 1st Rank", "🥈 2nd Rank", "🥉 3rd Rank"]
    for idx, row in ranked_df.head(3).iterrows():
      st.markdown(
          f"""
            <div class="rank-card">
                <b>{medals[idx]}</b>: <span style="font-size:1.1rem; color:#b8860b;">{row['Total']} / 45</span><br>
                <b>{row['name']}</b> (कक्षा: {row['class']})<br>
                <small>👥 {row['students']}</small>
            </div>
            """,
          unsafe_allow_html=True,
      )

    st.markdown("---")
    st.markdown("**सम्पूर्ण स्कोरशीट:**")

    display_df = ranked_df[
        ["Rank", "class", "name", "Total"]
    ].rename(
        columns={
            "class": "कक्षा",
            "name": "मॉडल",
            "Total": "कुल अंक (/45)",
        }
    )

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    csv_data = ranked_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "📥 रिजल्ट CSV डाउनलोड करें",
        data=csv_data,
        file_name="Science_Competition_Results.csv",
        mime="text/csv",
    )
