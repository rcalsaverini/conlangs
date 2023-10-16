import bs4
import pandas as pd

with open("waba.html", "r+") as file:
    html = file.read()
    
soup = bs4.BeautifulSoup(html, "html.parser")


def extract_word(tag):
    return tag.find("w").text

def extract_meaning(t):
    
    def get_part_of_speech(t):
        if t.find("pos") is None:
            return None
        return t.find("pos").text
    
    def get_meanings(t):
        return [m.text for m in t.find_all("span")]
    
    return {
        "part_of_speech": get_part_of_speech(t),
        "meanings": get_meanings(t)
    }

def extract_semantic_fields(tag):
    return [extract_meaning(t) for t in tag.find_all("t")]

words = [{"word": extract_word(tag), "semantic_fields": extract_semantic_fields(tag)} for tag in soup.find_all("div")]

df = pd.DataFrame([
    {
        "meaning_id": k,
        "word": word["word"],
        "meaning": meaning,
        "part_of_speech": semantic_field["part_of_speech"]
    }
    for word in words
    for semantic_field in word["semantic_fields"]
    for k, meaning in enumerate(semantic_field["meanings"])
]).pivot_table(
    index="word",
    columns="part_of_speech",
    values="meaning",
    aggfunc=lambda ws: "\n".join([f"• {w}" for w in ws])
).reset_index().fillna("").to_excel("waba.xlsx", index=False)

#.to_markdown("waba.md", index=False)
#.to_excel("waba.xlsx", index=False)