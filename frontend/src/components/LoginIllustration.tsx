import { PiStarFourBold } from "react-icons/pi";
import { LuMilk } from "react-icons/lu";
import Pastille from "./Pastille"
import { GiPeanut } from "react-icons/gi";
import { LuWheat } from "react-icons/lu";
import { LuFlaskConical } from "react-icons/lu"

function Illustration() {
    return (
        <div className="col d-flex flex-column justify-content-between align-items-center min-vh-100 p-4">
            <div className="d-flex align-items-center align-self-start main-page-illustration gap-1">
                <PiStarFourBold/>
                <p className="text-uppercase mb-0 fw-bold">Alimentation & sécurité</p>
            </div>
            <div className="illustration-rond illustration-container">
                <div className="cercle-orange">
                    <div className="halo-cercle-orange"></div>
                </div>
                <div className="cercle-vert-transparent">
                    <div className="cercle-vert"></div>
                </div>
                <div className="triangle-jaune"></div>
                <div className="green-dot"></div>
                <div className="hexagone-bleu"></div>
                <Pastille
                    texte="Lactose"
                    couleur="var(--couleur-allergene-bleu-1)"
                    icone={<LuMilk color={"white"}/>}
                    className="position-absolute pastille-lactose"
                />
                <Pastille
                    texte="Arachides"
                    couleur="var(--couleur-allergene-orange-1)"
                    icone={<GiPeanut color={"white"}/>}
                    className="position-absolute pastille-arachides"
                />
                <Pastille
                    texte="Gluten"
                    couleur="var(--couleur-allergene-jaune-1)"
                    icone={<LuWheat color={"white"}/>}
                    className="position-absolute pastille-gluten"
                />
                <Pastille
                    texte="Sulfate"
                    couleur="var(--couleur-allergene-vert-2)"
                    icone={<LuFlaskConical color={"white"}/>}
                    className="position-absolute pastille-sulfate"
                />
            </div>
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