<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->


<!-- ABOUT THE PROJECT -->
# AnkiAI

<h2>📚 Description</h2>

<p><strong>ankiAI-generator</strong> is a Python-based project designed to automate the creation of high-quality Anki flashcards from scanned or unstructured documents, all inside interactive Jupyter Notebooks.</p>

<h2>✨ Features</h2>
<ul>
    <li><strong>OCR PDFs with Sidecar Text Extraction</strong><br>
        Use <code>OCRmyPDF</code> to process scan PDFs and generate clean <code>.txt</code> sidecar files containing the recognized text.
    </li>
    <br/>
    <li><strong>Fact-by-Fact Summarization</strong><br>
        Automatically summarize extracted content into individual, precise facts using Google's <code>genai</code> API with Gemini 2.5 Flash, optimized for knowledge extraction.
    </li>
    <br/>
    <li><strong>Anki Flashcard Creation</strong><br>
        Generate well-structured flashcards from summarized facts and export them into Anki-compatible formats for easy import.
    </li>
</ul>

<h2>⚙️ Built With</h2>
<ul>
    <li><strong>Python</strong></li>
    <li><strong>OCRmyPDF</strong> for high-accuracy OCR</li>
    <li><strong>Google Generative AI (Gemini 2.5 Flash)</strong> for summarization and content generation</li>
</ul>

<h2>📈 Use Cases</h2>
<ul>
    <li>Quickly turning lecture notes, books, or scanned documents into study material</li>
    <li>Building personalized Anki decks from unstructured content</li>
    <li>Automating knowledge extraction and flashcard creation workflows</li>
</ul>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these steps.



### Installation

* Clone the repository
   ```sh
   git clone https://github.com/hugoschwabe/AnkiAI-generator.git
   ```
  or
	```sh
   git clone git@github.com:hugoschwabe/AnkiAI-generator.git
   ```
* An OCRmyPDF installation is neccessary. Follow the steps in the <a href="https://ocrmypdf.readthedocs.io/en/latest/installation.html">documentation</a>
* Create a <a href="https://ai.google.dev/gemini-api/docs/api-key">Gemini API key</a>.
* For this notebook to execute a list of python packages need to be installed. A requirements-file is provided.
  ```sh
  pip install -r requirements.txt
  ```
* Create <code>keyfile.txt</code> in the base directory.
* Copy and paste your Gemini API key into the <code>keyfile.txt</code>









<!-- LICENSE -->
## License

Distributed under the MIT license. See `LICENSE` for more information.




<!-- CONTACT -->
## Contact

Hugo Schwabe - [LinkedIn](https://linkedin.com/in/hugo-schwabe-1a57a7360) - schwabehugo@gmail.com

Project Link: [https://github.com/hugoschwabe/ankiAI-generator](https://github.com/hugoschwabe/ankiAI-generator)
