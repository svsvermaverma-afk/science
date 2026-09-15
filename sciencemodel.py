import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Mobile-First Viewport Config
st.set_page_config(
    page_title="ABIC Science Model Evaluation",
    page_icon="🔬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom Styling for Mobile UI
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
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 12px;
            color: #0f172a;
        }
        .rank-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-left: 5px solid #f59e0b;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 10px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
    </style>
""",
    unsafe_allow_html=True,
)

# ----------------- Google Sheets कनेक्शन -----------------
conn = st.connection("gsheets", type=GSheetsConnection)


def get_marks_data():
  try:
    df = conn.read(ttl=0)
    if df is None or df.empty:
      return pd.DataFrame(
          columns=[
              "model_id",
              "judge_name",
              "crit1",
              "crit2",
              "crit3",
              "total",
              "remarks",
          ]
      )
    df["model_id"] = pd.to_numeric(df["model_id"], errors="coerce").fillna(0).astype(int)
    return df
  except Exception:
    return pd.DataFrame(
        columns=[
            "model_id",
            "judge_name",
            "crit1",
            "crit2",
            "crit3",
            "total",
            "remarks",
        ]
    )


# ----------------- प्रतियोगिता के 35 मॉडल्स (मास्टर डेटा) -----------------
MODELS = [
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

df_base = pd.DataFrame(MODELS)

# ----------------- UI Header -----------------
st.markdown("### 🔬 विज्ञान मॉडल मूल्यांकन")
menu = st.radio(
    "",
    ["📝 मार्किंग फीड करें", "🏆 Top 3 परिणाम (45 में से)", "🗑️ सुधार / डिलीट"],
    horizontal=True,
    label_visibility="collapsed",
)

df_marks = get_marks_data()

# ----------------- 1. मार्किंग स्क्रीन -----------------
if menu == "📝 मार्किंग फीड करें":
  judge = st.selectbox(
      "👤 निर्णायक शिक्षक (Judge):",
      ["Shree S.K. Nayak", "Shri B.N.R. Tripathi", "Shri S.N. Singh"],
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
    st.warning("कोई मॉडल नहीं मिला।")
  else:
    chosen_label = st.selectbox("📦 मॉडल चुनें:", list(model_opts.keys()))
    m_id = model_opts[chosen_label]
    row = df_base[df_base["id"] == m_id].iloc[0]

    # Mobile Card Display
    st.markdown(
        f"""
        <div class="model-card">
            <div style="font-size: 1.1rem; font-weight: bold;">{row['name']}</div>
            <div style="font-size: 0.85rem; color: #475569;">वर्ग: <b>{row['group']}</b> | कक्षा: <b>{row['class']}</b></div>
            <div style="font-size: 0.85rem; margin-top: 5px;">👥 <b>विद्यार्थी:</b> {row['students']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Google Sheet से पहले से भरे अंक लोड करना
    existing = df_marks[
        (df_marks["model_id"] == m_id) & (df_marks["judge_name"] == judge)
    ]
    v1 = (
        float(existing.iloc[0]["crit1"])
        if not existing.empty and pd.notna(existing.iloc[0]["crit1"])
        else 0.0
    )
    v2 = (
        float(existing.iloc[0]["crit2"])
        if not existing.empty and pd.notna(existing.iloc[0]["crit2"])
        else 0.0
    )
    v3 = (
        float(existing.iloc[0]["crit3"])
        if not existing.empty and pd.notna(existing.iloc[0]["crit3"])
        else 0.0
    )
    v_rem = (
        str(existing.iloc[0]["remarks"])
        if not existing.empty and pd.notna(existing.iloc[0]["remarks"])
        else ""
    )
    if v_rem == "nan":
      v_rem = ""

    st.markdown("**🎯 अंक दर्ज करें (3 श्रेणियां × 5 = कुल 15 अंक):**")
    s1 = st.slider(
        "1. नवाचार / Creativity (Max 5)",
        0.0,
        5.0,
        v1,
        0.5,
        key=f"sl1_{m_id}_{judge}",
    )
    s2 = st.slider(
        "2. सिद्धांत व वर्किंग / Working (Max 5)",
        0.0,
        5.0,
        v2,
        0.5,
        key=f"sl2_{m_id}_{judge}",
    )
    s3 = st.slider(
        "3. प्रस्तुतीकरण / Viva (Max 5)",
        0.0,
        5.0,
        v3,
        0.5,
        key=f"sl3_{m_id}_{judge}",
    )

    total_judge = s1 + s2 + s3
    st.markdown(
        f"<div style='text-align:center; font-size:1.2rem; margin:8px;"
        f" font-weight:bold;'>प्राप्तांक: <span style='color:#16a34a;'>{total_judge}"
        " / 15</span></div>",
        unsafe_allow_html=True,
    )

    remarks = st.text_input("टिप्पणी / Remarks (वैकल्पिक):", value=v_rem)

    if st.button("💾 Google Sheet में सुरक्षित करें (SAVE)", type="primary"):
      # पुरानी एंट्री हटाएं ताकि डुप्लीकेट न हो
      new_df = df_marks[
          ~(
              (df_marks["model_id"] == m_id)
              & (df_marks["judge_name"] == judge)
          )
      ].copy()

      new_row = pd.DataFrame([{
          "model_id": int(m_id),
          "judge_name": str(judge),
          "crit1": float(s1),
          "crit2": float(s2),
          "crit3": float(s3),
          "total": float(total_judge),
          "remarks": str(remarks),
      }])

      updated_df = pd.concat([new_df, new_row], ignore_index=True)

      # Google Sheet को सीधे अपडेट करें
      conn.update(data=updated_df)
      st.toast(
          f"✅ {judge}: {total_judge}/15 Google Sheet में सुरक्षित हो गया!",
          icon="🎉",
      )
      st.rerun()

# ----------------- 2. रैंक व रिजल्ट (Junior / Senior out of 45) -----------------
elif menu == "🏆 Top 3 परिणाम (45 में से)":
  st.markdown("#### 🏆 वर्गवार टॉप 3 रैंक (Total: 45 Marks)")

  if df_marks.empty or "total" not in df_marks.columns:
    st.info("अभी तक किसी जज द्वारा नंबर नहीं भरे गए हैं।")
  else:
    # 3 जजों के कुल नंबर जोड़ना
    df_clean = df_marks.dropna(subset=["model_id", "total"])
    pivoted = df_clean.pivot_table(
        index="model_id", columns="judge_name", values="total", aggfunc="first"
    ).reset_index()

    merged = pd.merge(df_base, pivoted, left_on="id", right_on="model_id", how="left")

    for j in ["Shree S.K. Nayak", "Shri B.N.R. Tripathi", "Shri S.N. Singh"]:
      if j not in merged.columns:
        merged[j] = 0.0
      else:
        merged[j] = pd.to_numeric(merged[j], errors="coerce").fillna(0.0)

    merged["Total (out of 45)"] = (
        merged["Shree S.K. Nayak"]
        + merged["Shri B.N.R. Tripathi"]
        + merged["Shri S.N. Singh"]
    )

    def display_category_ranks(grp_title, grp_key, emoji):
      st.markdown(f"### {emoji} {grp_title}")
      grp_df = (
          merged[
              (merged["group"] == grp_key) & (merged["Total (out of 45)"] > 0)
          ]
          .sort_values(by="Total (out of 45)", ascending=False)
          .reset_index(drop=True)
      )

      if grp_df.empty:
        st.caption("इस वर्ग में अभी तक कोई अंक दर्ज नहीं हुआ है।")
        return

      grp_df["Rank"] = grp_df["Total (out of 45)"].rank(
          ascending=False, method="min"
      ).astype(int)

      medals = ["🥇 1st Rank", "🥈 2nd Rank", "🥉 3rd Rank"]
      for idx, r in grp_df.head(3).iterrows():
        st.markdown(
            f"""
                <div class="rank-card">
                    <div style="font-size:1.15rem; font-weight:bold; color:#b45309;">{medals[idx]} — {r['Total (out of 45)']:.1f} / 45</div>
                    <div style="font-size:1rem; font-weight:600;">{r['name']} (कक्षा: {r['class']})</div>
                    <div style="font-size:0.85rem; color:#475569;">👥 {r['students']}</div>
                </div>
                """,
            unsafe_allow_html=True,
        )

      with st.expander(f"📋 {grp_title} की पूरी मेरिट लिस्ट देखें"):
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

    # जूनियर वर्ग (6 से 8)
    display_category_ranks("जूनियर वर्ग (कक्षा 6 से 8)", "Junior (6 to 8)", "🌱")
    st.write("---")
    # सीनियर वर्ग (9 व 10)
    display_category_ranks("सीनियर वर्ग (कक्षा 9 व 10)", "Senior (9 to 10)", "🚀")

    st.write("---")
    csv_data = (
        merged.sort_values(by="Total (out of 45)", ascending=False)
        .to_csv(index=False)
        .encode("utf-8-sig")
    )
    st.download_button(
        "📥 पूरी मेरिट लिस्ट एक्सेल / CSV डाउनलोड करें",
        data=csv_data,
        file_name="Science_Exhibition_Final_Scores.csv",
        mime="text/csv",
    )

# ----------------- 3. सुधार व डिलीट स्क्रीन -----------------
else:
  st.markdown("#### 🗑️ गलत प्रविष्टि डिलीट करें")
  st.caption("यदि किसी जज से कोई गलत नंबर दर्ज हो गया हो, तो यहाँ से हटाएँ।")

  if df_marks.empty:
    st.info("Google Sheet में अभी कोई डेटा नहीं है।")
  else:
    entry_dict = {}
    for _, r in df_marks.iterrows():
      mid = int(r["model_id"])
      matching_models = df_base[df_base["id"] == mid]
      m_name = (
          matching_models.iloc[0]["name"]
          if not matching_models.empty
          else "Model"
      )
      m_class = (
          matching_models.iloc[0]["class"] if not matching_models.empty else ""
      )
      label = f"#{mid} ({m_class} - {m_name}) | जज: {r['judge_name']} | अंक: {r['total']}/15"
      entry_dict[label] = (mid, str(r["judge_name"]))

    sel_label = st.selectbox(
        "हटाने के लिए मॉडल और जज चुनें:", list(entry_dict.keys())
    )
    del_mid, del_judge = entry_dict[sel_label]

    if st.button("🗑️ Google Sheet से यह एंट्री हटाएं", type="primary"):
      updated_df = df_marks[
          ~(
              (df_marks["model_id"] == del_mid)
              & (df_marks["judge_name"] == del_judge)
          )
      ]
      conn.update(data=updated_df)
      st.success(
          f"मॉडल #{del_mid} के लिए {del_judge} जी का स्कोर Google Sheet से हटा"
          " दिया गया।"
      )
      st.rerun()
