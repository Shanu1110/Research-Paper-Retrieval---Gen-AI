import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer

st.set_page_config(page_title="Paper Retrieval System", layout="wide")

st.title("AI Paper Retrieval System")
st.markdown("---")

# Initialize session state
if 'papers' not in st.session_state:
    st.session_state.papers = [
        {
            'id': 1,
            'title': 'Neural Networks in Healthcare',
            'abstract': 'This paper explores the application of neural networks for medical diagnosis and patient monitoring systems.',
            'authors': 'Smith, Johnson, Williams',
            'year': 2024
        },
        {
            'id': 2,
            'title': 'Efficient Language Models',
            'abstract': 'We present optimized techniques for training large language models with reduced computational requirements.',
            'authors': 'Chen, Lee, Park',
            'year': 2024
        },
        {
            'id': 3,
            'title': 'Quantum Computing Basics',
            'abstract': 'An introduction to quantum algorithms and their applications in solving classical problems.',
            'authors': 'Kumar, Shah, Patel',
            'year': 2023
        },
    ]

if 'embedding_model' not in st.session_state:
    with st.spinner("Loading embedding model..."):
        st.session_state.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Create embeddings
    paper_embeddings = []
    for paper in st.session_state.papers:
        text = f"{paper['title']} {paper['abstract']}"
        embedding = st.session_state.embedding_model.encode(text)
        paper_embeddings.append(embedding)
    
    st.session_state.paper_embeddings = np.array(paper_embeddings)

# Sidebar
with st.sidebar:
    st.header("Settings")
    top_k = st.slider("Number of results to show", 1, len(st.session_state.papers), 2)
    st.markdown("---")
    st.write("**System Info:**")
    st.write(f"Total Papers: {len(st.session_state.papers)}")
    st.write(f"Embedding Dimension: {st.session_state.paper_embeddings.shape[1]}")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Search Papers")
    search_query = st.text_input("Enter your search query:", placeholder="e.g., machine learning, neural networks...")

with col2:
    st.subheader("Papers Available")
    st.metric("Total", len(st.session_state.papers))

if search_query:
    # Encode query
    query_embedding = st.session_state.embedding_model.encode(search_query)
    
    # Calculate similarities
    similarities = np.dot(st.session_state.paper_embeddings, query_embedding) / (
        np.linalg.norm(st.session_state.paper_embeddings, axis=1) * np.linalg.norm(query_embedding)
    )
    
    # Get top-k results
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    st.markdown("---")
    st.subheader(f"Results for: **{search_query}**")
    
    for rank, idx in enumerate(top_indices, 1):
        paper = st.session_state.papers[idx]
        similarity = float(similarities[idx])
        
        with st.container():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"### {rank}. {paper['title']}")
                st.write(f"**Authors:** {paper['authors']}")
                st.write(f"**Year:** {paper['year']}")
                st.write(f"**Abstract:** {paper['abstract']}")
            
            with col2:
                similarity_pct = int(similarity * 100)
                st.metric("Similarity", f"{similarity_pct}%")
            
            st.divider()
else:
    st.info("Enter a search query to begin.")
    
    st.markdown("---")
    st.subheader("Available Papers")
    
    for idx, paper in enumerate(st.session_state.papers, 1):
        with st.expander(f"{idx}. {paper['title']}"):
            st.write(f"**Authors:** {paper['authors']}")
            st.write(f"**Year:** {paper['year']}")
            st.write(f"**Abstract:** {paper['abstract']}")

st.markdown("---")
st.caption("Built with Streamlit & Sentence Transformers")
