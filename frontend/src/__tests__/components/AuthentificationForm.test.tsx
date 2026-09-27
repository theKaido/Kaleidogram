import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, it, expect } from "vitest"
import AuthentificationForm from "../../components/AuthentificationForm"

describe("AuthentificationForm", () => {
    it("affiche le mot de passe en clair au clic sur l'oeil", async () => {
        render(<AuthentificationForm />)

        const champMotDePasse = screen.getByPlaceholderText("************")
        expect(champMotDePasse).toHaveAttribute("type", "password")

        const boutonOeil = screen.getByRole("button", { name: "Afficher le mot de passe"})
        await userEvent.click(boutonOeil)

        expect(champMotDePasse).toHaveAttribute("type", "text")
    })
})