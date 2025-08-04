# 🎓 Spécialités Advisor

An interactive Streamlit app to help French high school students choose their **enseignements de spécialité** for Première and Terminale (penultimate and last year of high school— 
and discover which **university formations** (from Parcoursup) align with their choices.

🔗 **Live demo**: [https://arthurperal-specialites-advisor.streamlit.app](https://arthurperal-specialites-advisor.streamlit.app)  
📂 **Repo**: [GitHub](https://github.com/ArthurPeral/specialites-advisor)

---

## 💡 What it does

- Recommends 3 spécialités based on a student's **interests** and **academic strengths**
- Suggests the 2 spécialités to **keep in Terminale** and which one to drop
- Displays **real Parcoursup formations** that match that combo (with admission stats)
- Lets users **download** their recommendations

---

## 📊 Dataset

Data comes from the official **Parcoursup open data**, from data europa:  
👉 `fr-esr-parcoursup-enseignements-de-specialite-bacheliers-generaux.csv`

### 🧼 Data Cleaning Steps

All data preparation was done in a separate Jupyter notebook (`notebooks/Data Cleaning.ipynb`) and included:

- Renaming of the columns
- Filtering out irrelevant entries
- Normalizing spécialité names to a controlled list
- Parsing the `specialites` column into lists for matching logic
- Removing duplicates and non-general tracks

You can find both the **raw dataset** and the **cleaned version** in the `data/` folder.

---

## 🖼️ How it works

- Users select up to 5 interests and 5 strengths from predefined lists
- Each interest/strength maps to potential spécialités (with weighting chosen by the user)
- A recommendation engine selects the top 3 spécialités
- From these, 2 are selected to “keep” in Terminale
- Parcoursup data is queried for formations matching that exact combination

---

## 🛠 Tech Stack

- Python (pandas, Counter, Streamlit)
- Jupyter (for data prep)
- GitHub + Streamlit Cloud (for deployment)

---

## 🗂️ Project Structure

📦 specialites-advisor/

├── app.py # Streamlit app

├── requirements.txt

├── README.md

│

├── 📁 data/

│ ├── cleaned_specialites.csv

│ └── raw_specialites.csv

│

├── 📁 notebooks/

│ └── cleaning.ipynb


---

## 🙋 About the Author

Built by [Arthur Peral](https://www.linkedin.com/in/your-link), student in Data, Society & Organizations.

---

## 🚀 Try it now

👉 [Launch the app](https://arthurperal-specialites-advisor.streamlit.app)
