from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
import requests

class ActionGetBookDetails(Action):
    def name(self) -> Text:
        return "action_fetch_book_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        book_title = tracker.get_slot("book_title")  # Extract book title from slot
        if not book_title:
            dispatcher.utter_message("I couldn't find a book title.")
            return []
        
        # Debug: Log the extracted book title
        print(f"Extracted book title: {book_title}")

        api_url = f"https://all-books-api.p.rapidapi.com/title/{book_title}"
        headers = {
            'x-rapidapi-key': '47ff253e49mshd0b0a3464141f42p13fe4ajsn6658e1f37b9c',
            'x-rapidapi-host': 'all-books-api.p.rapidapi.com'
        }
        
        try:
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                
                # Extract relevant details from API response
                book_title = data.get('bookTitle', 'N/A')
                book_image = data.get('bookImage', '')
                book_description = data.get('bookDescription', 'No description available.')
                book_author = data.get('bookAuthor', 'Unknown Author')
                book_publisher = data.get('bookPublisher', 'Unknown Publisher')
                amazon_url = data.get('amazonBookUrl', '')
                book_isbn = data.get('bookIsbn', 'N/A')
                book_rank = data.get('bookRank', 'N/A')
                
                # Format the response message
                message = f"Here are the details for '{book_title}':\n\n"
                message += f"Author: {book_author}\n"
                message += f"Publisher: {book_publisher}\n"
                message += f"Description: {book_description}\n"
                message += f"Amazon URL: {amazon_url}\n"
                message += f"ISBN: {book_isbn}\n"
                message += f"Rank: {book_rank}\n"
                
                # Dispatch the message back to the user
                dispatcher.utter_message(text=message)
            
            else:
                dispatcher.utter_message("Sorry, I couldn't fetch details for that book at the moment.")
        
        except Exception as e:
            # Handle exceptions (e.g., API not responding)
            dispatcher.utter_message("Sorry, I couldn't fetch details for that book at the moment.")
            print(e)
        
        return []
