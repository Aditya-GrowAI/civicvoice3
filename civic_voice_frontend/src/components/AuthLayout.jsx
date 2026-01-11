import { Outlet, Navigate } from "react-router-dom";
import { useAuth } from "@clerk/clerk-react";

function AuthLayout() {
  const { isSignedIn, isLoaded } = useAuth();

  if (!isLoaded) {
    return <div className="d-flex justify-content-center mt-5"><div className="spinner-border" /></div>;
  }

  if (isSignedIn) {
    return <Navigate to="/home" replace />;
  }

  return <Outlet />;
}

export default AuthLayout;
