import { PiStarFourLight } from "react-icons/pi";

function Illustration() {
    return (
        <div className="col d-flex flex-column justify-content-between align-items-center min-vh-100 p-4">
            <div className="d-flex align-items-center align-self-start main-page-illustration gap-1">
                <PiStarFourLight/>
                <p className="text-uppercase mb-0">Alimentation & sécurité</p>
            </div>
            <div className="illustration-rond"></div>
            <div className="align-self-start">
                <h4 className="fw-bold">Vos allergènes, à un scan de vos clients</h4>
                <p className="main-page-illustration w-75">
                    Renseignez les allergènes de chaque plat et affichez un seul
                    QR code : vos clients consultent la liste depuis leur téléphone.
                </p>
            </div>
        </div>
    )
}

export default Illustration