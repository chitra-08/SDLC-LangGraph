from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
import streamlit as st


# Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize LLM
llm = ChatGroq(model="qwen-2.5-32b")

# Graph State
class State(TypedDict):
    user_input_requirements: str
    user_stories: str
    design_docs_functional: str
    design_docs_technical: str
    generate_code: str
    fixed_code: str
    test_cases: str
    po_feedback: str
    des_review_feedback:str
    code_review_feedback: str
    security_review_feedback: str
    testcase_review_feedback: str
    qa_testing_review_feedback: str

def user_input_reqs(state:State):
    print("User requirement", state["user_input_requirements"])

def create_user_stories(state: State):
    """Convert the user requirements into user stories"""
    #print("Inside create user stories")
    msg = llm.invoke(f"""You are a business analyst expert in writing user stories. Please take the user requirements {state['user_input_requirements']}
                     and convert it into user stories""")
    #print("User Stories: ", msg.content)
    print("User Stories Created")
    return ({"user_stories": msg.content})

def create_design_docs(state: State):
    """Create the functional and technical design documents"""
    if state['po_feedback'] == "Approved":
        msg1 = llm.invoke(f"""You are a funcational analyst and need to design functional document based on the user stories
                         {state["user_stories"]} and user requirements {state["user_input_requirements"]}.""")
        msg2 = llm.invoke(f"""You are a technical lead and need to design technical documents based on the user stories
                         {state["user_stories"]} and user requirements {state["user_input_requirements"]}. 
                         For techincal documents, you can use the UML diagrams as well.""")
        print("Functional and Technical Design Documents Created")
        return({"design_docs_functional":msg1.content, "design_docs_technical": msg2.content})

def gen_code(state:State):
    """Generate the code in java language based on the understanding from technical document"""
    if state['design_docs_technical'] != None:
        msg = llm.invoke(f"""You are an expert java programmer and based on your understandig from {state["design_docs_technical"]}, 
                         please write a java program on it.""")
        print("Code Generated")
        return ({"generate_code": msg.content})

def write_test_cases(state:State):
    if state["generate_code"] != None:
         msg = llm.invoke(f"""You are an QA. Based on the functional design document {state["design_docs_functional"]}, 
                         please write test cases..""")
         print("Test Cases Generated")
         return ({"test_cases": msg.content})

def product_owner_review(state:State):
     """Check if the user stories genearted are apt or not"""
     if state["user_stories"] != None:
          return({"po_feedback": "Approved"})
     else:
          return({"po_feedback": "Feedback"})

def po_feedback_approval(state:State):
    if state["po_feedback"] == "Approved":
        print("Product Owner Approved")
        return "Approved"
    
def review_user_stories(state:State):
    """Check if the user stories are appropriate"""
    pass

def design_review(state:State):
    """Check if technical and functional documents are apt."""
    if state["design_docs_functional"] != None and state["design_docs_technical"] != None:
        return({"des_review_feedback":"Approved"})
    else:
        return({"des_review_feedback": "Feedback"})

def design_review_approval(state:State):
    """Approval from reviewer"""
    if state["des_review_feedback"] == "Approved":
        return "Approved"
    else:
        return "Feedback"

def code_review(state:State):
    """Check if code is correct or not"""
    if state["generate_code"] != None:
        return({"code_review_feedback":"Approved"})
    else:
        return({"code_review_feedback": "Feedback"})

def code_review_approval(state:State):
    """Approval from reviewer"""
    if state["code_review_feedback"] == "Approved":
        return "Approved"
    else:
        return "Feedback"

def fix_code_after_security(state:State):
    pass

def fix_code_after_code_review(state: State):
    pass

def security_review(state:State):
     if state["generate_code"] != None:
        return({"security_review_feedback" : "Approved"})
     else:
         return({"security_review_feedback" : "Feedback"})

def security_review_approval(state:State):
    """Approval from reviewer"""
    if state["security_review_feedback"] == "Approved":
        return "Approved"
    else:
        return "Feedback"
    
def test_cases_review(state:State):
     if state["test_cases"] != None:
        return({"testcase_review_feedback" : "Approved"})
     else:
         return({"testcase_review_feedback" : "Feedback"})

def test_cases_review_approval(state:State):
    """Approval from reviewer"""
    if state["testcase_review_feedback"] == "Approved":
        return "Approved"
    else:
        return "Feedback"

def fix_test_cases_after_review(state:State):
    pass

def QA_Testing(state:State):
     if state["test_cases"] != None:
        return({"qa_testing_review_feedback" : "Approved"})
     else:
         return({"qa_testing_review_feedback" : "Feedback"})

def qa_testing_approval(state:State):
    """Approval from reviewer"""
    if state["qa_testing_review_feedback"] == "Approved":
        return "Passed"
    else:
        return "Failed"

def fix_code_after_qa_feedback(state:State):
    pass

