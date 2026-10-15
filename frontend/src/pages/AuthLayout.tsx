import Illustration from "../components/LoginIllustration.tsx"
import { Outlet } from "react-router"


function AuthLayout() {
    return (
        <div className="container-fluid">
            <div className="row">
                <div className="col d-none d-md-block illustration-fond">
                    <Illustration/>
                </div>
                <div className="col d-flex flex-column justify-content-center align-items-center min-vh-100">
                    <Outlet/>
                </div>
            </div>
        </div>
    )
}

export default AuthLayout