import { useState, useMemo } from 'react';

// This is a custom hook that encapsulates all the sidebar's logic.
export default function useScoutGroupSelector(jsonData) {
    // State management for the sidebar's functionality
    const [selectedScoutGroupIds, setSelectedScoutGroupIds] = useState(new Set());
    const [expandedVillageIds, setExpandedVillageIds] = useState(new Set());
    const [searchTerm, setSearchTerm] = useState('');

    // Logic to filter villages based on the search term
    const filteredVillages = useMemo(() => {
        if (!searchTerm) return jsonData.villages;
        const lowercasedFilter = searchTerm.toLowerCase();
        return jsonData.villages.filter(village =>
            village.name.toLowerCase().includes(lowercasedFilter) ||
            village.ScoutGroups.some(scoutGroup => scoutGroup.name.toLowerCase().includes(lowercasedFilter))
        );
    }, [searchTerm, jsonData.villages]);

    // Handler for expanding/collapsing a village
    const handleVillageToggle = (villageId) => {
        setExpandedVillageIds(prev => {
            const newSet = new Set(prev);
            newSet.has(villageId) ? newSet.delete(villageId) : newSet.add(villageId);
            return newSet;
        });
    };

    // Handler for selecting/deselecting villages or ScoutGroups
    const handleSelection = (type, id) => {
        console.log(type, id);
        setSelectedScoutGroupIds(prev => {
            const newSet = new Set(prev);
            if (type === 'village') {
                const village = jsonData.villages.find(v => v.id === id);
                console.log("BY VAL: " + JSON.stringify(village));
                if (!village) return newSet;
                const allScoutGroupInVillageSelected = village.ScoutGroups.every(t => newSet.has(t.id));
                village.ScoutGroups.forEach(t => {
                    allScoutGroupInVillageSelected ? newSet.delete(t.id) : newSet.add(t.id);
                });
            } else { // type === 'ScoutGroup'
                newSet.has(id) ? newSet.delete(id) : newSet.add(id);
            }
            return newSet;
        });
    };

    const clearSelection = () => setSelectedScoutGroupIds(new Set());

    // The hook returns all the necessary values and functions for the sidebar to use
    return {
        selectedScoutGroupIds,
        expandedVillageIds,
        searchTerm,
        setSearchTerm,
        filteredVillages,
        handleSelection,
        handleVillageToggle,
        clearSelection
    };
}