def Deployment(state:State):
    print("Deployment Completed")

def Monitoring_and_Feedback(state:State):
    print("Monitoring and Feedback Completed")

def Maintenance_and_Updates(state:State):
    print("Maintenance and Updates Completed")

# Build and compile the workflow
workflow1 = StateGraph(State)
    
# Add nodes
workflow1.add_node("user_input_reqs", user_input_reqs)
workflow1.add_node("create_user_stories", create_user_stories)
workflow1.add_node("product_owner_review", product_owner_review)
workflow1.add_node("review_user_stories", review_user_stories)
workflow1.add_node("create_design_docs", create_design_docs)
workflow1.add_node("design_review", design_review)
workflow1.add_node("gen_code", gen_code)
workflow1.add_node("code_review", code_review)
workflow1.add_node("fix_code_after_code_review", fix_code_after_code_review)
workflow1.add_node("security_review", security_review)
workflow1.add_node("write_test_cases", write_test_cases)
workflow1.add_node("fix_code_after_security", fix_code_after_security)
workflow1.add_node("test_cases_review", test_cases_review)
workflow1.add_node("fix_test_cases_after_review", fix_test_cases_after_review)
workflow1.add_node("QA_Testing", QA_Testing)
workflow1.add_node("fix_code_after_qa_feedback", fix_code_after_qa_feedback)
workflow1.add_node("Deployment", Deployment)
workflow1.add_node("Monitoring_and_Feedback", Monitoring_and_Feedback)
workflow1.add_node("Maintenance_and_Updates", Maintenance_and_Updates)

    
# Add edges
workflow1.add_edge(START, "user_input_reqs")
workflow1.add_edge("user_input_reqs", "create_user_stories")
workflow1.add_edge("create_user_stories", "product_owner_review")
workflow1.add_conditional_edges(
    "product_owner_review",
    po_feedback_approval,
    {
        "Approved": "create_design_docs",
        "Feedback": "review_user_stories"
    }
    )
workflow1.add_edge("review_user_stories", "create_user_stories")
workflow1.add_edge("create_design_docs", "design_review")
workflow1.add_conditional_edges(
    "design_review",
    design_review_approval,
    {
        "Approved": "gen_code",
        "Feedback": "create_design_docs"
    }
    )
workflow1.add_edge("gen_code", "code_review")
workflow1.add_conditional_edges(
    "code_review",
    code_review_approval,
    {
        "Approved": "security_review",
        "Feedback": "fix_code_after_code_review"
    }
    )
workflow1.add_edge("fix_code_after_code_review", "gen_code")
workflow1.add_conditional_edges(
    "security_review", 
    security_review_approval,
    {
        "Approved": "write_test_cases",
        "Feedback": "fix_code_after_security"
    }
    )
workflow1.add_edge("fix_code_after_security", "gen_code")
workflow1.add_edge("write_test_cases", "test_cases_review")
workflow1.add_conditional_edges(
    "test_cases_review", 
    test_cases_review_approval,
    {
        "Approved": "QA_Testing",
        "Feedback": "fix_test_cases_after_review"
    }
    )
workflow1.add_conditional_edges(
    "QA_Testing", 
    qa_testing_approval,
    {
        "Passed": "Deployment",
        "Failed": "fix_code_after_qa_feedback"
    }
    )
workflow1.add_edge("fix_test_cases_after_review", "write_test_cases")
workflow1.add_edge("fix_code_after_qa_feedback", "gen_code")
workflow1.add_edge("Deployment", "Monitoring_and_Feedback")
workflow1.add_edge("Monitoring_and_Feedback", "Maintenance_and_Updates")
workflow1.add_edge("Maintenance_and_Updates", END)

# Compile
sdlc_agent = workflow1.compile()

# Streamlit app
def main():
    """Run the Streamlit app for completing the tasks of Software Dev Life Cycle."""
    st.title("SDLC Project")
    st.write("Enter the user requirements for which you want to generate the user stories, design documents, code and test cases.")

    # Input field for YouTube URL
    user_requirements = st.text_input("Enter user requirements", "")

    # Button to generate blog
    if st.button("Generate Artifacts"):
        if user_requirements.strip() == "":
            st.warning("Please enter the user requirements!")
        else:
            with st.spinner("Processing user requirements..."):
                # Invoke the agent with the user requirements
                result = sdlc_agent.invoke({"user_input_requirements": user_requirements})
                
                # Display results
                st.subheader("User Stories")
                st.markdown(result["user_stories"])
                st.subheader("Functional Design Document")
                st.markdown(result["design_docs_functional"])
                st.subheader("Technical Design Document")
                st.markdown(result["design_docs_technical"])
                st.subheader("Code Generated")
                st.markdown(result["generate_code"])
                st.subheader("Test Cases Generated")
                st.markdown(result["test_cases"])

if __name__ == "__main__":
    main()