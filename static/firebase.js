// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/12.12.1/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/12.12.1/firebase-analytics.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/12.12.1/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/12.12.1/firebase-firestore.js";
// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDbu3k7TH2h5kSpmFHXGC7DyDBQUluwjQ8",
  authDomain: "sahayak-ai-86ab2.firebaseapp.com",
  projectId: "sahayak-ai-86ab2",
  storageBucket: "sahayak-ai-86ab2.firebasestorage.app",
  messagingSenderId: "96137110682",
  appId: "1:96137110682:web:567d3d6fa534da4500eb23",
  measurementId: "G-3THRN5K3JK"
};
// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
// Initialize Firebase Authentication and get a reference to the service
const auth = getAuth(app);
// Initialize Cloud Firestore and get a reference to the service
const db = getFirestore(app);
// Export the instances for use in other files
export { app, analytics, auth, db };