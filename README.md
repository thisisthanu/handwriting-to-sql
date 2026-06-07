# Handwriting-to-SQL Extraction Pipeline

## Overview
A full-stack web application that uses Google's Gemini 2.5 Flash AI to digitize handwritten forms. The app allows users to upload images of handwritten text, automatically extracts specific data points (Names, NIDs, Phone Numbers) into structured JSON, and inserts them into a local MySQL database. 

## Features
* **AI Image Processing:** Integrates the Google GenAI SDK to parse unstructured handwriting.
* **REST API Backend:** Built with Python and Flask to handle asynchronous image uploads and execute secure SQL transactions.
* **Interactive Dashboard:** A responsive, page-less Vanilla JavaScript frontend using the Fetch API for real-time CRUD operations.
* **Database Management:** Uses MySQL for persistent, relational data storage.

## Tech Stack
* **Frontend:** HTML5, CSS3, Vanilla JavaScript
* **Backend:** Python, Flask, Flask-CORS
* **Database:** MySQL
* **AI Engine:** Google Gemini API

## How It Works
1. A user uploads a photo of a handwritten document via the web UI.
2. The JavaScript client packages the image as a `FormData` object and POSTs it to the Flask backend.
3. Flask temporarily saves the image and securely routes it to the Gemini AI API with a strict JSON-formatting prompt.
4. The AI returns structured JSON data, which Flask parses and inserts into the MySQL database.
5. The frontend automatically fetches the updated SQL records and refreshes the UI without a page reload.
