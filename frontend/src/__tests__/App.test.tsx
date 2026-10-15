import { render, screen } from "@testing-library/react"
import { describe, it, expect, vi } from "vitest"
import { MemoryRouter } from "react-router"
import App from "../App"

vi.mock("../api/auth")

describe("routing", () => {
    it("affiche le formulaire d'inscription sur /auth/register", () => {
        render(
            <MemoryRouter initialEntries={["/auth/register"]}>
                <App />
            </MemoryRouter>
        )

        expect(screen.getByText("Inscription")).toBeInTheDocument()
    })

    it("redirige / vers le formulaire de connexion", () => {
        render(
            <MemoryRouter initialEntries={["/"]}>
                <App />
            </MemoryRouter>
        )

        expect(screen.getByRole("button", { name: "Se connecter" })).toBeInTheDocument()
    })
})
