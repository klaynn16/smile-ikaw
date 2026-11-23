STREAMLIT BOUQUET WEBSITE

FILES
- app.py: Streamlit website and browser animation
- bouquet3d.py: original bouquet renderer, adjusted so it can be imported by Streamlit
- requirements.txt: dependency for deployment

RUN ON YOUR COMPUTER
1. Install Python.
2. Open a terminal in this folder.
3. Install dependencies:
   pip install -r requirements.txt
4. Start the website:
   streamlit run app.py
5. Open the local URL shown in the terminal (usually http://localhost:8501).

PUBLISH ONLINE WITH STREAMLIT COMMUNITY CLOUD
1. Sign in to GitHub and create a NEW public repository, for example: bouquet-for-you.
2. Upload app.py, bouquet3d.py, and requirements.txt to the repository root.
3. Open https://share.streamlit.io/ and sign in with GitHub.
4. Click Create app / Deploy an app.
5. Select your repository, branch (usually main), and main file path: app.py.
6. Click Deploy. Wait for the app to finish building.
7. Copy the Streamlit app URL and send that link.

IMPORTANT
- Upload all three files to the same repository folder.
- Do not upload only bouquet3d.py; Streamlit starts from app.py.
- The original bouquet is rendered as colored animated text in the browser, preserving its rotating 3D-style ASCII look.
