import os
import requests


from flask import redirect, render_template, request, session

def get_book(isbn):

    # Contact API

    try:
        url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json"
        print(url)
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None


    info = response.json()
    return info

    # Parse response

    #try:
        #info = response.json()
        
         
       # return {



            #"title": info['ISBN:0553210696']['title']
            #"author": info[f"ISBN:{isbn}"]["authors"]["name"]
            #"publisher": info[f"ISBN:{isbn}"]["publishers"]["name"]
            #"publish_date": info[f"ISBN:{isbn}"]["publish_date"]
            #"cover_small": info[f"ISBN:{isbn}"]["cover"]["small"]
            #"cover_large": info[f"ISBN:{isbn}"]["cover"]["large"]
       # }
    #except (KeyError, TypeError, ValueError):
       # return None