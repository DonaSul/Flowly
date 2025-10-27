<p align="center">
  <img src="https://github.com/DonaSul/Flowly/blob/main/Flowly%20demo%20GIF.gif?raw=true" width="800" alt="Flowly demo">
</p>

 
 # Flowly 💬  
**Transforming Forms into Conversations**

Flowly reimagines how we collect information online.  
Instead of asking users to fill out static boxes, it turns forms into interactive, AI-driven conversations — making data collection feel more natural, engaging, and efficient. Whether for surveys, feedback, or onboarding, Flowly brings a human touch to digital interaction while still capturing structured, reliable data.

---

##  Key Features
-  Converts predefined form questions into conversational flows  
-  Gathers structured responses through natural dialogue  
-  Powered by OpenAI’s conversational intelligence  
-  Minimal, modern Streamlit interface  
-  Saves all responses and form templates locally  

---

## How It Works
Flowly combines conversational AI with structured form logic to turn static questionnaires into intelligent dialogue systems.  
Each form is defined by a set of predefined questions and goals, which Flowly processes and delivers through OpenAI’s o4-mini language model.  

As users respond, the system:
1. **Interprets input contextually** using the language model to understand intent and sentiment.  
2. **Adapts dialogue flow dynamically**, ensuring smooth transitions between questions and natural conversational tone.  
3. **Maintains structured data integrity** by mapping user responses to their corresponding form fields in real time.  
4. **Saves the full conversation** locally in JSON format for later analysis or integration.  

This architecture allows Flowly to preserve the reliability of traditional forms while enhancing user experience through responsive, human-like interaction.

---
## Current Stage
Flowly is a working MVP that showcases the core capabilities of conversational data collection.  
It focuses on proving the system’s architecture, dialogue flow, and AI integration, laying the groundwork for future development in areas such as response analytics, user personalization, and backend scalability.


## Built With
- **Python** — Core logic and AI integration  
- **Streamlit** — Front-end and interactive flow design  
- **OpenAI API** — For generating natural conversations  
- **VS Code** — Development environment  

---

## ⚙️ Run It Locally
To run Flowly on your machine:  

```bash
git clone https://github.com/DonaSul/Flowly.git
cd Flowly
pip install -r requirements.txt
streamlit run app.py



