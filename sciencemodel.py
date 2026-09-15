import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Science Model Marking System (Max 45 Marks)",
    page_icon="🔬",
    layout="wide",
)

# ----------------- डेटाबेस सेटअप -----------------
conn = sqlite3.connect("competition_scores_v2.db", check_same_thread=False)
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

# ----------------- शीट का डेटा (35 मॉडल्स) -----------------
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

# ----------------- UI हेडर -----------------
st.title("🔬 Science Model Evaluation & Rank Calculator")
st.caption("3 Judges × 15 Marks (3 Categories of 5 Marks Each) = Total 45 Marks")

tab1, tab2 = st.tabs(["📝 जज मूल्यांकन (Marking / 15)", "🏆 1st, 2nd, 3rd रैंक (Out of 45)"])

# ----------------- TAB 1: मूल्यांकन फ़ीडिंग -----------------
with tab1:
  col_j, col_c = st.columns([1, 1])

  with col_j:
    judge_name = st.selectbox(
        "निर्णायक शिक्षक चुनें (Select Judge):",
        ["Shree S.K. Nayak", "Shri B.N.R. Tripathi", "Shri S.N. Singh"],
    )

  with col_c:
    class_list = ["सभी कक्षाएं (All)"] + sorted(list(df_base["class"].unique()))
    selected_class = st.selectbox("कक्षा चुनें (Search by Class):", class_list)

  # कक्षा फ़िल्टर
  if selected_class != "सभी कक्षाएं (All)":
    filtered_df = df_base[df_base["class"] == selected_class]
  else:
    filtered_df = df_base

  st.write("---")

  # मॉडल चुनना
  model_options = {
      f"#{r['id']} | Class: {r['class']} | {r['name']}": r["id"]
      for _, r in filtered_df.iterrows()
  }

  if not model_options:
    st.warning("इस कक्षा का कोई मॉडल नहीं मिला।")
  else:
    selected_label = st.selectbox("मॉडल चुनें:", list(model_options.keys()))
    selected_id = model_options[selected_label]
    model_row = df_base[df_base["id"] == selected_id].iloc[0]

    # कार्ड विवरण
    st.info(f"""
        📌 **मॉडल क्र.**: {model_row['id']} | **कक्षा**: `{model_row['class']}` | **प्रकार**: `{model_row['type']}` | **श्रेणी**: `{model_row['cat']}`  
        🔬 **मॉडल का नाम**: **{model_row['name']}**  
        👥 **विद्यार्थी**: {model_row['students']}
        """)

    # अगर पहले से अंक दर्ज हैं तो लोड करें
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

    st.markdown("#### 🎯 3 श्रेणियों में अंक दें (अधिकतम 5 प्रत्येक = कुल 15)")

    c1_col, c2_col, c3_col = st.columns(3)
    with c1_col:
      crit1 = st.number_input(
          "1. नवाचार / Creativity (Max 5):",
          0.0,
          5.0,
          value=init_c1,
          step=0.5,
          key=f"c1_{selected_id}_{judge_name}",
      )
    with c2_col:
      crit2 = st.number_input(
          "2. वैज्ञानिक सिद्धांत / Working (Max 5):",
          0.0,
          5.0,
          value=init_c2,
          step=0.5,
          key=f"c2_{selected_id}_{judge_name}",
      )
    with c3_col:
      crit3 = st.number_input(
          "3. प्रस्तुति / Viva (Max 5):",
          0.0,
          5.0,
          value=init_c3,
          step=0.5,
          key=f"c3_{selected_id}_{judge_name}",
      )

    total_judge_score = crit1 + crit2 + crit3
    st.markdown(
        f"👉 **इस जज द्वारा कुल अंक:** `{total_judge_score} / 15`",
        unsafe_allow_html=True,
    )

    remarks = st.text_input("टिप्पणी / Remarks (वैकल्पिक):", value=init_rem)

    if st.button("💾 सुरक्षित करें (Save Score)", type="primary"):
      c.execute(
          """
            INSERT INTO marks (model_id, judge_name, crit1, crit2, crit3, total, remarks)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(model_id, judge_name) 
            DO UPDATE SET crit1=excluded.crit1, crit2=excluded.crit2, crit3=excluded.crit3, total=excluded.total, remarks=excluded.remarks
            """,
          (
              selected_id,
              judge_name,
              crit1,
              crit2,
              crit3,
              total_judge_score,
              remarks,
          ),
      )
      conn.commit()
      st.success(
          f"✅ {judge_name} जी के अंक सुरक्षित हो गए! (मॉडल #{selected_id}:"
          f" {total_judge_score}/15)"
      )

