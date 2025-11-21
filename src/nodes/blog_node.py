from src.states.blogstate import BlogState, LanguageMode, Blog

class BlogNode:
    """
    A class to represent the blog node.
    """

    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state: BlogState) -> BlogState:
        """
        Create the title for the blog.
        """
    
        if "topic" in state and state["topic"]:
            prompt = """
            You are an expert blog content writer. Use Markdown formatting.
            Generate a blog title for the topic: {topic}.
            This title should be creative and SEO friendly.
            """.strip()

            system_message = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)

            state["blog"] = Blog(
                title=response.content.strip(),
                content=state.get("blog", Blog(title="", content="")).content
            )

        return state

    def content_generator(self, state: BlogState) -> BlogState:
        
        if "topic" not in state or not state["topic"]:
            raise ValueError("topic is required in state to generate content")

        topic = state["topic"]

        mode = state.get("language_mode", LanguageMode.native)
        # converting the str to enum 
        if isinstance(mode, str):
           
            try:
                mode = LanguageMode(mode)
            except ValueError:
                mode = LanguageMode.native

        target_language = state.get("language", "english")

        if target_language.lower() == "english":
            mode = LanguageMode.native
            
        state["language_mode"] = mode
        
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
        - The language of the blog is {language_for_blog}.
        """.strip()

        response = self.llm.invoke(prompt)

        blog = Blog(title=state["blog"].title, 
                    content=response.content)
        state["blog"]= blog
        return state
       
      

    def translation(self, state: BlogState) -> BlogState:
    
        language = state.get("language", "english")
        blog = state.get("blog")

        if not isinstance(blog, Blog):
            return state 
        
        source_text = blog.content

        prompt = f"""
        You're an expert editorial translator.
        Translate the following text from English to {language}, preserving meaning, tone,
        and natural style. Do NOT do literal word-for-word translation.

        Text (Markdown):

        ```markdown
        {source_text}
        ```
        """.strip()

        translation_response = self.llm.invoke(prompt)
        blog.content = translation_response.content
        state["blog"] = blog
        return state

    def translation_router(self, state: BlogState) -> str:
        
        mode = state.get("language_mode", LanguageMode.native)

        if isinstance(mode, str):
            try:
                mode = LanguageMode(mode)
            except ValueError:
                mode = LanguageMode.native

        return "translation" if mode == LanguageMode.translation else "END"
