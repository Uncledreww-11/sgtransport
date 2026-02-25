from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import google_search


MODEL = "gemini-2.5-flash"

mrt_agent = LlmAgent(
    model=MODEL,
    name='mrt_agent',
    description='Finds Singapore MRT/LRT train route information between two locations.',
    instruction="""You are a Singapore MRT/LRT route expert.
    Given a start and end location in Singapore, use google_search to find:
    - Which MRT/LRT lines and stations to take
    - Number of stops and any line transfers needed
    - Estimated travel time by MRT/LRT
    - MRT/LRT fare (adult card fare using EZ-Link/NETS FlashPay/SimplyGo)
    - First and last train timings if relevant
    Search for "MRT route from [start] to [end] Singapore" to get accurate information.""",
    tools=[google_search]
)

bus_agent = LlmAgent(
    model=MODEL,
    name='bus_agent',
    description='Finds Singapore public bus route information between two locations.',
    instruction="""You are a Singapore public bus route expert.
    Given a start and end location in Singapore, use google_search to find:
    - Which bus services to take (SBS Transit / SMRT buses)
    - Bus stop numbers and names
    - Any bus transfers needed
    - Estimated travel time by bus
    - Bus fare (adult card fare)
    - Bus frequency and operating hours if relevant
    Search for "bus route from [start] to [end] Singapore" to get accurate information.""",
    tools=[google_search]
)

taxi_agent = LlmAgent(
    model=MODEL,
    name='taxi_agent',
    description='Finds Singapore taxi and private hire car fare estimates between two locations.',
    instruction="""You are a Singapore taxi and private hire car expert.
    Given a start and end location in Singapore, use google_search to find:
    - Estimated taxi fare (metered fare including flag-down, distance, and any surcharges)
    - Estimated Grab/Gojek ride-hailing fare range
    - Estimated travel time by car
    - Any peak hour or ERP surcharges to be aware of
    - Distance between the two locations
    Search for "taxi fare from [start] to [end] Singapore" and "Grab fare [start] to [end] Singapore".""",
    tools=[google_search]
)

cycle_walk_agent = LlmAgent(
    model=MODEL,
    name='cycle_walk_agent',
    description='Finds cycling and walking route information between two locations in Singapore.',
    instruction="""You are a Singapore cycling and walking route expert.
    Given a start and end location in Singapore, use google_search to find:
    - Walking distance and estimated time
    - Cycling distance and estimated time
    - Whether there are sheltered walkways or park connectors along the route
    - Availability of shared bicycle services (SG Bike, Anywheel) nearby
    - Whether the route is pedestrian/cyclist-friendly
    Search for "walking distance from [start] to [end] Singapore" and "cycling route [start] to [end] Singapore".""",
    tools=[google_search]
)

transport_workflow_agent = SequentialAgent(
    name="transport_workflow_agent",
    description="Sequential workflow that researches MRT, bus, taxi, cycling and walking options in Singapore.",
    sub_agents=[mrt_agent, bus_agent, taxi_agent, cycle_walk_agent],
)

root_agent = LlmAgent(
    model=MODEL,
    name='travel_agent',
    description="A Singapore transport planner that recommends the best route between two locations.",
    instruction="""You are a Singapore Transport Route Recommendation Assistant.

The user will provide a starting location and ending destination within Singapore. Your job is to find and recommend the best transport routes between these two locations using Singapore's transport network.

Delegate to the transport_workflow_agent which will gather information from these specialized agents:
1. mrt_agent - for MRT/LRT train routes
2. bus_agent - for public bus routes
3. taxi_agent - for taxi and Grab/Gojek fares
4. cycle_walk_agent - for cycling and walking options

After gathering all information, provide a clear summary table comparing ALL options:

| Transport Mode | Route | Est. Time | Est. Cost | Notes |
|---|---|---|---|---|

Then provide your **recommended best route** based on a balance of time, cost, and convenience.

Include any useful tips such as:
- Peak hour considerations
- ERP charges
- Sheltered walking routes
- Nearest MRT station alternatives

All prices should be in SGD. Do not ask the user for additional information.""",
    sub_agents=[transport_workflow_agent]
)