# ----------------- TAB 2: रैंक कैलकुलेटर (45 में से) -----------------
with tab2:
  st.subheader("🏆 परिणाम व रैंक कैलकुलेटर (Total Marks: 45)")

  df_scores = pd.read_sql_query("SELECT * FROM marks", conn)

  if df_scores.empty:
    st.warning(
        "⚠️ अभी तक किसी शिक्षक द्वारा अंक दर्ज नहीं किए गए हैं। कृपया टैब 1 में जाकर अंक भरें।"
    )
  else:
    # 3 जजों के कुल अंक पिवट करें
    pivoted = df_scores.pivot(
        index="model_id", columns="judge_name", values="total"
    ).reset_index()

    merged = pd.merge(df_base, pivoted, left_on="id", right_on="model_id", how="left")

    judges = ["Shree S.K. Nayak", "Shri B.N.R. Tripathi", "Shri S.N. Singh"]
    for j in judges:
      if j not in merged.columns:
        merged[j] = 0.0
      else:
        merged[j] = merged[j].fillna(0.0)

    # 45 में से कुल गणना
    merged["Total (out of 45)"] = (
        merged["Shree S.K. Nayak"]
        + merged["Shri B.N.R. Tripathi"]
        + merged["Shri S.N. Singh"]
    )

    # फ़िल्टर और सॉर्टिंग
    ranked_df = (
        merged[merged["Total (out of 45)"] > 0]
        .sort_values(by="Total (out of 45)", ascending=False)
        .reset_index(drop=True)
    )
    ranked_df["Rank"] = ranked_df["Total (out of 45)"].rank(
        ascending=False, method="min"
    ).astype(int)

    # टॉप 3 विजेता कार्ड्स
    if not ranked_df.empty:
      top3 = ranked_df.head(3)
      st.write("### 🎖️ टॉप 3 विजेता (Top 3 Rankers)")
      col1, col2, col3 = st.columns(3)

      cols = [col1, col2, col3]
      medals = ["🥇 1st Rank", "🥈 2nd Rank", "🥉 3rd Rank"]

      for idx, row in top3.iterrows():
        if idx < 3:
          with cols[idx]:
            st.metric(
                label=medals[idx],
                value=f"{row['name']}",
                delta=f"{row['Total (out of 45)']:.1f} / 45 Marks",
            )
            st.caption(f"कक्षा: **{row['class']}** | मॉडल #{row['id']}")
            st.caption(f"विद्यार्थी: {row['students']}")

      st.write("---")

    # पूरा मेरिट टेबल
    st.write("### 📋 पूरी रैंक और स्कोरशीट")
    display_cols = [
        "Rank",
        "id",
        "class",
        "name",
        "type",
        "Shree S.K. Nayak",
        "Shri B.N.R. Tripathi",
        "Shri S.N. Singh",
        "Total (out of 45)",
    ]

    st.dataframe(
        ranked_df[display_cols].rename(
            columns={
                "id": "क्र. सं.",
                "class": "कक्षा",
                "name": "मॉडल का नाम",
                "type": "प्रकार",
                "Shree S.K. Nayak": "S.K. Nayak (/15)",
                "Shri B.N.R. Tripathi": "B.N.R. Tripathi (/15)",
                "Shri S.N. Singh": "S.N. Singh (/15)",
                "Total (out of 45)": "कुल अंक (/45)",
            }
        ),
        use_container_width=True,
    )

    # एक्सेल डाउनलोड
    csv_file = ranked_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "📥 पूरी मेरिट लिस्ट एक्सेल / CSV डाउनलोड करें",
        data=csv_file,
        file_name="Science_Model_Merit_List_45_Marks.csv",
        mime="text/csv",
    )