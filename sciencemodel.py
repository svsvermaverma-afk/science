import os
import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Science Model Scoring & Management",
    page_icon="🔬",
    layout="wide",
)

# ----------------- स्थायी डेटाबेस सेटअप -----------------
DB_FILE = "competition_permanent_data.db"
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
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
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
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

# ----------------- UI Tabs -----------------
st.title("🔬 साइंस मॉडल अंकन एवं परिणाम पोर्टल")
tab1, tab2, tab3 = st.tabs(
    ["📝 अंक प्रविष्टि (Marking)", "📊 लाइव अंक शीट (Master Sheet)", "🗑️ डेटा प्रबंधन / डिलीट"]
)

# ----------------- TAB 1: अंक प्रविष्टि -----------------
with tab1:
  col_j, col_c = st.columns(2)
  with col_j:
    judge = st.selectbox(
        "निर्णायक शिक्षक (Judge):",
        ["Shree S.K. Nayak", "Shri B.N.R. Tripathi", "Shri S.N. Singh"],
    )
  with col_c:
    classes = ["सभी कक्षाएं"] + sorted(list(df_base["class"].unique()))
    sel_class = st.selectbox("कक्षा चुनें:", classes)

  f_df = df_base if sel_class == "सभी कक्षाएं" else df_base[df_base["class"] == sel_class]
  model_opts = {
      f"#{r['id']} ({r['class']}) - {r['name']}": r["id"]
      for _, r in f_df.iterrows()
  }

  if model_opts:
    chosen_label = st.selectbox("मॉडल चुनें:", list(model_opts.keys()))
    m_id = model_opts[chosen_label]
    row = df_base[df_base["id"] == m_id].iloc[0]

    st.info(
        f"**मॉडल:** {row['name']} | **कक्षा:** {row['class']} | **विद्यार्थी:**"
        f" {row['students']}"
    )

    # पहले का डेटा लोड करें
    c.execute(
        "SELECT crit1, crit2, crit3, remarks FROM marks WHERE model_id=? AND"
        " judge_name=?",
        (m_id, judge),
    )
    prev = c.fetchone()
    v1, v2, v3, v_rem = (
        (prev[0], prev[1], prev[2], prev[3]) if prev else (0.0, 0.0, 0.0, "")
    )

    c1, c2, c3 = st.columns(3)
    s1 = c1.number_input("नवाचार (0-5)", 0.0, 5.0, float(v1), 0.5)
    s2 = c2.number_input("सिद्धांत (0-5)", 0.0, 5.0, float(v2), 0.5)
    s3 = c3.number_input("प्रस्तुति (0-5)", 0.0, 5.0, float(v3), 0.5)
    rem = st.text_input("रिमार्क:", value=v_rem)

    tot = s1 + s2 + s3
    st.write(f"**प्राप्तांक:** `{tot} / 15`")

    if st.button("💾 अंक सुरक्षित करें (Save Score)", type="primary"):
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
      st.success(
          f"✅ {judge} जी द्वारा मॉडल #{m_id} के {tot}/15 अंक सुरक्षित कर लिए"
          " गए।"
      )

