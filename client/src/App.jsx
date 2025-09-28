import { CssBaseline } from "@mui/material";
import useScoutGroupSelector from "./useScoutGroupSelector.js";
import testData from "../testdata/testdata.json";
import ScoutGroupSelector from "./components/ScoutGroupSelector.jsx";

// --- Main Application Component ---
export default function App() {
  // All sidebar logic is now handled by the custom hook.
  const sidebarLogic = useScoutGroupSelector(testData);

  return (
    <div>
      <CssBaseline />
      <main
        style={{
          padding: "32px",
          width: "100%",
          height: "calc(100vh - 64px)",
        }}
      >
        <ScoutGroupSelector {...sidebarLogic} />
      </main>
    </div>
  );
}
