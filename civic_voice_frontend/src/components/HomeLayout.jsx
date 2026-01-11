import { Outlet } from "react-router-dom";
import NavBarHome from "./navBarHome";
import { useAuth, RedirectToSignIn } from "@clerk/clerk-react";

function HomeLayout() {
  const { isLoaded, isSignedIn } = useAuth();

  if (!isLoaded) {
    return <div className="d-flex justify-content-center mt-5"><div className="spinner-border" /></div>;
  }

  if (!isSignedIn) {
    return <RedirectToSignIn />;
  }

  return (
    <>
      <NavBarHome />
      <Outlet />
    </>
  );
}

export default HomeLayout;