# ----------------- TAB 2: लाइव मास्टर शीट -----------------
with tab2:
  st.subheader("📋 सभी मॉडल्स की विस्तृत अंक शीट")

  df_raw = pd.read_sql_query("SELECT * FROM marks", conn)

  if df_raw.empty:
    st.warning("अभी तक कोई डेटा दर्ज नहीं हुआ है।")
  else:
    # डिटेल्ड शीट: किस मॉडल को किस जज ने क्या-क्या नंबर दिए
    detail_df = pd.merge(
        df_raw, df_base, left_on="model_id", right_on="id", how="left"
    )
    detail_cols = [
        "model_id",
        "class",
        "name",
        "judge_name",
        "crit1",
        "crit2",
        "crit3",
        "total",
        "students",
    ]
    renamed_detail = detail_df[detail_cols].rename(
        columns={
            "model_id": "क्र. सं.",
            "class": "कक्षा",
            "name": "मॉडल का नाम",
            "judge_name": "जज शिक्षक",
            "crit1": "नवाचार (/5)",
            "crit2": "सिद्धांत (/5)",
            "crit3": "प्रस्तुति (/5)",
            "total": "कुल अंक (/15)",
            "students": "विद्यार्थी",
        }
    )

    st.dataframe(renamed_detail, use_container_width=True)

    # 45 में से रैंक और मेरिट समरी
    st.divider()
    st.subheader("🏆 फाइनल 45 में से मेरिट व रैंक")
    pivoted = df_raw.pivot(
        index="model_id", columns="judge_name", values="total"
    ).reset_index()
    merged = pd.merge(df_base, pivoted, left_on="id", right_on="model_id", how="left")

    for j in ["Shree S.K. Nayak", "Shri B.N.R. Tripathi", "Shri S.N. Singh"]:
      if j not in merged.columns:
        merged[j] = 0.0
      else:
        merged[j] = merged[j].fillna(0.0)

    merged["कुल अंक (45)"] = (
        merged["Shree S.K. Nayak"]
        + merged["Shri B.N.R. Tripathi"]
        + merged["Shri S.N. Singh"]
    )
    summary_df = (
        merged[merged["कुल अंक (45)"] > 0]
        .sort_values(by="कुल अंक (45)", ascending=False)
        .reset_index(drop=True)
    )
    summary_df["रैंक"] = summary_df["कुल अंक (45)"].rank(
        ascending=False, method="min"
    ).astype(int)

    rank_cols = [
        "रैंक",
        "id",
        "class",
        "name",
        "Shree S.K. Nayak",
        "Shri B.N.R. Tripathi",
        "Shri S.N. Singh",
        "कुल अंक (45)",
    ]
    st.dataframe(summary_df[rank_cols], use_container_width=True)

    # डाउनलोड बटन
    csv_bytes = summary_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "📥 पूरी मेरिट शीट डाउनलोड करें (.csv)",
        data=csv_bytes,
        file_name="Final_Science_Scoring_Sheet.csv",
        mime="text/csv",
    )

# ----------------- TAB 3: डेटा डिलीट व सुधार -----------------
with tab3:
  st.subheader("⚠️ गलत डेटा डिलीट या रीसेट करें")
  st.caption("यदि किसी जज से गलत नंबर चढ़ गया हो, तो यहाँ से सीधे उस प्रविष्टि को हटाया जा सकता है।")

  df_all = pd.read_sql_query("SELECT * FROM marks", conn)

  if df_all.empty:
    st.info("डेटाबेस अभी खाली है, डिलीट करने के लिए कोई प्रविष्टि नहीं है।")
  else:
    # ड्रॉपडाउन में दिखाने के लिए लिस्ट बनाएं
    entry_options = {}
    for _, r in df_all.iterrows():
      model_info = df_base[df_base["id"] == r["model_id"]].iloc[0]
      label = f"मॉडल #{r['model_id']} ({model_info['class']} - {model_info['name']}) | जज: {r['judge_name']} | अंक: {r['total']}/15"
      entry_options[label] = (r["model_id"], r["judge_name"])

    selected_entry = st.selectbox("डिलीट करने के लिए प्रविष्टि चुनें:", list(entry_options.keys()))
    del_mid, del_judge = entry_options[selected_entry]

    col_del1, col_del2 = st.columns([1, 2])
    with col_del1:
      if st.button("🗑️ चुनी हुई प्रविष्टि डिलीट करें", type="primary"):
        c.execute(
            "DELETE FROM marks WHERE model_id=? AND judge_name=?",
            (del_mid, del_judge),
        )
        conn.commit()
        st.warning(f"मॉडल #{del_mid} का {del_judge} जी का स्कोर हटा दिया गया है।")
        st.rerun()

    st.write("---")
    # पूरा डेटाबेस खाली करने का विकल्प (सुरक्षित पासवर्ड के साथ)
    with st.expander("🚨 पूरा डेटा रीसेट करें (Danger Zone)"):
      st.error("यह सभी जजों के सभी नंबर डिलीट कर देगा!")
      passcode = st.text_input("पुष्टि के लिए कोड लिखें ('CLEAR'):")
      if st.button("पूरा डेटाबेस खाली करें"):
        if passcode == "CLEAR":
          c.execute("DELETE FROM marks")
          conn.commit()
          st.success("पूरा डेटाबेस रीसेट हो गया है।")
          st.rerun()
        else:
          st.error("गलत कोड! प्रविष्टियां सुरक्षित हैं।")
