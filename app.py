from flask import Flask, request, jsonify, render_template
import joblib

app = Flask(__name__)

# Load vectorizer and 4 binary models
vectorizer = joblib.load('models/vectorizer.joblib')
clf_ie = joblib.load('models/clf_ie.joblib')
clf_ns = joblib.load('models/clf_ns.joblib')
clf_tf = joblib.load('models/clf_tf.joblib')
clf_jp = joblib.load('models/clf_jp.joblib')

# Dictionary of personality details
PERSONALITY_DATA = {
"INTJ": {
"name": "The Architect",
"quote": "The most merciful thing in the world is the inability of the human mind to correlate all its contents.",
"description": "INTJs are independent thinkers who love ideas and deep concepts. They are great at planning, solving problems, and seeing the bigger picture. They prefer alone time to recharge and enjoy working on smart, long-term goals."
},
"INTP": {
"name": "The Logician",
"quote": "You never fail until you stop trying.",
"description": "INTPs love to analyze how things work. They are curious, logical, and enjoy exploring theories and possibilities. They prefer to keep an open mind, ask big questions, and often need alone time to think things through."
},
"ENTJ": {
"name": "The Commander",
"quote": "If you want to be successful, you must respect one rule: never lie to yourself.",
"description": "ENTJs are natural leaders. They are confident, organized, and like to take charge. They enjoy making plans, solving problems, and pushing projects forward. They are driven by goals and love when things are efficient and clear."
},
"ENTP": {
"name": "The Debater",
"quote": "The best way to predict the future is to invent it.",
"description": "ENTPs love new ideas and discussions. They enjoy debating different views, finding creative solutions, and challenging old ways of thinking. They are quick thinkers who like to keep life interesting and fun."
},
"INFJ": {
"name": "The Advocate",
"quote": "Where there is love and inspiration, I don’t think you can go wrong.",
"description": "INFJs are caring, thoughtful, and insightful. They believe in helping others and making the world better. They often understand people’s feelings deeply and prefer meaningful conversations over small talk."
},
"INFP": {
"name": "The Mediator",
"quote": "The only way to do great work is to love what you do.",
"description": "INFPs are idealistic and warm-hearted. They care deeply about their values and enjoy helping people. They are creative, love to dream big, and enjoy spending time alone to recharge their energy."
},
"ENFJ": {
"name": "The Protagonist",
"quote": "Do what you can, with what you have, where you are.",
"description": "ENFJs are inspiring and supportive leaders. They care about people’s feelings and love to motivate and bring out the best in others. They enjoy teamwork, deep connections, and making a positive difference."
},
"ENFP": {
"name": "The Campaigner",
"quote": "Life is either a daring adventure or nothing at all.",
"description": "ENFPs are enthusiastic, creative, and full of energy. They enjoy new ideas, meeting people, and exploring possibilities. They love freedom and dislike boring routines, always ready for the next adventure."
},
"ISTJ": {
"name": "The Logistician",
"quote": "Discipline is the bridge between goals and accomplishment.",
"description": "ISTJs are practical, dependable, and organized. They like clear rules and prefer facts over guesses. They are hardworking, trustworthy, and feel good when they finish tasks properly and on time."
},
"ISFJ": {
"name": "The Defender",
"quote": "To the world you may be one person, but to one person you may be the world.",
"description": "ISFJs are caring and responsible. They enjoy helping others, keeping traditions alive, and creating a warm, safe environment. They are supportive friends who prefer harmony and avoid conflicts."
},
"ESTJ": {
"name": "The Executive",
"quote": "Success usually comes to those who are too busy to be looking for it.",
"description": "ESTJs are organized and strong-willed. They like structure, rules, and clear plans. They enjoy managing tasks, making sure things get done, and keeping everyone on track. They value honesty and responsibility."
},
"ESFJ": {
"name": "The Consul",
"quote": "Alone we can do so little; together we can do so much.",
"description": "ESFJs are warm, friendly, and caring. They enjoy helping people, organizing social events, and keeping things in order. They like to feel needed and love making others happy and comfortable."
},
"ISTP": {
"name": "The Virtuoso",
"quote": "Action is the foundational key to all success.",
"description": "ISTPs are curious, practical, and hands-on. They love to understand how things work and fix problems as they come up. They enjoy freedom and dislike too many rules, preferring to live in the moment."
},
"ISFP": {
"name": "The Adventurer",
"quote": "Life is either a daring adventure or nothing.",
"description": "ISFPs are gentle, creative, and flexible. They enjoy beauty, art, and nature. They live in the moment and love trying new experiences. They prefer to go with the flow and value personal freedom."
},
"ESTP": {
"name": "The Entrepreneur",
"quote": "Do not wait to strike till the iron is hot; but make it hot by striking.",
"description": "ESTPs are energetic, outgoing, and action-oriented. They love excitement, meeting new people, and solving problems right now. They prefer to take risks and figure things out as they go."
},
"ESFP": {
"name": "The Entertainer",
"quote": "The purpose of life is to live it, to taste experience to the utmost.",
"description": "ESFPs are fun-loving, social, and spontaneous. They enjoy making others laugh, living in the present, and trying new things. They bring energy to any room and love to share good times with friends."
},
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    user_text = data.get('message_input', '')

    X = vectorizer.transform([user_text])

    # Predict probabilities for each trait
    p_ie = clf_ie.predict_proba(X)[0][1]  # probability of I
    p_ns = clf_ns.predict_proba(X)[0][1]  # N
    p_tf = clf_tf.predict_proba(X)[0][1]  # T
    p_jp = clf_jp.predict_proba(X)[0][1]  # J

    # Construct MBTI type
    mbti = ("I" if p_ie >= 0.5 else "E") + \
           ("N" if p_ns >= 0.5 else "S") + \
           ("T" if p_tf >= 0.5 else "F") + \
           ("J" if p_jp >= 0.5 else "P")

    # Normalize trait scores to percentages
    traits = {
        "Introverted": round(p_ie * 100),
        "Intuitive": round(p_ns * 100),
        "Thinking": round(p_tf * 100),
        "Judging": round(p_jp * 100)
    }

    personality = PERSONALITY_DATA.get(mbti, {
        "name": "Unknown",
        "quote": "",
        "description": "Description not available."
    })

    return jsonify({
        "type": mbti,
        "nickname": personality['name'],
        "quote": personality['quote'],
        "description": personality['description'],
        "traits": traits
    })

if __name__ == '__main__':
    app.run(debug=True)
