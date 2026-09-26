import {useState} from "react"
import Illustration from "../components/LoginIllustration.tsx"
import Authentification from "../components/AuthentificationForm.tsx"


function Login() {
    return (
        <div className="container-fluid">
            <div className="row">
                <div className="col d-none d-md-block">
                    <Illustration/>
                </div>
                <div className="col d-flex flex-column justify-content-center align-items-center min-vh-100">
                    <Authentification/>
                </div>
            </div>
        </div>
    )
}

export default Login