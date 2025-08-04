import streamlit as st
import pandas as pd
from collections import Counter
import io

# ------------------------------
# Load dataset (already cleaned)
# ------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_specialites.csv")
    df["taux_admission"] = df['nb_candidats_admis'] / df['nb_candidats_voeu']
    return df

df = load_data()

# ------------------------------
# Valid spécialités (normalized naming)
# ------------------------------
valid_specialites = [
    "Arts",
    "Humanités, Littérature et Philosophie",
    "Histoire, Géographie, Géopolitique, Sciences politiques",
    "Numérique et Sciences Informatiques",
    "Physique-Chimie",
    "Sciences économiques et sociales",
    "Sciences de la vie et de la terre",
    "Biologie-Ecologie",
    "Mathématiques",
    "Langues, Littératures et Cultures Etrangères et Régionales",
    "Littératures, langues et culture de l'antiquité",
    "Sciences de l'ingénieur"
]

# ------------------------------
# Input mappings (already normalized)
# ------------------------------
interest_to_specialite = {
    "Medicine & health": ["Sciences de la vie et de la terre", "Physique-Chimie"],
    "Engineering & technology": ["Mathématiques", "Physique-Chimie", "Numérique et Sciences Informatiques", "Sciences de l'ingénieur"],
    "Law & politics": ["Histoire, Géographie, Géopolitique, Sciences politiques", "Sciences économiques et sociales", "Humanités, Littérature et Philosophie"],
    "Economics & business": ["Mathématiques", "Sciences économiques et sociales"],
    "Environment & sustainability": ["Sciences de la vie et de la terre", "Physique-Chimie"],
    "Psychology & human behavior": ["Sciences de la vie et de la terre", "Humanités, Littérature et Philosophie"],
    "Education & teaching": ["Humanités, Littérature et Philosophie", "Littératures, langues et culture de l'antiquité"],
    "Architecture & design": ["Arts", "Mathématiques", "Sciences de l'ingénieur"],
    "Science & research": ["Mathématiques", "Physique-Chimie", "Sciences de la vie et de la terre"],
    "Mathematics & logic": ["Mathématiques", "Numérique et Sciences Informatiques"],
    "Literature & philosophy": ["Humanités, Littérature et Philosophie", "Littératures, langues et culture de l'antiquité", "Langues, Littératures et Cultures Etrangères et Régionales"],
    "History & geopolitics": ["Histoire, Géographie, Géopolitique, Sciences politiques", "Humanités, Littérature et Philosophie"],
    "Computer science": ["Numérique et Sciences Informatiques", "Mathématiques"],
    "Space & astronomy": ["Mathématiques", "Physique-Chimie"],
    "Music": ["Arts"],
    "Visual arts": ["Arts"],
    "Theater & performance": ["Arts", "Humanités, Littérature et Philosophie"],
    "Writing & storytelling": ["Humanités, Littérature et Philosophie", "Littératures, langues et culture de l'antiquité"],
    "Film & media": ["Arts", "Langues, Littératures et Cultures Etrangères et Régionales"],
    "Fashion & aesthetics": ["Arts"],
    "Design & architecture": ["Arts", "Sciences de l'ingénieur"],
    "Entrepreneurship": ["Sciences économiques et sociales", "Mathématiques"],
    "Communication": ["Langues, Littératures et Cultures Etrangères et Régionales", "Humanités, Littérature et Philosophie"],
    "Leadership": ["Sciences économiques et sociales", "Histoire, Géographie, Géopolitique, Sciences politiques"],
    "Helping others / volunteering": ["Sciences de la vie et de la terre", "Humanités, Littérature et Philosophie"],
    "Public speaking": ["Histoire, Géographie, Géopolitique, Sciences politiques", "Langues, Littératures et Cultures Etrangères et Régionales"],
    "Management": ["Sciences économiques et sociales", "Mathématiques"],
    "Travel & cultures": ["Histoire, Géographie, Géopolitique, Sciences politiques", "Langues, Littératures et Cultures Etrangères et Régionales"],
    "Sports & fitness": ["Sciences de la vie et de la terre", "Mathématiques"],
    "Gaming": ["Numérique et Sciences Informatiques", "Mathématiques"],
    "Nature & animals": ["Sciences de la vie et de la terre"],
    "Food & cooking": ["Sciences de la vie et de la terre", "Physique-Chimie"],
    "DIY / crafting": ["Arts", "Sciences de l'ingénieur"],
    "Photography": ["Arts"],
    "Digital tools & technology": ["Numérique et Sciences Informatiques", "Mathématiques"]
}

