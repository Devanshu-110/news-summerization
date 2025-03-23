# import json
# import os
# from utils import save_company_news
# from utils import sentiment_analysis_model
# from utils import news_summarization, audio_output, Topic_finder
# from collections import Counter
# import time
# import re
# from deep_translator import GoogleTranslator
# from pydub import AudioSegment
# import gc
# import torch


# print("Company News Summarization")
    
# company_name = input("Enter Company Name: ")
    
# if company_name:
#     file_path = save_company_news(company_name)
        
#     if os.path.exists(file_path):
#         with open(file_path, "r", encoding="utf-8") as file:
#             articles = json.load(file)
                
#             for article in articles:
#                 print(f"\nTitle: {article['title']}")
#                 print(f"Content: {article['content'][:100]}...") 
#                 print(f"Read more: {article['url']}")
                
#         del articles
#         gc.collect()
#     else:
#         print("Failed to fetch news. Try again.")
# else:
#     print("Please enter a company name.")

# with open(f"Company/{company_name}.json", "r", encoding="utf-8") as file:
#     data = json.load(file)

# for article in data:
#     topics = Topic_finder(article['title'])
    
#     sentiment = sentiment_analysis_model(article['content'])
#     article["sentiment"] = sentiment['sentiment']
    
#     del sentiment
#     gc.collect()
    
#     summary = news_summarization(article["content"])
#     article["summary"] = summary
    
#     article["topics"] = topics
    
#     if torch.cuda.is_available():
#         torch.cuda.empty_cache()
    
#     gc.collect()

# with open(f"Company/{company_name}.json", "w", encoding="utf-8") as file:
#     json.dump(data, file, indent=4)

# with open(f"Company/{company_name}.json", "r", encoding="utf-8") as file:
#     articles = json.load(file)

# sentiment_counts = Counter(article["sentiment"] for article in articles)

# print("Sentiment Counts:")
# print("Positive:", sentiment_counts.get("Positive", 0))
# print("Negative:", sentiment_counts.get("Negative", 0))
# print("Neutral:", sentiment_counts.get("Neutral", 0))

# del articles
# del sentiment_counts
# gc.collect()

# with open(f"Company/{company_name}.json", "r", encoding="utf-8") as file:
#     data = json.load(file)

# translator = GoogleTranslator(source="en", target="hi")

# audio_folder = "audio"
# os.makedirs(audio_folder, exist_ok=True)

# for file in os.listdir(audio_folder):
#     file_path = os.path.join(audio_folder, file)
#     if os.path.isfile(file_path):
#         os.remove(file_path)

# text_data = ""
# audio_files = []

# def split_text(text, max_length=4500):
#     sentences = re.split(r'(?<=[.!?])\s+', text)
#     chunks = []
#     current_chunk = ""
    
#     for sentence in sentences:
#         if len(current_chunk) + len(sentence) + 1 <= max_length:
#             current_chunk += " " + sentence if current_chunk else sentence
#         else:
#             chunks.append(current_chunk)
#             current_chunk = sentence
    
#     if current_chunk:
#         chunks.append(current_chunk)
    
#     return chunks

# for i, article in enumerate(data, start=1):
#     title_translated = translator.translate(article['title'])
    
#     content_chunks = split_text(article['content'])
#     translated_chunks = []
    
#     for chunk in content_chunks:
#         try:
#             translated_chunk = translator.translate(chunk)
#             translated_chunks.append(translated_chunk)
#             time.sleep(0.5)
#         except Exception as e:
#             print(f"Error translating chunk: {str(e)}")
#             translated_chunks.append(f"Translation error: {str(e)}")
    
#     content_translated = " ".join(translated_chunks)
    
#     del content_chunks
#     gc.collect()

#     article_text = (f"अब, आप लेख संख्या {i} सुन रहे हैं जिसका शीर्षक है: {title_translated}\n"
#                     f"अब, आप लेख संख्या {i} की सामग्री सुन रहे हैं।\n"
#                     f"सामग्री: {content_translated}\n\n")

#     text_data += article_text

#     audio_file = f"{audio_folder}/article_{i}.mp3"
#     audio_output(article_text, audio_file)
#     audio_files.append(audio_file)
    
#     del article_text
#     del content_translated
#     del translated_chunks
#     gc.collect()
    
#     if torch.cuda.is_available():
#         torch.cuda.empty_cache()
    
#     time.sleep(1)

# output_file = f"Company/{company_name}_translated.txt"
# with open(output_file, "w", encoding="utf-8") as file:
#     file.write(text_data)

# del text_data
# gc.collect()

# def combine_audio_files(audio_folder, output_file):
#     try:
#         print(f"Combining audio files from {audio_folder}...")
#         audio_files = [f for f in os.listdir(audio_folder) if f.endswith('.mp3') and f != os.path.basename(output_file)]
        
#         if not audio_files:
#             print("No audio files found to combine.")
#             return False
            
#         audio_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]) if x.split('_')[-1].split('.')[0].isdigit() else 0)
#         print(f"Found {len(audio_files)} audio files to combine.")
        
#         combined = AudioSegment.empty()
        
