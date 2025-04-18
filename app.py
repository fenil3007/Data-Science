import streamlit as st
import pickle
import pandas as pd
import numpy as np

pipe = pickle.load(open('pipe2.pkl', 'rb'))

teams = [
    'Australia', 'India', 'Bangladesh', 'New Zealand', 'South Africa',
    'England', 'West Indies', 'Afghanistan', 'Pakistan', 'Sri Lanka'
]

cities = ['Colombo', 'Mirpur', 'Johannesburg', 'Dubai', 'Auckland', 'Cape Town', 'London',
          'Pallekele', 'Barbados', 'Sydney', 'Melbourne', 'Durban', 'St Lucia', 'Wellington',
          'Lauderhill', 'Hamilton', 'Centurion', 'Manchester', 'Abu Dhabi', 'Mumbai',
          'Nottingham', 'Southampton', 'Mount Maunganui', 'Chittagong', 'Kolkata',
          'Lahore', 'Delhi', 'Nagpur', 'Chandigarh', 'Adelaide', 'Bangalore',
          'St Kitts', 'Cardiff', 'Christchurch', 'Trinidad']

st.title('Cricket Score Predictor')

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select Batting Team', sorted(teams))

bowling_team_options = [team for team in teams if team != batting_team]

with col2:
    bowling_team = st.selectbox('Select Bowling Team', sorted(bowling_team_options))

city = st.selectbox('Select City', sorted(cities))

col3, col4, col5 = st.columns(3)

with col3:
    current_score = st.number_input('Current Score', min_value=0, format="%d")

with col4:
    overs = st.number_input('Overs Done', min_value=0.0, max_value=20.0, step=0.1)

with col5:
    wickets = st.number_input('Wickets Out', min_value=0, max_value=10, format="%d")

last_five = st.number_input('Runs Scored in Last Five Overs', min_value=0, format="%d")

if st.button('Predict Score'):
    # Extract over parts
    full_overs = int(overs)
    balls = round((overs - full_overs) * 10)

    if overs < 5.0 or overs > 19.5:
        st.error("⚠️ Overs must be between 5.0 and 19.5.")
    elif balls >= 6:
        st.error("⚠️ Invalid over input! In cricket, 1 over has 6 balls. You cannot enter 'X.6' or more. After 'X.5', next is '(X+1).0'.")
    elif current_score < 0:
        st.error("⚠️ Runs scored cannot be negative.")
    elif not (0 <= wickets <= 10):
        st.error("⚠️ Wickets must be between 0 and 10.")
    elif last_five > current_score:
        st.error("⚠️ Runs scored in the last five overs cannot exceed total runs scored.")
    elif last_five < 0:
        st.error("⚠️ Runs scored in the last five overs cannot be negative.")
    else:
        total_balls_bowled = full_overs * 6 + balls
        balls_left = 120 - total_balls_bowled
        wickets_left = 10 - wickets
        crr = current_score / overs if overs > 0 else 0

        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [city],
            'current_score': [current_score],
            'balls_left': [balls_left],
            'wickets_left': [wickets_left],
            'crr': [crr],
            'last_five': [last_five]
        })

        st.table(input_df)

        result = pipe.predict(input_df)
        st.success(f"🏏 Predicted Final Score: {int(result[0])}")
