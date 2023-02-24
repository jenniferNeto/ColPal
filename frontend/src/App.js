import LoginForm from "./components/auth/LoginForm";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import HomePage from "./pages/HomePage"
import AuthLayout from "./components/auth/AuthLayout";
function App() {
  return (
    <div className="App">

      <Router>
      
          <Routes>
            <Route element={<AuthLayout />}>
                <Route exact path="/" element={<HomePage />} />
            </Route>
            {/*Login */}
            <Route exact path="/login" element={<LoginForm />} />

          </Routes>
      </Router>

    </div>
  );
}

export default App;