#         for file in audio_files:
#             file_path = os.path.join(audio_folder, file)
#             try:
#                 audio = AudioSegment.from_mp3(file_path)
#                 combined += audio
#                 print(f"Added {file}")
                
#                 del audio
#                 gc.collect()
#             except Exception as e:
#                 print(f"Error processing {file}: {str(e)}")
                
#         combined.export(output_file, format="mp3")
#         print(f"Successfully combined audio files into {output_file}")
        
#         del combined
#         gc.collect()
        
#         return True
        
#     except Exception as e:
#         print(f"Error combining audio files: {str(e)}")
#         return False

# audio_folder = "audio"
# output_file = "combined_news.mp3"
# combine_audio_files(audio_folder, output_file)
# print("Audio combining process completed!")

# if torch.cuda.is_available():
#     torch.cuda.empty_cache()

# gc.collect()

import streamlit as st
import json
import os
from utils import save_company_news
from utils import sentiment_analysis_model
from utils import news_summarization, audio_output, Topic_finder
from collections import Counter
import time
import re
from deep_translator import GoogleTranslator
from pydub import AudioSegment
import gc
import torch

# Set page config
st.set_page_config(
    page_title=" News Summarization and Text-to-Speech Application ",
    page_icon="📰",
    layout="wide"
)

# Create necessary folders
os.makedirs("Company", exist_ok=True)
os.makedirs("audio", exist_ok=True)

def split_text(text, max_length=4500):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_length:
            current_chunk += " " + sentence if current_chunk else sentence
        else:
            chunks.append(current_chunk)
            current_chunk = sentence
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

def combine_audio_files(audio_folder, output_file):
    try:
        st.info(f"Combining audio files from {audio_folder}...")
        audio_files = [f for f in os.listdir(audio_folder) if f.endswith('.mp3') and f != os.path.basename(output_file)]
        
        if not audio_files:
            st.warning("No audio files found to combine.")
            return False
            
        audio_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]) if x.split('_')[-1].split('.')[0].isdigit() else 0)
        st.info(f"Found {len(audio_files)} audio files to combine.")
        
        combined = AudioSegment.empty()
        
        for file in audio_files:
            file_path = os.path.join(audio_folder, file)
            try:
                audio = AudioSegment.from_mp3(file_path)
                combined += audio
                
                del audio
                gc.collect()
            except Exception as e:
                st.error(f"Error processing {file}: {str(e)}")
                
        combined.export(output_file, format="mp3")
        st.success(f"Successfully combined audio files into {output_file}")
        
        del combined
        gc.collect()
        
        return True
        
    except Exception as e:
        st.error(f"Error combining audio files: {str(e)}")
        return False

