import os
import ocrmypdf
from google import genai
import chardet
from pathlib import Path
import time

# Replace API_KEY with your personal key
API_KEY = open("keyfile.txt", "r").read()
INPUT = "./input"            # Input folder for pdf files
OCR = "./ocr"
OUTPUT = "./output"          # Output folder for pdf and txt files
LANGUAGE = "deu"             # OCR language: deu = German, eng = English, etc.

prompts = {
    "prompt":"""Du erhälst die Inhalte einer Vorlseung an einer Universität als Eingabestring.
    Du sollst die Vorlesung zusammenfassen, indem du ausschließlich akademisch und thematisch wichtigen Fakten im Bezug zum Oberthema als String zurückgibst.
    Dabei kann es sich beispielsweise um Definitionen von Fachbegriffen, Einführung in Konzepte oder Beispiele handeln. 
    Das Format des Rückgabestrings ist: Fakt1///Fakt2///Fakt3.
    Sei präzise und verzichte auf alles, was nicht zu diesen Faketen gehört.
    Es folgt der Eingabestring: 
    """,
    "prompt_all":"""Du erhälst die Inhalte einer Vorlseung an einer Universität als Eingabestring.
    Deine Aufgabe ist es, eine umfassende Liste von Fakten aus dem Text zu extrahieren.
    Diese Fakten sollten alle wichtigen Konzepte, Definitionen, Beispiele und Kernaussagen der Vorlesung abdecken.
    Sei dabei ausführlich und extrahiere so viele relevante Fakten wie möglich.
    Das Format des Rückgabestrings ist: Fakt1///Fakt2///Fakt3.
    Es folgt der Eingabestring: 
    """
}
f_prompts = {
    "f_prompt":"""Eine Karteikarte besteht aus genau einer Frage und einer Antwort.
    Du sollst Karteikarten erstellen aus den Informationen im Eingabestring.
    Basierend auf diesem String sollst du alle sinnvollen Fragen stellen, die man zu den akademischen Inhalten stellen kann, und diese beantworten.
    Jede Zeile deiner Ausgabe muss folgendem Format entsprechen:  Frage1;Antwort1///Frage2;Antwort2///Frage3;Antwort3.
    Verwende keine Semikolons in der Frage oder in der Antwort.
    Beginne Fragen und Antworten direkt, nicht mit dem Wort Frage oder Antwort.
    Halte dich strikt an das Format Frage1;Antwort1///Frage2;Antwort2///Frage3;Antwort3
    Es folgt der Eingabestring: 
    """,
    "f_prompt_all":"""Du sollst Karteikarten erstellen aus den Informationen im Eingabestring.
    Der Eingabestring besteht aus Fakten im Format: Fakt1///Fakt2///Fakt3.
    Für jeden Fakt im Eingabestring sollst du eine oder mehrere sinnvolle Fragen stellen und diese beantworten, um möglichst viele Karteikarten zu erstellen.
    Jede Zeile deiner Ausgabe muss folgendem Format entsprechen:  Frage1;Antwort1///Frage2;Antwort2///Frage3;Antwort3.
    Verwende keine Semikolons in der Frage oder in der Antwort.
    Beginne Fragen und Antworten direkt, nicht mit dem Wort Frage oder Antwort.
    Halte dich strikt an das Format Frage1;Antwort1///Frage2;Antwort2///Frage3;Antwort3
    Es folgt der Eingabestring: 
    """
}

client = genai.Client(api_key=API_KEY)

def generate_data() -> None:
    """
    Scans the INPUT directory for PDF files and performs Optical Character Recognition (OCR) on each file.

    For each PDF, it generates a corresponding .txt file containing the extracted text in the OCR directory.
    It also saves the OCR'd PDF in the OCR directory. This function relies on the `ocrmypdf` library.
    """
    # Find all pdf files in input folder
    for filename in os.listdir(INPUT):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(INPUT, filename)
            output_pdf_path = os.path.join(OCR, filename)  # optional
            txt_filename = os.path.splitext(filename)[0] + ".txt"
            txt_path = os.path.join(OCR, txt_filename)

            print(f"Processing: {filename}")
            
            try:
                ocrmypdf.ocr(
                    pdf_path,
                    output_pdf_path,
                    sidecar=txt_path,
                    language=LANGUAGE,
                    force_ocr=True  # Falls PDF schon Text hat, trotzdem neu erkennen
                )
                print(f"-> Done: {txt_filename}")
            except Exception as e:
                print(f"Error at {filename}: {e}")

    print("All Files Processed!\n")

