
try:
    from agency import create_agency
    agency = create_agency()
    print("Agency created successfully")
    print("Agents:", [agent.name for agent in agency.agents])
except Exception as e:
    print(f"Error creating agency: {e}")
    import traceback
    traceback.print_exc()
