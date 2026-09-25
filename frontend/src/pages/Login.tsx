import { PiForkKnife } from "react-icons/pi";
import { FcGoogle } from "react-icons/fc";
import { CiMail } from "react-icons/ci";
import { FiLock } from "react-icons/fi";
import { IoMdEye } from "react-icons/io";

function Login() {
    return (
        <div className="container-fluid">
            <div className="row">
                <div className="col">Illustration</div>
                <div className="col d-flex flex-column justify-content-center align-items-center vh-100">
                    <div className="d-flex flex-column align-items-center w-50">
                        <h2 className=""><PiForkKnife/> Kaleidogram</h2>
                        <h3>Gestion des allergènes</h3>
                        <hr className="mx-2 w-100"></hr>
                        <button type="button" className="btn btn-light"><FcGoogle/> Se connecter avec Google</button>
                        <div className="d-flex align-items-center w-100">
                            <hr className="flex-grow-1" />
                            <b className="mx-2">OU PAR EMAIL</b>
                            <hr className="flex-grow-1" />
                        </div>
                        <label htmlFor="main-email">Adresse Mail</label>
                        <div className="input-group">
                            <span className="input-group-text" id="email-addon">
                                <CiMail size={20} />
                            </span>
                            <input
                                id="main-email"
                                type="email"
                                className="form-control"
                                placeholder="Votre.nom@exemple.com"
                            />
                        </div>
                        <label htmlFor="main-password">Mot de Passe</label>
                        <div className="input-group">
                            <span className="input-group-text" id="password-addon">
                                <FiLock size={20} />
                            </span>
                            <input
                                id="main-password"
                                type="password"
                                className="form-control"
                                placeholder="************"
                            />
                            <span className="input-group-text" id="show-password">
                                <IoMdEye size={20}/>
                            </span>
                        </div>
                        <div className="d-flex justify-content-between w-100">
                            <div>
                                <input type="checkbox" id="remember-user" name="bouton-se-souvenir" />
                                <label htmlFor="remember-user">Se souvenir de moi</label>
                            </div>
                            <div>
                                <a href="https:motdepasseoublie.com/aremplaceraveclevrailien">Mot de passe oublié</a>
                            </div>
                        </div>
                        <div>
                            <button type="button" className="btn connexion">Se connecter</button>
                        </div>
                        <div>
                            <p>Nouveau sur Kaleidogram ?</p>
                            <a type="text" href="https://github.com/theKaido/Kaleidogram">Créer un compte</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Login