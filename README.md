# CivicVoice - Civic Issue Reporting Platform

A full-stack web application that enables citizens to report civic issues (potholes, garbage, water leaks, street lights) using AI-powered image detection with Google Gemini.

## 🚀 Features

- **AI-Powered Detection**: Automatically identifies civic issues from uploaded images using Google Gemini 2.0
- **User Authentication**: Secure authentication with Clerk
- **Real-time Mapping**: Interactive map showing all reported issues
- **Email Notifications**: Automatic email alerts to authorities
- **MongoDB Integration**: Cloud database for scalable data storage
- **Responsive Design**: Works on desktop and mobile devices

## 📁 Project Structure

```
civicvoiceV2/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main API application
│   ├── gemini.py           # AI image detection
│   ├── auth.py             # Clerk authentication
│   ├── database.py         # MongoDB connection
│   ├── email_service.py    # Email notifications
│   ├── requirements.txt    # Python dependencies
│   ├── vercel.json         # Vercel deployment config
│   └── .env.example        # Environment variables template
│
└── civic_voice_frontend/    # React + Vite frontend
    ├── src/
    │   └── components/     # React components
    ├── package.json        # Node dependencies
    ├── vercel.json         # Vercel deployment config
    └── .env.example        # Environment variables template
```

## 🛠️ Local Development Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- MongoDB Atlas account
- Clerk account
- Google Gemini API key

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file (copy from `.env.example`):
   ```env
   MONGODB_URL=your_mongodb_connection_string
   CLERK_ISSUER_URL=your_clerk_issuer_url
   GOOGLE_API_KEY=your_google_gemini_api_key
   EMAIL_SENDER=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password
   EMAIL_RECEIVER=recipient_email@example.com
   ```

5. Run the server:
   ```bash
   uvicorn main:app --reload
   ```
   Backend will run at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd civic_voice_frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create `.env` file (copy from `.env.example`):
   ```env
   VITE_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
   VITE_API_URL=http://localhost:8000
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```
   Frontend will run at `http://localhost:5173`

## 🌐 Vercel Deployment

### Deploy Backend

1. **Create a new Vercel project** for the backend
2. **Set root directory** to `backend`
3. **Add environment variables** in Vercel dashboard:
   - `MONGODB_URL`
   - `CLERK_ISSUER_URL`
   - `GOOGLE_API_KEY`
   - `EMAIL_SENDER`
   - `EMAIL_PASSWORD`
   - `EMAIL_RECEIVER`
4. **Deploy** - Vercel will automatically detect the `vercel.json` configuration

### Deploy Frontend

1. **Create a new Vercel project** for the frontend
2. **Set root directory** to `civic_voice_frontend`
3. **Add environment variables** in Vercel dashboard:
   - `VITE_CLERK_PUBLISHABLE_KEY`
   - `VITE_API_URL` (your deployed backend URL, e.g., `https://your-backend.vercel.app`)
4. **Deploy**

> **Important**: After deploying the backend, update the frontend's `VITE_API_URL` environment variable with the backend's Vercel URL and redeploy the frontend.

## ⚠️ Known Limitations

### File Upload on Vercel

Vercel serverless functions don't support persistent file storage. The current implementation saves uploaded images to a local `uploads/` directory, which **won't work in production on Vercel**.

**Solutions for production:**
- Use **Vercel Blob** storage
- Use **AWS S3** or **Cloudinary**
- Use **Google Cloud Storage**

To implement cloud storage, you'll need to modify the `/upload` endpoint in `main.py` to upload images to your chosen cloud storage service instead of the local filesystem.

## 🔑 Environment Variables

### Backend
- `MONGODB_URL`: MongoDB connection string
- `CLERK_ISSUER_URL`: Clerk issuer URL for JWT validation
- `GOOGLE_API_KEY`: Google Gemini API key
- `EMAIL_SENDER`: Gmail address for sending notifications
- `EMAIL_PASSWORD`: Gmail app password
- `EMAIL_RECEIVER`: Email address to receive issue notifications

### Frontend
- `VITE_CLERK_PUBLISHABLE_KEY`: Clerk publishable key
- `VITE_API_URL`: Backend API URL (localhost for dev, Vercel URL for production)

## 📝 API Endpoints

- `GET /` - Health check
- `POST /requests` - Create manual issue request (requires auth)
- `POST /upload` - Upload image and detect issue (requires auth)
- `GET /issues` - Get all reported issues (public)

## 🤖 AI Detection

The app uses Google Gemini 2.0 Flash to detect:
- Potholes
- Garbage
- Water leaks
- Street lights
- Unknown (if unable to classify)

The AI detection includes:
- Retry logic with exponential backoff for rate limits
- Comprehensive error handling
- Graceful fallback to "unknown" on errors

## 📧 Email Notifications

Automatic email notifications are sent when issues are reported, including:
- Issue type
- Location coordinates
- Description
- Image (if available)

## 🗺️ Map Integration

Uses React Leaflet to display all reported issues on an interactive map with:
- Marker clustering
- Issue type icons
- Popup details

## 🔐 Authentication

Clerk handles user authentication with:
- JWT token validation
- Protected API routes
- User session management

## 📦 Technologies Used

### Backend
- FastAPI
- Google Gemini AI
- MongoDB (Motor async driver)
- Clerk (authentication)
- Python email (SMTP)

### Frontend
- React 19
- Vite
- React Router
- React Leaflet
- Clerk React
- Bootstrap 5

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues or questions:
1. Check the `.env.example` files for required environment variables
2. Ensure all dependencies are installed
3. Verify API keys are valid
4. Check Vercel deployment logs for errors

---

**Built with ❤️ for better civic engagement**
