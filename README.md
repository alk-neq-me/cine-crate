# cine-crate: Your Ultimate Movie Companion :clapper:

Welcome to **cine-crate**, a dynamic movie list app built with React Expo and powered by a Python FastAPI backend featuring a machine learning-based recommendation system. 🎬

## Features :sparkles:

- :movie_camera: Create and manage your personalized movie lists.
- :mag_right: Get movie recommendations using our advanced machine learning recommendation system.
- :iphone: Access your movie lists on-the-go with the mobile app.
- :rocket: Seamlessly combine React Expo with Python FastAPI for a full-stack experience.

## Getting Started :rocket:

Follow these steps to set up and run cine-crate:

### Server Setup :gear:

1. Start a Redis container using Docker for caching:
   
   ```sh
   sudo docker run --name cine-crate-redis -p 6379:6379 redis:latest && sudo docker rm cine-crate-redis
   ```

2. Set up the server:

   ```sh
   cd server
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn app:app --reload
   ```

### Mobile App Setup :iphone:

1. Install required packages:

   ```sh
   cd mobile
   yarn
   ```

2. Start the Expo development server:

   ```sh
   yarn expo start
   ```

### Contribution Guidelines :octocat:

We welcome contributions from the community! Feel free to open issues, submit pull requests, or provide suggestions. Together, we can make cine-crate even better. :muscle:

## License :scroll:

This project is licensed under the [MIT License](LICENSE).