strength_to_specialite = {
    "Français": ["Humanités, Littérature et Philosophie", "Littératures, langues et culture de l'antiquité"],
    "Histoire-Géographie": ["Histoire, Géographie, Géopolitique, Sciences politiques", "Humanités, Littérature et Philosophie"],
    "Langues vivantes (A ou B)": ["Langues, Littératures et Cultures Etrangères et Régionales", "Littératures, langues et culture de l'antiquité"],
    "Sciences économiques et sociales (SES)": ["Sciences économiques et sociales", "Histoire, Géographie, Géopolitique, Sciences politiques"],
    "Mathématiques": ["Mathématiques", "Numérique et Sciences Informatiques", "Physique-Chimie"],
    "Physique-Chimie": ["Physique-Chimie", "Mathématiques", "Sciences de l'ingénieur"],
    "Sciences de la vie et de la Terre (SVT)": ["Sciences de la vie et de la terre", "Physique-Chimie"],
    "Éducation physique et sportive (EPS)": ["Sciences de la vie et de la terre"],
    "Enseignement moral et civique (EMC)": ["Humanités, Littérature et Philosophie", "Histoire, Géographie, Géopolitique, Sciences politiques"],
    "Sciences numériques et technologie (SNT)": ["Numérique et Sciences Informatiques", "Mathématiques"]
}

interests_list = list(interest_to_specialite.keys())
strengths_list = list(strength_to_specialite.keys())

# ------------------------------
# Recommendation Functions
# ------------------------------
def recommend_specialites(interests, strengths, weight_strengths=1):
    total_scores = Counter()
    for interest in interests:
        for sp in interest_to_specialite.get(interest, []):
            total_scores[sp] += 1
    for strength in strengths:
        for sp in strength_to_specialite.get(strength, []):
            total_scores[sp] += weight_strengths
    return [sp for sp, _ in total_scores.most_common(3)]

def top_two_specialites(interests, strengths, weight_strengths=1):
    all_recos = recommend_specialites(interests, strengths, weight_strengths)
    keep = all_recos[:2]
    drop = all_recos[2] if len(all_recos) > 2 else None
    return keep, drop

def filter_formations(df, specialites_to_keep):
    return df[df['specialites_list'].apply(lambda x: all(sp in x for sp in specialites_to_keep))]

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="Spécialités Advisor", layout="wide")
st.title("🎓 Spécialités Advisor")

st.markdown("""
Welcome to **Spécialités Advisor**!  
This tool helps students in Seconde choose their spécialités for Première and Terminale
based on their **interests** and **academic strengths**.  
You'll also discover real **university formations** chosen by similar students from Parcoursup data.
""")

with st.sidebar:
    st.header("🧑‍🎓 Your Profile")
    st.caption("🎯 Select what you like and the subjects you're good at.")
    interests_input = st.multiselect("Select up to 5 interests:", interests_list, max_selections=5)
    strengths_input = st.multiselect("Select up to 5 strengths:", strengths_list, max_selections=5)
    weight_strengths = st.slider("How much should your strengths influence the result?", 1, 5, 2)
    generate = st.button("🔍 Get Your Recommendation")

if generate:
    if not interests_input or not strengths_input:
        st.warning("Please select at least one interest and one strength.")
    else:
        keep, drop = top_two_specialites(interests_input, strengths_input, weight_strengths)

        with st.expander("🎯 Your Personalized Recommendation", expanded=True):
            st.subheader("✅ Recommended spécialités for Première")
            st.markdown(f"**To keep for Terminale:** {', '.join(keep)}")
            if drop:
                st.markdown(f"**To drop later:** {drop}")

        matching_df = filter_formations(df, keep)

        st.subheader("🎓 Real Parcoursup Formations for this Combo")
        if not matching_df.empty:
            result_df = matching_df[['formation', 'specialites_list', 'nb_candidats_voeu', 'taux_admission']].sort_values(by="nb_candidats_voeu", ascending=False)
            st.dataframe(result_df)

            # Download CSV
            csv = result_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name='formations_recommendation.csv',
                mime='text/csv'
            )
        else:
            st.info("No matching university formations found for this combination.")


