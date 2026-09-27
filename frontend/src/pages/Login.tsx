import Illustration from "../components/LoginIllustration.tsx"
import AuthentificationForm from "../components/AuthentificationForm.tsx"


function Login() {
    return (
        <div className="container-fluid">
            <div className="row">
                <div className="col d-none d-md-block illustration-fond">
                    <Illustration/>
                </div>
                <div className="col d-flex flex-column justify-content-center align-items-center min-vh-100">
                    <AuthentificationForm/>
                </div>
            </div>
        </div>
    )
}

export default Login