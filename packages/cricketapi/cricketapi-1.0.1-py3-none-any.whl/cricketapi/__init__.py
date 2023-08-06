def print_featured_matches() -> str:
    from cricketapi.request_handlers.apis import RzApp
    print(RzApp().featured_matches_summary())