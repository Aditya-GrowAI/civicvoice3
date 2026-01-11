import React from "react";
import ReactDOM from "react-dom/client";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import { ClerkProvider } from "@clerk/clerk-react";

import App from "./App.jsx";
import AuthLayout from "./components/AuthLayout.jsx";
import HomeLayout from "./components/HomeLayout.jsx";

import LandingPage from "./components/LandingPage.jsx";
// import Login from "./components/login.jsx"; // Replaced by Clerk
// import Register from "./components/register.jsx"; // Replaced by Clerk
import Home from "./components/home.jsx";
import Problems from "./components/problems.jsx";
import Requests from "./components/requests.jsx";
import Admin from "./components/admin.jsx";
import About from "./components/about.jsx";
import { RedirectToSignIn, SignIn, SignUp, SignedIn, SignedOut } from "@clerk/clerk-react";

import "bootstrap/dist/js/bootstrap.bundle.min.js";

// Import your publishable key
const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY

if (!PUBLISHABLE_KEY) {
  throw new Error("Missing Publishable Key")
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { index: true, element: <LandingPage /> },

      // Clerk handles auth UI, so we can mount their components directly or use their hosted pages.
      // We'll keep the AuthLayout if it provides styling, but replace children.
      {
        element: <AuthLayout />,
        children: [
          { path: "login/*", element: <SignIn routing="path" path="/login" /> },
          { path: "register/*", element: <SignUp routing="path" path="/register" /> },
        ],
      },

      {
        element: <HomeLayout />,
        children: [
          {
            path: "home",
            element: (
              <>
                <SignedIn>
                  <Home />
                </SignedIn>
                <SignedOut>
                  <RedirectToSignIn />
                </SignedOut>
              </>
            )
          },
          { path: "problems", element: <Problems /> }, // Public?
          { path: "requests", element: <Requests /> },
          { path: "admin", element: <Admin /> },
          { path: "about", element: <About /> },
        ],
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ClerkProvider publishableKey={PUBLISHABLE_KEY}>
      <RouterProvider router={router} />
    </ClerkProvider>
  </React.StrictMode>
);