def read_data() -> dict[str, str]:
    """
    Reads text data from all .txt files in the OCR directory.

    Returns:
        dict[str, str]: A dictionary mapping filenames to their full text content.
    """
    file_contents = {}
    print("Reading input files...")
    for filename in os.listdir(OCR):
        if filename.lower().endswith(".txt"):
            path = os.path.join(OCR, filename)
            try:
                raw_bytes = Path(path).read_bytes()
                encoding = chardet.detect(raw_bytes)["encoding"] or "utf-8"
                decoded = raw_bytes.decode(encoding, errors="replace")
                file_contents[filename] = decoded
                print(f"  - Read {filename}: {len(decoded)} characters.")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
    return file_contents

def generate_text(prompt: str, data: dict[str, str], print_desc: str = None) -> dict[str, str]:
    """
    Generates text from the model for each entry in the input data dictionary.
    The content for each entry is chunked to handle large texts.

    Returns:
        dict[str, str]: A dictionary mapping filenames to LLM output.
    """
    if print_desc:
        print(print_desc)
    
    results = {}
    item_count = len(data)
    current_item = 0
    for key, content in data.items():
        current_item += 1
        print(f"Processing item {current_item}/{item_count}: '{key}'...")
        
        # Chunk the content
        chunks = [content[i:i+20000] for i in range(0, len(content), 20000)]
        full_response = ""
        for i, chunk in enumerate(chunks):
            print(f"  - Processing chunk {i+1}/{len(chunks)}...")
            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=prompt + chunk,
                config=genai.types.GenerateContentConfig(
                    thinking_config=genai.types.ThinkingConfig(
                        thinking_budget=4096
                    )
                )
            )
            full_response += response.text
            time.sleep(10)
        
        results[key] = full_response
        print(f"  - Finished item '{key}'.")
    
    return results

def save_card(res: dict[str, str]) -> None:
    """
    Saves the generated flashcards for each source file to a separate .txt file.
    """
    print(f"Saving flashcards for {len(res)} source file(s)...")

    for source_filename, flashcard_string in res.items():
        output_filename = f"anki_{os.path.splitext(source_filename)[0]}.txt"
        output_path = os.path.join(OUTPUT, output_filename)
        
        if not flashcard_string.strip():
            print(f"No content to save for {source_filename}.")
            continue
        
        res_list = flashcard_string.replace("\n", "///").replace(" /// ", "///").split("///")
        written_cards = 0
        failed = 0

        with open(output_path, "w", encoding="utf-8") as f:
            for elem in res_list:
                elem = elem.strip()
                if not elem or ";" not in elem:
                    if elem:
                        failed += 1
                    continue

                try:
                    question, answer = elem.split(";", 1)
                    question = question.strip()
                    answer = answer.strip()

                    if not question or not answer:
                        failed += 1
                        continue

                    if not question.endswith("?"):
                        question += "?"
                    if not answer.endswith("."):
                        answer += "."
                    
                    f.write(question + ";" + answer + "\n")
                    written_cards += 1
                except ValueError:
                    failed += 1
        
        if failed > 0:
            print(f"    Failed to parse or write {failed} elements for {source_filename}.")
        
        if written_cards > 0:
            print(f"    Successfully created {written_cards} flash cards in {output_path}.")
        else:
            print(f"    No flash cards were created for {source_filename}.")

def run() -> None:
    """
    Main function to orchestrate the entire flashcard generation pipeline.

    The process consists of the following steps:
    1.  Performs OCR on PDFs in the input folder to generate text files.
    2.  Reads the text data from the generated/provided text files.
    3.  Sends the text to the Gemini model to extract key facts.
    4.  Sends the extracted facts to the Gemini model to generate question-answer pairs for flashcards.
    5.  Parses the model's response and formats the flashcards.
    6.  Saves the final flashcards to a .txt file in the OUTPUT directory.
    """
    # PDF processing with OCR
    generate_data()

    # Retrieve information from input data
    data = read_data()
    
    # Create facts from information
    facts = generate_text(prompts["prompt_all"], data, "Extracting facts from input file...")

    # Create flashcards from facts
    res = generate_text(f_prompts["f_prompt_all"], facts, "Generating flashcards from extracted facts...")

    # Save flashcards
    save_card(res, "anki_flashcards.txt")

if __name__ == "__main__":
    run()