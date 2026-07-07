from google.adk.agents.llm_agent import Agent, LlmAgent
from google.adk.tools import google_search

MODEL = get_model()

HIKING_TRAIL_SYSTEM_INSTRUCTION = (
    "You are a specialized assistant for hiking trail finder. "
    "Your sole purpose is to use the 'google_search' tool to answer questions about hiking trails. "
    "If the user asks about anything other than hiking trails, "
    "politely state that you cannot help with that topic and can only assist with hiking trails queries. "
    "Do not attempt to answer unrelated questions or use tools for other purposes."
)

hiking_trail_finder_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='hiking_trail_finder_agent',
    description='A helpful assistant for user questions.',
    instruction=HIKING_TRAIL_SYSTEM_INSTRUCTION,
    output_key="trail_info",
    tools=[google_search]
)

distance_filter_agent = LlmAgent(
    model=MODEL,
    name="distance_filter_agent",
    #description="Plans the post outline from the topic + research bundle.",
    description="Filters the hiking trails based on distance.",
    instruction="""\
Found hiking trails under `trail_info`:
{trail_info}

Pick ONE angle and produce an Outline:
- trails that are withing 1 hour travel time from the user's location.
""",
    output_schema=Outline,
    output_key="outline",
)

root_agent = SequentialAgent(
    name="sequential_hike_finder",
    description=(
        "Find hiking trails -> Filter by distance -> Generate outline"
    ),
    sub_agents=[
        hiking_trail_finder_agent,
        distance_filter_agent,
    ],
)