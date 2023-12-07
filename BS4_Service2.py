from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bs4 import BeautifulSoup

app = FastAPI()

class LinkFinderRequest(BaseModel):
    link_number: int
    html_text: str

@app.post("/linkfinder")
def linkfinder(request: LinkFinderRequest):

    soup = BeautifulSoup(request.html_text, 'html.parser')
    
    # Find the element containing the text "Headlines"
    headlines_element = None
    for element in soup.find_all(['h3', 'p', 'div']):  # Adjust the tag list as needed
        if "Headlines" in element.get_text():
            headlines_element = element
            break
    
    # Check if the "Headlines" text was found
    if headlines_element:
        # Find the specified link after the element containing "Headlines"
        links_found = 0
        for sibling in headlines_element.find_all_next():
            if sibling.name == 'a' and sibling.has_attr('href'):
                links_found += 1
                if links_found == request.link_number:
                    return {"url": sibling['href']}
        if links_found < request.link_number:
            raise HTTPException(status_code=404, detail=f"No link number {request.link_number} found after 'Headlines'")
    else:
        raise HTTPException(status_code=404, detail="Text 'Headlines' not found in the HTML document.")

# If you need to run the application with Uvicorn programmatically:
# import uvicorn
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
# run locally $ uvicorn BS4_Service2:app

