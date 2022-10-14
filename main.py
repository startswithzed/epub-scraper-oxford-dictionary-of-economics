import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import csv

book = epub.read_epub('oxford-dictionary-of-economics.epub')

documents = []

# find the document structure of the book
for document in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
  doc_name = document.get_name()
  # print(doc_name)
  # the entries are are in documents named like 010_part1.xhtml
  if ("_part" in doc_name):
    documents.append(document)

# extract data from a single document first
    
# # find how the content is structured in a document
# soup = BeautifulSoup(documents[0].get_body_content(), "html.parser")
# # print(soup)

# # the one entry by extracting a <p>
# para = soup.find("p")
# # print(para)

# # extract title by extracting the span with class chaptersubt
# title = para.find("span", {"class": "chaptersubt"}).get_text()
# print(f"Title: {title}")

# # extract description by extracting  the span with class sc
# desc = para.get_text()[len(title)+1:]
# print(f"Description: {desc}")

# repeat the same for all documents and store them

entries = []
errors = []
    
for document in documents:
  soup = BeautifulSoup(document.get_body_content(), "html.parser")
  paras = [para for para in soup.find_all("p")]
  for para in paras:
    try:
      title = para.find("span", {"class": "chaptersubt"}).get_text()
      desc = para.get_text()[len(title)+1:]
      entries.append({
        "title": title,
        "description": desc
      })
    except AttributeError:
      errors.append(para)

print(f"Successfully extracted {len(entries)} entries")   
print(f"\nFirst 10 entries: \n")   
for i in range(0, 10):
  print(f"Entry {i+1}: {entries[i]}\n")

# write entries to a csv
field_names = ['title', 'description']
with open('entries.csv', 'w+') as csvfile:
  writer = csv.DictWriter(csvfile, fieldnames=field_names, delimiter='|')
  writer.writeheader()
  writer.writerows(entries)

print("\nCheck file entries.csv to see all entries")  
