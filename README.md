Emotion-Based Chatbot Music Recommendation System 🎵

Project Overview

This project is an "Emotion-Based Chatbot Music Recommendation System** that recommends songs to users based on their mood, detected through chatbot interactions. The system uses "Cohere API" for chatbot implementation and "Spotify API" for fetching and recommending songs. User login, signup, and session management are implemented securely using **Flask-SQLAlchemy** and **MySQL/SQLite**.

## Features

- **User Interaction**: Users can interact with a chatbot through text input.
- **Emotion Detection**: The chatbot analyzes the conversation to detect the user's mood or emotion.
- **Personalized Music Recommendations**: Based on the detected mood, the system recommends relevant songs.
- **Direct Song Access**: Each recommended song includes a play button that redirects to Spotify.
- **User Authentication**: Includes secure login and signup features with password validation and session management.
- **Data Storage**: User credentials and data are stored securely using MySQL or SQLite with SQLAlchemy ORM.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **APIs**:
  - **Cohere API** - for chatbot implementation
  - **Spotify API** - for fetching and recommending songs
- **Database**: MySQL / SQLite (via Flask-SQLAlchemy)

## Project Structure

```
📂 Emotion-Based-Music-Bot
│
├── frontend
│   ├── index.html
│   ├── styles.css
│   └── script.js
│
├── backend
│   ├── app.py
│   ├── appnew.py
│   ├── chatbot.py
│   └── spotify_integration.py
│
├── database
│   └── users.db
│
├── templates
│   ├── home.html
│   ├── login.html
│   └── signup.html
│
├── README.md
└── requirements.txt
```

## Installation and Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/manojreddy56/emotion-music-bot.git
   cd emotion-music-bot
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys**:

   - Create a `.env` file in the project root and add the following:
     ```env
     COHERE_API_KEY=your_cohere_api_key
     SPOTIFY_CLIENT_ID=your_spotify_client_id
     SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
     ```

4. **Set up Database**:

   - Modify `appnew.py` to configure the SQLAlchemy URI for your MySQL or SQLite database.
     ```python
     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///path/to/your/database.db'
     ```

5. **Initialize Database**:

   ```bash
   flask shell
   >>> from appnew import db
   >>> db.create_all()
   ```

6. **Run the application**:

   ```bash
   python app.py
   ```

7. **Access the application**:
   Visit `http://localhost:5000` in your browser.

## Usage

- **Signup/Login** to access the chatbot.
- Interact with the chatbot by typing messages.
- Receive personalized music recommendations based on your mood.
- Click on the play button to listen to songs directly on Spotify.

## Screenshots


*Chatbot user interface*


*Recommended songs list*

## Contributing

Feel free to open issues or submit pull requests for improvements. Contributions are always welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Created by Manoj*

