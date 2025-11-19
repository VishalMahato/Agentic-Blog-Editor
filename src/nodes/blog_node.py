from src.states.blogstate import BlogState


class BlogNode:
    """
    A class to represent he blog node 
    """

    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state: BlogState):
        """
        create the title for the blog

        Args:
            state (BlogState): _description_
        """

        if "topic" in state and state["topic"]:
            prompt = """
            You are an expert blog content writer. Use Markdown formatting.
            Generate a blog title for the topic: {topic}.
            This title should be creative and SEO friendly.
            """.strip()

            system_message = prompt.format(topic=state["topic"])

            response = self.llm.invoke(system_message)
            return {"blog": {"title": response.content}}

    def content_generation(self, state: BlogState):
        """Generates content for the blog

        Args:
            state (BlogState): _description_
        """
        if "topic" in state and state["topic"]:
            prompt = """
            You are an expert blog content writer. Use Markdown formatting.
            Generate a detailed blog content with the detailed breakdown for the topic: {topic}.
            This title should be creative and SEO friendly.
            """.strip()
            system_message = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {
                "blog": {
                    "title": state['blog']['title'],
                    "content": response.content
                }}
