import sqlite3
import pandas as pd
import streamlit as st

# Mobile viewport optimization
st.set_page_config(
    page_title="Science Model Scoring",
    page_icon="🔬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom Mobile Styling
st.markdown(
    """
    <style>
        .block-container { padding: 0.8rem 0.6rem; }
        .stButton>button {
            width: 100%;
            height: 3.2rem;
            font-size: 1.1rem !important;
            font-weight: bold;
            border-radius: 10px;
        }
        .model-card {
            background-color: #f1f5f9;
            border-left: 5px solid #2563eb;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 12px;
            color: #0f172a;
        }
        .rank-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-left: 5px solid #f59e0b;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
    </style>
""",
    unsafe_allow_html=True,
)

# ----------------- स्थायी SQLite डेटाबेस -----------------
conn = sqlite3.connect("permanent_science_data.db", check_same_thread=False)
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

# ----------------- 35 मॉडल्स का डेटा (Group: Junior / Senior) -----------------
DATA = [
    {
        "id": 1,
        "class": "6 A",
        "name": "Excilator",
        "group": "Junior (6 to 8)",
        "students": (
            "Arindam Kumar (40248), Kavyansh Kumar (40249), Sagar Gupta (40218)"
        ),
    },
    {
        "id": 2,
        "class": "6 B",
        "name": "water purifier for home",
        "group": "Junior (6 to 8)",
        "students": (
            "BULBUL YADAV (40308), AASHI SINGH (40192), ANIKA CHOUBEY (40326)"
        ),
    },
    {
        "id": 3,
        "class": "6 C",
        "name": "Smart toilet",
        "group": "Junior (6 to 8)",
        "students": (
            "Ayush Kumar singh (40287), Vivek Kumar (40312), Amar Jaiswal"
            " (40327)"
        ),
    },
    {
        "id": 4,
        "class": "6 D",
        "name": "Chandrayaan 3",
        "group": "Junior (6 to 8)",
        "students": (
            "Renu Jaiswal (44 40380), Aakriti raj (12 40350), Pari tiwari"
            " (40303)"
        ),
    },
    {
        "id": 5,
        "class": "6 D",
        "name": "चन्द्र यान 3",
        "group": "Junior (6 to 8)",
        "students": (
            "रेनू जायसवाल (44 40380), आकृति राज (12 40350), परी तिवारी (40"
            " 40303)"
        ),
    },
    {
        "id": 6,
        "class": "6 D",
        "name": "Water purification",
        "group": "Junior (6 to 8)",
        "students": (
            "Srishti (40195), Srishti kumari (40226), pari kumari (40352)"
        ),
    },
    {
        "id": 7,
        "class": "9 G",
        "name": "Science Model (General)",
        "group": "Senior (9 to 10)",
        "students": "Sana (39687), Ankita (39688), Aliya (39689)",
    },
    {
        "id": 8,
        "class": "7 A",
        "name": "Smart flood rescue and drainage system",
        "group": "Junior (6 to 8)",
        "students": (
            "Shubham singh (39696), Arunendra mishra (39701), Amit kumar"
            " (39644)"
        ),
    },
    {
        "id": 9,
        "class": "7 B",
        "name": "संघनन की प्रक्रिया",
        "group": "Junior (6 to 8)",
        "students": (
            "Afrin Nisha (39657), Sandhya Yadav (39664), Parveen Nisha (39656)"
        ),
    },
    {
        "id": 10,
        "class": "7 C",
        "name": "Mini Water Dispenser",
        "group": "Junior (6 to 8)",
        "students": (
            "Amit Raj (39853), Nihal Singh (39828), Vishal Kumar (39881)"
        ),
    },
    {
        "id": 11,
        "class": "7 D",
        "name": "पौधों में पोषण",
        "group": "Junior (6 to 8)",
        "students": (
            "आलिया बरकाती (39845/4), श्रद्धा पटेल (39744/61), अंशिका तिवारी"
            " (39679/13)"
        ),
    },
    {
        "id": 12,
        "class": "8 B",
        "name": "Hybrid Wind - Hydro Power",
        "group": "Junior (6 to 8)",
        "students": (
            "Anushka Singh (39285), Shubhi Prajapati (40437), Rishi (40439)"
        ),
    },
    {
        "id": 13,
        "class": "8 C",
        "name": "Pawan chakki",
        "group": "Junior (6 to 8)",
        "students": (
            "Anish Kumar (39231), Aadarsh Kumar Tiwari (39295), Danish Raja"
            " (39297)"
        ),
    },
    {
        "id": 14,
        "class": "8 D",
        "name": "Eco Alert Bin",
        "group": "Junior (6 to 8)",
        "students": (
            "Aditi Jaiswal (39269), Tanwangi Yadav (39260), Khushi Gupta"
            " (39395)"
        ),
    },
    {
        "id": 15,
        "class": "9 A",
        "name": "Zero west to energy",
        "group": "Senior (9 to 10)",
        "students": "Satyadev (36), Adarsh Singh (4), Suraj Narayan Yadav (51)",
    },
    {
        "id": 16,
        "class": "9 B",
        "name": "AI Robot assistant",
        "group": "Senior (9 to 10)",
        "students": (
            "Abhijit Singh (38629), Rishabh yadav (38773), Naveen kumar Gupta"
            " (40518)"
        ),
    },
    {
        "id": 17,
        "class": "9 C",
        "name": "Robot",
        "group": "Senior (9 to 10)",
        "students": (
            "Khusi kumari (38717), Sanjeevani pandey (39908), Chandani Maurya"
            " (38593)"
        ),
    },
    {
        "id": 18,
        "class": "9 C",
        "name": "Water power plant",
        "group": "Senior (9 to 10)",
        "students": (
            "Ramkrishn (38596), Ajay patel (38692), Akarshit Tiwari (38821)"
        ),
    },
    {
        "id": 19,
        "class": "9 C",
        "name": "Water purefire",
        "group": "Senior (9 to 10)",
        "students": (
            "Divya jaiswal (38601), Nainshi verma (38719), Priyanshu (38721)"
        ),
    },
    {
        "id": 20,
        "class": "9 D",
        "name": "मानव फेफड़ा",
        "group": "Senior (9 to 10)",
        "students": (
            "ADITI KUMARI YADAV (38656), SADHANA BHARTI (39910), NIDHI SHARMA"
            " (38648)"
        ),
    },
    {
        "id": 21,
        "class": "9 D",
        "name": "चंद्रयान 3",
        "group": "Senior (9 to 10)",
        "students": (
            "AARUSHI (38647), KHUSHI SHARMA (38598), SONAKSHI SAHANI (38784)"
        ),
    },
    {
        "id": 22,
        "class": "9 D",
        "name": "RAINWATER HARVESTING",
        "group": "Senior (9 to 10)",
        "students": (
            "VAISHNAVI SRIVASTAVA (40504), SAPNA KUMARI (40519), ANJALI KUMARI"
            " (40510)"
        ),
    },
    {
        "id": 23,
        "class": "9 E",
        "name": "Water cycle",
        "group": "Senior (9 to 10)",
        "students": (
            "Vaibhav pandey (38613), Utkarsh Kumar (40468), Suraj Kumar (38742)"
        ),
    },
    {
        "id": 24,
        "class": "9 F",
        "name": "ECO AND GREEN CITY",
        "group": "Senior (9 to 10)",
        "students": (
            "Divyansh Gupta (38728), Shubham Kumar (40530), Shubham Singh"
            " (38665)"
        ),
    },
    {
        "id": 25,
        "class": "9 G",
        "name": "Production of Biogas from Dung & Vegetable Peels.",
        "group": "Senior (9 to 10)",
        "students": (
            "Aakriti (38616), Sonam Singh (38627), Shikha Jaiswal (38624)"
        ),
    },
    {
        "id": 26,
        "class": "9 G",
        "name": "Road Safety",
        "group": "Senior (9 to 10)",
        "students": (
            "Rinni Kumari (40513), Arati Kumari (40535), Anushka Yadav (38803)"
        ),
    },
    {
        "id": 27,
        "class": "9 H",
        "name": "Automatic Street Light Working Model",
        "group": "Senior (9 to 10)",
        "students": (
            "Pihu Kumari (Sr- 38678), Anshika Prajapati (38654), Pihu (40462)"
        ),
    },
    {
        "id": 28,
        "class": "9 H",
        "name": "Hydraulic lift model based on pascal's law",
        "group": "Senior (9 to 10)",
        "students": (
            "Saniya Khatoon (38819), Nagma Khatoon (38753), Anchal Kumari"
            " (40514)"
        ),
    },
    {
        "id": 29,
        "class": "10 B",
        "name": "Accident prevention left",
        "group": "Senior (9 to 10)",
        "students": (
            "Abhinav Bharati (39937), Shivam Gupta (39933), Aditya Yadav"
            " (39940)"
        ),
    },
    {
        "id": 30,
        "class": "10 D",
        "name": "Automatic flood route safety system",
        "group": "Senior (9 to 10)",
        "students": (
            "Preeti Mishra (38102, Roll 32), Sakshi jaiswal (38077, Roll 43),"
            " Ragini yadav (38032, Roll 38)"
        ),
    },
    {
        "id": 31,
        "class": "10 E",
        "name": "Solar agro drier with Humidity",
        "group": "Senior (9 to 10)",
        "students": (
            "Krishna Jaiswal (40005), Roshan prajapati (39975), Abhishek Pathak"
            " (38100)"
        ),
    },
    {
        "id": 32,
        "class": "10 F",
        "name": "Simple Bridge Construction Engineering",
        "group": "Senior (9 to 10)",
        "students": (
            "Nishant Kumar Mishra (38020), Sudhanshu Kumar Mishra (38025), Ansh"
            " Kumar Sonkar (40082)"
        ),
    },
    {
        "id": 33,
        "class": "10 G",
        "name": "Human Eye model",
        "group": "Senior (9 to 10)",
        "students": "Diksha Rao, Vaishnavi (38225), Sapna (38124)",
    },
    {
        "id": 34,
        "class": "10 H",
        "name": "AI road detect machine",
        "group": "Senior (9 to 10)",
        "students": (
            "Sakshi Chaurasiya (38174, Roll 47), Shruti Singh (38154, Roll 54),"
            " Shareen Bano (38042, Roll 52)"
        ),
    },
    {
        "id": 35,
        "class": "10 H",
        "name": "School model",
        "group": "Senior (9 to 10)",
        "students": (
            "Sonali Sharma (38222), Sonali (Roll 55), Soni Paswan (Roll 58)"
        ),
    },
]

df_base = pd.DataFrame(DATA)

# ----------------- मेनू -----------------
st.markdown("### 🔬 विज्ञान मॉडल मूल्यांकन")
menu = st.radio(
    "",
    ["📝 मार्किंग फीड करें", "🏆 Top 3 रैंक (Junior/Senior)", "🗑️ डेटा सुधार / डिलीट"],
    horizontal=True,
    label_visibility="collapsed",
)

# ----------------- 1. मार्किंग स्क्रीन -----------------
if menu == "📝 मार्किंग फीड करें":
  judge = st.selectbox(
      "👤 निर्णायक शिक्षक (Judge):",
      ["Shri S.K. Nayak", "Shri B.N.R. Tripathi", "Shri S.N. Singh"],
  )

  class_list = ["सभी कक्षाएं (All)"] + sorted(list(df_base["class"].unique()))
  sel_class = st.selectbox("🏫 कक्षा चुनें:", class_list)

  f_df = (
      df_base if sel_class == "सभी कक्षाएं (All)" else df_base[df_base["class"] == sel_class]
  )

  model_opts = {
      f"#{r['id']} ({r['class']}) - {r['name']}": r["id"]
      for _, r in f_df.iterrows()
  }

  if not model_opts:
    st.warning("कोई मॉडल उपलब्ध नहीं है।")
  else:
    chosen_label = st.selectbox("📦 मॉडल चुनें:", list(model_opts.keys()))
    m_id = model_opts[chosen_label]
    row = df_base[df_base["id"] == m_id].iloc[0]

    st.markdown(
        f"""
        <div class="model-card">
            <div style="font-size: 1.05rem; font-weight: bold;">{row['name']}</div>
            <div style="font-size: 0.85rem; color: #475569;">
                वर्ग: <b>{row['group']}</b> | कक्षा: <b>{row['class']}</b>
            </div>
            <div style="font-size: 0.85rem; margin-top: 5px;">👥 <b>विद्यार्थी:</b> {row['students']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # पहले का डेटा लोड
    c.execute(
        "SELECT crit1, crit2, crit3, remarks FROM marks WHERE model_id=? AND"
        " judge_name=?",
        (m_id, judge),
    )
    prev = c.fetchone()
    v1 = float(prev[0]) if prev else 0.0
    v2 = float(prev[1]) if prev else 0.0
    v3 = float(prev[2]) if prev else 0.0
    v_rem = prev[3] if prev else ""

    st.markdown("**🎯 अंक दर्ज करें (कुल 15 में से):**")
    s1 = st.slider(
        "1. नवाचार / Creativity (Max 5)",
        0.0,
        5.0,
        v1,
        0.5,
        key=f"sl1_{m_id}_{judge}",
    )
    s2 = st.slider(
        "2. सिद्धांत / Working (Max 5)",
        0.0,
        5.0,
        v2,
        0.5,
        key=f"sl2_{m_id}_{judge}",
    )
    s3 = st.slider(
        "3. प्रस्तुति / Viva (Max 5)",
        0.0,
        5.0,
        v3,
        0.5,
        key=f"sl3_{m_id}_{judge}",
    )

    tot = s1 + s2 + s3
    st.markdown(
        f"<div style='text-align:center; font-size:1.2rem; margin:8px;"
        f" font-weight:bold;'>आपका स्कोर: <span style='color:#16a34a;'>{tot} /"
        " 15</span></div>",
        unsafe_allow_html=True,
    )

    rem = st.text_input("टिप्पणी / Remarks (वैकल्पिक):", value=v_rem)

    if st.button("💾 अंक सुरक्षित करें (SAVE)", type="primary"):
      c.execute(
          """
            INSERT INTO marks (model_id, judge_name, crit1, crit2, crit3, total, remarks)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(model_id, judge_name) 
            DO UPDATE SET crit1=excluded.crit1, crit2=excluded.crit2, crit3=excluded.crit3, total=excluded.total, remarks=excluded.remarks
            """,
          (m_id, judge, s1, s2, s3, tot, rem),
      )
      conn.commit()
      st.toast(f"✅ सुरक्षित हुआ! {judge}: {tot}/15 अंक", icon="🎉")

# ----------------- 2. रैंक व रिजल्ट स्क्रीन (Junior / Senior) -----------------
elif menu == "🏆 Top 3 रैंक (Junior/Senior)":
  st.markdown("#### 🏆 वर्गवार टॉप 3 परिणाम (Max 45 Marks)")

  df_raw = pd.read_sql_query("SELECT * FROM marks", conn)

  if df_raw.empty:
    st.info(
        "अभी तक किसी शिक्षक द्वारा नंबर दर्ज नहीं किए गए हैं। कृपया पहले अंक भरें।"
    )
  else:
    pivoted = df_raw.pivot(
        index="model_id", columns="judge_name", values="total"
    ).reset_index()
    merged = pd.merge(df_base, pivoted, left_on="id", right_on="model_id", how="left")

    for j in ["Shree S.K. Nayak", "Shri B.N.R. Tripathi", "Shri S.N. Singh"]:
      if j not in merged.columns:
        merged[j] = 0.0
      else:
        merged[j] = merged[j].fillna(0.0)

    merged["Total (out of 45)"] = (
        merged["Shree S.K. Nayak"]
        + merged["Shri B.N.R. Tripathi"]
        + merged["Shri S.N. Singh"]
    )

    # फंक्शन: ग्रुप के हिसाब से टॉप 3 और मेरिट दिखाना
    def show_group_results(group_name, title_emoji):
      st.markdown(f"### {title_emoji} {group_name}")
      grp_df = (
          merged[
              (merged["group"] == group_name)
              & (merged["Total (out of 45)"] > 0)
          ]
          .sort_values(by="Total (out of 45)", ascending=False)
          .reset_index(drop=True)
      )

      if grp_df.empty:
        st.caption(f"{group_name} में अभी तक कोई अंक दर्ज नहीं हैं।")
        return

      grp_df["Rank"] = grp_df["Total (out of 45)"].rank(
          ascending=False, method="min"
      ).astype(int)

      # Top 3 Cards
      medals = ["🥇 1st Rank", "🥈 2nd Rank", "🥉 3rd Rank"]
      for idx, row in grp_df.head(3).iterrows():
        st.markdown(
            f"""
                <div class="rank-card">
                    <div style="font-size:1.1rem; font-weight:bold; color:#b45309;">{medals[idx]} — {row['Total (out of 45)']} / 45</div>
                    <div style="font-size:1rem; font-weight:600;">{row['name']} (कक्षा: {row['class']})</div>
                    <div style="font-size:0.85rem; color:#475569;">👥 {row['students']}</div>
                </div>
                """,
            unsafe_allow_html=True,
        )

      # संक्षिप्त टेबल
      with st.expander(f"📋 {group_name} की पूरी मेरिट लिस्ट देखें"):
        disp = grp_df[
            [
                "Rank",
                "class",
                "name",
                "Shree S.K. Nayak",
                "Shri B.N.R. Tripathi",
                "Shri S.N. Singh",
                "Total (out of 45)",
            ]
        ].rename(
            columns={
                "class": "कक्षा",
                "name": "मॉडल",
                "Shree S.K. Nayak": "Nayak",
                "Shri B.N.R. Tripathi": "Tripathi",
                "Shri S.N. Singh": "Singh",
                "Total (out of 45)": "कुल (/45)",
            }
        )
        st.dataframe(disp, use_container_width=True, hide_index=True)

    # 1. जूनियर वर्ग (6 से 8)
    show_group_results("Junior (6 to 8)", "🌱 जूनियर वर्ग")
    st.write("---")
    # 2. सीनियर वर्ग (9 व 10)
    show_group_results("Senior (9 to 10)", "🚀 सीनियर वर्ग")

    st.write("---")
    # सम्पूर्ण बैकअप CSV
    csv_bytes = (
        merged.sort_values(by="Total (out of 45)", ascending=False)
        .to_csv(index=False)
        .encode("utf-8-sig")
    )
    st.download_button(
        "📥 पूरी फाइनल शीट (Excel/CSV) डाउनलोड करें",
        data=csv_bytes,
        file_name="Junior_Senior_Science_Results.csv",
        mime="text/csv",
    )

# ----------------- 3. डेटा सुधार / डिलीट -----------------
else:
  st.markdown("#### 🗑️ गलत डेटा सुधारें / डिलीट करें")
  st.caption(
      "यदि किसी जज ने गलती से गलत नंबर भर दिया हो, तो यहाँ से हटाकर दोबारा सही नंबर दे सकते हैं।"
  )

  df_all = pd.read_sql_query("SELECT * FROM marks", conn)

  if df_all.empty:
    st.info("डेटाबेस खाली है।")
  else:
    entry_opts = {}
    for _, r in df_all.iterrows():
      model_info = df_base[df_base["id"] == r["model_id"]].iloc[0]
      label = f"#{r['model_id']} ({model_info['class']}) {model_info['name']} | जज: {r['judge_name']} | अंक: {r['total']}/15"
      entry_opts[label] = (r["model_id"], r["judge_name"])

    sel_entry = st.selectbox(
        "हटाने के लिए प्रविष्टि चुनें:", list(entry_opts.keys())
    )
    del_id, del_j = entry_opts[sel_entry]

    if st.button("🗑️ यह प्रविष्टि डिलीट करें", type="primary"):
      c.execute(
          "DELETE FROM marks WHERE model_id=? AND judge_name=?", (del_id, del_j)
      )
      conn.commit()
      st.success(f"मॉडल #{del_id} के लिए {del_j} जी के अंक हटा दिए गए हैं।")
      st.rerun()
