import { List, Typography, Button, Paper } from "@mui/material";
import SearchField from "./SearchField.jsx";
import VillageListItem from "./VillageListItem.jsx";

export default function ScoutGroupSelector({
  filteredVillages = [],
  selectedScoutGroupIds,
  expandedVillageIds,
  searchTerm = "",
  setSearchTerm = () => {},
  handleSelection = () => {},
  handleVillageToggle = () => {},
  clearSelection = () => {},
}) {
  return (
    <Paper
      elevation={3}
      sx={{
        padding: "24px",
        display: "flex",
        flexDirection: "column",
        borderRadius: "16px",
        height: "100%",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "16px",
        }}
      >
        <Typography variant="h5" component="h2" fontWeight="600">
          Byar och kårer
        </Typography>
        <Button
          onClick={clearSelection}
          disabled={selectedScoutGroupIds.size === 0}
        >
          Rensa val
        </Button>
      </div>

      <SearchField
        placeholder="Sök efter by eller kår..."
        searchTerm={searchTerm}
        setSearchTerm={setSearchTerm}
      />

      <List sx={{ flexGrow: 1, overflowY: "auto", pr: 1 }}>
        {filteredVillages.map((village) => {
          const ScoutGroupsInVillage = village.ScoutGroups.map((t) => t.id);
          const selectedInVillage = ScoutGroupsInVillage.filter((id) =>
            selectedScoutGroupIds.has(id)
          );
          const isAllSelected =
            ScoutGroupsInVillage.length > 0 &&
            selectedInVillage.length === ScoutGroupsInVillage.length;
          const isPartiallySelected =
            selectedInVillage.length > 0 && !isAllSelected;
          const isExpanded = expandedVillageIds.has(village.id);

          return (
            <VillageListItem
              key={village.id}
              village={village}
              isAllSelected={isAllSelected}
              isPartiallySelected={isPartiallySelected}
              isExpanded={isExpanded}
              handleVillageToggle={handleVillageToggle}
              handleSelection={handleSelection}
              selectedScoutGroupIds={selectedScoutGroupIds}
            />
          );
        })}
      </List>
    </Paper>
  );
}
