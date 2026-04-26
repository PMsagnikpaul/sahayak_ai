import { auth, db } from './firebase.js';
import { 
    createUserWithEmailAndPassword, 
    signInWithEmailAndPassword 
} from "https://www.gstatic.com/firebasejs/12.12.1/firebase-auth.js";
import { 
    collection, 
    addDoc 
} from "https://www.gstatic.com/firebasejs/12.12.1/firebase-firestore.js";

document.addEventListener('DOMContentLoaded', () => {
    // 1. Connect to input fields and buttons from index.html
    const loginBtn = document.getElementById('loginBtn');
    const signupBtn = document.getElementById('signupBtn');
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const authError = document.getElementById('authError');

    const showError = (msg, isSuccess = false) => {
        if (!authError) return alert(msg);
        authError.textContent = msg;
        authError.style.color = isSuccess ? '#10b981' : '#ef4444';
        authError.classList.add('show');
    };

    const clearError = () => {
        if (!authError) return;
        authError.textContent = '';
        authError.classList.remove('show');
    };

    // Clear error on input change
    [nameInput, emailInput, passwordInput].forEach(input => {
        if (input) input.addEventListener('input', clearError);
    });

    // 2. Handle User Sign Up (Create Account)
    signupBtn.addEventListener('click', async (e) => {
        e.preventDefault(); // Prevent the form from refreshing the page
        clearError();
        
        const name = nameInput.value.trim();
        const email = emailInput.value.trim();
        const password = passwordInput.value;
        
        // Basic validation
        if (!email || !password || !name) {
            showError('Please enter your name, email, and password for sign up.');
            return;
        }

        const originalBtnText = signupBtn.textContent;
        signupBtn.textContent = 'Signing up...';
        signupBtn.disabled = true;

        try {
            // First, create the user account in Firebase Auth
            const userCredential = await createUserWithEmailAndPassword(auth, email, password);
            const user = userCredential.user;
            
            // Next, store the additional user data in Firestore
            await addDoc(collection(db, "users"), {
                name: name,
                email: email,
                roles: ["requester"]
            });

            showError('Account created successfully! Redirecting...', true);
            
            // Clear the inputs
            nameInput.value = '';
            emailInput.value = '';
            passwordInput.value = '';
            
            setTimeout(() => {
                window.location.href = '/dashboard/';
            }, 1000);
            
        } catch (error) {
            // Failure: Handle errors
            let errorMessage = error.message;
            if (error.code === 'auth/email-already-in-use') errorMessage = 'This email is already registered.';
            else if (error.code === 'auth/weak-password') errorMessage = 'Password should be at least 6 characters.';
            else if (error.code === 'auth/invalid-email') errorMessage = 'Please enter a valid email address.';
            
            showError(errorMessage);
        } finally {
            signupBtn.textContent = originalBtnText;
            signupBtn.disabled = false;
        }
    });

    // 3. Handle User Log In
    loginBtn.addEventListener('click', async (e) => {
        e.preventDefault(); // Prevent the form from refreshing the page
        clearError();
        
        const email = emailInput.value.trim();
        const password = passwordInput.value;
        
        // Basic validation
        if (!email || !password) {
            showError('Please enter both email and password to log in.');
            return;
        }

        const originalBtnText = loginBtn.textContent;
        loginBtn.textContent = 'Logging in...';
        loginBtn.disabled = true;

        try {
            // Firebase Log In
            const userCredential = await signInWithEmailAndPassword(auth, email, password);
            const user = userCredential.user;
            
            showError('Logged in successfully! Redirecting...', true);
            
            // Clear the inputs
            if (nameInput) nameInput.value = '';
            emailInput.value = '';
            passwordInput.value = '';
            
            setTimeout(() => {
                window.location.href = '/dashboard/';
            }, 1000);
            
        } catch (error) {
            // Failure: Handle errors
            let errorMessage = error.message;
            if (error.code === 'auth/user-not-found' || error.code === 'auth/invalid-credential' || error.code === 'auth/wrong-password') {
                errorMessage = 'Invalid email or password.';
            } else if (error.code === 'auth/invalid-email') {
                errorMessage = 'Please enter a valid email address.';
            }
            
            showError(errorMessage);
        } finally {
            loginBtn.textContent = originalBtnText;
            loginBtn.disabled = false;
        }
    });
});
