import LoginForm from "./components/auth/LoginForm";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import PipelineCreate from "./pages/PipelineCreate"
import Pipeline from "./pages/Pipeline";
import PipelineVerify from "./pages/PipelineVerify"
import AuthLayout from "./components/auth/AuthLayout";
import HomePage from "./pages/HomePage";
import { UserProvider } from "./context/UserContext";
function App() {
  return (
    <div className="App">

      <Router>
      <UserProvider>
          <Routes>
            <Route element={<AuthLayout />}>
                <Route exact path="/" element={<HomePage />} />
            </Route>
            <Route element={<AuthLayout />}>
                <Route exact path="/pipeline/:pipeline_id" element={<Pipeline />} />
            </Route>
            <Route element={<AuthLayout />}>
                <Route exact path="/pipeline-create" element={<PipelineCreate />} />
            </Route>
            <Route element={<AuthLayout />}>
                <Route exact path="/pipeline-verify" element={<PipelineVerify />} />
            </Route>
            {/*Login */}
            <Route exact path="/login" element={<LoginForm />} />

          </Routes>
          </UserProvider>
      </Router>

    </div>
  );
}

export default App;
