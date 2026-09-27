import type { ReactNode } from "react"

type PastilleProps = {
    texte: string
    couleur: string
    icone: ReactNode
    className?: string
}

function Pastille({texte, couleur, icone, className}: PastilleProps) {
    return (
        <div className={`d-flex align-items-center gap-2 pastille ${className}`}>
            <div className="pastille-icone" style={{ backgroundColor: couleur }}>
                {icone}
            </div>
            <span>{texte}</span>
        </div>
    )
}

export default Pastille
