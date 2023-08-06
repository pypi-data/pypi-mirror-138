def print_thank_you_msg() -> None:
    thanks_msg = """
»»————---------🏏---------————----««
This package is in development.  

    You can get full access to api.  
    from WWW.CRICKETAPI.COM       
»»————---------🏏---------————----««
    """
    print("\n \n")
    print(thanks_msg)



def print_featured_matches() -> None:
    from cricketapi.request_handlers.apis import RzApp
    print(RzApp().featured_matches_summary())
    print_thank_you_msg()