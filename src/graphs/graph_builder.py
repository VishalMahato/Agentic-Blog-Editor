from langgraph.graph import StateGraph, START, END
from src.llms.groqllm import GroqLLM
from src.states.blogstate import BlogState
from src.nodes.blog_node import BlogNode


class GraphBuilder:
    "Manages and orchestrates graphs"

    def __init__(self, llm):
        self.llm = llm

    # ---------- Plain topic graph ----------
    def build_topic_graph(self):
        """
        Build a Graph to generate blogs on the provided topic
        """
        graph = StateGraph(BlogState)
        blog_node_obj = BlogNode(self.llm)

        # Nodes
        graph.add_node("title_creation", blog_node_obj.title_creation)
        graph.add_node("content_generation", blog_node_obj.content_generation)

        # Edges
        graph.add_edge(START, "title_creation")
        graph.add_edge("title_creation", "content_generation")
        graph.add_edge("content_generation", END)

        return graph.compile()


    def build_language_topic_graph(self):
        """
        Build a graph that:
        1. Creates title
        2. Generates content    
        3. Routes: translate or not (conditional edge)
        """
        graph = StateGraph(BlogState)
        blog_node_obj = BlogNode(self.llm)

        # Nodes
        graph.add_node("title_creation", blog_node_obj.title_creation)
        graph.add_node("content_generator", blog_node_obj.content_generator)

      
        graph.add_node("translation_router", blog_node_obj.translation_router)


        graph.add_node("translater", blog_node_obj.translater)

        graph.add_edge(START, "title_creation")
        graph.add_edge("title_creation", "content_generator")
        graph.add_edge("content_generator", "translation_router")

     
        graph.add_conditional_edges(
            "translation_router",                  
            blog_node_obj.translation_router,       
            {
                "translater": "translater",          
                END: END,                          
            },
        )

        return graph.compile()

    def setup_graph(self, usecase: str):
        usecase = usecase.lower()
        if usecase == "topic":
            return self.build_topic_graph()
        elif usecase == "language_topic":
            return self.build_language_topic_graph()
        else:
            raise ValueError(f"Unknown usecase: {usecase!r}")


# below code is for langsmith/langgraph studio
llm = GroqLLM().get_llm()

# get the graph
graph_builder = GraphBuilder(llm)
graph = graph_builder.setup_graph(usecase="topic")   # or "language_topic"
