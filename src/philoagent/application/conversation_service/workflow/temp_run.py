import asyncio
import sys
from pathlib import Path
from langchain_core.messages import HumanMessage

# Handle both module import and direct script execution
try:
    from .graph import create_simple_workflow
    from .state import PhilosopherState
except ImportError:
    # If relative imports fail, use absolute imports
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from philoagent.conversation_service.workflow.graph import create_simple_workflow
    from philoagent.conversation_service.workflow.state import PhilosopherState

# Create the workflow graph
graph = create_simple_workflow()

async def main():
    # Initialize the state with required fields
    initial_state = {
        "messages": [HumanMessage(content="Hello, how are you?")],
        "philosopher_name": "Aristotle",
        "philosopher_context": "Ancient Greek philosopher",
        "philosopher_perspective": "Logic and ethics",
        "philosopher_style": "Socratic method",
        "summary": ""
    }
    
    # Run the graph
    messages = await graph.ainvoke(initial_state)
    
    # Print results
    print("Messages:")
    for message in messages.get("messages", []):
        print(f"  {message}")
    
    print(f"\nSummary: {messages.get('summary', '')}")

if __name__ == "__main__":
    asyncio.run(main())