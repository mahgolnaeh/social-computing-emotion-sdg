SDG_LINKS = {
    "No Poverty": "https://sdgs.un.org/goals/goal1",
    "Zero Hunger": "https://sdgs.un.org/goals/goal2",
    "Good Health and Well-being": "https://sdgs.un.org/goals/goal3",
    "Quality Education": "https://sdgs.un.org/goals/goal4",
    "Gender Equality": "https://sdgs.un.org/goals/goal5",
    "Clean Water and Sanitation": "https://sdgs.un.org/goals/goal6",
    "Affordable and Clean Energy": "https://sdgs.un.org/goals/goal7",
    "Decent Work and Economic Growth": "https://sdgs.un.org/goals/goal8",
    "Industry, Innovation and Infrastructure": "https://sdgs.un.org/goals/goal9",
    "Reduced Inequality": "https://sdgs.un.org/goals/goal10",
    "Sustainable Cities and Communities": "https://sdgs.un.org/goals/goal11",
    "Responsible Consumption and Production": "https://sdgs.un.org/goals/goal12",
    "Climate Action": "https://sdgs.un.org/goals/goal13",
    "Life Below Water": "https://sdgs.un.org/goals/goal14",
    "Life on Land": "https://sdgs.un.org/goals/goal15",
    "Peace, Justice and Strong Institutions": "https://sdgs.un.org/goals/goal16",
    "Partnerships for the Goals": "https://sdgs.un.org/goals/goal17"
}


def get_sdg_link(sdg_title: str) -> str | None:
    return SDG_LINKS.get(sdg_title)
