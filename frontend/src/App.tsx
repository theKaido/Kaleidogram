import AuthLayout from "./pages/AuthLayout.tsx"
import { Routes, Route, Navigate } from "react-router"
import RegistrationForm from "./components/RegistrationForm.tsx"
import AuthentificationForm from "./components/AuthentificationForm.tsx"

function App() {
    return (
        <Routes>
           <Route path="/" element={<Navigate to="/auth/login" replace />}/>
           <Route path="auth" element={<AuthLayout/>}>
               <Route path="login" element={<AuthentificationForm />}/>
               <Route path="register" element={<RegistrationForm />}/>
           </Route>
        </Routes>
    )
}

export default App
