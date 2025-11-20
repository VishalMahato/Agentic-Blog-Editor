from src.states.blogstate import BlogState, LanguageMode
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

    def content_generator(self, state: BlogState) -> BlogState:

        if "topic" not in state or not state["topic"]:
            raise ValueError("topic is required in state to generate content")

        topic = state["topic"]

        mode = state.get("language_mode", LanguageMode.native)
        state["language_mode"] = mode

        target_language = state.get("language", "english")

        if mode == LanguageMode.native:
            language_for_blog = target_language
        else:
            language_for_blog = "english"

        prompt = f"""
        You are an expert blog content writer. Use Markdown formatting.
        Generate a detailed blog content with a detailed breakdown for the topic: {topic}.
        The desired length of the blog is around 1200 words.
        The title should be creative and SEO friendly.

        # Strict Rule
        - The Language of the blog is {language_for_blog}
        """.strip()

   
        response = self.llm.invoke(prompt)

      
        if "blog" not in state or state["blog"] is None:
            from src.states.blogstate import Blog
            state["blog"] = Blog(title="", content="")

        state["blog"].content = response.content
        return state
    
    
    
