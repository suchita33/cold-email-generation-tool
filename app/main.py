import streamlit as st
import sys
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from PortfolioLinks import Portfolio
from utils import clean_text

# Set the page configuration
st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("Cold Email Generator")
    st.write("Welcome to the Cold Email Generator. Enter a URL to generate tailored cold emails.")

    url_input = st.text_input(
        "Enter the URL of the job posting:",
        value="https://jobs.bendingspoons.com/positions/63c6dfcf9a2ee17858ce2194?utm_medium=job_post&utm_campaign=london&utm_source=linkedin",
        placeholder="e.g., https://example.com/job"
    )
    
    submit_button = st.button("Generate Email")

    if submit_button:
        if url_input:
            try:
                # Load and clean data
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                
                # Load portfolio and extract jobs
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)
                
                # Display jobs
                if isinstance(jobs, list):
                    for job in jobs:
                        st.subheader("Job Details")
                        st.write("**Role:**", job.get('role', 'N/A'))
                        st.write("**Experience Required:**", job.get('experience', 'N/A'))
                        st.write("**Skills:**", job.get('skills', []))
                        
                        links = portfolio.query_links(job.get('skills', []))
                        email = llm.write_mail(job, links)
                        st.subheader("Generated Email")
                        st.code(email, language='markdown')
                else:
                    st.write("**Job Details:**", jobs)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