def process_company_news(company_name):
    with st.spinner("Fetching company news..."):
        file_path = save_company_news(company_name)
        
        if not os.path.exists(file_path):
            st.error("Failed to fetch news. Try again.")
            return False
        
        with open(file_path, "r", encoding="utf-8") as file:
            articles = json.load(file)
            
        st.success(f"Found {len(articles)} articles for {company_name}")
        
        # Display a preview of the articles
        with st.expander("Preview Articles"):
            for article in articles:
                st.subheader(article['title'])
                st.write(f"{article['content'][:100]}...") 
                st.write(f"[Read more]({article['url']})")
        
        del articles
        gc.collect()
    
    with st.spinner("Analyzing sentiment, extracting topics, and generating summaries..."):
        progress_bar = st.progress(0)
        
        with open(f"Company/{company_name}.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        
        total_articles = len(data)
        
        for i, article in enumerate(data):
            topics = Topic_finder(article['title'])
            
            sentiment = sentiment_analysis_model(article['content'])
            article["sentiment"] = sentiment['sentiment']
            
            del sentiment
            gc.collect()
            
            summary = news_summarization(article["content"])
            article["summary"] = summary
            
            article["topics"] = topics
            
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            gc.collect()
            progress_bar.progress((i + 1) / total_articles)
        
        with open(f"Company/{company_name}.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    
    with st.spinner("Counting sentiment..."):
        with open(f"Company/{company_name}.json", "r", encoding="utf-8") as file:
            articles = json.load(file)
        
        sentiment_counts = Counter(article["sentiment"] for article in articles)
        
        st.write("### Sentiment Analysis")
        col1, col2, col3 = st.columns(3)
        col1.metric("Positive", sentiment_counts.get("Positive", 0))
        col2.metric("Negative", sentiment_counts.get("Negative", 0))
        col3.metric("Neutral", sentiment_counts.get("Neutral", 0))
        
        del articles
        del sentiment_counts
        gc.collect()
    
    with st.spinner("Translating content and generating audio..."):
        with open(f"Company/{company_name}.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        
        translator = GoogleTranslator(source="en", target="hi")
        
        audio_folder = "audio"
        os.makedirs(audio_folder, exist_ok=True)
        
        # Clear previous audio files
        for file in os.listdir(audio_folder):
            file_path = os.path.join(audio_folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        text_data = ""
        audio_files = []
        
        progress_bar = st.progress(0)
        
        for i, article in enumerate(data, start=1):
            title_translated = translator.translate(article['title'])
            
            content_chunks = split_text(article['content'])
            translated_chunks = []
            
            for chunk in content_chunks:
                try:
                    translated_chunk = translator.translate(chunk)
                    translated_chunks.append(translated_chunk)
                    time.sleep(0.5)
                except Exception as e:
                    st.error(f"Error translating chunk: {str(e)}")
                    translated_chunks.append(f"Translation error: {str(e)}")
            
            content_translated = " ".join(translated_chunks)
            
            del content_chunks
            gc.collect()
        
            article_text = (f"अब, आप लेख संख्या {i} सुन रहे हैं जिसका शीर्षक है: {title_translated}\n"
                            f"अब, आप लेख संख्या {i} की सामग्री सुन रहे हैं।\n"
                            f"सामग्री: {content_translated}\n\n")
        
            text_data += article_text
        
            audio_file = f"{audio_folder}/article_{i}.mp3"
            audio_output(article_text, audio_file)
            audio_files.append(audio_file)
            
            del article_text
            del content_translated
            del translated_chunks
            gc.collect()
            
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            progress_bar.progress(i / len(data))
            time.sleep(1)
        
        output_file = f"Company/{company_name}_translated.txt"
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(text_data)
        
        del text_data
        gc.collect()
    
    with st.spinner("Combining audio files..."):
        output_file = "combined_news.mp3"
        combine_success = combine_audio_files(audio_folder, output_file)
        
        if combine_success:
            st.success("Audio combining process completed!")
        else:
            st.error("Failed to combine audio files.")
        
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        gc.collect()
    
    return True

# Main app interface
st.title("Company News Summarization and Audio Generation")

with st.sidebar:
    st.header("Enter Company Details")
    company_name = st.text_input("Company Name")
    process_button = st.button("Process Company News", type="primary")

# Process data when button is clicked
if process_button and company_name:
    success = process_company_news(company_name)
    if success:
        st.session_state.processing_complete = True
        st.session_state.company_name = company_name
elif process_button and not company_name:
    st.error("Please enter a company name.")

# Show results after processing
if 'processing_complete' in st.session_state and st.session_state.processing_complete:
    company_name = st.session_state.company_name
    
    st.header(f"Results for {company_name}")
    
    # Create tabs for different outputs
    tab1, tab2, tab3 = st.tabs(["Summary", "Translated Text", "Audio"])
    
    with tab1:
        st.subheader("News Summary")
        try:
            with open(f"Company/{company_name}.json", "r", encoding="utf-8") as file:
                articles = json.load(file)
            
            for i, article in enumerate(articles, 1):
                with st.expander(f"Article {i}: {article['title']}"):
                    st.write(f"**Summary:** {article['summary']}")
                    st.write(f"**Sentiment:** {article['sentiment']}")
                    st.write(f"**Topics:** {', '.join(article['topics'])}")
                    st.write(f"**URL:** {article['url']}")
        except Exception as e:
            st.error(f"Error loading summary data: {str(e)}")
    
    with tab2:
        st.subheader("Translated Text (Hindi)")
        try:
            with open(f"Company/{company_name}_translated.txt", "r", encoding="utf-8") as file:
                text_content = file.read()
            st.download_button(
                label="Download Translated Text",
                data=text_content,
                file_name=f"{company_name}_translated.txt",
                mime="text/plain"
            )
            st.text_area("Content", text_content, height=400)
        except Exception as e:
            st.error(f"Error loading translated text: {str(e)}")
    
    with tab3:
        st.subheader("Audio Files")
        
        st.write("### Combined Audio")
        try:
            with open("combined_news.mp3", "rb") as file:
                combined_audio_bytes = file.read()
                
            st.audio(combined_audio_bytes, format="audio/mp3")
            st.download_button(
                label="Download Combined Audio",
                data=combined_audio_bytes,
                file_name="combined_news.mp3",
                mime="audio/mp3"
            )
        except Exception as e:
            st.error(f"Error loading combined audio: {str(e)}")
        
        st.write("### Individual Article Audio Files")
        try:
            audio_files = [f for f in os.listdir("audio") if f.endswith('.mp3')]
            audio_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]) if x.split('_')[-1].split('.')[0].isdigit() else 0)
            
            for audio_file in audio_files:
                with st.expander(f"{audio_file}"):
                    with open(f"audio/{audio_file}", "rb") as file:
                        audio_bytes = file.read()
                    st.audio(audio_bytes, format="audio/mp3")
                    st.download_button(
                        label=f"Download {audio_file}",
                        data=audio_bytes,
                        file_name=audio_file,
                        mime="audio/mp3"
                    )
        except Exception as e:
            st.error(f"Error loading individual audio files: {str(e)}")

# Instructions at the bottom
with st.expander("How to use this app"):
    st.write("""
    1. Enter the name of a company in the sidebar.
    2. Click 'Process Company News' button to start the analysis.
    3. Wait for the processing to complete (this may take some time depending on the number of articles).
    4. View the results in the different tabs:
       - Summary: See sentiment analysis, topics, and summaries of each article
       - Translated Text: View the Hindi translation of all articles
       - Audio: Listen to or download the audio files in Hindi
    """)
